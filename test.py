
import pandas as pd
import numpy as np

column_names = ['id', 'name', 'imdb_index', 'imdb_id', 'name_pcode_nf', 'surname_pcode', 'md5sum']

dates = pd.date_range('20130101', periods=6)
df = pd.read_csv('data/char_name.csv', header=None, names=column_names, nrows = 10000)



# q = 'SELECT * FROM df'

# result = pysqldf(q)


q = 'id > 60 and id < 100'
result = df.query(q)

print(result)
