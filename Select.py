import re


def perform_selections(query_relations, selects_for_relations):
    for qr in query_relations:
        for s in selects_for_relations[qr]:
            print('performing select', s, 'for relation', qr)
            # print(query_relations[qr])
            query_relations[qr] = perform_selection(s, query_relations[qr], qr)


# rename: mapping from abbreviation (like 'ct') to actual relation name (like 'company type')
# selection_string: e.g. "ct.kind = 'production companies'"
def perform_selection(relation, selection_string):
    ss = str(selection_string)

    if re.match('.*IS NOT NULL.*', ss):
        # print('case IS NOT NULL')
        parts = [x.strip() for x in ss.split('IS NOT NULL')]
        # print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]

        selection = relation[~relation[attribute].isnull()]
        return selection
    elif re.match('.*IS NULL.*', ss):
        # print('case IS NULL')
        parts = [x.strip() for x in ss.split('IS NULL')]
        # print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]

        selection = relation[relation[attribute].isnull()]
        return selection
    elif re.match('.*!=.*', ss):
        parts = [x.strip() for x in ss.split('!=')]
        # print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)

        selection = relation[relation[attribute] != value]
        return selection
    elif re.match('.*>=.*', ss):

        parts = [x.strip() for x in ss.split('>=')]
        # print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)
        # print('value:', value)

        query = attribute + ' >= ' + value
        # print('query:', query)
        selection = relation.query(query)
        return selection
    elif re.match('.*=.*', ss):
        parts = [x.strip() for x in ss.split('=')]
        # print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)

        selection = None

        try:
            number = int(value)
            query = attribute + ' == ' + value
            selection = relation.query(query)
        except ValueError:
            selection = relation[relation[attribute] == value]

        return selection
    elif re.match('.*<.*', ss):
        # return relation

        parts = [x.strip() for x in ss.split('<')]
        # print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)

        query = attribute + ' < ' + value
        selection = relation.query(query)
        return selection

    elif re.match('.*>.*', ss):
        # return relation

        parts = [x.strip() for x in ss.split('>')]
        # print(parts)
        lefthand = parts[0]
        lefthand_parts = lefthand.split('.')

        attribute = lefthand_parts[1]
        value = parts[1]
        value = strip_quotes(value)
        # print('value:', value)

        query = attribute + ' > ' + value
        # print('query:', query)
        selection = relation.query(query)
        return selection

    elif re.match('.* OR .*', ss, re.IGNORECASE):
        # print('case OR')
        # print('ss:', ss)
        remove_outer_parentheses(ss)
        or_parts = ss.split(' OR ')

        values = []
        attribute = ""

        for op in or_parts:
            parts = [x.strip() for x in op.split('LIKE')]
            lefthand = parts[0]
            lefthand_parts = [x.strip() for x in lefthand.split(".")]
            attribute = lefthand_parts[1]
            value = parts[1]
            value = strip_quotes(value)
            value = value.replace("%", ".*")
            values.append(value)

        match_string = ''
        for v in values:
            match_string += v + '|'
        match_string = match_string[0:-1]

        # print('match string:', match_string)
        # print('attribute:', attribute)

        selection = relation[~relation[attribute].isnull() & relation[attribute].str.match(match_string)]
        return selection

    elif re.match('.*LIKE.*', ss, re.IGNORECASE):
        remove_outer_parentheses(ss)

        parts = []
        negation = False
        if re.match('.*NOT LIKE.*', ss):
            parts = [x.strip() for x in ss.split('NOT LIKE')]
            negation = True
        else:
            parts = [x.strip() for x in ss.split('LIKE')]
        # print(parts)

        left_hand = parts[0]
        lefthand_parts = [x.strip() for x in left_hand.split(".")]

        attribute = lefthand_parts[1]
        # print(attribute)
        value = parts[1]
        value = strip_quotes(value)

        value = value.replace("%", ".*")
        # print(value)

        if negation:
            value = '^((?!' + value + ').)*$'

        # print(list(relation))
        selection = relation[~relation[attribute].isnull() & relation[attribute].str.match(value)]
        return selection
    elif re.match('.* BETWEEN .*', ss, re.IGNORECASE):
        # print('case BETWEEN')
        remove_outer_parentheses(ss)

        parts = ss.split('BETWEEN')
        left_hand = parts[0]
        left_hand_parts = [x.strip() for x in left_hand.split(".")]

        attribute = left_hand_parts[1]
        # print(attribute)

        values = parts[1]
        value_parts = [x.strip() for x in values.split('ABCDE')]
        low = value_parts[0]
        high = value_parts[1]
        # print('low:', low)
        # print('high:', high)

        query = attribute + ' > ' + low + ' and ' + attribute + ' < ' + high
        # print('query:', query)
        selection = relation.query(query)
        return selection
    elif re.match('.* IN .*', ss):
        # print('case IN')

        parts = [x.strip() for x in ss.split(' IN ')]
        left_hand = parts[0]
        left_hand_parts = [x.strip() for x in left_hand.split(".")]

        attribute = left_hand_parts[1]
        # print(attribute)

        right_hand = parts[1]
        list = remove_outer_parentheses(right_hand)
        items = [strip_quotes(x.strip()) for x in list.split(',')]
        # print('items:', items)

        selection = relation[relation[attribute].isin(items)]
        return selection

        return relation
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
