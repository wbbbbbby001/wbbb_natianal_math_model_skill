"""
==========================================
wbbb_math_skill 论文正文深度硬检测脚本
用法：
  python depth_check.py <论文.md> [论文.tex] [论文.pdf]
  示例: python depth_check.py final_paper.md paper/main.tex paper/main.pdf
输出：PASS / REFINE + 深度要素缺失项
口径：正文页数下限 + 深度要素清单（见 references/paper_depth_expansion.md）
      standard 模式正文（题目→摘要→…→参考文献）≥20 页，目标 23-28，2026 上限 30
==========================================
"""
import os
import re
import sys
from pathlib import Path


class DepthChecker:
    def __init__(self, md_text='', tex_text='', pdf_path=None, mode='standard'):
        self.md = md_text
        self.tex = tex_text
        self.pdf_path = pdf_path
        self.mode = mode
        self.blob = md_text + '\n' + tex_text
        self.issues = []
        self.passes = []

    def add_issue(self, cat, problem, fix=''):
        self.issues.append({'类别': cat, '问题': problem, '修正建议': fix})

    def add_pass(self, msg):
        self.passes.append(msg)

    # ---------- 正文页数 ----------
    def check_body_pages(self):
        # standard 模式正文必须 >23 页（即 >=24，目标 24-28，上限 30）：问题重述/问题分析按"扩写标准"展开后，
        # 20 页下限已不足以支撑深度，>23 为硬门禁（2026 实战复盘：仅做足推导不下沉附录也常到 24+ 页）
        target = {'standard': (24, 28), 'fast': (16, 28), 'sprint': (12, 28)}.get(self.mode, (24, 28))
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            self.add_issue('正文页数', '未提供 main.pdf，跳过页数检查（务必用 xelatex 编译后检测）',
                           '编译 main.pdf 后重跑，或在审阅时人工核对正文页数')
            return
        try:
            import fitz
        except ImportError:
            self.add_issue('正文页数', '缺 pymupdf(fitz)，无法读 PDF 页数', 'pip install pymupdf')
            return
        doc = fitz.open(self.pdf_path)
        n = len(doc)
        # 附录起始：优先用"运行环境说明"（附录四件套的固定开场）；退化为"附录"字样且出现在文档后半部
        appendix_page = n
        for i in range(n):
            t = doc[i].get_text()
            if '运行环境说明' in t or ('附录' in t and i + 1 > n * 0.5):
                appendix_page = i + 1
                break
        # 正文到参考文献结束，取附录前一页（若与参考文献共享页则略保守，门禁只要求下限，不影响判定）
        body_pages = max(0, appendix_page - 1)
        lo, hi = target
        if body_pages < lo:
            self.add_issue('正文页数', f'正文仅 {body_pages} 页（要求 ≥{lo}，目标 {lo}-{hi}）',
                           '按 references/paper_depth_expansion.md 深度要素清单逐项扩充'
                           '（推导展开/算法伪代码/全量结果表/过程图/灵敏度理论验证/物理合理性讨论）')
        elif body_pages > 30:
            self.add_issue('正文页数', f'正文 {body_pages} 页，超过 2026 上限 30 页',
                           '精简冗余表述，图表/长代码下沉附录')
        else:
            self.add_pass(f'正文页数达标（{body_pages} 页，目标 {lo}-{hi}）')

    # ---------- 深度要素 ----------
    def check_pseudocode(self):
        if re.search(r'\\begin\{algorithm\}|\\begin\{algorithmic\}|\\begin\{lstlisting\}', self.blob):
            self.add_pass('算法伪代码/代码块存在')
        else:
            self.add_issue('算法伪代码', '无 algorithm/algorithmic 或代码块环境',
                           '核心求解流程配 algorithm 伪代码（输入/分步/输出/检验）')

    def check_figures(self):
        n = len(re.findall(r'\\includegraphics', self.tex))
        if n >= 8:
            self.add_pass(f'图数量达标（{n} 张）')
        elif n >= 5:
            self.add_issue('图表深度', f'图仅 {n} 张（建议 ≥8：原理图+过程图+结果图）',
                           '每问补 ≥2 张过程图（频谱/相位/拟合对比/分布图）')
        else:
            self.add_issue('图表深度', f'图仅 {n} 张（要求 ≥5）',
                           '补技术路线图、每问过程图、灵敏度/分布图')

    def check_tables(self):
        n = len(re.findall(r'\\begin\{table\}', self.tex))
        if n >= 8:
            self.add_pass(f'表数量达标（{n} 张）')
        elif n >= 5:
            self.add_issue('图表深度', f'表仅 {n} 张（建议 ≥8：全量结果矩阵/汇总表）',
                           '决策/结果类补全量结果表与汇总表')
        else:
            self.add_issue('图表深度', f'表仅 {n} 张（要求 ≥5）',
                           '补符号表、数据特征表、全量结果表')

    def check_sensitivity_theory(self):
        if re.search(r'理论.{0,8}验证|解析灵敏度|灵敏度.{0,8}理论|对照理论', self.blob):
            self.add_pass('灵敏度含理论-数值交叉验证')
        else:
            self.add_issue('灵敏度理论', '灵敏度分析缺理论-数值交叉验证',
                           '对闭式反演式求解析灵敏度（如 δd/d=-δn/n），与数值扰动结果对比')

    def check_result_summary(self):
        if re.search(r'结果.{0,6}汇总|汇总表|最终结果表|结果总结', self.blob):
            self.add_pass('存在结果汇总表')
        else:
            self.add_issue('结果汇总', '缺全量结果汇总表（所有子问题结果+极差+不确定度+判定）',
                           '加一张收口表：子问题×方法/通道×结果×不确定度×判定')

    def check_physical_validation(self):
        if re.search(r'物理.{0,8}合理|典型量级|行业|合理性验证|跨.{0,4}一致性', self.blob):
            self.add_pass('存在结果物理合理性/讨论')
        else:
            self.add_issue('物理合理性', '缺结果物理合理性或跨问一致性讨论',
                           '结果与行业/物理典型量级对比，讨论跨子问题一致性')

    def check_per_question_sections(self):
        if re.search(r'问题[一二三四五六N]\s*模型|\\section\{问题[一二三四五六N]', self.blob):
            self.add_pass('每问独立成章')
        else:
            self.add_issue('每问成章', '未按"问题X模型建立及求解"每问独立成章',
                           '把模型建立与求解拆为每问一个一级章节')

    def check_discussion_depth(self):
        # 每问结果解读：识别"由表X可见/如表X所示/分析如下"结构化解读 或 量化结论短语
        patterns = [
            r'由表.{0,100}(可见|表明|说明)',
            r'由.{0,10}图.{0,100}(可见|表明|说明)',
            r'如表.{0,80}(所示|可见)',
            r'分析如下',
            r'(相对偏差|误差|偏差|精度|可靠|稳健|一致)仅?.{0,20}(%|μm|μ|量级|倍)',
            r'表明.{0,40}(%|μm|mm|量级|倍|稳定|一致)',
        ]
        if any(re.search(p, self.blob) for p in patterns):
            self.add_pass('存在结果量化解读')
        else:
            self.add_issue('结果解读', '缺结果量化解读（"由表X可见…"级）',
                           '每个结果表/图配 ≥2 句量化解读（趋势/原因/物理含义）')

    def run_all(self):
        print('=' * 60)
        print('论文正文深度硬检测')
        print('=' * 60)
        self.check_body_pages()
        self.check_pseudocode()
        self.check_figures()
        self.check_tables()
        self.check_sensitivity_theory()
        self.check_result_summary()
        self.check_physical_validation()
        self.check_per_question_sections()
        self.check_discussion_depth()
        return self.report()

    def report(self):
        n_issue = len(self.issues)
        n_pass = len(self.passes)
        status = 'PASS' if n_issue == 0 else 'REFINE'
        print(f"通过: {n_pass} 项 | 不通过: {n_issue} 项")
        print(f"状态: {status}")
        for i in self.issues:
            print(f"  [缺失] {i['类别']}: {i['问题']}")
            if i['修正建议']:
                print(f"      → {i['修正建议']}")
        if status == 'PASS':
            print('\n✅ 正文深度达标，可进入终审')
        else:
            print('\n⚠️ 按 references/paper_depth_expansion.md 深度要素清单定向补齐后重测')
        return status


def main():
    if len(sys.argv) < 2:
        print('用法: python depth_check.py <论文.md> [论文.tex] [论文.pdf]')
        sys.exit(2)
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f'错误：文件不存在 - {md_path}')
        sys.exit(1)
    md = md_path.read_text(encoding='utf-8', errors='replace')
    tex_path = Path(sys.argv[2]) if len(sys.argv) > 2 and Path(sys.argv[2]).exists() else None
    tex = tex_path.read_text(encoding='utf-8', errors='replace') if tex_path else ''
    pdf_path = sys.argv[3] if len(sys.argv) > 3 else None
    DepthChecker(md, tex, pdf_path, mode='standard').run_all()


if __name__ == '__main__':
    main()
