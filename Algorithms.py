from QueryGraph import *
import pandas as pd
import random


def sample_index(S, A, I, n, lsuffix='_S', rsuffix='_A'):
    assert isinstance(S, pd.DataFrame)
    assert isinstance(A, pd.DataFrame)
    assert isinstance(I, str) and I in list(A.index)
    assert isinstance(n, int)

    # Simulating a hash join
    if I is None:
        return S.join(A, how='inner', lsuffix=lsuffix, rsuffix=rsuffix)

    # Simulating a index-nested-lookup join
    cpt = []  # count per tuple
    for row in S.itertuples():
        row = list(row)
        index = row[0]
        cpt.append((row, A[I].value_counts()[index]))
    _sum = sum(count for (_, count) in cpt)
    S_out = []
    sid = random.sample(range(_sum), min(n, _sum))
    for id in sid:
        chosen = max(i for i in range(len(cpt)) if sum(count for (_, count) in cpt[:i]) <= id)
        assert isinstance(chosen, int)
        tS = cpt[chosen][0]
        offset = id - sum(count for (_, count) in cpt[:chosen])
        assert offset+1 < cpt[chosen][1]
        tA = list(A[A[I] == tS[0]].iloc[offset+1])
        S_out.append(tS + tA)
    return pd.DataFrame(S_out, columns=[col+lsuffix for col in S.columns]+[col+rsuffix for col in A.columns])


def estimate_query(G, b, n):
    samples = dict()
    for R in G.get_relations():
        R_set = frozenset({R})
        samples[R_set] = R.sample_table(n)
        print(samples[R_set])
    budget = b
    for size in range(1, len(G.get_relations())):
        get_entries_of_size = ((k, v) for (k, v) in samples.items() if len(k) == size)
        for (exp_in, S_in) in get_entries_of_size:
            for R in G.get_neighbours(exp_in):
                exp_out = set(exp_in) | {R}
                if (exp_out not in samples.keys() or len(samples[exp_out].index) < n / 10) \
                        and (R.has_index(exp_in) or len(R) <= n):
                    S_out = sample_index(S_in, R.df, R.get_index(exp_in), n)
                    samples[exp_out] = S_out
                    budget -= sample_cost(S_in, S_out, R)
                    if budget < 0:
                        return samples
    return samples


def sample_cost(s_in, s_out, R):
    assert isinstance(s_in, pd.DataFrame)
    assert isinstance(s_out, pd.DataFrame)
    assert isinstance(R, Relation)
    return s_in.shape[1] + s_out.shape[1]
