import dataset as data
import sqlparse

query = "SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND mc.note  not like '%(as Metro-Goldwyn-Mayer Pictures)%' and (mc.note like '%(co-production)%' or mc.note like '%(presents)%') AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;"

parsed = sqlparse.parse(query)

comparisons = []
joins = []
selects = []

for t in parsed[0].tokens:
    if isinstance(t, sqlparse.sql.Where):
        for tt in t.tokens:
            if isinstance(tt, sqlparse.sql.Comparison):
                comparisons.append(tt)

for c in comparisons:
    split = str(c[4]).split('.')
    if len(split) > 1:
        if data.isColumnName(split[1]):
            joins.append(c)
        else:
            selects.append(c)
    else:
        selects.append(c)

print('joins:')
for j in joins:
    print(j)

print('\nselects:')
for s in selects:
    print(s)

