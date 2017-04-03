import SelectParser as sp

queries = []

with open('data/all-queries-filtered.sql') as f:
    queries = f.readlines()

for q in queries:
    if q.startswith('/*'):
        queries.remove(q)

def execute(sql):
    where = sp.get_where(sql)
    joins = where[0]

    tuples = set()
    for j in joins:
        LR = [x.strip() for x in str(j).split('=')]
        L = LR[0].split('.')[0]
        R = LR[1].split('.')[0]
        print(L, R)
        t = (L, R)
        if t in tuples:
            print('duplicate')
            exit(0)
        else:
            tuples.add(t)


q = "SELECT * FROM test as t, test2 as t2 WHERE t.id = t2.id AND t.movie_id = t2.movie_id;"
# execute(q)

for q in queries:
    execute(q)

