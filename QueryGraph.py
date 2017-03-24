import pandas as pd


class QueryGraph:
    def __init__(self, tables, selects, joins):
        self.V = []
        self.E = dict()

        for op in selects:
            # TODO: call function here to calculate pandas dfs for selects
            self.V.append(op)



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

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value


class Predicate:
    def __init__(self, R1, R2):
        assert isinstance(R1, Relation) and isinstance(R2, Relation)
        self.u = R1
        self.v = R2

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value
