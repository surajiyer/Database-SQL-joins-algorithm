import select_parser


def estimate_query(G, b, n):
    pass


queries = tuple(open('join-order-benchmark/allqueries.sql', 'r'))
# print(select_parser.select_stmt.parseString(queries[0]).dump())
for qry in queries:
    print(select_parser.get_tables(qry))
    print(select_parser.get_where(qry))
    break
