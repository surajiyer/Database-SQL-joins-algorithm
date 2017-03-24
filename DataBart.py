import pandas as pd
import re

# change as needed
csv_location = 'D:/Bart/IMDb dataset/imdb/'

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

all_columns = aka_name_columns + aka_title_columns + cast_info_columns + char_name_columns + comp_cast_type_columns + \
              company_name_columns + company_type_columns + complete_cast_columns + info_type_columns + keyword_columns + \
              kind_type_columns + link_type_columns + movie_companies_columns + movie_info_idx_columns + movie_keyword_columns + \
              movie_link_columns + name_columns + role_type_columns + title_columns + movie_info_columns + person_info_columns


relations = {}

# (un)comment to load desired csv files
#relations['aka_name'] = pd.read_csv(csv_location + 'aka_name.csv', header=None, names=aka_name_columns)
#relations['aka_title'] = pd.read_csv(csv_location + 'aka_title.csv', header=None, names=aka_title_columns)
#relations['cast_info'] = pd.read_csv(csv_location + 'cast_info.csv', header=None, names=cast_info_columns)
#relations['char_name'] = pd.read_csv(csv_location + 'char_name.csv', header=None, names=char_name_columns)
#relations['comp_cast_type'] = pd.read_csv(csv_location + 'comp_cast_type.csv', header=None, names=comp_cast_type_columns)
#relations['company_name'] = pd.read_csv(csv_location + 'company_name.csv', header=None, names=company_name_columns)
relations['company_type'] = pd.read_csv(csv_location + 'company_type.csv', header=None, names=company_type_columns)
#relations['complete_cast'] = pd.read_csv(csv_location + 'complete_cast.csv', header=None, names=complete_cast_columns)
relations['info_type'] = pd.read_csv(csv_location + 'info_type.csv', header=None, names=info_type_columns)
#relations['keyword'] = pd.read_csv(csv_location + 'keyword.csv', header=None, names=keyword_columns)
#relations['kind_type'] = pd.read_csv(csv_location + 'kind_type.csv', header=None, names=kind_type_columns)
#relations['link_type'] = pd.read_csv(csv_location + 'link_type.csv', header=None, names=link_type_columns)
relations['movie_companies'] = pd.read_csv(csv_location + 'movie_companies.csv', header=None, names=movie_companies_columns)
#relations['movie_info_idx'] = pd.read_csv(csv_location + 'movie_info_idx.csv', header=None, names=movie_info_idx_columns)
#relations['movie_keyword'] = pd.read_csv(csv_location + 'movie_keyword.csv', header=None, names=movie_keyword_columns)
#relations['movie_link'] = pd.read_csv(csv_location + 'movie_link.csv', header=None, names=movie_link_columns)
#relations['name'] = pd.read_csv(csv_location + 'name.csv', header=None, names=name_columns)
#relations['role_type'] = pd.read_csv(csv_location + 'role_type.csv', header=None, names=role_type_columns)
#relations['title'] = pd.read_csv(csv_location + 'title.csv', header=None, names=title_columns)
#relations['movie_info'] = pd.read_csv(csv_location + 'movie_info.csv', header=None, names=movie_info_columns)
#relations['person_info'] = pd.read_csv(csv_location + 'person_info.csv', header=None, names=person_info_columns)

#rename: mapping from abbreviation (like 'ct') to actual relation name (like 'company type')
#selection_string: e.g. "ct.kind = 'production companies'"
def perform_selection(renames, selection_string):
    ss = str(selection_string)
    if re.match('.*=.*', ss):
        parts = [x.strip() for x in ss.split('=')]
        print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')
        relation_name = renames[lefthand_parts[0]]
        attribute = lefthand_parts[1]
        value = parts[1]
        value = stripQuotes(value)

        relation = relations[relation_name]
        selection = relation[relation[attribute] == value]

        return selection
    elif re.match('.*like.*', ss):
        if ss.startswith('(') and ss.endswith(')'):
            ss = ss[1:-1]

        parts = []
        negation = False
        if (re.match('.*not like.*', ss)):
            parts = [x.strip() for x in ss.split('not like')]
            negation = True
        else:
            parts = [x.strip() for x in ss.split('like')]
        print(parts)

        left_hand = parts[0]
        lefthand_parts = [x.strip() for x in left_hand.split(".")]
        relation_name = renames[lefthand_parts[0]]
        attribute = lefthand_parts[1]
        print(attribute)
        value = parts[1]
        value = stripQuotes(value)

        value = value.replace("%", ".*")
        print(value)

        relation = relations[relation_name]
        print(relation_name)
        if negation:
            value = '^((?!' + value + ').)*$'

        selection = relation[~relation[attribute].isnull() & relation[attribute].str.match(value)]
        return selection

def isColumnName(c):
    return (c in all_columns)

def stripQuotes(value):
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    return value

#testing

df = relations['movie_companies']
#selectionEqual = df[df['kind'] == 'distributors']
#selectionLike = df[~df['note'].isnull() & df['note'].str.match('^((?!.*support.*).)*$')]
#selectionIn = df[df['id'].isin([1, 2, 3, 4])]
#print(selectionLike)