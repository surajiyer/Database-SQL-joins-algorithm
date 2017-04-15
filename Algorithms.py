from math import factorial

import math

from QueryGraph import *
import pandas as pd
import random
from progressbar import ProgressBar, Bar, Percentage


def sample_index(S, A, I, n):
    assert isinstance(S, pd.DataFrame)
    assert isinstance(A, pd.DataFrame)
    assert isinstance(I, dict)
    assert isinstance(n, int)

    if not I:
        # Simulating a hash join
        df = S.merge(A, how='outer')
    else:
        # Simulating an index-nested-lookup join
        A_keys = [next(iter(x))[0] for x in I.values()]
        S_keys = [next(iter(x))[1] for x in I.values()]
        assert len(A_keys) == len(S_keys)
        assert all(k in A.columns for k in A_keys) and all(k in S.columns for k in S.columns)

        # file = open('log.txt', 'w')

        # file.write('I:')
        # file.write(str(I))
        # file.write('A_keys:')
        # file.write(str(A_keys))
        # file.write('S_keys:')
        # file.write(str(S_keys))

        # if 'chn_id' in S.columns:
        #     print(S['chn_id'])

        cpt = []  # count per tuple
        for index, row in S.iterrows():
            ixs = list()
            for i, k in enumerate(S_keys):
                # print('k:', k, 'row[k]:', row[k], 'str(row[k]):', str(row[k]))

                # file.write('\nk:')
                # file.write(k)
                # file.write('\nrow[k]')
                # file.write(str(row[k]))
                # file.write('\nstr(row[k])')
                # file.write(str(type(row[k]).__name__))
                if not math.isnan(row[k]):
                    if isinstance(row[k], str):
                        ixs.append(A_keys[i] + ' == "' + str(row[k]) + '"')
                    else:
                        ixs.append(A_keys[i] + ' == ' + str(row[k]))
                # print('ixs:', ixs)
                else:
                    ixs.append(A_keys[i] + ' != ' + A_keys[i])
            # ixs = [A_keys[i] + ' == "' + str(row[k]) + '"' for i, k in enumerate(S_keys)]
            # file.write(str(ixs))
            # print('total ixs:', ixs)
            if len(ixs) > 0:
                cpt.append((row, len(A.query(" & ".join(ixs)).index)))
        _sum = sum(count for (_, count) in cpt)
        S_out = []
        sid = random.sample(range(_sum), min(n, _sum))
        for id in sid:
            chosen = max(i for i in range(len(cpt)) if sum(count for (_, count) in cpt[:i]) <= id)
            assert isinstance(chosen, int)
            tS = cpt[chosen][0]
            offset = id - sum(count for (_, count) in cpt[:chosen])
            assert offset < cpt[chosen][1]
            ixs = [A_keys[i] + ' == ' + str(tS[k]) for i, k in enumerate(S_keys)]
            tS = list(tS)
            tA = list(A.query(" & ".join(ixs)).iloc[offset])
            S_out.append(tS + tA)
        cols = list(S.columns) + list(A.columns)
        df = pd.DataFrame(S_out, columns=cols)

    # Return the merged samples
    df.relation_name = str([S.relation_name, A.relation_name])
    return {'df': df, 'matches':_sum}


def estimate_query(G, b, n, max_join_size):
    samples = dict()
    estimates = dict()
    for R in G.get_relations().values():
        R_set = frozenset({R})
        samples[R_set] = R.sample_table(n)
        estimates[R_set] = R.df.shape[0]
    budget = b

    # initialize a progress bar
    widgets = ['> Processed: ', Percentage(), ' ', Bar()]
    bar = ProgressBar(widgets=widgets, max_value=len(G.get_relations()), redirect_stdout=True).start()

    for size in bar(range(1, min(max_join_size, len(G.get_relations())) + 1)):
        get_entries_of_size = [(k, v) for (k, v) in samples.items() if len(k) == size]
        random.shuffle(get_entries_of_size)
        for (exp_in, S_in) in get_entries_of_size:
            for R in G.get_neighbors(exp_in):
                exp_out = exp_in | {R}
                if (exp_out not in samples.keys() or len(samples[exp_out].index) < n / 10) \
                        and (R.has_index(exp_in)):
                    result = sample_index(S_in, R.df, R.get_index(exp_in), n)
                    S_out = result['df']
                    match_count = result['matches']
                    # print('match count:', match_count)
                    # print('S_out size:', S_out.shape[0])
                    if S_out.shape[0] > 0:
                        # print('exp_in:', exp_in, 'exp_out:', exp_out)
                        # print('match count:', match_count)
                        # print('estimate of exp_in:', estimates[exp_in])
                        # print('S_out size:', S_out.shape[0])
                        estimates[exp_out] = match_count * estimates[exp_in] / S_out.shape[0]
                        # print('estimate of exp_out:', estimates[exp_out])
                    else:
                        estimates[exp_out] = 0
                    samples[exp_out] = S_out
                    # budget -= sample_cost(S_in, S_out, R)
                    # if budget < 0:
                    #     return {'samples': samples, "estimates": estimates}
        bar.update(size)
    bar.finish()
    return {'samples': samples, "estimates": estimates}


def merge(S, A, I):
    assert isinstance(S, pd.DataFrame)
    assert isinstance(A, pd.DataFrame)
    assert isinstance(I, dict)

    # Join
    A_keys = [next(iter(x))[0] for x in I.values()]
    S_keys = [next(iter(x))[1] for x in I.values()]
    assert len(A_keys) == len(S_keys)
    assert all(k in A.columns for k in A_keys) and all(k in S.columns for k in S.columns)
    df = S.merge(A, left_on=S_keys, right_on=A_keys, how='inner')
    return df


def calculate_query(G, max_join_size):
    samples = dict()
    for R in G.get_relations().values():
        R_set = frozenset({R})
        samples[R_set] = R.df

    # initialize a progress bar
    widgets = ['> Processed: ', Percentage(), ' ', Bar()]
    bar = ProgressBar(widgets=widgets, max_value=len(G.get_relations())).start()
    for size in bar(range(1, min(max_join_size, len(G.get_relations())) + 1)):
        get_entries_of_size = [(k, v) for (k, v) in samples.items() if len(k) == size]
        for (exp_in, S_in) in get_entries_of_size:
            for R in G.get_neighbors(exp_in):
                exp_out = exp_in | {R}
                # print('exp_out:', exp_out)
                if exp_out not in samples.keys():
                    S_out = merge(S_in, R.df, R.get_index(exp_in))
                    # S_out = S_in
                    samples[exp_out] = S_out

        bar.update(size)
    bar.finish()
    return samples


def sample_cost(s_in, s_out, R):
    assert isinstance(s_in, pd.DataFrame)
    assert isinstance(s_out, pd.DataFrame)
    assert isinstance(R, Relation)
    return s_in.shape[0] + s_out.shape[0]
    # return s_out.shape[0] * R.shape[0] / s_in.shape[0]
