# 阶段3：论文手 → final_paper.md + paper/*.tex + paper/main.pdf

> 目标：12 模块论文三格式输出（md 预览 + tex 源文件 + pdf 终稿），通过格式硬检测与摘要5审。建议耗时 12-24h。

## 入口条件

- `code/` + `figures/` + `data/` 已产出，state 含每问结果数值。

## 加载

- `references/paper_structure.md`（12 模块结构 + 全局格式）
- `references/paper_depth_expansion.md`（**正文深度扩充清单**，防"正文太薄"）
- `references/abstract_guide.md`（摘要规范）
- `templates/writer_output.md`（LaTeX 模板）
- `templates/abstract_checklist.md`（摘要5审）
- `references/format_checker.md`（出口门禁用）

## 任务

1. **12 模块顺序写作**（结构分占 20%，模块不可缺失）：
   题目 → 摘要 → 关键词 → 问题重述（自主改写不抄题）→ 问题分析（四要素+流程图）→ 模型假设（3-5条）→ 符号说明（三线表）→ **每问独立成章**"问题一模型建立及求解"…（核心 8-12 页，可中文序号）→ 模型检验（误差+灵敏度+稳健性）→ 模型改进与推广 → 模型优缺点（分问）→ 参考文献（5-10 条）+附录（**四件套**，见下）。
2. **附录四件套**（对齐 2024B 优秀论文，详见 `references/appendix_guide.md`）：
   - 表1「支撑文件目录」+ 表2「附录目录」；
   - **分问全量代码**：把 `code/` 每个求解脚本完整贴入对应附录（`lstlisting` 全文 + 逐行中文注释 + 运行环境 + "对应正文第 X 节/表 X"说明），**禁止只贴关键片段**；
   - 运行环境 + 一键复现说明；AI 使用说明（2026 强制）。
3. **三格式输出**：
   - `final_paper.md`（预览/协作）
   - `paper/main.tex` + `paper/sections/*.tex`（分章节）+ `compile.bat`
   - `paper/main.pdf`（xelatex 编译终稿）
4. **摘要**：最后写，800-1000 字三段式，**修改 ≥5 遍**，跑 5 审（`templates/abstract_checklist.md`）。
5. **全局格式**（`references/paper_structure.md`）：单倍行距、首行缩进 2 字符、A4 上下/左右 2.5cm、中文宋体 + 英文 Times New Roman、三线表、表上图下、公式居中编号右对齐、**正文（题目→参考文献）≤30 页无目录**；**页眉留空、页码阿拉伯数字居中于页脚；一级标题用中文数字（一、二、三…）；附录用数字编号（附录1、附录2…，禁止字母）**。
6. **正文深度**（`references/paper_depth_expansion.md`）：standard 模式正文 **必须 >23 页（即 ≥24，目标 24-28）**；按深度要素清单补齐——问题重述"背景分段展开+数据说明+逐问重述"、问题分析"数据特征+**逐问单独分析**+重难点+选型+技术路线"、推导逐步展开（≥6 步/问）、算法伪代码（\caption 标题与 \State 正文中文、\Require/\If/\Else 关键字保持英文标准伪代码）、每问 ≥2 张过程图、全量结果表、灵敏度理论-数值交叉验证、物理合理性讨论、全量结果汇总表。**12 模块齐全只是"合规"，页数与深度要素齐备才是"达标"**。

## 出口门禁

- [ ] `python scripts/format_check.py final_paper.md` 返回 **PASS**（或仅 low 级问题修正后 PASS）
- [ ] **正文深度**：`python scripts/depth_check.py final_paper.md paper/main.tex paper/main.pdf` 返回 **PASS**（正文页数 >23 即 ≥24 + 深度要素齐全）；低于下限 → refine 按扩充清单补齐。**注意 depth_check 靠附录"运行环境说明"字样定位附录起点，附录标题必须写成"运行环境说明"（而非"运行环境"），否则附录起点被误判到后半部、正文页数虚高，需人工逐页核对**
- [ ] `paper/main.pdf` 编译成功（xelatex 无 Error），文件 >50KB，页面正常
- [ ] **xelatex 日志 Overfull \hbox = 0**：宽表已用 `\small`+`p{}` 换行/`\resizebox`，表格居中不超右边界
- [ ] **图表编号引用一致**：正文"表X/图X"引用与实际编号对位（优先 `\label`/`\ref`）；每问独立成章时公式标签已同步重编号
- [ ] **页眉页脚与编号**：页眉留空（PDF 页边距内无任何文字/横线）；页码阿拉伯数字居中于页脚（正文与附录全部页面）；一级标题中文数字（一、二、三…）；附录为数字编号（附录1、附录2…，无字母）
- [ ] 摘要5审全过（字数/三段式/每问模型+算法+结果/创新+双检验/数据一致）
- [ ] **附录四件套完成**：表1 支撑文件目录 + 表2 附录目录 + 分问全量代码（code/ 每问脚本完整贴入，非片段）+ 运行环境说明；附录代码与 `code/` 实际文件一致
- [ ] **L2 跨阶段回检**：正文模型名称、结果数值、创新点与 `state/decision_log.json`（建模手/编程手阶段记录）一致；不一致 → 定向回滚到冲突阶段精修
- [ ] 匿名：全文无姓名/学校/学号/Logo（含页眉页脚、文件名）
- [ ] **无 AI 编辑痕迹**：全文无"单独成页/占位/待插入/同上结构/用于直接展示"等词；表注用标准"注："

**verdict**：匿名泄露/数据矛盾/PDF 编译失败 → `block`；格式项未达标 → `refine`（只改该处，iter≤2）；全过 → `pass`。

## 产出

- `final_paper.md`、`paper/`（main.tex + sections/*.tex + compile.bat + main.pdf）
- `format_check_report.md`
- state 更新：`scores.stage_3`、`current_stage=4`。
