# 论文手输出模板

> 此模板定义 `final_paper.md` + `paper/*.tex` + `paper/main.pdf` 的完整输出结构。
> **核心原则**：
> 1. 严格按国赛 12 模块标准结构（顺序不可调换、模块不可缺失，结构分占 20%）；
> 2. 三格式输出：.md（预览）+ .tex（源文件）+ .pdf（终稿）；
> 3. xelatex 编译生成 PDF，编译失败给修复指引；
> 4. 所有图表引用 `figures/` 下的中文标注图片（SimHei 无乱码）。

---

# 论文手交付文件

**题号**：{题号} **日期**：{YYYY-MM-DD}

---

## 一、12 模块结构（书 §7.1）

| 序号 | 模块 | 建议页数 |
|------|------|---------|
| 1 | 论文题目 | 1-2 行 |
| 2 | 摘要 | 不超过 1 页 |
| 3 | 关键词 | 4-6 个 |
| 4 | 问题重述 | 0.5 页 |
| 5 | 问题分析 | 0.5-1 页 |
| 6 | 模型假设 | 0.5 页 |
| 7 | 符号说明 | 0.5-1 页 |
| 8 | 模型建立与求解 | 8-12 页 |
| 9 | 模型检验 | 1-2 页 |
| 10 | 模型改进与推广 | 0.5-1 页 |
| 11 | 模型优缺点 | 0.5-1 页 |
| 12 | 参考文献 + 附录 | 0.5 页 + 不计页附录 |

**硬性要求（2026 口径）**：正文 = 题目→摘要→…→参考文献，**≤30 页**，不要目录；附录**不计页数**，可到几十页。
**深度提示**：参考模板 = 2024B 官方优秀论文 **23 页正文 + 14 页附录**。正文做足推导过程、全量结果表、方案编号表、每问独立成章、独立灵敏度章、分问模型评价；**所有代码细节全部下沉附录（分问全量贴入）**。详见 `references/paper_depth_guide.md` + `references/appendix_guide.md`。

## 二、全局格式（书 §7.2，单倍行距）

- A4；上下 2.5cm、左右 2.5cm；单倍行距；正文首行缩进 2 字符；
- 中文宋体，英文/数字/公式 Times New Roman；
- 题目 16 号加粗居中；一级 14 号加粗居中；二三级 12 号加粗左对齐；正文 12 号；
- 表格一律三线表（无竖线/无彩色填充）；**表题在上、图题在上**（图序号+图名在图片上方、中文图题；图内标注也用中文，配 SimHei 字体防乱码）；图表编号连续；
- 公式独占一行居中、编号右对齐；禁止大段空白行。

## 三、输出文件结构

```
<PROJECT_ROOT>/
├── final_paper.md                   # Markdown 论文（预览）
├── format_check_report.md           # 格式检测报告
└── paper/
    ├── main.tex                     # LaTeX 主文件
    ├── sections/                    # 分章节
    │   ├── 0_title.tex
    │   ├── 1_abstract.tex           # 摘要+关键词（1 页内）
    │   ├── 2_problem_restatement.tex
    │   ├── 3_problem_analysis.tex
    │   ├── 4_assumptions.tex
    │   ├── 5_symbols.tex            # 符号说明（三线表）
    │   ├── 6_model_solution.tex     # 模型建立与求解：每问独立成章（问题一/二/…/N 模型建立及求解，核心 8-12 页）
    │   ├── 7_model_validation.tex   # 模型检验（灵敏度独立成节）
    │   ├── 8_improvement.tex        # 改进+推广+优缺点（分问）
    │   ├── 9_references.tex         # 参考文献
    │   └── 10_appendix.tex          # 附录四件套：表1支撑文件目录+表2附录目录+分问全量代码+运行环境说明（+数据/AI说明）
    ├── main.pdf                     # 编译终稿
    └── compile.bat                  # 编译脚本
```

## 四、LaTeX 主文件模板（main.tex）

```latex
% !TEX program = xelatex
\documentclass[UTF8,12pt,a4paper]{ctexart}

% ===== 页眉页脚：页眉留空；页码阿拉伯数字居中于页脚（强制）=====
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% ===== 一级标题中文数字（强制）：一、问题重述 / 五、问题一模型建立及求解；二级保留 1.1 =====
\ctexset{
  section = {
    name = {,、},
    number = \chinese{section},
    aftername = {},
  },
}
\renewcommand{\thesection}{\chinese{section}}          % 交叉引用显示"第五节"等中文
\renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}}  % 二级保留 1.1

% ===== 页面布局：A4，四边距 2.5cm =====
\usepackage[margin=2.5cm]{geometry}

% ===== 数学与公式 =====
\usepackage{amsmath,amssymb,amsthm,bm}

% ===== 图表（booktabs 三线表）=====
\usepackage{graphicx,float,subcaption}
\usepackage{booktabs,longtable,multirow,array}
\usepackage{caption}

% ===== 代码列表 =====
\usepackage{listings,xcolor}

% ===== 其他 =====
\usepackage{hyperref,cite,enumitem,siunitx}
\usepackage{algorithm,algpseudocode}

% ===== 配置：单倍行距、首行缩进 2 字符 =====
\hypersetup{unicode=true,hidelinks}
\setlength{\parindent}{2em}
\linespread{1.0}                 % 单倍行距（书 §7.2）
\emergencystretch=1.5em          % 允许轻微拉伸断行，避免长公式段落右边界溢出
% ⚠️ 公式字号统一：禁止 \resizebox/\scalebox 套公式（会改字号）；超宽公式用 \tfrac 或 aligned 拆行
\captionsetup{font=small,labelfont=bf}

% 图形路径（指向 figures 目录）
\graphicspath{{../figures/}}

% ===== 表格统一 small + 仅超宽才缩放（防窄表被 resizebox 放大）=====
\AtBeginEnvironment{tabular}{\small}
\newbox\tabbox
\newcommand{\fittab}[1]{%
  \setbox\tabbox=\hbox{#1}%
  \ifdim\wd\tabbox>\textwidth
    \resizebox{\textwidth}{!}{#1}%
  \else
    #1%
  \fi}

\lstset{
  basicstyle=\small\ttfamily, breaklines=true, frame=single,
  numbers=left, numberstyle=\tiny, showstringspaces=false,
  columns=fullflexible, keepspaces=true
}

\begin{document}

% ===== 题目与摘要 =====
\input{sections/0_title}
\input{sections/1_abstract}

% ===== 正文 12 模块 =====
\input{sections/2_problem_restatement}
\input{sections/3_problem_analysis}
\input{sections/4_assumptions}
\input{sections/5_symbols}
\input{sections/6_model_solution}   % 内含多个 \section：问题一模型建立及求解 / 问题二… / …
\input{sections/7_model_validation}
\input{sections/8_improvement}

% ===== 参考文献 =====
\input{sections/9_references}

% ===== 附录 =====
\appendix
\input{sections/10_appendix}

\end{document}
```

## 五、章节模板要点

> **排版纪律（写每一节都遵守）**：
> - **宽表**：列数多或含长文本的表格，必须 `\small`/`\footnotesize` + `p{宽度}` 列（长文本列内换行）或 `\resizebox{\textwidth}{!}{...}`；`\centering` 对超版心表格无效会向右溢出；编译后核对日志 Overfull \hbox 为 0。
> - **图表编号**：图表加 `\label{tab:..}`/`\label{fig:..}`，正文一律用 `\ref` 引用；新增/删除图表后不再逐条改数字。
> - **表注**：补充说明用"注：…"，禁止"本列用于…/读者可…"设计辩护语气。
> - **禁 AI 痕迹**：论文内严禁"（单独成页）""（占位）""待插入""同上结构""用于直接展示…"等编辑说明式文字（见 `references/paper_structure.md` §五）。

### 0_title.tex
```latex
\begin{center}
  {\zihao{3}\bfseries {核心改进/基础模型+研究算法+研究对象+核心问题/应用场景}}
\end{center}
```

### 1_abstract.tex（摘要，最后写，≥5 遍修改）
```latex
\begin{center}{\zihao{4}\bfseries 摘要}\end{center}
{三段式：虎头 150-200 字(背景+问题) → 猪肚 450-550 字(方法+创新+每问模型算法量化结果) → 豹尾 200-250 字(创新+检验+价值)}
\par\noindent\textbf{关键词：}关键词1 关键词2 关键词3 关键词4 关键词5 关键词6
\clearpage
```

### 2_problem_restatement.tex（自主改写，不抄原题，≤300 字，**必配原创流程图**）
```latex
\section{问题重述}
\subsection{问题背景}{用自己的话重写，含行业应用+痛点+研究意义}
\subsection{已知条件与核心问题}
\begin{enumerate}[nosep]
  \item \textbf{问题一：}{概述}
  \item \textbf{问题二：}{概述}
  \item \textbf{问题N：}{概述}
\end{enumerate}
% 原创生产/流程示意图（对齐 2024B 优秀论文图1；不得截图原题图）
\subsection{生产流程示意图}
% ⚠️ 图题规范（强制）：图序号+图名放图片上方，即 \caption+\label 写在 \includegraphics 之前；图题用中文，图内标注也用中文（配 SimHei 字体，编程手生成图时配置）
\begin{figure}[H]\centering
  \caption{生产系统流程示意}
  \label{fig:process}
  \includegraphics[width=0.8\textwidth]{fig_process.png}
\end{figure}
```

### 3_problem_analysis.tex（四要素 + 流程图）
```latex
\section{问题分析}
\subsection{数据特征分析}{描述统计特征、分布、异常}
\subsection{解题重难点}{\textbf{重点}：...；\textbf{难点}：...}
\subsection{模型选型依据与创新切入点}{为什么选这些模型、创新点在哪}
\subsection{整体建模流程}
\begin{figure}[H]\centering
  \includegraphics[width=0.85\textwidth]{fig_workflow.png}
  \caption{整体建模流程（数据预处理$\to$四问建模求解$\to$模型检验）}
  \label{fig:workflow}
\end{figure}
% ⚠️ 整体建模流程图必须覆盖全部子问题（每问一个阶段框），不得只画某一问的流程；分问流程子图另画
```

### 4_assumptions.tex（3-5 条）
```latex
\section{模型假设}
\begin{enumerate}[nosep,label=A\arabic*:]
  \item \textbf{{假设名称}}：{内容}。依据：{设立依据}。此假设{对模型的影响}。
\end{enumerate}
```

### 5_symbols.tex（三线表，表题在上）
```latex
\section{符号说明}
\begin{table}[H]\centering
\caption{Main symbols and definitions}
\label{tab:symbols}
\begin{tabular}{cllc}
\toprule Symbol & Definition & Unit & Type \\
\midrule
{sym1} & {def1} & {unit1} & Decision variable \\
\bottomrule
\end{tabular}
\end{table}
```

### 6_model_solution.tex（核心 8-12 页，**每问独立成章**，对齐优秀论文五/六/七/八）
> 每问一个 `\section`（可配中文序号"问题一模型建立及求解"…），每问五步写作框架；决策/枚举/统计类必配「方案编号表 + 全量表达式表 + 全量结果矩阵 + 最优决策表 / 两情形对照总结表」。
```latex
\section{问题一模型建立及求解}
\subsection{模型适配分析}{选型理由+对比优势}
\subsection{公式推导}
\begin{align}
  {关键公式} \label{eq:1} \\
  {关键公式} \label{eq:2}
\end{align}
\subsection{变量与约束定义}{决策变量/目标函数/边界约束}
\subsection{算法求解设计}{求解软件、算法参数、迭代规则（复杂算法配伪代码；算法 \caption 标题与 \State 正文用中文，\Require/\Ensure/\If/\Else 等关键字保持英文标准伪代码，勿 \algrenewcommand 重定义）}
\subsection{结果输出解读}{三线表+高清图表+量化数据；决策类给全量方案表，统计类给两情形对照总结表}

\section{问题二模型建立及求解}{同上五步结构；先给方案编号表，再给全量表达式表}
\section{问题N模型建立及求解}{同上五步结构}
```

### 7_model_validation.tex（三大检验单独成节，**灵敏度分析独立成节**）
```latex
\section{模型检验}
\subsection{误差分析}{RMSE/MAE/MAPE/R² 表格+结论}
\subsection{灵敏度分析}{独立成节：核心参数±10%/±20%扰动 + 关键参数专项扰动(如贝叶斯先验超参数 α,β)，配扰动影响图，篇幅≥检验的1/3}
\subsection{稳健性检验}{(1)算法替换 (2)样本缩扩 (3)噪声注入}
\subsection{模型对比验证}{基准模型 vs 本文模型，量化对比}
```

### 8_improvement.tex（改进+推广+**分问评价**）
```latex
\section{模型评价与推广}
\subsection{分问题模型评价}{对齐优秀论文：逐问写优点+缺点
  (问题一) 优点：{量化写实}；缺点：{客观温和，如样本量受决策函数权重影响}
  (问题二) 优点：{精准闭式、无估计误差}；缺点：{迁移到复杂流程推导难度大}
  (问题三) 优点：{状态-决策结构清晰/DP高效}；缺点：{状态空间随规模指数增长}}
\subsection{改进方向}{短期+长期}
\subsection{跨场景推广}{可迁移至哪些同类场景}
```

### 9_references.tex（5-10 条，中外文结合，国标）
```latex
\begin{thebibliography}{99}
\bibitem{1} Author A. Paper Title[J]. Journal, Year, Vol(Issue): Pages.
\bibitem{2} Author B. Book Title[M]. Publisher, Year.
\end{thebibliography}
```

### 10_appendix.tex（**附录四件套**，对齐优秀论文 P24-37，详见 `references/appendix_guide.md`）
> **附录编号用阿拉伯数字（附录1、附录2、…），禁止字母（附录A/B/C）**；用 `\section*{附录N …}`（无编号）精确显示"附录1/附录2/…"，对齐优秀论文命名；正文用 `\ref{...}`/文字"见附录 X"引用，表1/表2 中"对应附录"列必须与附录实际编号一致。
```latex
\clearpage
\section*{附录：代码与数据说明}   % ⚠️ 参考文献后必须有"附录"大标题，再进运行环境说明
% ===== 运行环境说明（四件套之4）=====
\textbf{运行环境}：Python 3.12，numpy/scipy/pandas/matplotlib/sklearn。
依赖清单见支撑材料 code/requirements.txt。一键复现：\texttt{python main\_solver.py}。

% ===== 四件套之1：支撑文件目录表（对齐优秀论文表1）=====
\begin{table}[H]\centering
\caption{支撑文件目录}
\begin{tabular}{lll}
\toprule
支撑文件名称 & 文件内容 & 对应附录 \\
\midrule
data_loading.py        & 数据读取与预处理 & 附录1 \\
question1\_model.py    & 问题一抽样检验模型求解 & 附录2 \\
question2\_model.py    & 问题二方案决策求解 & 附录3 \\
question3\_model.py    & 问题三状态-决策DP求解 & 附录4 \\
question4\_model.py    & 问题四贝叶斯/蒙特卡洛 & 附录5 \\
model\_validation.py   & 灵敏度/稳健性/对比检验 & 附录6 \\
visualization.py       & 全部图表生成 & 附录6 \\
\bottomrule
\end{tabular}
\end{table}

% ===== 四件套之2：附录目录表（对齐优秀论文表2）=====
\begin{table}[H]\centering
\caption{附录目录}
\begin{tabular}{ll}
\toprule
附录 & 名称 \\
\midrule
附录1 & 数据读取与预处理代码 \\
附录2 & 问题一求解代码 \\
附录3 & 问题二求解代码 \\
附录4 & 问题三求解代码 \\
附录5 & 问题四求解代码 \\
附录6 & 模型检验与可视化代码 \\
\bottomrule
\end{tabular}
\end{table}

% ===== 四件套之3：分问全量代码（每问一个附录，完整 lstlisting，非片段）=====
\section*{附录1 数据读取与预处理代码}
% 本代码对应正文第 X 节（数据预处理），输出 data/processed_*.csv。
\begin{lstlisting}[language=Python]
{code/data_loading.py 全文}
\end{lstlisting}

\section*{附录2 问题一求解代码}
% 本代码对应正文"问题一模型建立及求解"，结果见表 X。
\begin{lstlisting}[language=Python]
{code/question1_model.py 全文}
\end{lstlisting}

\section*{附录3 问题二求解代码}  % 完整粘贴 code/question2_model.py 全文
\section*{附录4 问题三求解代码}  % 完整粘贴 code/question3_model.py 全文
\section*{附录5 问题四求解代码}  % 完整粘贴 code/question4_model.py 全文
\section*{附录6 模型检验与可视化代码}  % 完整粘贴 code/model_validation.py + visualization.py 全文

% ===== 附加：AI 使用说明（2026 强制）=====
\section*{AI使用说明}
本论文在以下环节使用AI辅助工具（严格按2026国赛要求）：
\begin{enumerate}[nosep]
  \item {环节与用途}
  \item ...
\end{enumerate}
工具名称：{AI工具名} 版本：{版本} 开发方：{开发方} 使用日期：{YYYY年MM月DD日-MM月DD日}
核心建模与推导由队伍完成，AI生成内容经人工审核验证。

% ===== 附加：处理数据说明 =====
\section*{处理数据说明}
```

## 六、编译脚本（compile.bat）

```batch
@echo off
cd /d "%~dp0"
echo [1/2] First pass (xelatex)...
xelatex -interaction=nonstopmode main.tex
if %errorlevel% neq 0 ( echo ERROR: first pass failed; pause; exit /b 1 )
echo [2/2] Second pass (xelatex)...
xelatex -interaction=nonstopmode main.tex
if %errorlevel% neq 0 ( echo ERROR: second pass failed; pause; exit /b 1 )
echo Compilation SUCCESS! Output: main.pdf
del /q main.aux main.out main.log main.toc 2>nul
pause
```

## 七、与编程手衔接检查（输出前必须确认）

- [ ] `code/` 中所有 .py 已由编程手生成且可运行
- [ ] `figures/` 中所有图片已生成（中文标注、SimHei 无乱码、≥300DPI）
- [ ] `data/` 中处理后数据已生成
- [ ] 论文引用的图表编号与编程手输出一致
- [ ] 论文引用的数值与 `state/decision_log.json` 中编程手回填的结果一致

> **论文手交付清单**：
> - [ ] `final_paper.md`（12 模块完整）
> - [ ] `paper/main.tex` + `paper/sections/*.tex`（11 个章节文件）
> - [ ] `paper/main.pdf`（xelatex 编译成功）⚠️ 最关键产出
> - [ ] `paper/compile.bat`
> - [ ] `format_check_report.md`（`scripts/format_check.py` 检测 PASS）
> - [ ] 摘要5审通过；匿名检查 0 结果；单倍行距；正文（题目→参考文献）≤30 页无目录
> - [ ] **附录四件套完成**：表1 支撑文件目录 + 表2 附录目录 + 分问全量代码（code/ 每问脚本完整贴入）+ 运行环境说明
