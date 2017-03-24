import select_parser as sp
import pprint
import data
import Algorithm1
from QueryGraph import *


pp = pprint.PrettyPrinter(indent=4)

def estimate_query(G, b, n):
    samples = {}
    for R in G.get_relations():
        R_set = frozenset({R})
        samples[R_set] = sample_relation(R, n)
        #print(samples[R_set])
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

#connections = [('A', 'B'), ('B', 'C'), ('B', 'D'),
  #                 ('C', 'D'), ('A', 'F'), ('F', 'C')]
connections = []
queries = tuple(open('join-order-benchmark/allqueries.sql', 'r'))
for qry in queries:
    print('###############################################')
    print('Query:', qry)
    print('Relations:')
    relations = sp.get_tables(qry)
    print(relations)
    print('\nPredicates:')
    _, joins = sp.get_where(qry)

    for statement in joins:
        stat = str(statement)
        temp = [x.strip() for x in stat.split("=")]
        print("temp", temp)
        table_name0 = temp[0].split(".")
        table_name1 = temp[1].split(".")
        #print("table0", table_name0[0], "table1", table_name1[0])
        table1 = relations.get(table_name0[0])
        table2 = relations.get(table_name1[0])
        print("table1", table1)
        print("table2", table2)
        #rel1 = Relation(data.load_csv(table1))
        #print("rel1", rel1)
        #rel2 = Relation(data.load_csv(table2))
       # assert(isinstance(panda, pd.DataFrame))
        connections.append((table1, table2))

    print("connections", connections)

    g = QueryGraph(connections)
    pp.pprint(g._graph)
    break
