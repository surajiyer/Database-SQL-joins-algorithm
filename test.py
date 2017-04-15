import math
import pandas as pd
from Algorithms import *
from SelectParser import *
from DataLoader import *
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

# column_names = ['id', 'name', 'imdb_index', 'imdb_id', 'name_pcode_nf', 'surname_pcode', 'md5sum']
# dates = pd.date_range('20130101', periods=6)
# df = pd.read_csv('data/char_name.csv', header=None, names=column_names, nrows = 10000)
# # q = 'SELECT * FROM df'
# # result = pysqldf(q)
# q = 'id > 60 and id < 100'
# result = df.query(q)
# print(result)

def get_estimates(qry, max_join_size, sample_size):
    results = dict()
    for i in range(1, max_join_size + 1):
        results[i] = list()

    # cardinalities = dict()
    # for i in range(1, max_join_size + 1):
    #     results[i] = list()

    G = QueryGraph(get_tables(qry), *get_where(qry), test=False)
    R = G.get_relations()
    assert all(isinstance(r, Relation) for r in R.values())

    cardinalities = calculate_query(G, max_join_size)
    result = estimate_query(G, 100000, sample_size, max_join_size)
    estimates = result['estimates']
    # samples = result['samples']
    # for k, v in samples.items():
    #     print('\n')
    #     print('sample size:', k)
    #     print('estimated size:', estimates.get(k))
    #     print('actual size:', cardinalities.get(k).shape[0])
    #     print(v.shape[0])
    #     print(v.head())

    for size in range(1, min(max_join_size, len(G.get_relations())) + 1):
        get_entries_of_size = [(k, v) for (k, v) in cardinalities.items() if len(k) == size]
        for k, v in get_entries_of_size:
            t = (math.floor(estimates.get(k)), v.shape[0])
            results[size].append(t)
            # print(str(math.floor(estimates.get(k))) + "," + str(v.shape[0]))
        # print('\n')

    return results

if __name__ == "__main__":
    # queries = ["SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND mc.note NOT LIKE '%(as Metro-Goldwyn-Mayer Pictures)%' AND (mc.note LIKE '%(co-production)%' OR mc.note LIKE '%(presents)%') AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;", \
    # "SELECT MIN(cn.name) AS movie_company, MIN(mi_idx.info) AS rating, MIN(t.title) AS drama_horror_movie FROM company_name AS cn, company_type AS ct, info_type AS it1, info_type AS it2, movie_companies AS mc, movie_info AS mi, movie_info_idx AS mi_idx, title AS t WHERE cn.country_code  = '[us]' AND ct.kind  = 'production companies' AND it1.info = 'genres' AND it2.info = 'rating' AND (mi.info  IN ('Drama', 'Horror')) AND mi_idx.info  > '8.0' AND (t.production_year  BETWEEN 2005 ABCDE 2008) AND t.id = mi.movie_id AND t.id = mi_idx.movie_id AND mi.info_type_id = it1.id AND mi_idx.info_type_id = it2.id AND t.id = mc.movie_id AND ct.id = mc.company_type_id AND cn.id = mc.company_id AND mc.movie_id = mi.movie_id AND mc.movie_id = mi_idx.movie_id AND mi.movie_id = mi_idx.movie_id;"]

    # qry = "SELECT * FROM cast_info AS ci, aka_title AS at WHERE ci.movie_id = at.movie_id;"

    # df = DataLoader.load_pickle('aka_name')
    # df.columns = ['an' + '_' + c for c in DataLoader.columns['aka_name']]
    # name = "Smith, Jessica Noel"
    # # q = 'an_name' + ' == "' + name + '"'
    # q = 'an_imdb_index != an_imdb_index'
    # sel = df.query(q)
    # # print(sel)
    # sample = sel.sample(1)
    # print(sample)
    # # print(math.isnan(sample['an_imdb_index']))
    # print(math.isnan(sample['an_id']))

    queries = []

    with open('data/all-queries-filtered.sql') as f:
        queries = f.readlines()

    for q in queries:
        if q.startswith('/*'):
            queries.remove(q)

    estimates = dict()
    max_join_size = 6
    sample_size = 100
    for i in range(1, max_join_size + 1):
        estimates[i] = list()

    file = open('results-log.txt', 'w')

    for q in queries[4:8]:
        new_results = get_estimates(q, max_join_size, sample_size)
        for i in range(1, max_join_size + 1):
            estimates_for_size = new_results[i]
            for t in estimates_for_size:
                estimates[i].append(t)

        print('\n\n')
        for i in range(2, max_join_size + 1):
            size_estimates = estimates[i]
            for t in size_estimates:
                print(i, t[0], t[1])
                file.write(str(i) + ', ' + str(t[0]) + ', ' + str(t[1]) + '\n')

    print('\n\n')
    print('final:')
    file.write('\n\nfinal:\n')
    for i in range(2, max_join_size + 1):
        size_estimates = estimates[i]
        for t in size_estimates:
            print(i, t[0], t[1])
            file.write(str(i) + ', ' + str(t[0]) + ', ' + str(t[1]) + '\n')

    # Test G.get_neighbors()
    # R_set = set(list(R.values())[:3])
    # print('\nexp_in:', R_set, 'neighbors:', G.get_neighbors(R_set))
    # x = list(R.values())[0]
    # print(x, x.has_index(R_set))

    # sample_size = 1000
    #
    # # Test algorithm 1
    # df1 = load_pickle('aka_title')
    # df2 = load_pickle('movie_companies')
    #
    # full_join = df1.merge(df2, on='movie_id')
    # full_join_size = full_join.shape[0]
    #
    # df1.relation_name = 'at'
    # df1.columns = [df1.relation_name + '_' + c for c in df1.columns]
    #
    # df1_sample = df1.sample(sample_size)
    # df1_sample.relation_name = 'at'
    #
    #
    # df2.relation_name = 'mc'
    # df2.columns = [df2.relation_name + '_' + c for c in df2.columns]
    #
    # # print(df1_sample)
    #
    # print(list(df1_sample.columns))
    # print(list(df2.columns))
    # print('size of df1:', df1.shape[0])
    # print('size of df2:', df2.shape[0])
    # result = sample_index(df1_sample, df2, {'at': {('mc_movie_id', 'at_movie_id')}}, sample_size)
    # print('# matches:', result['matches'])
    #
    # print('full join size:', full_join_size)
    # print('cardinality estimate:', (df1.shape[0] * result['matches']) / sample_size)
    #
    # print('\n\n')
    # df2_sample = df2.sample(sample_size)
    # df2_sample.relation_name = 'mc'
    # # df1.name = 'at'
    # result = sample_index(df2_sample, df1, {'mc': {('at_movie_id', 'mc_movie_id')}}, sample_size)
    # print('# matches:', result['matches'])
    # print('cardinality estimate:', (df2.shape[0] * result['matches']) / sample_size)

    # df3 = load_pickle('movie_info')
    # df3.name = 'mi'
    # df3.columns = [df3.name + '_' + c for c in df3.columns]
    # join_sample_2 = sample_index(join_sample, df3, {'at': {('mi_movie_id', 'at_movie_id')}}, 10)
    #
    # print('\n\njoin_sample_2:')
    # print(join_sample_2)
