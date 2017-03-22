#import select_parser
import dataset
import Algorithm1

def estimate_query(G, b, n):
    samples = {}
    for R in G.getRelations():
        samples[R]= sampleRelation(R,n)
        print(samples[R])
    budget = b
    for size in range(1, G.getRelations().size()-1):
        for (expin, Sin) in samples.getEntriesOfSize(size)
            for R in G.getNeighbours(expin)
                expout = expin + R
                if (samples[expout].size() < n/10) && (R.hasIndex(expin) || len(R) <= n)):
                    Sout = Algorithm1.sampleIndex(Sin, R.getIndex(expin), n)
                    samples[expout] = Sout
                    budget -= sampleCost(Sin, Sout, R)
                    if budget < 0:
                        return samples
    return samples

def sampleRelation(R, n):
    return dataset.sampleTable(R, n)  # Has to be dataset.R

queries = tuple(open('join-order-benchmark/allqueries.sql', 'r'))
for qry in queries:
    print('###############################################')
    print('Query:', qry)
    print('Relations:')
    print(select_parser.get_tables(qry))
    print('\nPredicates:')
    select_parser.get_where(qry)
    # break
