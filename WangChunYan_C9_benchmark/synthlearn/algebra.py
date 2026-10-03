"""Core abstraction: a procedurally generated *novel algebra*.

An "algebra universe" is a finite abstract symbol set together with a binary
operation defined by a uniformly random Cayley table.  Because the table is
drawn fresh for every instance, the answer to any expression is provably
absent from any pretraining corpus.  That novelty guarantee is what lets the
benchmark separate genuine learning from memorization.

Expressions are represented as nested tuples:
    - a leaf symbol is a plain ``int`` (index into the symbol set)
    - a compound expression is a ``(left, right)`` tuple

Example (n=4, symbols a/b/c/d):  ``((0, 1), 3)`` renders as ``((a*b)*d)``.
"""

from __future__ import annotations

import random


class Algebra:
    """A novel binary algebra over ``n_symbols`` abstract symbols.

    Attributes
    ----------
    symbols : list[str]
        Single-letter symbols (``a``..``z``).
    table : list[list[int]]
        ``table[i][j]`` is the result index of ``symbols[i] * symbols[j]``.
    unary : list[int]
        Optional leaf transformation (a permutation).  ``use_unary`` is kept as
        a difficulty extension; the v1 core benchmark uses the identity.
    """

    def __init__(self, n_symbols: int = 4, use_unary: bool = False, seed: int = 0):
        if not 2 <= n_symbols <= 26:
            raise ValueError("n_symbols must be in [2, 26]")
        self.n = n_symbols
        self.seed = seed
        self.use_unary = use_unary
        self.rng = random.Random(seed)
        self.symbols = [chr(97 + i) for i in range(self.n)]

        # Uniformly random Cayley table: every entry independent and fresh.
        self.table = [
            [self.rng.randrange(self.n) for _ in range(self.n)]
            for _ in range(self.n)
        ]

        self.unary = list(range(self.n))
        if use_unary:
            self.rng.shuffle(self.unary)

    # ------------------------------------------------------------------ #
    # Evaluation
    # ------------------------------------------------------------------ #
    def evaluate(self, expr) -> int:
        """Return the result index of ``expr``."""
        if isinstance(expr, int):
            return self.unary[expr] if self.use_unary else expr
        left, right = expr
        return self.table[self.evaluate(left)][self.evaluate(right)]

    def answer(self, expr) -> str:
        """Return the output symbol for ``expr``."""
        return self.symbols[self.evaluate(expr)]

    # ------------------------------------------------------------------ #
    # Rendering
    # ------------------------------------------------------------------ #
    def render(self, expr) -> str:
        """Render ``expr`` as an infix string, e.g. ``((a*b)*d)``."""
        if isinstance(expr, int):
            return self.symbols[expr]
        return "(" + self.render(expr[0]) + "*" + self.render(expr[1]) + ")"

    def table_str(self) -> str:
        """Render the full Cayley table as a fixed-width text block."""
        header = "    " + " ".join(self.symbols)
        rows = [header]
        for i in range(self.n):
            row = " ".join(self.symbols[self.table[i][j]] for j in range(self.n))
            rows.append(f"{self.symbols[i]}   {row}")
        return "\n".join(rows)
