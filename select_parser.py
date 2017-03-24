import sqlparse as sp
import re
import data


def get_tables(sql_stmt):
    """
    Parse the tables of a SQL query
    :param sql_stmt:
    :return:
    """
    statement = sp.parse(sql_stmt)[0]
    from_token = next(token for i, token in enumerate(statement.tokens)
                      if (isinstance(token, sp.sql.IdentifierList) or isinstance(token, sp.sql.Identifier))
                      and str(statement.token_prev(i, skip_cm=True, skip_ws=True)[1]).lower() == 'from')
    if isinstance(from_token, sp.sql.IdentifierList):
        id_list = list(from_token.get_identifiers())
    elif isinstance(from_token, sp.sql.Identifier):
        id_list = [from_token]
    result = dict([(k[-1].value, k[0].value) for k in id_list])
    return result


def get_where(sql_stmt):
    """
    Parse the WHERE clause of a SQL query
    :param sql_stmt:
    :return:
    """
    statement = sp.parse(sql_stmt)[0]
    joins, selects = [], []
    # rename_map = {}
    where_token = next((token for token in statement.tokens if isinstance(token, sp.sql.Where)), None)

    if where_token is not None:
        # for t in statement.tokens:
        #     if isinstance(t, sp.sql.Where):
        #     from_token = statement.token_prev(statement.token_index(t), skip_ws=True)
        #     renames = str(from_token[1]).split(',')
        #
        #     for r in renames:
        #         rename_parts = [x.strip() for x in r.split('AS')]
        #         rename_map[rename_parts[1]] = rename_parts[0]

        for tt in where_token.tokens:
            if isinstance(tt, sp.sql.Comparison):
                split = str(tt[-1]).split('.')
                print(split)
                if len(split) > 1 and data.is_column_name(split[1]):
                    joins.append(tt)
                else:
                    selects.append(tt)
            elif re.match('.*like.*', str(tt)) or re.match('.*IN.*', str(tt)):
                selects.append(tt)

        # print('\nstatement: ')
        # print(statement)

        # print('\nrenames: ')
        # print(rename_map)

        print('\nselects:')
        for s in selects:
            print(s)

        print('joins:')
        for j in joins:
            print(j)

    return selects, joins

if __name__ == "__main__":
    tests = """select * from xyzzy as xyz where z > 100
        select * from xyzzy where z > 100 order by zz
        select * from xyzzy
        select * from xyz where x like '%(voice)%' AND (y = 1 OR x=2)
        SELECT MIN(mc.note) AS production_note, MIN(t.title) AS movie_title, MIN(t.production_year) AS movie_year FROM company_type AS ct, info_type AS it, movie_companies AS mc, movie_info_idx AS mi_idx, title AS t WHERE ct.kind = 'production companies' AND it.info = 'top 250 rank' AND mc.note  not like '%(as Metro-Goldwyn-Mayer Pictures)%' and (mc.note like '%(co-production)%' or mc.note like '%(presents)%') AND ct.id = mc.company_type_id AND t.id = mc.movie_id AND t.id = mi_idx.movie_id AND mc.movie_id = mi_idx.movie_id AND it.id = mi_idx.info_type_id;
        """.splitlines()

    for t in tests:
        print(t)
        print(get_tables(t))
        get_where(t)
        print()
