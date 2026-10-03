# AI 生成日志 / AI Generation Log

**作者 / Author:** WangChunYan
**挑战 / Challenge:** C2A — Track 1 Learning
**日期 / Date:** 2026-10-03

---

## 工具 / Tools Used

- **DeepSeek Harness 编码智能体（deepseek-v4-pro）** —— 论文分析、benchmark 调研、方案构思、提案撰写、多轮迭代
- **web_search / web_fetch** —— 核实文献真实性，避免「引用造假」

---

## 论文精读 / Paper Analysis

- **方法：** 将资料包中的 DeepMind 论文摘要（`deepmind-agi-cognitive-framework-summary.pdf`）交由 AI 提取结构，并用 web 检索交叉核实论文本体（arXiv:2605.28405），确认作者（Burnell, Yamamori, Firat 等）与十大认知能力分类。
- **关键提取：**
  1. 通用智能被拆解为 10 个认知能力，其中 **Learning、Metacognition、Attention、Executive Functions、Social Cognition 为评估缺口最大的五个赛道**。
  2. 论文强调传统 benchmark（MMLU、BIG-bench）易被「刷分」、训练数据污染，需「从模型评估转向系统评估」。
  3. 三阶段评估协议（认知评估 → 人类基线 → 认知画像）启发了我方的 Phase A/B/C 学习轨迹设计。
  4. Learning 赛道的核心困难 = 「区分真正的学习与预训练记忆的检索」，建议使用 held-out 认知任务——这直接催生了「程序化生成新颖代数」的核心思路。
- **迭代：** 1 轮精读 + 1 轮追问（ARC 与 Learning 赛道的关系、如何从构造上保证答案不在训练数据中）。

---

## Benchmark 调研 / Benchmark Research

- **搜索策略：**
  - Query 1: `Google DeepMind Measuring Progress Toward AGI Cognitive Framework 2026 authors`
  - Query 2: `Chollet 2019 On the Measure of Intelligence ARC benchmark`
  - Query 3: `Lake Baroni SCAN compositional generalization 2018`
- **发现并核实的真实文献：**
  - **ARC（Chollet, 2019, arXiv:1911.01547）**：去记忆化设计的鼻祖，但其视觉网格格式难以程序化大批量生成与自动评分。
  - **SCAN（Lake & Baroni, 2018, arXiv:1711.00350）**：组合泛化的经典框架，但规则固定，存在训练数据泄漏风险。
  - **Levels of AGI（Morris et al., 2024, arXiv:2311.02462）**：AGI 分级框架，提供「能力进展」的评估语境。
  - **BIG-bench（2022）、MMLU（Hendrycks et al., 2020）**：作为「传统基准易被刷分」的反面对照。
- **评估结果：** 共调研 6 个真实 benchmark，最终选择 ARC 的「去记忆化哲学」与 SCAN 的「组合泛化维度」作为两大借鉴支柱。
- **红线说明：** 示例包中出现的 `ARC-AGI-3`、`arXiv:2601.10904`、`LLM-Uncertainty-Bench` 等引用无法通过检索核实，**故全部弃用**，只采用可查证的来源，保证「研究严谨性」不扣分。

---

## 提案撰写 / Proposal Writing

- **初稿生成：** 提供「赛道 + 调研结果 + 核心想法（程序化生成新颖运算系统 + 三阶段协议）」，要求 AI 生成四段式双语提案初稿。
- **迭代次数：** 3 轮
  - 第 1 轮：初稿偏学术、缺具体示例 → 要求补充一个可手工验算的代数宇宙示例（Cayley 表 + 深度-1 示例 + 深度-2 测试）。
  - 第 2 轮：三阶段协议与 KSTAR 的对应不够清晰 → 重构为「Phase A 测 K₀ / Phase B 测归纳 / Phase C 测 ΔR→K 更新」。
  - 第 3 轮：补充人类基线数字、难度梯度比例（40/40/20）与 7 天可行性时间表。
- **人工修改（WangChunYan 审阅）：**
  - 用希腊字母 {α, β, γ} 替代图形符号（▲●■），避免终端/浏览器渲染兼容性问题。
  - 手工验算了示例中全部深度-2 表达式的答案，确保提案中的示例「可复现、无笔误」。
  - 删除了无法核实的 2026 年「前沿」引用，替换为可查证文献。

---

## 手动步骤说明 / Manual Steps Justification

| 手动步骤 | 为什么没用 AI |
|----------|-------------|
| 符号集选择（α/β/γ） | 需确保跨终端/浏览器渲染稳定，AI 不了解渲染兼容性 |
| 示例答案手工验算 | 提案中的每个示例必须数学上正确，需人工核对 Cayley 表计算结果 |
| 引用真实性把关 | 防止 AI 幻觉出「看起来权威但不存在」的 2026 年论文 |

---

## AI 段位自评 / AI Usage Level

**🔵 进阶** —— 多轮对话迭代优化 prompt，审阅并修正 AI 输出，核心思路（程序化生成 + 三阶段协议 + 组合泛化指标）为人工与 AI 协同构思。尚未达到完整 workflow 编排的「驾驭」水平。
