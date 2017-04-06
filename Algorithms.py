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

        cpt = []  # count per tuple
        for index, row in S.iterrows():
            ixs = [A_keys[i] + ' == ' + str(row[k]) for i, k in enumerate(S_keys)]
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
    df.name = str([S.name, A.name])
    return df


def estimate_query(G, b, n):
    samples = dict()
    for R in G.get_relations().values():
        R_set = frozenset({R})
        samples[R_set] = R.sample_table(n)
    budget = b

    # initialize a progress bar
    widgets = ['> Processed: ', Percentage(), ' ', Bar()]
    bar = ProgressBar(widgets=widgets, max_value=len(G.get_relations())).start()

    for size in bar(range(1, len(G.get_relations()))):
        get_entries_of_size = [(k, v) for (k, v) in samples.items() if len(k) == size]
        for (exp_in, S_in) in get_entries_of_size:
            print(exp_in, G.get_neighbors(exp_in))
            for R in G.get_neighbors(exp_in):
                exp_out = exp_in | {R}
                if (exp_out not in samples.keys() or len(samples[exp_out].index) < n / 10) \
                        and (R.has_index(exp_in) or len(R) <= n):
                    S_out = sample_index(S_in, R.df, R.get_index(exp_in), n)
                    samples[exp_out] = S_out
                    budget -= sample_cost(S_in, S_out, R)
                    if budget < 0:
                        return samples
        bar.update(size)
    bar.finish()
    return samples


def sample_cost(s_in, s_out, R):
    assert isinstance(s_in, pd.DataFrame)
    assert isinstance(s_out, pd.DataFrame)
    assert isinstance(R, Relation)
    return s_in.shape[0] + s_out.shape[0]
