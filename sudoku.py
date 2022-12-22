#!/usr/bin/env python

# Sudoku solver

import re
import sys


def banner(message, loud=False):
    rtn = f"===== {message} ====="
    if loud:
        rule = "=" * (len(message) + 12)
        rtn = "\n".join([rule, rtn, rule])
    return rtn


class Cell(object):
    """Stack of values on a single entry in the puzzle."""

    def __init__(self, puzzle, idx):
        self.idx = idx
        self.row = idx // puzzle.size + 1
        self.col = idx % puzzle.size + 1
        self.stack = set(range(1, puzzle.size + 1))

    @property
    def coords(self):
        return self.row, self.col

    @property
    def size(self):
        return len(self.stack)

    def force(self, value):
        """Force this entry to be a set with the given `value`"""
        assert isinstance(value, set)
        print(f"Set {self.coords} to {value}")
        self.stack = value

    def prune(self, value):
        """Remove elements in set `value` from this cell."""
        assert isinstance(value, set)
        # print(f"Prune {value} from {self.coords}")
        if len(self.stack) > 1:
            self.stack -= value
            if len(self.stack) == 1:
                print(f"Constrained {self.coords} to {self.stack}")
                return self
        return None

    def __str__(self):
        values = list(self.stack)
        if len(values) == 1:
            # It's a single value; return it.
            return f" {values[0]}  "
        else:
            # It has multiple values; return how many.
            return f"[{len(values)}] "


class WorkQueue(object):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.queue = []

    def __str__(self):
        output = banner("Queue") + "\n"
        if len(self.queue) > 1:
            output += "\n".join([f"{cell.coords} {cell.stack}" for cell in self.queue])
        else:
            output += "empty"
        return output

    @property
    def empty(self):
        return len(self.queue) == 0

    def add(self, cell):
        self.queue.append(cell)
        print(self)

    def do_one(self):
        assert not self.empty
        cell = self.queue.pop(0)
        assert cell.size == 1
        self.puzzle.set(cell.idx, list(cell.stack)[0])
        print(self)


class Puzzle(object):
    def __init__(self, dim=3):
        self.dim = dim
        self.size = self.dim * self.dim
        self.length = self.size * self.size
        self.cells = [Cell(self, idx) for idx in range(self.length)]
        self.work = WorkQueue(self)

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
        print(banner("Puzzle loaded", True))

    def solve(self):
        while not self.work.empty:
            self.work.do_one()

    def set(self, idx, val):
        assert isinstance(val, int)
        print(self)
        arg = {val}
        for entry in self.row_containing(idx) + self.col_containing(idx) + self.block_containing(idx):
            cell = entry.prune(arg)
            if cell is not None:
                self.work.add(cell)
        self.cells[idx].force(arg)

    def row(self, row):
        """Return the row of the puzzle at index `row`."""
        assert row < self.size
        return self.cells[row * self.size: (row + 1) * self.size]

    def row_containing(self, idx):
        """Return the row of the puzzle containing the given `idx`."""
        assert idx < self.length
        return self.row(idx // self.size)

    def col(self, col):
        """Return a column of the puzzle at index `col`."""
        assert col < self.size
        return self.cells[col: col + self.length: self.size]

    def col_containing(self, idx):
        """Return the column of the puzzle containing the given `idx`."""
        assert idx < self.length
        return self.col(idx % self.size)

    def block(self, idx):
        """Return the sub-block of the puzzle at index `idx`."""
        assert idx < self.size
        row, col = divmod(idx, self.dim)
        return [self.cells[r * self.size + c]
                for r in range(row * self.dim, row * self.dim + self.dim)
                for c in range(col * self.dim, col * self.dim + self.dim)]

    def block_containing(self, idx):
        """Return the sub-block of the puzzle containing the given `idx`."""
        assert idx < self.length
        row = idx // (self.size * self.dim)
        col = (idx % self.size) // self.dim
        return self.block(row * self.dim + col)

    def __str__(self):
        """Create a string that represents the puzzle."""
        rtn = ''
        cols = 0
        rows = 0
        for entry in self.cells:
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
    if len(sys.argv) == 3:
        puzzle = Puzzle(int(sys.argv[1]))
        puzzle.load(sys.argv[2])
    else:
        puzzle = Puzzle()
        if len(sys.argv) == 2:
            puzzle.load(sys.argv[1])

    print(puzzle)
    puzzle.solve()
    print(puzzle)
