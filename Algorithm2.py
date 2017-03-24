import select_parser as sp
import data
import Algorithm1
from QueryGraph import *


def estimate_query(G, b, n):
    samples = {}
    for R in G.get_relations():
        R_set = frozenset({R})
        samples[R_set] = sample_relation(R, n)
        print(samples[R_set])
    budget = b
    for size in range(1, G.get_relations().size()):
        for (exp_in, S_in) in get_entries_of_size(samples, size):
            for R in G.get_neighbours(exp_in):
                exp_out = exp_in + frozenset({R})
                if (samples[exp_out].size() < n / 10) and (R.has_index(exp_in) or len(R) <= n):
                    S_out = Algorithm1.sampleIndex(S_in, R.get_index(exp_in), n)
                samples[exp_out] = S_out
                budget -= sample_cost(S_in, S_out, R)
                if budget < 0:
                    return samples
    return samples


def sample_relation(R, n):
    assert isinstance(R, Relation)
    return data.sample_table(R, n)


def get_entries_of_size(samples, size):
    assert isinstance(samples, list) and all(isinstance(s, pd.DataFrame) for s in samples)
    assert isinstance(size, int)
    for s in samples:
        yield s, len(s)


queries = tuple(open('join-order-benchmark/allqueries.sql', 'r'))
for qry in queries:
    print('###############################################')
    print('Query:', qry)
    print('Relations:')
    print(sp.get_tables(qry))
    print('\nPredicates:')
    sp.get_where(qry)
    # break
