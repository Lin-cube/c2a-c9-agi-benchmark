"""Three-phase evaluation protocol, learning-efficiency curve, and feedback demo.

Phase A (zero-knowledge baseline, measures K0):
    compositional items with NO examples -> should be ~chance; this also
    validates novelty (a model scoring far above chance may have seen the rule).

Phase B (example-based learning, measures K0 -> K1 induction):
    the model is shown the full depth-1 table, then tested on *deeper*
    compositions it has never seen.  Only genuine rule induction generalizes.

Phase C (feedback learning, measures the DeltaR -> update-K loop):
    items are answered one at a time; a wrong answer is immediately followed by
    the correct one.  We measure whether behaviour improves.
"""

from __future__ import annotations

from .algebra import Algebra
from .generator import all_depth1_pairs, generate_phase_items
from .scoring import accuracy, feedback_accuracy
from .baselines import SymbolicLearner


def evaluate_universe(
    model_factory,
    algebra: Algebra,
    *,
    n_a: int = 40,
    n_b: int = 100,
    n_c: int = 60,
    min_leaves: int = 3,
    max_leaves: int = 6,
    base_seed: int = 0,
) -> dict:
    """Run one algebra universe through the full three-phase protocol.

    ``model_factory`` is a zero-argument callable returning a *fresh* model, so
    each phase starts from a clean slate (Phase A is deliberately unfitted).
    """
    # Phase A — zero-knowledge baseline (no examples)
    items_a = generate_phase_items(algebra, n_a, min_leaves, max_leaves, seed=base_seed)
    acc_a = accuracy(model_factory(), algebra, items_a)

    # Phase B — learn the full depth-1 table, generalize to deeper compositions
    training = [(e, algebra.answer(e)) for e in all_depth1_pairs(algebra.n)]
    items_b = generate_phase_items(algebra, n_b, min_leaves, max_leaves, seed=base_seed + 1000)
    m_b = model_factory()
    m_b.fit(training, algebra)
    acc_b = accuracy(m_b, algebra, items_b)

    # Phase C — feedback learning on a fresh item set
    items_c = generate_phase_items(algebra, n_c, min_leaves, max_leaves, seed=base_seed + 2000)
    m_c = model_factory()
    m_c.fit(training, algebra)
    acc_c = feedback_accuracy(m_c, algebra, items_c)

    return {
        "phase_a": acc_a,
        "phase_b": acc_b,
        "phase_c": acc_c,
        "learning_gain": acc_b - acc_a,
        "feedback_gain": acc_c - acc_b,
    }


def efficiency_curve(
    algebra: Algebra,
    *,
    n_test: int = 100,
    min_leaves: int = 3,
    max_leaves: int = 6,
    seed: int = 0,
):
    """Sweep the number of memorized table entries k and report accuracy.

    Returns a list of ``(k, accuracy)`` pairs.  This operationalises the
    *learning efficiency* metric: how many examples are needed before a
    symbolic learner can generalize compositionally.
    """
    training = [(e, algebra.answer(e)) for e in all_depth1_pairs(algebra.n)]
    items = generate_phase_items(algebra, n_test, min_leaves, max_leaves, seed=seed)
    n2 = algebra.n * algebra.n
    curve = []
    for k in range(2, n2 + 1, 2):
        model = SymbolicLearner(capacity=k, seed=123)
        model.fit(training, algebra)
        curve.append((k, accuracy(model, algebra, items)))
    return curve


def feedback_completion_demo(
    algebra: Algebra,
    *,
    capacity: int = 8,
    n_test: int = 100,
    min_leaves: int = 3,
    max_leaves: int = 6,
    seed: int = 0,
) -> dict:
    """Demonstrate the KSTAR DeltaR -> update-K loop concretely.

    A symbolic learner starts with only ``capacity`` table entries (few-shot),
    is tested, then receives the *missing* depth-1 entries as corrective
    feedback, and is tested again.  The accuracy jump is the feedback gain.
    """
    training = [(e, algebra.answer(e)) for e in all_depth1_pairs(algebra.n)]
    items = generate_phase_items(algebra, n_test, min_leaves, max_leaves, seed=seed)

    model = SymbolicLearner(capacity=capacity, seed=7)
    model.fit(training, algebra)
    acc_before = accuracy(model, algebra, items)

    for expr, ans in training:
        key = (algebra.symbols[expr[0]], algebra.symbols[expr[1]])
        if key not in model.table:
            model.on_feedback(expr, ans, algebra)
    acc_after = accuracy(model, algebra, items)

    return {
        "capacity": capacity,
        "acc_before": acc_before,
        "acc_after": acc_after,
        "feedback_gain": acc_after - acc_before,
    }
