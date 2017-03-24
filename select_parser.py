# select_parser.py
# Copyright 2010, Paul McGuire
#
# a simple SELECT statement parser, taken from SQLite's SELECT statement
# definition at http://www.sqlite.org/lang_select.html
#
# from pyparsing import *
import sqlparse as sp
import re
import data

# LPAR, RPAR, COMMA = map(Suppress, "(),")
# select_stmt = Forward().setName("select statement")
#
# # keywords
# (UNION, ALL, AND, INTERSECT, EXCEPT, COLLATE, ASC, DESC, ON, USING, NATURAL, INNER,
#  CROSS, LEFT, OUTER, JOIN, AS, INDEXED, NOT, SELECT, DISTINCT, FROM, WHERE, GROUP, BY,
#  HAVING, ORDER, BY, LIMIT, OFFSET) = map(CaselessKeyword, """UNION, ALL, AND, INTERSECT,
#  EXCEPT, COLLATE, ASC, DESC, ON, USING, NATURAL, INNER, CROSS, LEFT, OUTER, JOIN, AS, INDEXED, NOT, SELECT,
#  DISTINCT, FROM, WHERE, GROUP, BY, HAVING, ORDER, BY, LIMIT, OFFSET""".replace(",", "").split())
# (CAST, ISNULL, NOTNULL, NULL, IS, BETWEEN, ELSE, END, CASE, WHEN, THEN, EXISTS,
#  COLLATE, IN, LIKE, GLOB, REGEXP, MATCH, ESCAPE, CURRENT_TIME, CURRENT_DATE,
#  CURRENT_TIMESTAMP) = map(CaselessKeyword, """CAST, ISNULL, NOTNULL, NULL, IS, BETWEEN, ELSE,
#  END, CASE, WHEN, THEN, EXISTS, COLLATE, IN, LIKE, GLOB, REGEXP, MATCH, ESCAPE,
#  CURRENT_TIME, CURRENT_DATE, CURRENT_TIMESTAMP""".replace(",", "").split())
# keyword = MatchFirst((UNION, ALL, INTERSECT, EXCEPT, COLLATE, ASC, DESC, ON, USING, NATURAL, INNER,
#                       CROSS, LEFT, OUTER, JOIN, AS, INDEXED, NOT, SELECT, DISTINCT, FROM, WHERE, GROUP, BY,
#                       HAVING, ORDER, BY, LIMIT, OFFSET, CAST, ISNULL, NOTNULL, NULL, IS, BETWEEN, ELSE, END, CASE, WHEN,
#                       THEN, EXISTS, COLLATE, IN, LIKE, GLOB, REGEXP, MATCH, ESCAPE, CURRENT_TIME, CURRENT_DATE,
#                       CURRENT_TIMESTAMP))
#
# identifier = ~keyword + Word(alphas, alphanums + "_")
# collation_name = identifier.copy()
# column_name = identifier.copy()
# column_alias = identifier.copy()
# table_name = identifier.copy()
# table_alias = identifier.copy()
# index_name = identifier.copy()
# function_name = identifier.copy()
# parameter_name = identifier.copy()
# database_name = identifier.copy()
#
# # expression
# expr = Forward().setName("expression")
#
# integer = Regex(r"[+-]?\d+")
# numeric_literal = Regex(r"\d+(\.\d*)?([eE][+-]?\d+)?")
# string_literal = QuotedString("'")
# blob_literal = Combine(oneOf("x X") + "'" + Word(hexnums) + "'")
# literal_value = (numeric_literal | string_literal | blob_literal |
#                  NULL | CURRENT_TIME | CURRENT_DATE | CURRENT_TIMESTAMP)
# bind_parameter = (
#     Word("?", nums) |
#     Combine(oneOf(": @ $") + parameter_name)
# )
# type_name = oneOf("TEXT REAL INTEGER BLOB NULL")
#
# expr_term = (
#     CAST + LPAR + expr + AS + type_name + RPAR |
#     EXISTS + LPAR + select_stmt + RPAR |
#     function_name + LPAR + Optional(delimitedList(expr)) + RPAR |
#     literal_value |
#     bind_parameter |
#     identifier
# )
#
# UNARY, BINARY, TERNARY = 1, 2, 3
# expr << operatorPrecedence(expr_term,
#                            [
#                                (oneOf('- + ~') | NOT, UNARY, opAssoc.LEFT),
#                                ('||', BINARY, opAssoc.LEFT),
#                                (oneOf('* / %'), BINARY, opAssoc.LEFT),
#                                (oneOf('+ -'), BINARY, opAssoc.LEFT),
#                                (oneOf('<< >> & |'), BINARY, opAssoc.LEFT),
#                                (oneOf('< <= > >='), BINARY, opAssoc.LEFT),
#                                (oneOf('= == != <>') | IS | IN | LIKE | GLOB | MATCH | REGEXP, BINARY, opAssoc.LEFT),
#                                ('||', BINARY, opAssoc.LEFT),
#                                ((BETWEEN, AND), TERNARY, opAssoc.LEFT),
#                            ])
#
# compound_operator = (UNION + Optional(ALL) | INTERSECT | EXCEPT)
#
# ordering_term = expr + Optional(COLLATE + collation_name) + Optional(ASC | DESC)
#
# join_constraint = Optional(ON + expr | USING + LPAR + Group(delimitedList(column_name)) + RPAR)
#
# join_op = COMMA | (Optional(NATURAL) + Optional(INNER | CROSS | LEFT + OUTER | LEFT | OUTER) + JOIN)
#
# join_source = Forward()
# single_source = ((Group(database_name("database") + "." + table_name("table")) | table_name("table")) +
#                  Optional(Optional(AS) + table_alias("table_alias")) +
#                  Optional(INDEXED + BY + index_name("name") | NOT + INDEXED)("index") |
#                  (LPAR + select_stmt + RPAR + Optional(Optional(AS) + table_alias)) |
#                  (LPAR + join_source + RPAR))
#
# join_source << single_source + ZeroOrMore(join_op + single_source + join_constraint)
#
# result_column = "*" | table_name + "." + "*" | (expr + Optional(Optional(AS) + column_alias))
# select_core = (SELECT + Optional(DISTINCT | ALL) + Group(delimitedList(result_column))("columns") +
#                Optional(FROM + join_source) +
#                Optional(WHERE + expr("where_expr")) +
#                Optional(GROUP + BY + Group(delimitedList(ordering_term)("group_by_terms")) +
#                         Optional(HAVING + expr("having_expr"))))
#
# select_stmt << (select_core + ZeroOrMore(compound_operator + select_core) +
#                 Optional(ORDER + BY + Group(delimitedList(ordering_term))("order_by_terms")) +
#                 Optional(LIMIT + (integer + OFFSET + integer | integer + COMMA + integer)))
#
# like_stmt = Optional(NOT) + \
#             Group(Word(alphas, alphanums) + "." + Word(alphas, alphanums) | Word(alphas, alphanums)) + \
#             LIKE + \
#             Word(alphanums + '_%()[]')
#
# where_stmt = (WHERE + OneOrMore(ZeroOrMore(like_stmt)))


def get_tables(sql_stmt):
    """
    Parse the tables of a SQL query
    :param sql_stmt:
    :return:
    """
    statement = sp.parse(sql_stmt)[0]
    print(statement.tokens)
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

        print('joins:')
        for j in joins:
            print(j)

        print('\nselects:')
        for s in selects:
            print(s)

    return joins, selects

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
