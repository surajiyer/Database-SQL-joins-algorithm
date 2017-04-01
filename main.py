import select
import select_parser as sp
import data as d

queries = []

with open('data/all-queries-filtered.sql') as f:
    queries = f.readlines()

for q in queries:
    if q.startswith('/*'):
        queries.remove(q)


def execute(sql):
    where = sp.get_where(sql)
    selects = where[1]

    query_relations = {}
    selects_for_relation = {}

    renames = sp.get_tables(sql)
    print('tables:')
    for t in renames:
        # print('loading', renames[t], '...')
        d.load_csv(renames[t])
        rel = d.data[renames[t]]['data']
        query_relations[t] = rel
        selects_for_relation[t] = []

    for s in selects:
        ss = select.remove_outer_parentheses(str(s))
        table_abr = ss.split('.')[0]
        selects_for_relation[table_abr].append(ss)
        print(s)

    print('\nselects and sizes:')
    for qr in query_relations:
        print('table:', qr, ', size:', len(query_relations[qr].index), ', selects:', selects_for_relation[qr])

    select.perform_selections(query_relations, selects_for_relation)

    print('sizes after selection:')
    for qr in query_relations:
        print('table:', qr, ', size:', len(query_relations[qr].index))


# only handle first n queries
n = 3
for q in queries[:n]:
    execute(q)
