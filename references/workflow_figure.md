# 整体建模流程图（整体流程 / 技术路线）制作规范与模板

> 依据：2025 C 题（NIPT）实战复盘。问题分析/问题重述中的"整体建模流程"图历经 4 版迭代，最终确定为 v4 方案。**核心教训**：
> ① 整体流程图必须覆盖全部子问题（每问一个阶段框），不得只画某一问的流程冒充（被判"不完整"）；
> ② 所有文字标签必须加白色描边背景（`bbox`），否则文字压箭线/压背景形成"文字遮挡"；
> ③ 框内分项与产出标注之间必须留足间距，白底产出框若覆盖分项文字即为遮挡；
> ④ 窄表/标题文字字号过大、过密均会被判定不美观。

---

## 一、v4 设计规范（本 skill 的标准）

| 设计元素 | 规范 |
|---------|------|
| 面板容器 | 整图套浅灰圆角面板（`FancyBboxPatch`），专业排版、内容归拢 |
| 标题层级 | 大标题 17pt 加粗 + 副标题 11pt（副标题加白底），间距≥0.013 |
| 数据层 | 浅蓝带条（`#DEEBF7` 底 + `#6BAED6` 边），两行：主行（处理流程）+ 次行（数据来源/行数列数） |
| 各问题框 | 每问一个独立色框（蓝/绿/紫/橙 依次），**编号并入标题前缀**（`① 问题一 · 相关性+回归`），避免角标与标题重叠 |
| 框内结构 | 标题 → 3 个模型分项（间距≥0.05）→ **白底虚线产出框**（`产出：关系模型+显著性`），分项下沿与产出框上沿间距≥0.01 |
| 数据流标签 | 数据层→各问箭头带标签（Y浓度/达标时间/多因素/特征标签）；问间横向箭头带链接标签（达标时间/多因素扩展/…） |
| **防遮挡铁律** | **所有文字标签统一 `bbox=dict(facecolor='white', edgecolor='none', alpha=0.9, pad=0.25)`**——标签压箭线、压背景均不遮挡 |
| 检验层 | 浅珊瑚带条（`#FDEEEC` 底 + `#E3A29B` 边）+ 深灰结论框（`#4A4A4A`），右向箭头衔接 |
| 图例 | 底部：`■数据层 ■各问题建模 ■检验与结论 ──→流向 虚线框=产出物` |
| 输出规格 | `figsize=(12.5, 7.3)`，300 DPI，中文 SimHei 无乱码，`bbox_inches='tight'` |

---

## 二、可复用模板函数（复制进 code/visualization.py 直接可用）

```python
# ---------- 整体建模流程（技术路线）图：v4 标准模板 ----------
def draw_pipeline_flowchart(
        title='整体建模流程', subtitle='数据预处理 → 建模求解 → 模型检验',
        data_layer='数据层：数据读取与清洗  ｜  数据解析/缺失处理  ｜  特征构造',
        data_source='输入：附件.xlsx  ｜  样本量 × 特征数',
        questions=None,        # list[(编号, 问题名, 子题名)]，如 [('①','问题一','相关性+回归'),...]
        items=None,            # list[list[str]]，每问的模型/方法分项
        outputs=None,          # list[str]，每问的产出物标注
        data_arrow_labels=None,   # list[str]，数据层→各问箭头标签
        link_labels=None,      # list[str]，问间链接标签（长度=问数-1）
        validation='模型检验：误差分析  ｜  灵敏度分析  ｜  稳健性检验',
        conclusion='结论输出', save='fig16_整体建模流程.png'):
    """整体建模流程图 v4：面板容器 + 编号前缀 + 每问产出标注 + 白底标签防遮挡 + 图例"""
    from matplotlib.patches import FancyBboxPatch
    BBOX = dict(facecolor='white', edgecolor='none', alpha=0.9, pad=0.25)
    C_PANEL_F, C_PANEL_E = '#F7F8FA', '#C9D2DD'
    C_DATA, C_DATA_E, C_DATA_T = '#DEEBF7', '#6BAED6', '#1F4E79'
    C_Q = ['#2166AC', '#2E8B57', '#984EA3', '#E07B00']
    C_VALID, C_VALID_E, C_VALID_T = '#FDEEEC', '#E3A29B', '#8C4A44'
    C_CONC, C_GRAY = '#4A4A4A', '#8A8F98'
    N = len(questions)
    fig, ax = plt.subplots(figsize=(12.5, 7.3))
    ax.axis('off'); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(FancyBboxPatch((0.015, 0.015), 0.97, 0.97, boxstyle="round,pad=0.01",
                                facecolor=C_PANEL_F, edgecolor=C_PANEL_E, linewidth=1.2))
    ax.text(0.5, 0.965, title, ha='center', va='center', fontsize=17, fontweight='bold')
    ax.text(0.5, 0.925, subtitle, ha='center', va='center', fontsize=11, color=C_GRAY, bbox=BBOX)
    # 数据层带条
    ax.add_patch(FancyBboxPatch((0.05, 0.78), 0.90, 0.115, boxstyle="round,pad=0.008",
                                facecolor=C_DATA, edgecolor=C_DATA_E, linewidth=1.5))
    ax.text(0.5, 0.86, data_layer, ha='center', va='center', fontsize=11.5,
            color=C_DATA_T, fontweight='bold')
    ax.text(0.5, 0.815, data_source, ha='center', va='center', fontsize=8.5, color='#5B7FA6')
    # 各问题框：宽度随 N 自适应
    gap = 0.035
    box_w = (0.875 - (N - 1) * gap) / N
    box_h, box_y = 0.34, 0.36
    x0 = 0.045
    for i in range(N):
        x = x0 + i * (box_w + gap)
        col = C_Q[i % len(C_Q)]
        ax.add_patch(FancyBboxPatch((x, box_y), box_w, box_h, boxstyle="round,pad=0.01",
                                    facecolor=col, edgecolor='none', alpha=0.93))
        ax.text(x + box_w / 2, box_y + box_h - 0.05, f'{questions[i][0]} {questions[i][1]} · {questions[i][2]}',
                ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        for si, it in enumerate(items[i]):
            ax.text(x + box_w / 2, box_y + box_h - 0.115 - si * 0.056, it,
                    ha='center', va='center', fontsize=8.6, color='white')
        ax.add_patch(FancyBboxPatch((x + 0.02, box_y + 0.045), box_w - 0.04, 0.048,
                                    boxstyle="round,pad=0.006", facecolor='white', alpha=0.97,
                                    edgecolor=col, linestyle='--', linewidth=1.1))
        ax.text(x + box_w / 2, box_y + 0.069, f'产出：{outputs[i]}', ha='center', va='center',
                fontsize=7.8, color=col, fontweight='bold')
        # 数据层→本框箭头 + 白底标签
        ax.annotate('', xy=(x + box_w / 2, box_y + box_h + 0.012),
                    xytext=(x + box_w / 2, 0.775),
                    arrowprops=dict(arrowstyle='->', color=C_DATA_E, lw=1.6))
        ax.text(x + box_w / 2, 0.728, data_arrow_labels[i], ha='center', va='center',
                fontsize=7.2, color='#6B7280', bbox=BBOX)
        # 问间链接箭头 + 白底标签
        if i < N - 1:
            ax.annotate('', xy=(x + box_w + 0.026, box_y + box_h / 2),
                        xytext=(x + box_w + 0.004, box_y + box_h / 2),
                        arrowprops=dict(arrowstyle='->', color='#9CA3AF', lw=1.7))
            ax.text(x + box_w + 0.015, box_y + box_h / 2 + 0.05, link_labels[i],
                    ha='center', va='center', fontsize=7.2, color='#6B7280', bbox=BBOX)
    # 检验带条 + 结论
    ax.add_patch(FancyBboxPatch((0.05, 0.12), 0.58, 0.105, boxstyle="round,pad=0.008",
                                facecolor=C_VALID, edgecolor=C_VALID_E, linewidth=1.5))
    ax.text(0.34, 0.1725, validation, ha='center', va='center', fontsize=11,
            color=C_VALID_T, fontweight='bold')
    ax.add_patch(FancyBboxPatch((0.70, 0.12), 0.25, 0.105, boxstyle="round,pad=0.008",
                                facecolor=C_CONC, edgecolor='none', alpha=0.94))
    ax.text(0.825, 0.1725, conclusion, ha='center', va='center', fontsize=11,
            color='white', fontweight='bold')
    for i in range(N):
        x = x0 + i * (box_w + gap)
        ax.annotate('', xy=(x + box_w / 2, 0.245), xytext=(x + box_w / 2, box_y - 0.015),
                    arrowprops=dict(arrowstyle='->', color='#B9BEC6', lw=1.5))
    ax.annotate('', xy=(0.685, 0.1725), xytext=(0.64, 0.1725),
                arrowprops=dict(arrowstyle='->', color='#8A8F98', lw=1.9))
    # 图例
    lg_y = 0.045
    for lx, col, lab in [(0.10, C_DATA_E, '数据层'), (0.20, C_Q[0], '各问题建模'),
                         (0.32, C_VALID_E, '检验与结论')]:
        ax.text(lx, lg_y, '■', ha='center', va='center', fontsize=11, color=col)
        ax.text(lx + 0.015, lg_y, lab, ha='left', va='center', fontsize=8.5, color=C_GRAY)
    ax.text(0.45, lg_y, '──→  数据 / 结果流向', ha='left', va='center', fontsize=8.5, color=C_GRAY)
    ax.text(0.86, lg_y, '虚线框 = 每问产出物', ha='left', va='center', fontsize=8.5, color=C_GRAY)
    fig.savefig(save, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'[图] {save}')
```

### 调用示例（2025 C 题 4 问）

```python
draw_pipeline_flowchart(
    data_layer='数据层：数据读取与清洗  ｜  孕周解析 / 缺失异常处理  ｜  达标时间计算',
    data_source='输入：附件.xlsx  ｜  男胎 1082 行 × 31 列  ｜  女胎 605 行 × 29 列',
    questions=[('①', '问题一', '相关性 + 回归'), ('②', '问题二', '分组 + 时点优化'),
               ('③', '问题三', '生存分析建模'), ('④', '问题四', '女胎异常判定')],
    items=[['Pearson/Spearman', 'Logistic生长曲线', '混合效应 LMM'],
           ['数据驱动达标时间', 'BMI 区间分割', '期望风险最小化'],
           ['删失数据构造', 'AFT 对数正态', 'Cox 交叉验证'],
           ['SMOTE 不平衡处理', 'LR/RF/XGBoost', '软投票集成']],
    outputs=['关系模型 + 显著性', 'BMI 分组 + 最佳时点', '达标比例曲线 + 时点', '判定规则 + AUC'],
    data_arrow_labels=['Y浓度', '达标时间', '多因素', '特征/标签'],
    link_labels=['达标时间', '多因素扩展', '女胎数据'],
    save='figures/fig16_整体建模流程.png')
```

---

## 三、适配其他赛题

- **问数 N 任意**：框宽自动按 `box_w=(0.875-(N-1)*gap)/N` 缩放，颜色循环 `C_Q[i % 4]`；N=3 或 N=5 均可用。
- **无数据层**：直接删数据带条与箭头，把各问框上移到 y≈0.78 附近。
- **无独立检验层**：删检验带条，结论框改放底部居中。
- **配色**：可换 `C_Q` 为题目配色；保持浅色底 + 深色字、深色底 + 白字的对比原则。

## 四、落地检查清单

- [ ] 覆盖全部子问题（每问一框），非单问流程
- [ ] 所有文字标签带白底 `bbox`（防遮挡）
- [ ] 框内分项下沿与产出框上沿间距≥0.01（防白底覆盖文字）
- [ ] 标题/带条字号层级清晰（17/11.5/11/10/8.6/7.8）
- [ ] 300 DPI、中文 SimHei 无乱码、`bbox_inches='tight'`
- [ ] 嵌入 PDF 后人工目检：无文字重叠、无越界、无箭头压字
