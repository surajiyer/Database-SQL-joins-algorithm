import pandas as pd
import numpy as np
from Algorithms import *
from SelectParser import *
import SelectParser as sp

# column_names = ['id', 'name', 'imdb_index', 'imdb_id', 'name_pcode_nf', 'surname_pcode', 'md5sum']
# dates = pd.date_range('20130101', periods=6)
# df = pd.read_csv('data/char_name.csv', header=None, names=column_names, nrows = 10000)
# # q = 'SELECT * FROM df'
# # result = pysqldf(q)
# q = 'id > 60 and id < 100'
# result = df.query(q)
# print(result)

if __name__ == "__main__":
    qry = "SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND mc.note  not like '%(as Metro-Goldwyn-Mayer Pictures)%' and (mc.note like '%(co-production)%' or mc.note like '%(presents)%') AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;"
    G = QueryGraph(get_tables(qry), *get_where(qry))
    R = G.get_relations()
    assert all(isinstance(r, Relation) for r in R.values())

    # queries = []
    #
    # with open('data/all-queries-filtered.sql') as f:
    #     queries = f.readlines()
    #
    # for q in queries:
    #     if q.startswith('/*'):
    #         queries.remove(q)
    #
    #
    # for q in queries:
    #     where = sp.get_where(q)

