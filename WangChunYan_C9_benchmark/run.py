"""SynthLearn demo runner.

Runs the deterministic baselines over a batch of procedurally generated
algebra universes and writes the aggregate results as JSON + Markdown.

Usage:
    python run.py                 # default: 10 universes, n=4 symbols
    python run.py --universes 20 --symbols 5
    python run.py --outdir results
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from synthlearn import (
    Algebra,
    MajorityBaseline,
    RandomBaseline,
    RoteBaseline,
    SymbolicLearner,
    efficiency_curve,
    evaluate_universe,
    feedback_completion_demo,
)


def mean(xs):
    return statistics.fmean(xs) if xs else float("nan")


def run(args):
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    baselines = {
        "random": lambda: RandomBaseline(seed=0),
        "majority": lambda: MajorityBaseline(seed=0),
        "rote": lambda: RoteBaseline(seed=0),
        "symbolic (oracle)": lambda: SymbolicLearner(capacity=None, seed=0),
    }

    # Aggregate metrics per baseline across universes.
    agg = {name: {"phase_a": [], "phase_b": [], "phase_c": [],
                  "learning_gain": [], "feedback_gain": []} for name in baselines}

    universes = []
    for u in range(args.universes):
        algebra = Algebra(n_symbols=args.symbols, use_unary=False, seed=u)
        row = {"seed": u, "symbols": args.symbols}
        for name, factory in baselines.items():
            res = evaluate_universe(factory, algebra, base_seed=u)
            for k, v in res.items():
                agg[name][k].append(v)
            row[name] = {k: round(v, 4) for k, v in res.items()}
        # Learning-efficiency curve on the first universe (deterministic).
        if u == 0:
            row["efficiency_curve"] = [
                {"k": k, "accuracy": round(a, 4)}
                for k, a in efficiency_curve(algebra, seed=0)
            ]
            row["feedback_completion_demo"] = {
                k: round(v, 4) for k, v in feedback_completion_demo(algebra).items()
            }
        universes.append(row)

    summary = {}
    for name in baselines:
        summary[name] = {
            "phase_a_mean": round(mean(agg[name]["phase_a"]), 4),
            "phase_b_mean": round(mean(agg[name]["phase_b"]), 4),
            "phase_c_mean": round(mean(agg[name]["phase_c"]), 4),
            "learning_gain_mean": round(mean(agg[name]["learning_gain"]), 4),
            "feedback_gain_mean": round(mean(agg[name]["feedback_gain"]), 4),
        }

    result = {
        "benchmark": "SynthLearn",
        "track": "Track 1 - Learning",
        "generated": date.today().isoformat(),
        "config": {
            "universes": args.universes,
            "symbols": args.symbols,
            "use_unary": False,
            "n_phase_a": 40,
            "n_phase_b": 100,
            "n_phase_c": 60,
            "min_leaves": 3,
            "max_leaves": 6,
        },
        "summary": summary,
        "universes": universes,
    }

    json_path = os.path.join(outdir, "results.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    md = render_markdown(result)
    md_path = os.path.join(outdir, "results.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Wrote {json_path} and {md_path}")
    print(md)


def render_markdown(result) -> str:
    cfg = result["config"]
    lines = [
        "# SynthLearn 基线测试结果（自动生成）",
        "",
        f"- 生成日期：{result['generated']}",
        f"- 配置：{cfg['universes']} 个代数宇宙 × {cfg['symbols']} 符号 × "
        f"(A={cfg['n_phase_a']}, B={cfg['n_phase_b']}, C={cfg['n_phase_c']} 题)，"
        f"组合叶子数 {cfg['min_leaves']}–{cfg['max_leaves']}",
        "",
        "## 汇总（各宇宙平均准确率）",
        "",
        "| 基线 | Phase A（无示例） | Phase B（给全表） | Phase C（反馈） | 学习增益 | 反馈增益 |",
        "|------|-------------------|-------------------|-----------------|----------|----------|",
    ]
    for name, s in result["summary"].items():
        lines.append(
            f"| {name} | {s['phase_a_mean']:.4f} | {s['phase_b_mean']:.4f} | "
            f"{s['phase_c_mean']:.4f} | {s['learning_gain_mean']:+.4f} | "
            f"{s['feedback_gain_mean']:+.4f} |"
        )
    lines.append("")

    u0 = result["universes"][0]
    if "efficiency_curve" in u0:
        lines += ["## 学习效率曲线（宇宙 #0，symbolic 学习者，容量 k）", ""]
        pts = ", ".join(f"k={p['k']}:{p['accuracy']:.2f}" for p in u0["efficiency_curve"])
        lines.append(pts)
        lines.append("")

    if "feedback_completion_demo" in u0:
        d = u0["feedback_completion_demo"]
        lines += [
            "## 反馈学习演示（宇宙 #0，KSTAR ΔR→K 闭环）",
            "",
            f"- 容量 {d['capacity']} 条表项：反馈前 {d['acc_before']:.4f} → 反馈后 {d['acc_after']:.4f}",
            f"- 反馈增益 = {d['feedback_gain']:+.4f}",
            "",
        ]

    lines.append("> 注：`symbolic (oracle)` 是真正归纳规则的学习者（上界）；`rote` 是只背题、不会泛化的记忆者。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SynthLearn baseline demo")
    parser.add_argument("--universes", type=int, default=10)
    parser.add_argument("--symbols", type=int, default=4)
    parser.add_argument("--outdir", type=str, default="results")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
