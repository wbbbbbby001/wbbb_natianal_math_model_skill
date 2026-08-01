# 代码手输出模板

> 此模板定义 `code_and_figures.md` 与 `code/*.py` 的结构与铁律。
> **核心原则**：
> 1. 按题面实际问题数 N 生成 `question1_model.py … questionN_model.py`，数据处理单独文件，全部可独立运行；
> 2. 所有代码逐行中文注释，无黑箱；
> 3. ⚠️ **所有图片标注统一中文（Chinese Only）**，必须配置 SimHei 中文字体防乱码；希腊/数学符号用 `\u` 转义保持源码 ASCII（附录无缺字）。

---

# {题号} 数学建模代码与图像全集

**生成时间**：{YYYY-MM-DD HH:MM}
**运行环境**：{Python 3.x / MATLAB R202x}

---

## 0. 代码文件清单与运行说明

### 0.1 各文件功能对照表

| 文件名 | 功能 | 依赖 | 可独立运行 |
|--------|------|------|-----------|
| `data_loading.py` | 数据读取 | 无 | ✅ |
| `data_eda.py` | 数据探索分析 | data_loading | ✅ |
| `data_preprocessing.py` | 数据预处理 | data_loading | ✅ |
| `question1_model.py` | 问题一模型与求解 | data_preprocessing | ✅ |
| `question2_model.py` | 问题二模型与求解 | data_preprocessing | ✅ |
| `questionN_model.py` | 问题N模型与求解 | data_preprocessing | ✅ |
| `model_validation.py` | 三大检验（误差/灵敏度/稳健性/对比） | question* | ✅ |
| `visualization.py` | 图表生成 | 上述所有 | ✅ |
| `main_solver.py` | 主入口（一键运行） | 上述所有 | ✅ |
| `requirements.txt` | Python 依赖清单 | 无 | - |

### 0.2 运行环境与依赖

```bash
python --version  # Python 3.9+
pip install -r requirements.txt
```

### 0.3 运行顺序

```
一键：python main_solver.py
逐个：python data_loading.py → data_eda.py → data_preprocessing.py
     → question1_model.py → ... → questionN_model.py
     → model_validation.py → visualization.py
```

### 0.4 附录映射表（论文手直接照此贴代码）

> 代码手在 `code_and_figures.md` 里必须给出这张表，论文手按它把每个文件全文贴入对应附录（对齐优秀论文"支撑文件目录表+附录目录"）。

| 附录 | 名称 | 对应 code/ 文件 | 对应正文节/表 |
|------|------|----------------|--------------|
| 附录1 | 数据读取与预处理代码 | data_loading.py / data_preprocessing.py | 第 X 节 |
| 附录2 | 问题一求解代码 | question1_model.py | 第 X 节 / 表 X |
| 附录3 | 问题二求解代码 | question2_model.py | 第 X 节 / 表 X |
| 附录4 | 问题三求解代码 | question3_model.py | 第 X 节 / 表 X |
| 附录5 | 问题四求解代码 | question4_model.py | 第 X 节 / 表 X |
| 附录6 | 检验与可视化代码 | model_validation.py / visualization.py | 第 X 节 |

### 0.5 每个 .py 文件头注释模板（附录粘贴就绪）

> 每个求解文件头部必须含以下注释块，保证论文手能全文贴入附录且评审能看懂：

```python
"""
==========================================
文件名：question2_model.py
功能：问题二 16/32 方案期望决策求解
对应正文：第 X 节 / 表 X
运行环境：Python 3.12，numpy/scipy
依赖：data_loading.py, data_preprocessing.py
可独立运行：python question2_model.py
==========================================
"""
```

---

## ⚠️ 图片生成铁律（代码手必须遵守）

### 铁律1：所有图表标注统一使用中文（Chinese Only）

**为什么**：论文与图件应保持中文一致（图题在上+中文、图内标注中文）。matplotlib 默认字体不含中文字形，直接写中文会乱码（方块字符）；**必须先在 rcParams 配置中文字体（SimHei / 微软雅黑 / Noto Sans SC）**，并给希腊/数学符号用 `\u` 转义（保证附录 lstlisting 里源码为纯 ASCII、无缺字）。

**正确示例** ✅（配 SimHei 字体后）：
```python
ax.set_xlabel('时间 (h)')
ax.set_ylabel('数量（件）')
ax.set_title('实际与预测趋势对比')
ax.legend(['观测值', '模型'], loc='best')
ax.set_title('波数范围 1000-3000 cm$^{-1}$（含符号）')   # 数学符号用 mathtext，希腊字母用 \\u 转义
```

**必须配置**（文件头 rcParams，否则中文乱码成方块）：
```python
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['SimHei', 'Microsoft YaHei', 'Noto Sans SC', 'DejaVu Sans'],
    'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
})
```

**附录安全**：图内出现的 ≥、→、ν、θ、₂ 等符号，源码字符串一律写 `\\u2265`、`\\u2192`、`\\u03bd`、`\\u03b8`、`\\u2082` 转义（运行时 Python 解出原符号，源码保持 ASCII），避免附录 lstlisting 在等宽字体（lmmono）下缺字。

### 铁律2：每个绘图文件开头必须设置 matplotlib 全局参数

```python
import matplotlib
matplotlib.use('Agg')  # 非交互后端，避免 GUI 依赖
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix',
    'axes.unicode_minus': False,     # 负号防方块
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
    'axes.linewidth': 1.0,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'lines.linewidth': 1.2,
})

# 学术配色（ColorBrewer 风格）
COLORS = ['#2166AC', '#D6604D', '#4DAF4A', '#984EA3', '#FF7F00', '#A65628']
```

### 铁律3：图片质量验收标准

每张图生成后检查：
- [ ] 放大 200% 无像素化/马赛克
- [ ] 无任何方块/豆腐块字符（乱码典型表现）
- [ ] 所有文字标注清晰可读
- [ ] 分辨率 ≥300 DPI
- [ ] 宽度 8-16cm（打印尺寸）
- [ ] 配色美观，彩色图在灰度下仍可辨识
- [ ] 每图配 50 字内专业图注（论文图题用中文并放图片上方；图内坐标/图例/标题标注统一中文，SimHei 无乱码）

---

## 1. 数据获取与读取 → code/data_loading.py

```python
"""
==========================================
模块：数据读取 (data_loading.py)
功能：读取赛题提供的原始数据文件（相对路径/自动检测）
可独立运行：python data_loading.py
==========================================
"""
import os
import glob
import pandas as pd

def load_all_data(data_dir='.'):
    """自动检测并读取数据目录下的数据文件，返回 {name: DataFrame}"""
    data = {}
    # 支持 xlsx/csv/txt，按文件名排序
    for ext in ('*.xlsx', '*.csv', '*.txt'):
        for filepath in sorted(glob.glob(os.path.join(data_dir, ext))):
            name = os.path.splitext(os.path.basename(filepath))[0]
            try:
                if filepath.endswith('.xlsx'):
                    df = pd.read_excel(filepath)
                else:
                    df = pd.read_csv(filepath, encoding='utf-8')
            except Exception as e:   # 异常捕获 + 兼容逻辑
                print(f"[WARN] 读取失败 {filepath}: {e}")
                continue
            df.columns = [str(c).strip() for c in df.columns]  # 列名清洗
            data[name] = df
            print(f"Loaded {name}: {df.shape}")
    return data

if __name__ == '__main__':
    data = load_all_data()
    for name, df in data.items():
        print(f"\n{name}:\n  head:\n{df.head(10)}\n  tail:\n{df.tail(5)}")
```

---

## 2. 数据探索分析（EDA）→ code/data_eda.py

```python
"""
==========================================
模块：数据探索分析 (data_eda.py)
功能：描述统计、分布、缺失、异常检测
可独立运行：python data_eda.py
==========================================
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from data_loading import load_all_data

plt.rcParams.update({'font.family': 'serif', 'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})

def eda_analysis(data):
    """描述统计：均值/方差/偏度/峰度/缺失/异常"""
    results = {}
    for name, df in data.items():
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        stats = {}
        for col in num_cols:
            vals = df[col].dropna().values
            stats[col] = {
                'mean': float(np.mean(vals)), 'std': float(np.std(vals)),
                'min': float(np.min(vals)), 'max': float(np.max(vals)),
                'missing': int(df[col].isnull().sum()),
                'skew': float(pd.Series(vals).skew()),
            }
            print(f"{name}.{col}: mean={stats[col]['mean']:.4f} missing={stats[col]['missing']}")
        results[name] = stats
    return results

if __name__ == '__main__':
    data = load_all_data()
    eda_analysis(data)
```

---

## 3. 数据预处理 → code/data_preprocessing.py

```python
"""
==========================================
模块：数据预处理 (data_preprocessing.py)
功能：分级缺失填充 + 多方法异常处理 + 标准化/编码 + 特征工程
可独立运行：python data_preprocessing.py
==========================================
"""
import numpy as np
import pandas as pd
from data_loading import load_all_data

def preprocess_data(data):
    processed = {}
    for name, df in data.items():
        dfp = df.copy()
        num_cols = dfp.select_dtypes(include=[np.number]).columns.tolist()
        for col in num_cols:
            # 1) 缺失值分级处理：<5% 均值/中位数；5%-30% 插值；>30% 预测填充(回退中位数)
            miss = dfp[col].isnull().sum()
            if miss > 0:
                rate = miss / len(dfp)
                if rate < 0.05:
                    dfp[col].fillna(dfp[col].median(), inplace=True)
                elif rate < 0.30:
                    dfp[col] = dfp[col].interpolate(method='linear')
                else:
                    dfp[col].fillna(dfp[col].median(), inplace=True)
                print(f"  {name}.{col}: {rate*100:.1f}% missing handled")
            # 2) 异常值：3σ 准则 + 箱线图 IQR 联用（替换为中位数）
            col_clean = dfp[col].dropna().values
            mu, sd = np.mean(col_clean), np.std(col_clean)
            q1, q3 = np.percentile(col_clean, [25, 75]); iqr = q3 - q1
            mask = (dfp[col] > mu + 3*sd) | (dfp[col] < mu - 3*sd) | \
                   (dfp[col] > q3 + 1.5*iqr) | (dfp[col] < q1 - 1.5*iqr)
            if mask.sum() > 0:
                dfp.loc[mask, col] = dfp[col].median()
                print(f"  {name}.{col}: {int(mask.sum())} outliers replaced")
        # 3) 标准化：Z-score（可按需启用）
        processed[name] = dfp
    return processed

if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    data = load_all_data()
    processed = preprocess_data(data)
    for name, dfp in processed.items():
        out = f"data/processed_{name}.csv"
        dfp.to_csv(out, index=False, encoding='utf-8-sig')
        print(f"Saved: {out}")
```

---

## 4. 模型求解代码（每问独立文件，共 N 个）

### 4.1 问题一 → code/question1_model.py

```python
"""
==========================================
模块：问题一 (question1_model.py)
问题：{问题一描述}
模型：{模型名称}
算法：{求解算法}
可独立运行：python question1_model.py
==========================================
"""
import numpy as np
from data_loading import load_all_data
from data_preprocessing import preprocess_data

def solve_question1(processed_data):
    """建立并求解问题一，返回关键结果 dict"""
    # TODO: 依据 modeling_thought.md 实现
    results = {'key_metric': 0.0, 'conclusion': ''}
    return results

if __name__ == '__main__':
    data = load_all_data()
    processed = preprocess_data(data)
    r = solve_question1(processed)
    print("Question 1 Results:", r)
```

### 4.2 问题二 → code/question2_model.py
{同上结构：solve_question2}

### 4.N 问题N → code/questionN_model.py
{同上结构：solve_questionN}

---

## 5. 模型检验代码 → code/model_validation.py

```python
"""
==========================================
模块：模型检验 (model_validation.py)
功能：误差分析 + 灵敏度分析 + 稳健性检验 + 多模型对比
可独立运行：python model_validation.py
==========================================
"""
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def error_analysis(y_true, y_pred, name):
    """误差分析：RMSE/MAE/MAPE/R²"""
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1e-10))) * 100)
    r2 = float(r2_score(y_true, y_pred))
    print(f"[{name}] RMSE={rmse:.4f} MAE={mae:.4f} MAPE={mape:.2f}% R2={r2:.4f}")
    return {'RMSE': rmse, 'MAE': mae, 'MAPE': mape, 'R2': r2}

def sensitivity_analysis(func, param, base, variations=(-0.2, -0.1, 0.1, 0.2)):
    """灵敏度分析：参数 ±10%/±20% 扰动，观察结果变化率"""
    baseline = func(param, base)
    for var in variations:
        new = func(param, base * (1 + var))
        delta = (new - baseline) / abs(baseline) * 100
        print(f"  {param} {var*100:+.0f}%: result={new:.4f}, delta={delta:+.2f}%")

def robustness_test(func, data, noise_levels=(0.01, 0.02, 0.05)):
    """稳健性检验：加噪 + 样本缩扩"""
    baseline = func(data)
    for level in noise_levels:
        noisy = data * (1 + np.random.normal(0, level, data.shape))
        delta = abs(func(noisy) - baseline) / abs(baseline) * 100
        print(f"  noise {level*100:.0f}%: delta={delta:.2f}%")
```

---

## 6. 结果可视化 → code/visualization.py

> ⚠️ 图片标注铁律再次强调：**所有 title/xlabel/ylabel/legend/text 统一英文**。

```python
"""
==========================================
模块：可视化与图像生成 (visualization.py)
功能：生成全部竞赛级图表
可独立运行：python visualization.py
==========================================
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ===== matplotlib 全局配置（中文标注，SimHei 防乱码）=====
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['SimHei', 'Microsoft YaHei', 'Noto Sans SC', 'DejaVu Sans'],
    'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
    # ...（其余字号/DPI 配置同前）
})
plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'stix', 'axes.unicode_minus': False,
    'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 11,
    'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9,
    'figure.dpi': 300, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    'axes.linewidth': 1.0, 'axes.grid': True, 'grid.alpha': 0.3,
    'grid.linestyle': '--', 'lines.linewidth': 1.2,
})
COLORS = ['#2166AC', '#D6604D', '#4DAF4A', '#984EA3', '#FF7F00', '#A65628']

def plot_trend(x, y_obs, y_pred, xlabel, ylabel, title, save_path):
    """通用趋势对比图（实际 vs 模型）"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(x, y_obs, color=COLORS[0], linewidth=1.0, label='Observed')
    ax.plot(x, y_pred, color=COLORS[1], linewidth=1.4, linestyle='--', label='Model')
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title)
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300); plt.close()
    print(f"Generated: {save_path}")

def plot_heatmap(matrix, xticklabels, yticklabels, cbar_label, title, save_path):
    """通用热力图（相关性/敏感性）"""
    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(matrix, cmap='RdYlBu_r', aspect='auto')
    ax.set_xticks(range(len(xticklabels))); ax.set_xticklabels(xticklabels)
    ax.set_yticks(range(len(yticklabels))); ax.set_yticklabels(yticklabels)
    ax.set_title(title)
    fig.colorbar(im, ax=ax, label=cbar_label)
    plt.tight_layout(); plt.savefig(save_path, dpi=300); plt.close()
    print(f"Generated: {save_path}")

if __name__ == '__main__':
    # 依据各问结果调用绘图函数
    pass
```

---

## 7. 主入口 → code/main_solver.py

```python
"""
==========================================
主求解程序 (main_solver.py)
功能：一键运行全部流程
用法：python main_solver.py
==========================================
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loading import load_all_data
from data_eda import eda_analysis
from data_preprocessing import preprocess_data
# 按问题数 N 动态导入（以 question1 为例）
from question1_model import solve_question1
# from question2_model import solve_question2
# from questionN_model import solve_questionN
from model_validation import error_analysis, sensitivity_analysis, robustness_test

def main():
    print("=" * 60)
    print("  CUMCM Complete Solver")
    print("=" * 60)
    data = load_all_data()
    eda_analysis(data)
    processed = preprocess_data(data)
    r1 = solve_question1(processed)
    # r2 = solve_question2(processed); ...
    print("Results:", r1)

if __name__ == '__main__':
    main()
```

---

## 8. 代码环境说明

### requirements.txt

```
numpy>=1.24
scipy>=1.10
matplotlib>=3.7
pandas>=2.0
openpyxl>=3.1
scikit-learn>=1.3
```

---

> **代码手交付清单**：
> - [ ] `code/`：data_loading / data_eda / data_preprocessing / question1~N / model_validation / visualization / main_solver + requirements.txt
> - [ ] 全部文件可独立运行（`if __name__ == '__main__'`）
> - [ ] `scripts/verify_code.py` 检测通过（语法编译 + import 冒烟）
> - [ ] `figures/`：全部中文标注（SimHei 无乱码）、≥300 DPI、每图有图注、附录源码无缺字（符号用 \u 转义）
> - [ ] `data/`：处理后 CSV（前 10 行 + 后 5 行展示）
> - [ ] 关键结果数值已回填 `state/decision_log.json`
> - [ ] `code_and_figures.md` 已生成
