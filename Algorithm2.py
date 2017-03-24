import select_parser as sp
import data
import Algorithm1


def estimate_query(G, b, n):
    samples = {}
    for R in G.getRelations():
        R_set = frozenset({R})
        samples[R_set] = sample_relation(R, n)
        print(samples[R_set])
    budget = b
    for size in range(1, G.getRelations().size() - 1):
        for (exp_in, Sin) in samples.get_entries_of_size(size)
            for R in G.getNeighbours(exp_in)
                exp_out = exp_in + R
                if (samples[exp_out].size() < n / 10) and (R.hasIndex(exp_in) or len(R) <= n)):
                    S_out = Algorithm1.sampleIndex(S_in, R.getIndex(exp_in), n)
                samples[exp_out] = S_out
                budget -= sample_cost(S_in, S_out, R)
                if budget < 0:
                    return samples
    return samples


def sample_relation(R, n):
    return data.sample_table(R, n)


queries = tuple(open('join-order-benchmark/allqueries.sql', 'r'))
for qry in queries:
    print('###############################################')
    print('Query:', qry)
    print('Relations:')
    print(sp.get_tables(qry))
    print('\nPredicates:')
    sp.get_where(qry)
    # break
