# 拿来说明 / Attribution（C9 阶段）

**作者 / Author:** WangChunYan
**挑战 / Challenge:** C9 — Track 1 Learning（Benchmark 实现）
**日期 / Date:** 2026-10-03

---

## 借鉴来源 / References

| 来源 / Source | 链接 / Link | 借了什么 / What was borrowed |
|---------------|-------------|------------------------------|
| ARC (Chollet, 2019) | [arXiv:1911.01547](https://arxiv.org/abs/1911.01547) | 「任务不得依赖预训练知识」的设计哲学 + few-shot 抽象推理范式 |
| SCAN (Lake & Baroni, 2018) | [arXiv:1711.00350](https://arxiv.org/abs/1711.00350) | 「组合泛化」作为核心测量维度 + 序列到序列的评分思路 |
| DeepMind 框架 (2026) | [arXiv:2605.28405](https://ar5iv.labs.arxiv.org/html/2605.28405) | 三阶段评估协议 + Learning 赛道「区分学习与记忆」的核心问题 |
| Levels of AGI (Morris et al., 2024) | [arXiv:2311.02462](https://arxiv.org/abs/2311.02462) | 能力分级语境 |
| BIG-bench (2022) | [arXiv:2206.04615](https://arxiv.org/abs/2206.04615) | 程序化生成评测任务（programmatic tasks）的组织方式 |
| KSTAR 框架 | 课程资料 | ΔR→K 更新闭环（落地为 Phase C 反馈学习） |

---

## 拿来的部分 / Adopted

- **从 ARC 拿了**：去记忆化哲学——随机生成保证答案不在训练数据中。
- **从 SCAN 拿了**：组合泛化作为「真学习」的试金石。
- **从 BIG-bench 拿了**：程序化生成任务（programmatic）的组织与自动评分范式。
- **从 DeepMind 拿了**：三阶段协议，改造成 Phase A/B/C。
- **从 KSTAR 拿了**：ΔR→K 闭环，落地为「反馈学习演示」。

## 去掉的部分 / Removed

| 来源 | 做了什么 | 我不要 | 原因 |
|------|---------|--------|------|
| ARC | 视觉网格格式 | 去掉视觉，改符号代数 | 视觉难程序化大批量生成、评分需网格匹配 |
| SCAN | 固定规则集 | 去掉固定规则 | 泄漏风险；改每次随机生成 Cayley 表 |
| BIG-bench | 海量零散任务 | 只取「程序化生成」组织方式 | 任务要聚焦单一认知能力，不能摊大饼 |

## 我的改进 / My Improvements

1. **随机 Cayley 表构造「新颖代数」**：比 ARC 的视觉网格、SCAN 的固定规则更彻底——每个实例的答案从构造上全新，且「不可结合」特性使套用错误理论（如假定结合律）必然失败。
2. **「可学习性」约束**：明确训练示例必须能唯一确定运算表（否则题目欠定、答案不唯一），把一元变换降级为扩展项——这是对 SCAN/ARC 都没显式讨论的「well-posedness」问题的显式处理。
3. **学习效率曲线**：把「few-shot」从「题目只给 5 条」改造成「扫描 k 条到多少才能泛化」的量化指标，既保留少样本精神，又避免欠定。
4. **四档基线 + 三阶段 + KSTAR 闭环**：用 `random / majority / rote / symbolic` 四档明确刻画出「记忆 vs 学习」的分水岭，并用反馈演示把 ΔR→K 变成可运行实验。
