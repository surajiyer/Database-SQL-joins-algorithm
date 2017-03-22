import pandas as pd

# change as needed
csv_location = '../../IMDb dataset/imdb/'

aka_name_columns = ['id', 'person_id', 'name', 'imdb_index', 'name_pcode_cf', 'name_pcode_nf', 'surname_pcode',
                    'md5sum']
aka_title_columns = ['id', 'movie_id', 'title', 'imdb_index', 'kind_id', 'production_year', 'imdb_id', 'phonetic_code',
                     'episode_of_id', 'season_nr', 'note', 'md5sum']
cast_info_columns = ['id', 'person_id', 'movie_id', 'person_role_id' 'note', 'nr_order', 'role_id']
char_name_columns = ['id', 'name', 'imdb_index', 'imdb_id', 'name_pcode_nf', 'surname_pcode', 'md5sum']
comp_cast_type_columns = ['id', 'kind']
company_name_columns = ['id', 'name', 'country_code', 'imdb_id', 'name_pcode_nf', 'name_pcode_sf', 'md5sum']
company_type_columns = ['id', 'kind']
complete_cast_columns = ['id', 'movie_id', 'subject_id', 'status_id']
info_type_columns = ['id', 'info']
keyword_columns = ['id', 'keyword', 'phonetic_code']
kind_type_columns = ['id', 'kind']
link_type_columns = ['id', 'link']
movie_companies_columns = ['id', 'movie_id', 'company_id', 'company_type_id', 'note']
movie_info_idx_columns = ['id', 'movie_id', 'info_type_id', 'info', 'note']
movie_keyword_columns = ['id', 'movie_id', 'keyword_id']
movie_link_columns = ['id', 'movie_id', 'linked_movie_id', 'link_type_id']
name_columns = ['id', 'name', 'imdb_index', 'imdb_id', 'gender', 'name_pcode_cf', 'name_pcode_nf', 'surname_pcode',
                'md5sum']
role_type_columns = ['id', 'role']
title_columns = ['id', 'title', 'imdb_index', 'kind_id', 'production_year', 'imdb_id', 'phonetic_code', 'episode_of_id',
                 'season_nr', 'episode_nr', 'series_years', 'md5sum']
movie_info_columns = ['id', 'movie_id', 'info_type_id', 'info', 'note']
person_info_columns = ['id', 'person_id', 'info_type_id', 'info', 'note']

# (un)comment to load desired csv files
aka_name = pd.read_csv(csv_location + 'aka_name.csv', header=None, names=aka_name_columns)
# aka_title = pd.read_csv(csv_location + 'aka_title.csv', header=None, names=aka_title_columns)
# cast_info = pd.read_csv(csv_location + 'cast_info.csv', header=None, names=cast_info_columns)
char_name = pd.read_csv(csv_location + 'char_name.csv', header=None, names=char_name_columns)
# comp_cast_type = pd.read_csv(csv_location + 'comp_cast_type.csv', header=None, names=comp_cast_type_columns)
# company_name = pd.read_csv(csv_location + 'company_name.csv', header=None, names=company_name_columns)
# company_type = pd.read_csv(csv_location + 'company_type.csv', header=None, names=company_type_columns)
# complete_cast = pd.read_csv(csv_location + 'complete_cast.csv', header=None, names=complete_cast_columns)
# info_type = pd.read_csv(csv_location + 'info_type.csv', header=None, names=info_type_columns)
# keyword = pd.read_csv(csv_location + 'keyword.csv', header=None, names=keyword_columns)
# kind_type = pd.read_csv(csv_location + 'kind_type.csv', header=None, names=kind_type_columns)
# link_type = pd.read_csv(csv_location + 'link_type.csv', header=None, names=link_type_columns)
# movie_companies = pd.read_csv(csv_location + 'movie_companies.csv', header=None, names=movie_companies_columns)
# movie_info_idx = pd.read_csv(csv_location + 'movie_info_idx.csv', header=None, names=movie_info_idx_columns)
# movie_keyword = pd.read_csv(csv_location + 'movie_keyword.csv', header=None, names=movie_keyword_columns)
# movie_link = pd.read_csv(csv_location + 'movie_link.csv', header=None, names=movie_link_columns)
# name = pd.read_csv(csv_location + 'name.csv', header=None, names=name_columns)
# role_type = pd.read_csv(csv_location + 'role_type.csv', header=None, names=role_type_columns)
# title = pd.read_csv(csv_location + 'title.csv', header=None, names=title_columns)
# movie_info = pd.read_csv(csv_location + 'movie_info.csv', header=None, names=movie_info_columns)
# person_info = pd.read_csv(csv_location + 'person_info.csv', header=None, names=person_info_columns)

join = aka_name.join(other=char_name, lsuffix='_aka_name', rsuffix='_char_name')
print(join.head())
