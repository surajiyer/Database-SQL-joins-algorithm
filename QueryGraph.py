import pandas as pd
import select_parser as sp
from collections import defaultdict
import pandas as pd

class QueryGraph:
    """ Graph data structure, undirected by default. """

    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """ Remove all references to node """

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """ Is node1 directly connected to node2 """

        return node1 in self._graph and node2 in self._graph[node1]

    def find_path(self, node1, node2, path=[]):
        """ Find any path between node1 and node2 (may not be shortest) """

        path = path + [node1]
        if node1 == node2:
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node not in path:
                new_path = self.find_path(node, node2, path)
                if new_path:
                    return new_path
        return None

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

    # def __init__(self, tables, selects, joins):
    #     self.V = []
    #     self.E = dict()
    #
    #     for op in selects:
    #         # TODO: call function here to calculate pandas dfs for selects
    #         self.V.append(op)
    #     for v in self.V:
    #         self.E[v] = set()
    #         for j in joins:
    #             self.E[v].add
    #     pass

    def get_relations(self):
        return self.V

    def get_neighbors(self, R):
        assert isinstance(R, Relation), 'R must be a relation expression'


class Relation:
    def __init__(self, df):
        assert isinstance(df, pd.DataFrame)
        self.df = df

    def get_index(self):
        pass

    def has_index(self):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value

    def __len__(self):
        return len(self.df.index)


class Predicate:
    def __init__(self, R1, R2):
        assert isinstance(R1, Relation) and isinstance(R2, Relation)
        self.u = R1
        self.v = R2

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value

