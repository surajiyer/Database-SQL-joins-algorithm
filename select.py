import re

def perform_selections(query_relations, selects_for_relations):
    for qr in query_relations:
        for s in selects_for_relations[qr]:
            print('performing select', s, 'for relation', qr)
            # print(query_relations[qr])
            query_relations[qr] = perform_selection(s, query_relations[qr])


# rename: mapping from abbreviation (like 'ct') to actual relation name (like 'company type')
# selection_string: e.g. "ct.kind = 'production companies'"
def perform_selection(selection_string, relation):
    ss = str(selection_string)
    if re.match('.*IS NULL.*', ss, re.IGNORECASE):
        parts = [x.strip() for x in ss.split('IS NULL')]
        print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]

        selection = relation[relation[attribute].isnull()]
        return selection
    elif re.match('.*!=.*', ss):
        parts = [x.strip() for x in ss.split('!=')]
        print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)

        selection = relation[relation[attribute] != value]
        return selection
    elif re.match('.*=.*', ss):
        parts = [x.strip() for x in ss.split('=')]
        print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)

        selection = relation[relation[attribute] == value]
        return selection
    elif re.match('.*<.*', ss):
        parts = [x.strip() for x in ss.split('<')]
        print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)

        query = attribute + ' < ' + value
        selection = relation.query(query)
        return selection
    elif re.match('.*>.*', ss):
        parts = [x.strip() for x in ss.split('>')]
        print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)

        query = attribute + ' > ' + value
        print('query:', query)
        selection = relation.query(query)
        return selection
    elif re.match('.*like.*', ss, re.IGNORECASE):
        remove_outer_parentheses(ss)

        parts = []
        negation = False
        if re.match('.*not like.*', ss):
            parts = [x.strip() for x in ss.split('not like')]
            negation = True
        else:
            parts = [x.strip() for x in ss.split('like')]
        print(parts)

        left_hand = parts[0]
        lefthand_parts = [x.strip() for x in left_hand.split(".")]

        attribute = lefthand_parts[1]
        print(attribute)
        value = parts[1]
        value = strip_quotes(value)

        value = value.replace("%", ".*")
        print(value)

        if negation:
            value = '^((?!' + value + ').)*$'

        # print(list(relation))
        selection = relation[~relation[attribute].isnull() & relation[attribute].str.match(value)]
        return selection
    else:
        return relation


def strip_quotes(value):
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    return value


def remove_outer_parentheses(ss):
    if ss.startswith('(') and ss.endswith(')'):
        return ss[1:-1]
    else:
        return ss

# testing

# df = d.data['movie_companies']['data']
# selectionEqual = df[df['kind'] == 'distributors']
# selectionLike = df[~df['note'].isnull() & df['note'].str.match('^((?!.*support.*).)*$')]
# selectionIn = df[df['id'].isin([1, 2, 3, 4])]
# print(selectionLike)
