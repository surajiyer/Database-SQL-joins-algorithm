import pandas as pd

# CSV files location
csv_location = 'data/'

# Data dict object containing all the dataframes and other info
data = {
    'aka_name': {
        'columns': ['id', 'person_id', 'name', 'imdb_index', 'name_pcode_cf', 'name_pcode_nf', 'surname_pcode',
                    'md5sum']
    },
    'aka_title': {
        'columns': ['id', 'movie_id', 'title', 'imdb_index', 'kind_id', 'production_year', 'imdb_id', 'phonetic_code',
                    'episode_of_id', 'season_nr', 'note', 'md5sum']
    },
    'cast_info': {
        'columns': ['id', 'person_id', 'movie_id', 'person_role_id', 'note', 'nr_order', 'role_id']
    },
    'char_name': {
        'columns': ['id', 'name', 'imdb_index', 'imdb_id', 'name_pcode_nf', 'surname_pcode', 'md5sum']
    },
    'comp_cast_type': {
        'columns': ['id', 'kind']
    },
    'company_name': {
        'columns': ['id', 'name', 'country_code', 'imdb_id', 'name_pcode_nf', 'name_pcode_sf', 'md5sum']
    },
    'company_type': {
        'columns': ['id', 'kind']
    },
    'complete_cast': {
        'columns': ['id', 'movie_id', 'subject_id', 'status_id']
    },
    'info_type': {
        'columns': ['id', 'info']
    },
    'keyword': {
        'columns': ['id', 'keyword', 'phonetic_code']
    },
    'kind_type': {
        'columns': ['id', 'kind']
    },
    'link_type': {
        'columns': ['id', 'link']
    },
    'movie_companies': {
        'columns': ['id', 'movie_id', 'company_id', 'company_type_id', 'note']
    },
    'movie_info_idx': {
        'columns': ['id', 'movie_id', 'info_type_id', 'info', 'note']
    },
    'movie_keyword': {
        'columns': ['id', 'movie_id', 'keyword_id']
    },
    'movie_link': {
        'columns': ['id', 'movie_id', 'linked_movie_id', 'link_type_id']
    },
    'name': {
        'columns': ['id', 'name', 'imdb_index', 'imdb_id', 'gender', 'name_pcode_cf', 'name_pcode_nf', 'surname_pcode',
                    'md5sum']
    },
    'role_type': {
        'columns': ['id', 'role']
    },
    'title': {
        'columns': ['id', 'title', 'imdb_index', 'kind_id', 'production_year', 'imdb_id', 'phonetic_code',
                    'episode_of_id',
                    'season_nr', 'episode_nr', 'series_years', 'md5sum']
    },
    'movie_info': {
        'columns': ['id', 'movie_id', 'info_type_id', 'info', 'note']
    },
    'person_info': {
        'columns': ['id', 'person_id', 'info_type_id', 'info', 'note']
    }
}

# Create a list of all column names
all_columns = []
for v in data.values():
    all_columns.extend(v['columns'])


def load_csv(name):
    """ Load the given CSV file only """
    if name not in data.keys():
        raise ValueError('Invalid file')
    if 'data' not in data[name].keys() or data[name]['data'] is None:
        tp = pd.read_csv(csv_location + name + '.csv', iterator=True, chunksize=1000, header=None,
                         names=data[name]['columns'])
        data[name]['data'] = pd.concat(tp, ignore_index=True)

    return data[name]['data']


def load_all_csv():
    """ Load all the csv data files """
    for k in data.keys():
        print('Loading data %s' % k)
        data[k]['data'] = pd.read_csv(csv_location + k + '.csv', header=None, names=data[k]['columns'])


def sample_table(name, n):
    if name not in data.keys():
        raise ValueError('Invalid file')
    if data[name]['data'] is None:
        raise ValueError('Load the %s data first' % name)
    return data[name]['data'].sample(n)


def is_column_name(c):
    return c in all_columns


if __name__ == "__main__":
    print(is_column_name('person_role_id'))
