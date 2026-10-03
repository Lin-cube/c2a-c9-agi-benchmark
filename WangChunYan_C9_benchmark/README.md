# SynthLearn — 程序化新颖规则学习基准

> **赛道：** Track 1 — Learning（学习）
> **作者：** WangChunYan
> **对应提案：** `../WangChunYan_C2A_proposal.md`
> **原则：** AI-First · 拿来主义（站在 ARC / SCAN / DeepMind 框架的肩膀上）

SynthLearn 测量 LLM 的**真正学习能力**（而非预训练记忆）：模型能否从少数示例中归纳出一个**可证不存在于任何训练数据中的**抽象二元运算，并把它**组合泛化**到未见过的嵌套表达式？

---

## 核心思想

当前 LLM 评估混淆了「记忆」与「学习」：few-shot 答对可能来自预训练语料，而非真的学会。SynthLearn 用**程序化生成的新颖代数**从构造上根除这一混淆：

- **符号集**：`{a, b, c, d}` 等抽象符号
- **二元运算 `*`**：由**均匀随机 Cayley 表**定义（每个实例全新，答案可证不在任何训练数据中）
- **组合泛化**：训练示例只覆盖「深度 1」（单次运算），测试覆盖「深度 ≥ 2」的嵌套表达式——只有真正归纳出运算表才能答对，记忆表面模式必然失败

## 三阶段协议（KSTAR 对齐）

| 阶段 | 内容 | 测量的 KSTAR 环节 |
|------|------|-------------------|
| **Phase A** | 无示例，直接作答 | 基线知识 K₀（顺带验证新颖性） |
| **Phase B** | 给完整深度-1 表，测更深的组合 | K₀ → K₁ 的规则归纳 |
| **Phase C** | 逐题作答，答错即揭示答案 | ΔR → 更新 K 的反馈学习闭环 |

**核心指标：** 学习增益 `Learning Gain = acc(B) − acc(A)`；反馈增益 `Feedback Gain = acc(C) − acc(B)`；组合泛化度（深度 ≥ 2 未见表达式准确率）；学习效率（达到 80% 准确率所需示例数）。

## 目录结构

```
WangChunYan_C9_benchmark/
├── run.py                  # CLI 入口，运行基线并产出 results.json / results.md
├── requirements.txt        # 仅用标准库，无第三方依赖
├── README.md
└── synthlearn/
    ├── algebra.py          # Algebra：随机 Cayley 表 + 表达式求值
    ├── generator.py        # 程序化生成表达式/数据集
    ├── baselines.py        # random / majority / rote / symbolic 四档基线
    ├── scoring.py          # 精确匹配评分 + 指标
    ├── evaluate.py         # 三阶段评测 + 学习效率曲线 + 反馈演示
    └── adapter.py          # （可选）OpenAI 兼容 LLM 适配器
```

## 快速开始

```bash
cd WangChunYan_C9_benchmark
python run.py                    # 默认 10 个宇宙、4 符号，结果写入 results/
python run.py --universes 20 --symbols 5
```

运行后查看 `results/results.md`（人类可读）与 `results/results.json`（结构化数据）。

## 基线说明

| 基线 | 行为 | 预期表现 |
|------|------|---------|
| `random` | 均匀随机猜 | 各阶段 ≈ 1/n（无学习） |
| `majority` | 永远输出最频繁的训练答案 | 各阶段 ≈ 1/n（无学习） |
| `rote` | 只背见过的 (表达式→答案)，不会泛化 | 组合测试 ≈ 1/n（记忆者，不学习） |
| `symbolic` | 从示例重建 Cayley 表并精确求值 | 组合测试 ≈ 100%（真正的学习者/上界） |

这四档基线本身就能证明 benchmark 的**区分度**：只有 `symbolic`（真学习）能跨组合泛化，`rote`（记忆）与 `random` 都停在随机水平——这正是 Track 1 要测量的「学习 vs 记忆」的分水岭。

## 测试真实前沿模型（可选）

设置环境变量后，把 `adapter.LLMAdapter` 传给评测管线即可：

```bash
export SYNTHLEARN_API_KEY=sk-...          # 必填
export SYNTHLEARN_MODEL=gpt-4o             # 可选，默认 gpt-4o
export SYNTHLEARN_BASE_URL=https://api.openai.com/v1   # 可选
```

> 本仓库的 `run.py` 只用确定性基线（无需 API key、结果可复现）。真实模型测试结果见 `../WangChunYan_C9_测试结果.md` 中的说明。

## 复现性

- 所有随机性都由显式 `seed` 控制（`Algebra(seed=...)`、`generate_phase_items(seed=...)`、基线 `seed=...`）。
- 评分是单字母**精确匹配**，无人工判断、无部分分。
- 仅依赖 Python 3.10+ 标准库，无需 pip install。
