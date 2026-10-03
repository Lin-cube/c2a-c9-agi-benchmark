# AI 生成日志 / AI Generation Log（C9 阶段）

**作者 / Author:** WangChunYan
**挑战 / Challenge:** C9 — Track 1 Learning（Benchmark 开发）
**日期 / Date:** 2026-10-03

---

## 工具 / Tools Used

- **DeepSeek Harness 编码智能体（deepseek-v4-pro）** —— 技术规格转化、代码框架生成、调试优化、文档生成
- **Python 3.13 标准库** —— 运行与验证（无第三方依赖）

---

## 技术规格转化 / Spec Conversion

- **方法：** 把 C2A 提案交给 AI，要求输出「输入/输出格式、评分函数、数据集结构、模块划分」。
- **关键决策：**
  - 表达式用嵌套元组 `(left, right)` 表示叶子/内部节点，`int` 表示叶子，天然支持递归求值。
  - 评分用单字母精确匹配，确定性、无人工。
  - 模块拆分为 `algebra / generator / baselines / scoring / evaluate / adapter` 六块，职责单一。
- **迭代：** 1 轮初稿 + 1 轮「可学习性」追问（见反思报告）。

## Benchmark 代码生成 / Code Generation

- **AI 生成：** `algebra.py`（随机 Cayley 表 + 求值/渲染）、`generator.py`（随机二叉树 + 全深度-1 表）、`baselines.py`（四档基线）、`scoring.py`、`evaluate.py`（三阶段 + 效率曲线 + 反馈演示）、`run.py`（CLI + JSON/MD 输出）、`adapter.py`（OpenAI 兼容）。
- **调试轮次：** 3 轮
  - 第 1 轮：一元变换导致任务欠定 → 收敛为 v1 仅二元运算，一元降级为扩展项。
  - 第 2 轮：`rote`/`majority` 基线在组合测试上的行为需明确（二者都退化为「众数偏置」，值相等），确认这是预期而非 bug。
  - 第 3 轮：`run.py` 控制台中文在 Windows GBK 终端乱码 → 改为**写入 UTF-8 文件**（results.md/json），控制台输出仅为辅助。
- **运行验证：** `python run.py` 一次通过，10 宇宙 × 4 基线全部产出，数字可复现。

## 测试运行 / Test Execution

- 由 AI 直接执行 `python run.py`，产出 `results/results.json`（结构化）与 `results/results.md`（可读）。
- 结果解读也由 AI 完成：三档分离（100% / 37.8% / 25%）、效率曲线单调、反馈增益 +0.69。

## 文档生成 / Documentation

- AI 生成 `README.md`、`task说明.md`、`测试结果.md`、`反思报告.md`，作者审阅后定稿。

## 手动步骤说明 / Manual Steps Justification

| 手动步骤 | 为什么没用 AI |
|----------|-------------|
| 「可学习性」数学推演（欠定判定） | AI 初版直接实现了欠定的一元变换，需人工做参数计数推演才发现并纠正 |
| 引用真实性核实 | AI 会倾向编造「2026 年前沿论文」，需人工逐条 web 检索核实 |
| 示例答案验算 | Cayley 表计算结果需人工核对，确保文档示例无笔误 |
| 结果数字合理性审查 | 需人工判断「rote≈majority=37.8%」是合理现象而非实现错误 |

---

## AI 段位自评 / AI Usage Level

**🟣 驾驭** —— 本阶段已不是「一问一答」，而是设计了完整的模块化 workflow（规格→生成→调试→运行→文档），并让 AI 自主完成「运行 + 结果解读」的闭环；关键的正确性判断仍由人工把关。
