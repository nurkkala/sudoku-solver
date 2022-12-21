#!/usr/bin/env python

## Sudoku solver

import re;
import sys;

class Entry(object):
    """Stack of values on a single entry in the puzzle."""
    def __init__(self, idx):
        self.idx = idx
        self.stack = set(range(1,10))

    def force(self, value):
        assert(isinstance(value, set))
        self.stack = value
    
    def prune(self, value):
        assert(isinstance(value, set))
        if len(self.stack) > 1:
            self.stack -= value
            if len(self.stack) == 1:
                print "Constrained {0} to {1}".format(self.idx, self.stack)

    def __str__(self):
        values = list(self.stack)
        if len(values) == 1:
            return ' {0}  '.format(values[0])
        else:
            return '_{0}_ '.format(len(values))

class Puzzle(object):
    def __init__(self, path=None, dim=3):
        self.dim = dim
        self.size = self.dim * self.dim
        self.length = self.size * self.size
        self.frame = [Entry(e) for e in range(self.length)]
        if path is not None:
            self.load(path)

    def load(self, path):
        """Load a puzzle from the file at 'path'."""
        f = open(path, 'rt')
        idx = 0
        for row in f:
            row = row.rstrip()
            if re.search(r'---------', row): continue
            row, n = re.subn(r'[|\s]', '', row)
            for col in row:
                if col.isdigit():
                    self.set(idx, int(col))
                idx += 1
        f.close()

    def set(self, idx, val):
        arg = set([val])
        for entry in self.row_of(idx):
            entry.prune(arg)
        for entry in self.col_of(idx):
            entry.prune(arg)
        for entry in self.cell_of(idx):
            entry.prune(arg)
        self.frame[idx].force(arg)

    def row(self, row):
        assert(row < self.size)
        return self.frame[row * self.size : (row + 1) * self.size]

    def row_of(self, idx):
        assert(idx < self.length)
        r = int(idx / self.size)
        return self.row(r)

    def col(self, col):
        assert(col < self.size)
        return self.frame[col : col + (self.length) : self.size]

    def col_of(self, idx):
        assert(idx < self.length)
        c = idx % self.size
        return self.col(c)

    def cell(self, cell):
        assert(cell < self.size)
        Row, Col = divmod(cell, self.dim)
        return [self.frame[r * self.size + c]
                for r in range(Row * self.dim, Row * self.dim + self.dim)
                for c in range(Col * self.dim, Col * self.dim + self.dim)]

    def cell_of(self, idx):
        assert(idx < self.length)
        Row = idx / (self.size * self.dim)
        Col = (idx % self.size) / self.dim
        c = Row * self.dim + Col
        return self.cell(c)

    def __str__(self):
        """Create a string that represents the puzzle."""
        rtn = ''
        cols = 0
        rows = 0
        for entry in self.frame:
            rtn += entry.__str__()
            cols += 1
            if cols % self.size == 0:
                rtn += "\n"
                rows += 1
                if rows < self.size and rows % self.dim == 0:
                    rtn += ('----' * self.size) + ('--' * (self.dim - 1)) + "\n"
            elif cols % self.dim == 0:
                rtn += '| '
        return rtn

if __name__ == '__main__':
    puzzle = Puzzle(sys.argv[1])
    print puzzle
