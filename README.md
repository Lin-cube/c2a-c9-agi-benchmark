# WangChunYan — C2A / C9 完整提交包

> **挑战：** C2A / C9 — 衡量 AGI 的认知能力（DeepMind × Kaggle）
> **赛道：** Track 1 — Learning（学习）
> **方案名：** SynthLearn（程序化新颖规则学习基准）
> **截止：** 2026-12-31 23:59（北京时间）

---

## 一句话说明

> 这是我的 C2A 提案，选择了 Track 1（学习能力）。SynthLearn 用随机 Cayley 表构造「可证不存在于训练数据中」的新颖代数，通过「零知识基线 → 示例学习 → 反馈学习」三阶段协议，量化模型到底是「学会了新规则」还是「背下了表面模式」。欢迎反馈！

---

## 交付物清单 / Deliverables

### 阶段一：C2A 提案

| 文件 | 说明 |
|------|------|
| `WangChunYan_C2A_proposal.md` | 提案正文（四段式，含具体示例 + KSTAR 连接） |
| `WangChunYan_C2A_AI日志.md` | 论文精读/调研/写作的 AI 使用记录 |
| `WangChunYan_C2A_拿来说明.md` | 借鉴来源 + 拿去改分析 |

### 阶段二：C9 正式实现

| 文件 | 说明 |
|------|------|
| `WangChunYan_C9_benchmark/` | 完整可运行代码（含 README，仅标准库，无第三方依赖） |
| `WangChunYan_C9_task说明.md` | 任务描述 + 评分标准 + 效度论证 |
| `WangChunYan_C9_测试结果.md` | 四档基线的真实测试数据（可复现） |
| `WangChunYan_C9_反思报告.md` | 500–800 字反思（含失败经验 + 改进方案） |
| `WangChunYan_C9_AI日志.md` | 开发全过程 AI 使用记录 |
| `WangChunYan_C9_拿来说明.md` | 参考的 benchmark/论文 + 取舍分析 |

---

## 快速复现

```bash
cd WangChunYan_C9_benchmark
python run.py                    # 产出 results/results.json + results/results.md
python run.py --universes 20 --symbols 5
```

运行环境：Python 3.10+（仅标准库）。

## 核心结论（一句话）

四档基线在组合泛化测试上呈现**清晰三分离**：规则归纳学习者 100%、死记硬背者 37.8%（纯众数偏置）、随机者 25%——SynthLearn 有效切开了「学习」与「记忆」的分水岭。
