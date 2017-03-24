import data as d
import select
import select_parser as sp

# sql = "SELECT * FROM movie_companies as mc WHERE (mc.note IS NULL);"
# sql = "SELECT chn.name FROM char_name AS chn WHERE (chn.name like '%(John)%');"
# sql = "SELECT MIN(chn.name) AS uncredited_voiced_character, MIN(t.title) AS russian_movie FROM char_name AS chn, cast_info AS ci, company_name AS cn, company_type AS ct, movie_companies AS mc, role_type AS rt, title AS t WHERE (ci.note  like '%(voice)%') and (ci.note like '%(uncredited)%') AND cn.country_code  = '[ru]' AND rt.role  = 'actor' AND t.production_year > 2005 AND t.id = mc.movie_id AND t.id = ci.movie_id AND ci.movie_id = mc.movie_id AND chn.id = ci.person_role_id AND rt.id = ci.role_id AND cn.id = mc.company_id AND ct.id = mc.company_type_id;"
# sql = "SELECT MIN(cn.name) AS company_name, MIN(lt.link) AS link_type, MIN(t.title) AS western_follow_up FROM company_name AS cn, company_type AS ct, keyword AS k, link_type AS lt, movie_companies AS mc, movie_info AS mi, movie_keyword AS mk, movie_link AS ml, title AS t WHERE cn.country_code !='[pl]' AND (cn.name LIKE '%Film%' OR cn.name LIKE '%Warner%') AND ct.kind ='production companies' AND k.keyword ='sequel' AND (lt.link LIKE '%follow%') AND (mc.note IS NULL) AND (mi.info IN ('Sweden', 'Norway', 'Germany', 'Denmark', 'Swedish', 'Denish', 'Norwegian', 'German', 'English')) AND (t.production_year BETWEEN 1950 AND 2010) AND lt.id = ml.link_type_id AND ml.movie_id = t.id AND t.id = mk.movie_id AND mk.keyword_id = k.id AND t.id = mc.movie_id AND mc.company_type_id = ct.id AND mc.company_id = cn.id AND mi.movie_id = t.id AND ml.movie_id = mk.movie_id AND ml.movie_id = mc.movie_id AND mk.movie_id = mc.movie_id AND ml.movie_id = mi.movie_id AND mk.movie_id = mi.movie_id AND mc.movie_id = mi.movie_id;"
sql = "SELECT MIN(mi.info) AS release_date, MIN(miidx.info) AS rating, MIN(t.title) AS german_movie FROM company_name AS cn, company_type AS ct, info_type AS it, info_type AS it2, kind_type AS kt, movie_companies AS mc, movie_info AS mi, movie_info_idx AS miidx, title AS t WHERE cn.country_code ='[de]' AND ct.kind ='production companies' AND it.info ='rating' AND it2.info ='release dates' AND kt.kind ='movie' AND mi.movie_id = t.id AND it2.id = mi.info_type_id AND kt.id = t.kind_id AND mc.movie_id = t.id AND cn.id = mc.company_id AND ct.id = mc.company_type_id AND miidx.movie_id = t.id AND it.id = miidx.info_type_id AND mi.movie_id = miidx.movie_id AND mi.movie_id = mc.movie_id AND miidx.movie_id = mc.movie_id;"

where = sp.get_where(sql)
selects = where[1]

query_relations = {}
selects_for_relation = {}

renames = sp.get_tables(sql)
print('tables:')
for t in renames:
    print('loading', renames[t], '...')
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
    print(qr, selects_for_relation[qr])
    print(qr, len(query_relations[qr].index))

select.perform_selections(query_relations, selects_for_relation)

print('sizes after selection:')
for qr in query_relations:
    print(qr, len(query_relations[qr].index))
