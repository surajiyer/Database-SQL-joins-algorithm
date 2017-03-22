import select_parser


def estimate_query(G, b, n):
    pass


queries = tuple(open('join-order-benchmark/allqueries.sql', 'r'))
# queries = ("SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year "
#            "FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t "
#            "WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND "
#            "(mc.note  not like '%(as Metro-Goldwyn-Mayer Pictures)%') and ((mc.note like '%(co-production)%') or "
#            "(mc.note like '%(presents)%')) AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND "
#            "t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;")
# queries = ("SELECT MIN(chn.name) AS uncredited_voiced_character, MIN(t.title) AS russian_movie "
#            "FROM char_name AS chn, cast_info AS ci, company_name AS cn, company_type AS ct, movie_companies AS mc, "
#            "role_type AS rt, title AS t "
#            "WHERE (ci.note  like '%(voice)%') and (ci.note like '%(uncredited)%') AND cn.country_code  = '[ru]' AND "
#            "rt.role  = 'actor' AND t.production_year > 2005 AND t.id = mc.movie_id AND t.id = ci.movie_id AND "
#            "ci.movie_id = mc.movie_id AND chn.id = ci.person_role_id AND rt.id = ci.role_id AND cn.id = mc.company_id "
#            "AND ct.id = mc.company_type_id;", "")

for qry in queries:
    print('###############################################')
    print('Query:', qry)
    print('Relations:')
    print(select_parser.get_tables(qry))
    print('\nPredicates:')
    select_parser.get_where(qry)
    # break
