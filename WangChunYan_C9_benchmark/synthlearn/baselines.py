"""Reference baselines with a shared callable interface.

A "model" is any object exposing two methods:

    fit(training, algebra)      # training: list[(expr, answer_symbol)]
    predict(algebra, expr)      # -> predicted symbol

Baselines let us demonstrate the benchmark's discrimination power — and in
particular the gap between *memorizers* and *learners* — without a paid API.
"""

from __future__ import annotations

import random
from collections import Counter


class RandomBaseline:
    """Uniform random guessing.  No learning whatsoever."""

    name = "random"

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)

    def fit(self, training, algebra):
        return None

    def predict(self, algebra, expr) -> str:
        return algebra.symbols[self.rng.randrange(algebra.n)]


class MajorityBaseline:
    """Always predict the most frequent training output (a weak non-learner)."""

    name = "majority"

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)
        self.mode = None
        self.fitted = False

    def fit(self, training, algebra):
        self.mode = Counter(ans for _, ans in training).most_common(1)[0][0]
        self.fitted = True

    def predict(self, algebra, expr) -> str:
        if not self.fitted:
            return algebra.symbols[self.rng.randrange(algebra.n)]
        return self.mode


class RoteBaseline:
    """Rote memorizer: recalls exact training items, else falls back.

    On unseen compositional expressions it cannot generalize — modelling an
    LLM that only pattern-matches and never induces the underlying rule.
    """

    name = "rote"

    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)
        self.mem = {}
        self.fallback = None
        self.fitted = False

    def fit(self, training, algebra):
        self.mem = {algebra.render(expr): ans for expr, ans in training}
        self.fallback = Counter(ans for _, ans in training).most_common(1)[0][0]
        self.fitted = True

    def predict(self, algebra, expr) -> str:
        if not self.fitted:
            return algebra.symbols[self.rng.randrange(algebra.n)]
        return self.mem.get(algebra.render(expr), self.fallback)

    def on_feedback(self, expr, ans, algebra):
        self.mem[algebra.render(expr)] = ans


class SymbolicLearner:
    """A genuine rule-induction learner (oracle / upper bound).

    Reconstructs the Cayley table from depth-1 examples and evaluates nested
    expressions exactly.  ``capacity`` limits how many table entries it is
    allowed to memorize, which lets us measure *learning efficiency* (how many
    examples are needed before compositional generalization succeeds).
    """

    name = "symbolic"

    def __init__(self, capacity: int | None = None, seed: int = 0):
        self.capacity = capacity
        self.rng = random.Random(seed)
        self.table = {}
        self.fitted = False

    def fit(self, training, algebra):
        pairs = list(training)
        self.rng.shuffle(pairs)
        if self.capacity is not None:
            pairs = pairs[: self.capacity]
        for expr, ans in pairs:
            i, j = expr
            self.table[(algebra.symbols[i], algebra.symbols[j])] = ans
        self.fitted = True

    def _eval(self, expr, algebra) -> str:
        if isinstance(expr, int):
            return algebra.symbols[expr]
        left = self._eval(expr[0], algebra)
        right = self._eval(expr[1], algebra)
        return self.table[(left, right)]

    def predict(self, algebra, expr) -> str:
        if not self.fitted:
            return algebra.symbols[self.rng.randrange(algebra.n)]
        try:
            return self._eval(expr, algebra)
        except KeyError:
            # A not-yet-learned table entry: fall back to a guess.
            return algebra.symbols[self.rng.randrange(algebra.n)]

    def on_feedback(self, expr, ans, algebra):
        """Incorporate a depth-1 (i, j) feedback pair into the table."""
        if (
            isinstance(expr, tuple)
            and len(expr) == 2
            and isinstance(expr[0], int)
            and isinstance(expr[1], int)
        ):
            self.table[(algebra.symbols[expr[0]], algebra.symbols[expr[1]])] = ans
