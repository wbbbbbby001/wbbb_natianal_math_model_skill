# 阶段2：编程手 → code/ + figures/ + data/

> 目标：把建模思路变成可独立运行、可复现、可直接进论文的代码与图表。建议耗时 12-18h。

## 入口条件

- `modeling_thought.md` 已产出；
- state 中问题数 N 已确定（来自阶段0）。

## 加载

- `references/model_catalog.md`（模型/算法实现）
- `templates/coder_output.md`（代码结构模板，含英文图铁律）
- `scripts/verify_code.py`（出口门禁用）
- 光谱/周期信号类题目（薄膜干涉、频谱分析、波形反演等）另加 `references/spectral_processing_notes.md`（单位一致性/包络窗宽/FFT频率公式/三方法交叉验证/高阶效应判据）

## 任务

1. **读取** `modeling_thought.md` 与 state，确认每问的模型与算法。
2. 在 `<PROJECT_ROOT>/` 下创建 `code/`，**按问题数 N 动态生成**：

```
code/
├── data_loading.py            # 数据读取（不依赖本地绝对路径，相对路径+自动检测）
├── data_eda.py                # 数据探索分析（描述统计/分布/缺失/异常）
├── data_preprocessing.py      # 数据预处理（分级缺失填充/3σ+箱线+LOF/标准化/编码/特征工程）
├── question1_model.py … questionN_model.py   # 每问一个独立文件（N 来自 state）
├── model_validation.py        # 三大检验：误差(RMSE/MAE/MAPE/R²) + 灵敏度(±10%/±20%) + 稳健性(换算法/缩扩样本/加噪)
├── visualization.py           # 全部图表生成
├── main_solver.py             # 主入口：一键串联所有模块
└── requirements.txt           # 依赖清单
```

3. **每个 .py 文件要求**：
   - `if __name__ == '__main__':` 入口，可独立运行；
   - 相对路径/自动检测数据位置，异常捕获 + 读取失败兼容；
   - 逐行中文注释；
   - **绘图统一中文标注**（title/xlabel/ylabel/legend/text 全中文，文件头必须配置 SimHei/微软雅黑中文字体防乱码，见 `templates/coder_output.md`）；希腊/数学符号（≥、→、ν、θ、₂ 等）源码用 `\u` 转义保持 ASCII，避免附录 lstlisting 缺字；
   - **附录粘贴就绪（对齐优秀论文附录）**：每个文件头部必须有完整模块注释块——文件名、功能、对应正文第 X 节/表 X、运行环境、依赖；**按问拆分文件**（`questionN_model.py` = 一个求解环节一个文件），保证论文手能把每个文件**全文**直接贴入对应附录，无需删减。
4. **图片规范**：≥300 DPI、宽度 8-16cm、学术配色、无截图、无乱码、图内标注统一中文（配 SimHei 中文字体）。**图题规范**：论文中的图题（LaTeX \caption）用中文并放图片上方（\caption+\label 写在 \includegraphics 之前）；图内坐标/图例/标题也用中文。
5. **结果输出**：处理后数据前 10 行 + 后 5 行，保存 CSV 到 `data/`。
6. 生成 `code_and_figures.md`（文件清单/运行说明/每图说明）。
7. **回填数值**：每问关键结果（最优值、误差、检验指标）写入 state，供论文手引用。

## 出口门禁

- [ ] 运行 `python scripts/verify_code.py code/`：全部 .py **语法编译通过 + import 冒烟 + main_solver 可跑**，输出 PASS 报告
- [ ] 每张图 ≥300 DPI、中文标注（SimHei 无乱码，放大检查）
- [ ] 每问均有：结果数值 + 图表 + 检验指标，已回填 state
- [ ] 代码无硬编码赛题数据路径、可复现（随机种子固定）
- [ ] **物理单位自检**：含相位公式（如 $\varphi=4\pi n d\cos\theta\,\nu$）的代码，确认 $d$ 与 $\nu$ 单位匹配（μm vs cm⁻¹ 需换算），用合成真值验证反演误差 <1e-3
- [ ] **周期/谱类方法交叉验证**：周期估计类题目跑通 FFT + 相位 + 极值三方法，方法间极差 <2%（见 `spectral_processing_notes.md`）；包络滤波窗宽 ≥8 信号周期
- [ ] 无 high 级问题（代码不可运行/结果与建模方案矛盾）

**verdict**：任一 high → `block`；存在 mid（如个别图未达标）→ `refine`（只修该图/该文件）；全过 → `pass`（进入阶段3）。

## 产出

- `code/`（N+6 个 .py + requirements.txt）、`figures/`、`data/`
- `code_and_figures.md`
- state 更新：`results`（每问数值）、`scores.stage_2`、`current_stage=3`。
