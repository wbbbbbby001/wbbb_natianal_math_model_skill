---
name: wbbb_math_skill
description: 数学建模国赛（CUMCM）端到端协作技能。当用户点名 wbbb_math_skill、说"wbbb 建模""开始建模""国赛全流程""三角色输出"，或要求按国赛规则完成选题→建模手→编程手→论文手→终审提交全链路时使用。提供选题黄金30分钟、72小时时间轴、持久状态机、阶段门禁评分、摘要5审、格式硬检测、md/tex/pdf 三格式终稿。此技能不用于普通数据分析或非竞赛论文写作；当用户已在用 mathmodel-skill（10阶段）或 math-modeling（三角色强制协议）时不重复触发。
---

# wbbb_math_skill — 国赛数学建模全链路重型工作流

5 阶段把 72 小时国赛协作变成可恢复、可检查、可收敛的流程。用户回答关键问题，agent 维护状态与评分。每阶段有入口条件与出口门禁，未达标定向精修（迭代上限 2），跨阶段一致性由 L2 回检兜底。

**权威口径**：论文结构、格式、摘要、检验、时间规划一律以《2026 国赛三天速成国奖》宝书为准；当届官方规则（时间轴、查重、匿名、AI 披露）需现场核对官网。本 skill 不硬编码任何具体年份题目。

---

## 运行路径

- `SKILL_ROOT`：本文件所在目录（只读）。领域知识在 `references/`，输出模板在 `templates/`，工具脚本在 `scripts/`。
- `PROJECT_ROOT`：用户工作目录。所有建模产物（`modeling_thought.md`、`code/`、`figures/`、`paper/`、`state/`）只写入这里。
- 状态持久化：`<PROJECT_ROOT>/state/decision_log.json`（模板见 `templates/decision_log.json`，由 agent 读写，不让用户手编）。

---

## Quick Start（用户说"开始建模"）

1. 一句话开场（≤50 字）："启动 wbbb 国赛建模工作流，5 阶段 + 状态机，全程问答式。"
2. 用 AskUserQuestion 收集缺失的启动字段（已提供的字段不再问，合并成一轮）：
   - 竞赛（默认 cumcm 国赛；mcm/电工杯也可跑，规则口径需另核）
   - 题号与题目 PDF/文本路径（"未公布"亦可）
   - 队员数 + 分工（建模/编程/写作）
   - 截止时间（"距现在 X 小时"或具体时刻）
3. agent 自动初始化：
   - 无 `<PROJECT_ROOT>/state/decision_log.json` → 从 `templates/decision_log.json` 复制并写入竞赛字段；
   - 已存在 → 读 `current_stage` 恢复断点。
4. 进入 `references/stage_00_kickoff.md`（选题 + 时间规划），不重复问已知字段。

**已有 state 触发**（用户中途回来）：读 `state/decision_log.json` 的 `current_stage`，加载对应 `references/stage_NN_*.md`，不重复读领域参考。

---

## 5 阶段索引

| # | 阶段 | 文件 | 建议耗时 | 核心产出 | 出口门禁（verdict 依据） |
|---|------|------|---------|---------|--------------------------|
| 0 | 启动与选题 | `references/stage_00_kickoff.md` | 0.5-2h | 定题 + 题型判定 + 72h 时间规划 | 题号/题型/问题数写入 state；选题铁律满足 |
| 1 | 建模手 | `references/stage_01_modeler.md` | 6-12h | `modeling_thought.md`（全链路建模思路） | L1 评分：模型选型有理由、创新点显性、公式≥10/问、**推导完整（分布建模→闭式→解释，无"直接给公式"跳跃）**、符号统一 |
| 2 | 编程手 | `references/stage_02_coder.md` | 12-18h | `code/*.py` + `figures/*.png` + `data/*.csv` | `verify_code.py` 全脚本可运行；图内中文标注（SimHei 无乱码）≥300DPI；结果数值回填 state |
| 3 | 论文手 | `references/stage_03_writer.md` | 12-24h | `final_paper.md` + `paper/*.tex` + `paper/main.pdf` | `format_check.py` PASS；PDF 编译成功；摘要5审；**优秀论文深度结构（问题重述：背景分段展开+数据说明+逐问重述；问题分析：数据特征+逐问单独分析+重难点+选型+技术路线；每问独立成章；独立灵敏度章；模型评价分问）**；**正文深度：standard 模式正文页数>23（即≥24，目标 24-28，上限 30）且 `depth_check.py` PASS**；**附录四件套：支撑文件目录表+附录目录表+分问全量代码+运行环境说明（2026 正文≤30 页，附录不计页数）**；**Overfull=0（表格不超版心居中）+ 无AI编辑痕迹**；L2 一致性回检 |
| 4 | 终审与提交 | `references/stage_04_final.md` | 2-6h | 终稿 + 支撑材料包 + 合规清单 | 五步终审通过；匿名/查重/MD5/提前提交合规 |

**三角色交付主线**（本 skill 招牌）：阶段1 建模手 → `modeling_thought.md`；阶段2 编程手 → `code/`+`figures/`；阶段3 论文手 → `final_paper.md`+`paper/`。每个角色拿到前一个角色的完整产物，禁止跳步。

---

## 渐进式加载协议（省 token 的关键）

**只在进入阶段 N 时加载 `references/stage_NN_*.md`，切勿一次全读。**

| 触发 | 加载 |
|------|------|
| 每阶段开头 | `<PROJECT_ROOT>/state/decision_log.json`（必读） |
| 每阶段结尾 | 写回 decision_log（决策 + 评分 + 产物路径） |
| 开始建模（总览） | `references/judging_standards.md`（评审标准+潜规则） |
| 阶段0 选题 | `references/rules_2026.md`（当届规则）+ `references/time_plan_72h.md`（时间轴） |
| 阶段1 建模手 | `references/seven_steps.md` + `references/score_modules.md` + `references/innovation_paths.md` + `references/model_catalog.md` + `references/paper_depth_guide.md`（推导深度标准） + `templates/modeler_output.md`；光谱/周期信号类题目另加 `references/spectral_processing_notes.md` |
| 阶段2 编程手 | `references/model_catalog.md` + `templates/coder_output.md`；光谱/周期信号类题目另加 `references/spectral_processing_notes.md`（单位一致性/包络窗宽/三方法交叉验证） |
| 阶段3 论文手 | `references/paper_structure.md` + `references/abstract_guide.md` + `references/paper_depth_guide.md`（结构与篇幅标准） + `references/paper_depth_expansion.md`（正文深度扩充清单，防"正文太薄"） + `references/workflow_figure.md`（整体建模流程图模板，问题分析/重述必用） + `references/appendix_guide.md`（附录四件套） + `templates/writer_output.md` + `templates/abstract_checklist.md` |
| 阶段4 终审提交 | `references/format_checker.md` + `references/rules_2026.md` |
| 需要检测 | `scripts/format_check.py`（合规）、`scripts/depth_check.py`（深度）、`scripts/verify_code.py`（代码），按需运行 |

领域参考文件是**懒加载**知识库；SKILL.md 主体保持精简，不复制参考内容。

---

## 收敛准则（verdict 统一定义）

每阶段出口门禁按本定义收敛。**verdict 优先级从高到低：**

| verdict | 触发 | 行为 |
|---------|------|------|
| `block` | 存在任意 high 级问题（如结果与数据矛盾、代码不可运行、匿名泄露） | 暂停，用户介入 |
| `pass` | L1 各维度 ≥7 且无 high 级问题 | 进入下一阶段 |
| `refine` | 存在中/低问题未达 pass | 定向精修（只改问题点），`iter += 1`，上限 2 |
| `carryover` | iter 达 2 仍不通过 | 进入下一阶段，标记问题由 L2 回检兜底 |

- **L1 评分**：对当阶段维度（建模/代码/论文各有专属维度）逐项 1-10 打分，分数与判定写入 decision_log。
- **L2 跨阶段回检**：阶段3/4 末尾对照 decision_log 检查模型名称、结果数值、创新点全文一致；发现冲突 → 定向回滚到冲突阶段精修，不重做整段。

---

## 运行模式（按剩余时间自动推荐）

| 剩余时间 | 模式 | 说明 |
|----------|------|------|
| >48h | standard | 完整 5 阶段，L1 门禁全开 |
| 12-48h | standard + fast | 阶段1-2 正常，阶段3 只保核心章节，门禁简化 |
| <12h | fast | 直进阶段3 核心写作 + 阶段4 终审，跳阶段0-2 建模细节，沿用现有 state |

用户可用指令手动切换；切换记录写入 state 的 `events`。

---

## 用户指令快捷

- "开始建模" / "选题" → 阶段0 启动
- "建模手输出" / "进入阶段1" → 执行阶段1
- "代码手输出" / "进入阶段2" → 执行阶段2
- "论文手输出" / "进入阶段3" → 执行阶段3
- "摘要5审" → 单独跑 `templates/abstract_checklist.md` 的 5 审
- "格式检测" → 跑 `scripts/format_check.py` + 报告
- "正文深度检测" / "深度检测" → 跑 `scripts/depth_check.py final_paper.md paper/main.tex paper/main.pdf`（正文页数 + 深度要素）
- "代码检测" / "验证代码" → 跑 `scripts/verify_code.py`
- "终审" / "提交检查" / "进入阶段4" → 五步终审 + 合规清单
- "看进度" → 输出 decision_log 摘要（当前阶段 + 各阶段评分）
- "回退到阶段N" → 读 decision_log，回退 current_stage 并清理 ≥N 节点
- "全量输出" → 阶段0→4 完整执行
- "编译PDF" → 仅编译 LaTeX 生成 PDF

---

## 输出文件总览（完整执行后）

```
<PROJECT_ROOT>/
├── modeling_thought.md          # 阶段1：建模手全链路思路
├── code_and_figures.md          # 阶段2：代码与图像说明文档
├── final_paper.md               # 阶段3：Markdown 论文
├── format_check_report.md       # 阶段4：格式检测报告
├── state/decision_log.json      # 状态机（运行态，自动维护）
├── code/                        # 阶段2：按问题数动态生成
│   ├── data_loading.py / data_eda.py / data_preprocessing.py
│   ├── question1_model.py … questionN_model.py   # N = 题面实际子问题数
│   ├── model_validation.py / visualization.py / main_solver.py
│   └── requirements.txt
├── figures/                     # 阶段2：中文标注（SimHei 无乱码），≥300DPI
├── data/                        # 阶段2：处理后 CSV
└── paper/                       # 阶段3：md+tex+pdf 三格式
    ├── main.tex + sections/*.tex + compile.bat + main.pdf
    # 论文呈现对齐优秀论文深度（见 references/paper_depth_guide.md + paper_depth_expansion.md + appendix_guide.md）：
    #   问题重述配原创流程图；每问独立成章（问题一模型建立及求解…）；决策类给全量方案表；
    #   算法伪代码 + 全量结果表 + 过程图（每问≥2 张）+ 灵敏度理论-数值交叉验证 + 物理合理性讨论；
    #   灵敏度分析独立成节；模型评价分问写；
    #   附录四件套：支撑文件目录表 + 附录目录表 + 分问全量代码（全部 code/*.py 完整贴入） + 运行环境说明
    #   正文（题目→摘要→…→参考文献）standard 模式>23 页（即≥24，目标 24-28，上限 30）；附录不计页数
```
