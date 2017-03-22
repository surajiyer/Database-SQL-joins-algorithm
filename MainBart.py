import dataset as data
import sqlparse
import re
query = "SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND (mc.note  not like '%(as Metro-Goldwyn-Mayer Pictures)%') and (mc.note like '%(co-production)%' or mc.note like '%(presents)%') AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;"
query2 = "SELECT MIN(t.title) AS movie_title FROM keyword AS k, movie_info AS mi, movie_keyword AS mk, title AS t WHERE (k.keyword  like '%sequel%') AND (mi.info IN ('Sweden', 'Norway', 'Germany', 'Denmark', 'Swedish', 'Denish', 'Norwegian', 'German')) AND t.production_year > 2005 AND t.id = mi.movie_id AND t.id = mk.movie_id AND mk.movie_id = mi.movie_id AND k.id = mk.keyword_id;"

combined = query + query2

parsed = sqlparse.parse(query)

joins = []
selects = []
rename_map = {}

statement = parsed[0]

for t in statement.tokens:
    if isinstance(t, sqlparse.sql.Where):
        from_token = statement.token_prev(statement.token_index(t), skip_ws=True)
        renames = str(from_token[1]).split(',')

        for r in renames:
            rename_parts = [x.strip() for x in r.split('AS')]
            rename_map[rename_parts[1]] = rename_parts[0]

        for tt in t.tokens:
            if isinstance(tt, sqlparse.sql.Comparison):
                split = str(tt[4]).split('.')
                if len(split) > 1 and data.isColumnName(split[1]):
                    joins.append(tt)
                else:
                    selects.append(tt)
            elif re.match('.*like.*', str(tt)) or re.match('.*IN.*', str(tt)):
                selects.append(tt)

print('\nstatement: ')
print(statement)

print('\nrenames: ')
print(rename_map)

print('\njoins:')
for j in joins:
    print(j)

print('\nselects:')
for s in selects:
    print(s)
print('\n\n')


for i in [0, 1, 2]:
    print('selecting: ', selects[i])
    selection = data.perform_selection(rename_map, selects[i])
    print('selection:')
    print(selection, "\n\n")

