"""SynthLearn — a procedural novel-rule learning benchmark.

SynthLearn measures genuine learning (as opposed to pretraining memorization)
by asking models to induce a *provably novel* abstract binary operation from
examples and then generalize it compositionally to unseen nested expressions.

See README.md for the full task specification.
"""

from .algebra import Algebra
from .generator import all_depth1_pairs, generate_phase_items, random_tree
from .baselines import (
    RandomBaseline,
    MajorityBaseline,
    RoteBaseline,
    SymbolicLearner,
)
from .scoring import accuracy, learning_gain, feedback_gain
from .evaluate import evaluate_universe, efficiency_curve, feedback_completion_demo

__all__ = [
    "Algebra",
    "all_depth1_pairs",
    "generate_phase_items",
    "random_tree",
    "RandomBaseline",
    "MajorityBaseline",
    "RoteBaseline",
    "SymbolicLearner",
    "accuracy",
    "learning_gain",
    "feedback_gain",
    "evaluate_universe",
    "efficiency_curve",
    "feedback_completion_demo",
]

__version__ = "1.0.0"
