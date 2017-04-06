import DataLoader
import pandas as pd
import Select
from collections import defaultdict


class QueryGraph:
    def __init__(self, tables, joins, selects, test=False):
        assert isinstance(tables, dict) and all(isinstance(t[0], str) and isinstance(t[1], str) for t in tables.items())
        assert isinstance(joins, list) and all(isinstance(j, str) for j in joins)
        assert isinstance(selects, list) and all(isinstance(s, str) for s in selects)

        selects_for_relation = defaultdict(list)
        for s in selects:
            print('Building Select:', s)
            ss = Select.remove_outer_parentheses(str(s))
            table_abr = ss.split('.')[0]
            selects_for_relation[table_abr].append(ss)

        print('\nRelations:')
        self.V = dict()
        for (k, v) in tables.items():
            # Load the data
            print('Loading', (k, v))
            if test:
                df = pd.DataFrame()
            else:
                df = DataLoader.load_pickle(v)
                df.columns = [k + '_' + c for c in DataLoader.columns[v]]

                # Perform selections on the data
                for s in selects_for_relation[k]:
                    df = Select.perform_selection(df, s)
            df.name = k

            # Create a relation node
            r = Relation(df)
            self.V[k] = r

        # Create the predicate edges
        self.E = {v: set() for v in self.V}
        joins = [j.replace(' ', '').split('=') for j in joins]
        joins = [(t1.split('.'), t2.split('.')) for t1, t2 in joins]
        for t1, t2 in joins:
            print('t1:', t1, ', t2:', t2)
            assert t1[0] in self.V.keys() and t2[0] in self.V.keys()

            # Add edges between them
            r1, r2 = self.V[t1[0]], self.V[t2[0]]

            # set r2 as neighbor of r1
            if r2 in r1.neighbors.keys():
                r1.neighbors[r2].add((t1[1], t2[1]))
                self.E[r1].add(r2)
            else:
                r1.neighbors[r2] = {(t1[1], t2[1])}
                if r1 in self.E.keys():
                    self.E[r1].add(r2)
                else:
                    self.E[r1] = {r2}

            # set r1 as neighbor of r2
            if r1 in r2.neighbors.keys():
                r2.neighbors[r1].add((t2[1], t1[1]))
                self.E[r2].add(r1)
            else:
                r2.neighbors[r1] = {(t2[1], t1[1])}
                if r2 in self.E.keys():
                    self.E[r2].add(r1)
                else:
                    self.E[r2] = {r1}

        # Print all the neighbors
        print('\nNeighbors:')
        for k, v in self.V.items():
            print(k, ':', v.neighbors)

        print('\nEdges:')
        for k, v in self.E.items():
            print(k, ':', v)

    def get_relations(self):
        return self.V

    def get_neighbors(self, R_set):
        assert isinstance(R_set, frozenset) and all(isinstance(r, Relation) for r in R_set)
        return set().union(*[self.E.get(r, set()) for r in R_set]).difference(R_set)


class Relation:
    def __init__(self, df):
        assert isinstance(df, pd.DataFrame) and hasattr(df, 'name')
        self.df = df
        self.neighbors = dict()

    def _has_index(self, others):
        assert isinstance(others, frozenset) and all(isinstance(r, Relation) for r in others)
        x = {r: self.neighbors[r] for r in self.neighbors.keys() & others}
        return len(x) > 0, x

    def get_index(self, others):
        _, x = self._has_index(others)
        return x

    def has_index(self, others):
        has_ix, _ = self._has_index(others)
        return has_ix

    def sample_table(self, n):
        assert isinstance(n, int)
        if n > self.df.shape[0]:
            return self.df
        x = self.df.sample(n)
        x.name = self.df.name
        return x

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise AttributeError('Cannot change constant attribute')
        self.__dict__[key] = value

    def __len__(self):
        return len(self.df.index)

    def __hash__(self):
        return hash(self.df.name) ^ hash(frozenset(self.df.index))  # ^ hash(self.neighbors)

    def __eq__(self, other):
        return self.df.equals(other.df) and self.neighbors == other.neighbors

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)

    def __str__(self):
        return self.df.name

    def __repr__(self):
        return self.df.name
