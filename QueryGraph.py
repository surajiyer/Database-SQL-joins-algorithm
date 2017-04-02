import pandas as pd
import Select
import DataLoader


class QueryGraph:
    def __init__(self, tables, joins, selects):
        assert isinstance(tables, dict) and all(isinstance(t[0], str) and isinstance(t[1], str) for t in tables.items())
        assert isinstance(joins, list) and all(isinstance(j, str) for j in joins)
        assert isinstance(selects, list) and all(isinstance(s, str) for s in selects)

        self.V = []
        self.E = dict()

        for (k, v) in tables.items():
            df = DataLoader.load_pickle(v)
            df.name = k

        for op in selects:
            # TODO: call function here to calculate pandas dfs for selects
            Select.perform_selections()
            self.V.append(op)
        for v in self.V:
            self.E[v] = set()
            for j in joins:
                self.E[v].add
        pass

    def get_relations(self):
        return self.V

    def get_neighbors(self, R):
        assert isinstance(R, Relation), 'R must be a relation expression'


class Relation:
    def __init__(self, df):
        assert isinstance(df, pd.DataFrame)
        self.df = df
        self.neighbors = dict()

    def get_index(self, other):
        assert isinstance(other, Relation)
        return self.df.index

    def has_index(self, other):
        assert isinstance(other, Relation)
        return False

    def sample_table(self, n):
        assert isinstance(n, int)
        return self.df.sample(n)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value

    def __len__(self):
        return len(self.df.index)


class Predicate:
    def __init__(self, R1, R2, predicate):
        assert isinstance(R1, Relation) and isinstance(R2, Relation)
        self.u = R1
        self.v = R2

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value
