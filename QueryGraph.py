import DataLoader
import pandas as pd


class QueryGraph:
    def __init__(self, tables, joins, selects):
        assert isinstance(tables, dict) and all(isinstance(t[0], str) and isinstance(t[1], str) for t in tables.items())
        assert isinstance(joins, list) and all(isinstance(j, str) for j in joins)
        assert isinstance(selects, list) and all(isinstance(s, str) for s in selects)

        print('\nRelations:')
        self.V = dict()
        for (k, v) in tables.items():
            # Load the data
            print('Loading', (k, v))
            df = DataLoader.load_pickle(v)
            # df = pd.DataFrame()
            df.name = k

            # Perform selections on the data
            # TODO: do some selects on the df

            # Create a relation node
            r = Relation(df)
            self.V[k] = r

        # Create the predicate edges
        self.E = {v: set() for v in self.V}
        joins = [j.replace(' ', '').split('=') for j in joins]
        joins = [(t1.split('.'), t2.split('.')) for t1, t2 in joins]
        for t1, t2 in joins:
            assert t1[0] in self.V.keys() and t2[0] in self.V.keys()

            # Add edges between them
            r1, r2 = self.V[t1[0]], self.V[t2[0]]

            # set r2 as neighbor of r1
            if r2 in r1.neighbors.keys():
                r1.neighbors[r2].add((t1[1], t2[1]))
                self.E[r1].add(r2)
            else:
                r1.neighbors[r2] = {(t1[1], t2[1])}
                self.E[r1] = {r2}

            # set r1 as neighbor of r2
            if r1 in r2.neighbors.keys():
                r2.neighbors[r1].add((t2[1], t1[1]))
                self.E[r2].add(r1)
            else:
                r2.neighbors[r1] = {(t2[1], t1[1])}
                self.E[r2] = {r1}

        # Print all the neighbors
        print('\nNeighbors:')
        for k, v in self.V.items():
            print(k, ':', v.neighbors)

    def get_relations(self):
        return self.V

    def get_neighbors(self, R):
        assert isinstance(R, Relation), 'R must be a relation'
        return self.E.get(R, default=set())


class Relation:
    def __init__(self, df):
        assert isinstance(df, pd.DataFrame) and hasattr(df, 'name')
        self.df = df
        self.neighbors = dict()

    def get_index(self, other):
        assert isinstance(other, Relation) and hasattr(other.df, 'name')
        x = self.neighbors.get(other.df.name, default=set())
        if not x:
            return None
        x = next(iter(x))[1]
        return x

    def has_index(self, other):
        assert isinstance(other, Relation) and hasattr(other.df, 'name')
        x = self.neighbors.get(other.df.name, default=None)
        return x is not None

    def sample_table(self, n):
        assert isinstance(n, int)
        return self.df.sample(n)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value

    def __len__(self):
        return len(self.df.index)

    def __hash__(self):
        return hash(self.df.name) ^ hash(frozenset(self.df.index))# ^ hash(self.neighbors)

    def __eq__(self, other):
        return self.df.equals(other.df) and self.neighbors == other.neighbors

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __repr__(self):
        return self.df.name


# class Predicate:
#     def __init__(self, R1, R2, predicate):
#         assert isinstance(R1, Relation) and isinstance(R2, Relation)
#         self.u = R1
#         self.v = R2
#
#     def __setattr__(self, key, value):
#         if key in self.__dict__:
#             raise AttributeError('Cannot change constant attribute')
#         self.__dict__[key] = value
