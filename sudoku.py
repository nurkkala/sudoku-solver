#!/usr/bin/env python

# Sudoku solver

import re
import sys


class Entry(object):
    """Stack of values on a single entry in the puzzle."""

    def __init__(self, idx, frame_size):
        self.idx = idx
        self.frame_size = frame_size
        self.stack = set(range(1, 10))

    @property
    def coords(self):
        return self.idx // self.frame_size + 1, self.idx % self.frame_size + 1

    def force(self, value):
        """Force this entry to be a set with the given `value`"""
        assert isinstance(value, set)
        print(f"Set {self.coords} to {value}")
        self.stack = value

    def prune(self, value):
        """Remove elements in set `value` from this entry."""
        assert isinstance(value, set)
        # print(f"Prune {value} from {self.coords}")
        if len(self.stack) > 1:
            self.stack -= value
            if len(self.stack) == 1:
                print("Constrained {0} to {1}".format(self.coords, self.stack))

    def __str__(self):
        values = list(self.stack)
        if len(values) == 1:
            # It's a single value; return it.
            return ' {0}  '.format(values[0])
        else:
            # It has multiple values; return how many.
            return '[{0}] '.format(len(values))


class Puzzle(object):
    def __init__(self, path=None, dim=3):
        self.dim = dim
        self.size = self.dim * self.dim
        self.length = self.size * self.size
        self.frame = [Entry(e, self.size) for e in range(self.length)]
        if path is not None:
            self.load(path)

    def load(self, path):
        """Load a puzzle from the file at 'path'."""
        with open(path, "rt") as f:
            idx = 0
            for row in f:
                row = row.strip()
                if re.search(r'---------', row):
                    continue
                row, n = re.subn(r'[|\s]', '', row)
                for col in row:
                    if col.isdigit():
                        self.set(idx, int(col))
                    idx += 1

    def set(self, idx, val):
        assert isinstance(val, int)
        print(self)
        arg = {val}
        for entry in self.row_of(idx):
            entry.prune(arg)
        for entry in self.col_of(idx):
            entry.prune(arg)
        for entry in self.sub_block_of(idx):
            entry.prune(arg)
        self.frame[idx].force(arg)

    def row(self, row):
        """Return the row of the puzzle at index `row`."""
        assert row < self.size
        return self.frame[row * self.size: (row + 1) * self.size]

    def row_of(self, idx):
        """Return the row of the puzzle containing the given `idx`."""
        assert idx < self.length
        return self.row(idx // self.size)

    def col(self, col):
        """Return a column of the puzzle at index `col`."""
        assert col < self.size
        return self.frame[col: col + self.length: self.size]

    def col_of(self, idx):
        """Return the column of the puzzle containing the given `idx`."""
        assert idx < self.length
        return self.col(idx % self.size)

    def sub_block(self, idx):
        """Return the sub-block of the puzzle at index `idx`."""
        assert idx < self.size
        row, col = divmod(idx, self.dim)
        return [self.frame[r * self.size + c]
                for r in range(row * self.dim, row * self.dim + self.dim)
                for c in range(col * self.dim, col * self.dim + self.dim)]

    def sub_block_of(self, idx):
        """Return the sub-block of the puzzle containing the given `idx`."""
        assert idx < self.length
        row = idx // (self.size * self.dim)
        col = (idx % self.size) // self.dim
        return self.sub_block(row * self.dim + col)

    def __str__(self):
        """Create a string that represents the puzzle."""
        rtn = ''
        cols = 0
        rows = 0
        for entry in self.frame:
            rtn += str(entry)
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
    print(puzzle)
