"""
==========================================
wbbb_math_skill 国赛论文格式硬检测脚本
用法：
  python format_check.py <论文.md> [论文.tex]
  示例: python format_check.py final_paper.md paper/main.tex
输出：PASS / FAIL / BLOCK + 不通过项详情（含严重程度 high/mid/low）
口径：以《2026国赛三天速成国奖》宝书为准（摘要800-1000字、关键词4-6个、
      单倍行距、正文30页内、12模块结构、三线表、匿名、查重≤20%、AI披露）
==========================================
"""
import os
import re
import sys
from pathlib import Path

CJK_RE = re.compile(r'[\u4e00-\u9fff]')
ASCII_WORD_RE = re.compile(r'[A-Za-z][A-Za-z0-9\.\-]*')

FORBIDDEN_PHRASES = [
    ('随着社会快速发展', '万能套话，直接切入问题'),
    ('该问题具有深远的研究意义', '空话，改为具体说明'),
    ('笔者认', '主观表述，改为"本文"'),
    ('我认为', '主观表述'),
    ('显然', '不严谨，改为量化描述'),
    ('效果显著', '模糊描述，改为具体数据'),
    ('有所提升', '模糊描述，改为"提升X%"'),
    ('如下表', '模糊指代，改为"表X展示"'),
    ('见上图', '模糊指代，改为"图X展示"'),
    ('详见上图', '模糊指代'),
    ('众所周知', '套话'),
    # ---- AI 编辑痕迹（写作纪律，一眼可见，直接删）----
    ('单独成页', 'AI编辑痕迹，删除'),
    ('单独一页', 'AI编辑痕迹'),
    ('用于直接展示', 'AI设计说明语气，改为自然表述'),
    ('（占位）', '模板占位符，替换为真实内容'),
    ('待插入', '模板占位符'),
    ('待完善', '模板占位符'),
    ('同上结构', '模板占位符，写入论文前替换为真实内容'),
]

ANON_PATTERNS = [
    (r'姓名', '身份信息'),
    (r'学号', '身份信息'),
    (r'指导教师', '身份信息'),
    (r'校徽', 'Logo'),
    (r'参赛编号', '参赛编号'),
    (r'University', '院校信息'),
    (r'College', '院校信息'),
    (r'学校名', '院校信息'),
]

GENERIC_KEYWORDS = ['数学建模', '问题分析', '模型建立', '数据分析', '研究探讨']


def count_zh_words(text: str) -> int:
    """中文按字计，英文按词计，近似'字数'口径。"""
    cjk = len(CJK_RE.findall(text))
    ascii_words = len(ASCII_WORD_RE.findall(text))
    return cjk + ascii_words


class PaperFormatChecker:
    def __init__(self, paper_md: str, paper_tex: str = '', figures_dir: str = None, md_path: str = ''):
        self.md = paper_md
        self.tex = paper_tex
        self.figures_dir = figures_dir
        self.md_path = md_path  # 真实文件路径（用于定位同级 code/ 目录）
        self.issues = []
        self.passes = []

    def add_issue(self, category, problem, severity, fix):
        self.issues.append({'类别': category, '问题': problem,
                            '严重程度': severity, '修正建议': fix})

    def add_pass(self, msg):
        self.passes.append(msg)

    # ---------- 检测项 ----------

    def check_abstract(self):
        """摘要：800-1000 字、单页内、纯文字、三段式要素。"""
        # 摘要正文在下一个标题或"关键词："行处截止（关键词不计入摘要字数）
        m = re.search(r'#+\s*摘要\s*\n(.*?)(?=\n\s*#+\s|\n\s*\*?\*?关键词|\Z)', self.md, re.DOTALL)
        if not m:
            self.add_issue('摘要', '未找到"## 摘要"章节', 'high', '添加摘要章节')
            return
        abstract = m.group(1)
        n = count_zh_words(abstract)
        if n < 800:
            self.add_issue('摘要', f'字数不足（约 {n} 字，要求 800-1000）', 'high', '补充至 800 字以上')
        elif n > 1000:
            self.add_issue('摘要', f'字数超限（约 {n} 字，要求 800-1000）', 'mid', '精简至 1000 字以内')
        else:
            self.add_pass(f'摘要字数合规（约 {n} 字）')
        if '$' in abstract:
            self.add_issue('摘要', '含公式符号（$ 或 $$）', 'high', '移除摘要中所有公式')
        for ch, name in [('？', '问句'), ('!', '感叹句'), ('！', '感叹句')]:
            if ch in abstract:
                self.add_issue('摘要', f'含{name}({ch})', 'mid', '改为陈述句')
        if re.search(r'[图表]\s*\d', abstract):
            self.add_issue('摘要', '含图表引用', 'high', '移除图表引用')
        if re.search(r'\[\d+\]|\^\[|\(参考文献', abstract):
            self.add_issue('摘要', '含引用标号', 'mid', '移除引用标注')
        for kw, pat in [('模型', r'模型'), ('算法', r'算法'), ('结果', r'结果'),
                        ('检验', r'检验|验证'), ('灵敏度', r'灵敏度|敏感性'),
                        ('稳健性/鲁棒性', r'稳健|鲁棒')]:
            if not re.search(pat, abstract):
                self.add_issue('摘要', f'摘要缺核心要素"{kw}"', 'mid', '补充对应内容')

    def check_keywords(self):
        m = re.search(r'关键词[：:]\s*(.+)', self.md)
        if not m:
            self.add_issue('关键词', '未找到"关键词"行', 'high', '添加关键词行')
            return
        kw = re.split(r'[;；,\s]+', m.group(1).strip())
        kw = [k for k in kw if k]
        if not (4 <= len(kw) <= 6):
            self.add_issue('关键词', f'数量{len(kw)}个，要求 4-6 个', 'mid', '调整关键词数量')
        else:
            self.add_pass(f'关键词数量合规（{len(kw)}个）')
        used = [w for w in kw if w in GENERIC_KEYWORDS]
        if used:
            self.add_issue('关键词', f'使用禁用泛义词：{used}', 'low', '替换为具体模型/算法/方法名')

    def check_structure(self):
        """12 模块结构完整性（书 §7.1，结构分占 20%）。"""
        required = [
            ('摘要', r'摘要'), ('关键词', r'关键词'), ('问题重述', r'问题重述'),
            ('问题分析', r'问题分析'), ('模型假设', r'模型假设'), ('符号说明', r'符号说明'),
            ('模型建立与求解', r'模型建立|模型求解'), ('模型检验', r'模型检验|模型验证'),
            ('模型改进与推广', r'模型改进|模型推广'), ('模型优缺点', r'优缺点'),
            ('参考文献', r'参考文献|参考文 献|thebibliography'), ('附录', r'附录|Appendi'),
        ]
        for name, pat in required:
            if re.search(pat, self.md) or re.search(pat, self.tex):
                self.add_pass(f'✓ 模块 "{name}" 存在')
            else:
                self.add_issue('结构', f'缺少"{name}"模块', 'high', f'添加"{name}"章节')

    def check_numbering(self):
        """图表编号连续性。"""
        for label, pat in [('图', r'图\s*(\d+)'), ('表', r'表\s*(\d+)')]:
            nums = sorted({int(x) for x in re.findall(pat, self.md)})
            if not nums:
                continue
            full = set(range(min(nums), max(nums) + 1))
            missing = full - set(nums)
            if missing:
                self.add_issue('图表编号', f'{label}编号不连续，缺失 {label}{sorted(missing)}', 'mid', '检查编号跳号')
            else:
                self.add_pass(f'{label}编号连续（{label}{min(nums)}-{label}{max(nums)}）')
        # 引用审计：tex 图表若未用 \label，新增/删除图表后硬编码编号会错位
        if self.tex and re.search(r'\\caption\{', self.tex):
            n_cap = len(re.findall(r'\\caption\{', self.tex))
            n_lab = len(re.findall(r'\\label\{(tab|fig):', self.tex))
            if n_lab < n_cap:
                self.add_issue('图表编号', f'{n_cap} 个图表仅 {n_lab} 个带 \\label，硬编码"表X/图X"引用易错位', 'low',
                               '给图表加 \\label{{tab/fig:...}} 并用 \\ref 引用；或每次新增/删除图表后全文核对编号')

    def check_anonymity(self):
        found = []
        for pat, what in ANON_PATTERNS:
            for m in re.finditer(pat, self.md, re.IGNORECASE):
                ctx = self.md[max(0, m.start() - 15):m.end() + 15].replace('\n', ' ')
                found.append(f'{what}: "{pat}" 上下文 ...{ctx}...')
        if found:
            for f in found[:3]:
                self.add_issue('匿名', f'可能含身份信息 - {f}', 'high', '彻底删除所有个人/院校信息（含文件名/文档属性/页眉页脚）')
        else:
            self.add_pass('匿名检测通过')

    def check_forbidden(self):
        for phrase, reason in FORBIDDEN_PHRASES:
            c = self.md.count(phrase)
            if c > 0:
                self.add_issue('禁止用语', f'"{phrase}" 出现 {c} 次 — {reason}', 'low', '替换为更专业/具体的表达')

    def check_ai_disclosure(self):
        if re.search(r'AI.{0,10}使用说明|人工智能.{0,10}使用说明|AI\s*工具', self.md) or \
           re.search(r'AI.{0,10}使用说明|AI\s*工具', self.tex):
            self.add_pass('✓ AI 使用说明存在')
        else:
            self.add_issue('AI披露', '未找到 AI 使用说明（2026 国赛强制要求，放附录4）', 'mid', '在附录添加 AI 工具使用说明')

    def check_appendix(self):
        """附录完整性：附录四件套（对齐 2024B 优秀论文 P24-37）。
        表1 支撑文件目录 + 表2 附录目录 + 分问全量代码 + 运行环境说明。
        """
        blob = self.md + '\n' + self.tex
        if not re.search(r'附录|Appendi', blob):
            self.add_issue('附录', '缺少附录模块', 'high', '添加附录（四件套）')
            return
        # 1) 支撑文件目录表
        if re.search(r'支撑文件目录|支撑文件', blob):
            self.add_pass('✓ 附录有表1「支撑文件目录」')
        else:
            self.add_issue('附录', '缺少表1「支撑文件目录」（code/ 文件→功能→对应附录）', 'mid',
                           '对齐优秀论文表1，列出每个脚本文件')
        # 2) 附录目录表
        if re.search(r'附录目录', blob):
            self.add_pass('✓ 附录有表2「附录目录」')
        else:
            self.add_issue('附录', '缺少表2「附录目录」（附录编号→名称）', 'mid',
                           '对齐优秀论文表2，列出附录1-N 及名称')
        # 3) 分问全量代码：检查 code/ 下每个 .py 是否在附录中（以文件名出现为准）
        code_dir = os.path.join(os.path.dirname(self.md_path), 'code') if self.md_path else 'code'
        if os.path.isdir(code_dir):
            py_files = sorted(f for f in os.listdir(code_dir) if f.endswith('.py'))
            missing = [f for f in py_files if f not in blob]
            if not py_files:
                self.add_issue('附录', 'code/ 目录为空或未找到', 'mid', '确认 code/ 存在且含 .py')
            elif missing:
                self.add_issue('附录', f'以下 code/ 文件未在附录出现（应完整贴入）：{missing}', 'mid',
                               '把每个求解脚本全文贴入对应附录，非关键片段')
            else:
                self.add_pass(f'✓ 附录覆盖全部 code/ 脚本（{len(py_files)} 个）')
            # 4) 运行环境说明
            if re.search(r'运行环境|requirements|Python\s*[\d.]', blob):
                self.add_pass('✓ 附录有运行环境/一键复现说明')
            else:
                self.add_issue('附录', '缺少运行环境/一键复现说明（版本/依赖/requirements）', 'low',
                               '附录开头加运行环境 + python main_solver.py 一键复现')
        else:
            self.add_issue('附录', '找不到 code/ 目录，无法核验附录代码完整性', 'low',
                           '确认 final_paper.md 与 code/ 同级')
        # 5) 每问独立成章（对齐优秀论文五/六/七/八）
        if re.search(r'问题[一二三四五六N]\s*模型', blob) or \
           re.search(r'\\section\{问题[一二三四五六N]', self.tex):
            self.add_pass('✓ 每问独立成章（问题X模型建立及求解）')
        else:
            self.add_issue('结构', '未按"问题X模型建立及求解"每问独立成章', 'low',
                           '把模型建立与求解拆为每问一个一级章节（对齐优秀论文）')

    def check_tex(self):
        """LaTeX 层检查（若提供 .tex）。"""
        if not self.tex:
            self.add_pass('未提供 .tex，跳过 LaTeX 层检查')
            return
        t = self.tex
        if 'booktabs' not in t:
            self.add_issue('LaTeX', '未加载 booktabs（三线表宏包）', 'mid', '\\usepackage{booktabs}')
        for name in ['documentclass', 'begin{document}', 'end{document}']:
            if name not in t:
                self.add_issue('LaTeX', f'缺少 {name}', 'high', f'补齐 {name}')
        for tm in re.finditer(r'\\begin\{tabular\}\{([^}]*)\}', t):
            spec = tm.group(1)
            if '|' in spec:
                self.add_issue('LaTeX', '表格列说明含竖线(|)，非三线表', 'mid', '去掉竖线，使用 booktabs 的 toprule/midrule/bottomrule')
            # 宽表提示：自动宽度列 ≥6 且表内无 \small/\footnotesize/\resizebox 时需核对宽度
            # （\centering 对超版心的表格无效，会向右溢出）
            cols = [c for c in spec if c in 'clr']
            has_scale = bool(re.search(r'\\small|\\footnotesize|\\scriptsize|\\resizebox', t[max(0, tm.start()-300):tm.start()]))
            if len(cols) >= 6 and 'p{' not in spec and not has_scale:
                self.add_issue('LaTeX', f'表格 {len(cols)} 列无 p{{}} 换行/\\small 缩放，需核对是否超版心', 'low',
                               '若超版心：宽表用 \\small + p{{宽度}} 列（或 \\resizebox{\\textwidth}{!}{...}）保证居中不超界')
        if re.search(r'\\includegraphics', t) and not re.search(r'\\graphicspath', t):
            self.add_issue('LaTeX', '有图片但缺 graphicspath 配置', 'low', '添加 \\graphicspath{{../figures/}}')
        # 单倍行距：linespread 应接近 1.0
        ls = re.search(r'\\linespread\{([\d.]+)\}', t)
        if ls and float(ls.group(1)) > 1.1:
            self.add_issue('LaTeX', f'行距 linespread={ls.group(1)}，书要求单倍行距', 'mid', '改为 \\linespread{1.0}')

    def check_pagination_numbering(self):
        """页眉页脚 + 章节编号 + 附录编号。
        页眉留空；页码阿拉伯数字居中于页脚；一级标题用中文数字（一、二、三…）；
        附录用数字编号（附录1、附录2…），禁用字母（附录A/B/C）。
        """
        blob = self.md + '\n' + self.tex
        # 1) 页眉留空 + 页码页脚居中（tex 层）
        if self.tex:
            if re.search(r'\\fancyfoot\s*\[C\]\{\\thepage\}', self.tex, re.IGNORECASE):
                self.add_pass('✓ 页码居中于页脚（\\fancyfoot[C]{\\thepage}）')
            else:
                self.add_issue('页眉页脚', '未找到"页码居中于页脚"配置（\\fancyfoot[C]{\\thepage}）', 'mid',
                               '加载 fancyhdr：\\pagestyle{fancy}、\\fancyhf{}、\\fancyfoot[C]{\\thepage}、\\headrulewidth=0pt')
            if re.search(r'\\fancyhf\{\}|\\fancyhead\{\}', self.tex) and re.search(r'\\headrulewidth[^\n]*\{\s*0pt\s*\}', self.tex):
                self.add_pass('✓ 页眉留空（\\fancyhf{} 清空 + \\headrulewidth=0pt）')
            else:
                self.add_issue('页眉页脚', '未确认页眉留空（应 \\fancyhf{} 清空页眉页脚、\\headrulewidth=0pt 去掉页眉横线）', 'mid',
                               '用 fancyhdr 清空页眉：\\fancyhf{}、\\fancyfoot[C]{\\thepage}、\\renewcommand{\\headrulewidth}{0pt}')
        # 2) 一级标题中文数字编号
        headings = re.findall(r'^#{1,3}\s*(\S.*)', self.md, re.MULTILINE)
        arabic_h1 = [h for h in headings if re.match(r'^\d+[、\s]', h)]
        if arabic_h1:
            self.add_issue('章节编号', f'标题用阿拉伯数字一级编号：{arabic_h1[:5]}', 'mid',
                           '一级标题改为中文数字（一、二、三…，如"一、问题重述"），二级可用阿拉伯（1.1）')
        else:
            self.add_pass('✓ 标题无阿拉伯数字一级编号（应为中文数字）')
        if self.tex:
            if re.search(r'\\chinese\{section\}', self.tex):
                self.add_pass('✓ tex 一级章节中文数字编号（\\chinese{section}）')
            else:
                self.add_issue('章节编号', 'tex 未启用一级章节中文数字编号（缺 \\chinese{section}）', 'mid',
                               '\\ctexset{section={name={,、},number=\\chinese{section},aftername={}}} + \\renewcommand{\\thesection}{\\chinese{section}}')
        # 3) 附录数字编号（禁用字母）
        if re.search(r'附录[A-Z]', blob):
            self.add_issue('附录编号', '附录用字母编号（附录A/B/C…），应改为数字（附录1、2、3…）', 'mid',
                           '全部"附录X"改为"附录N"（N 为阿拉伯数字），表1/表2 与正文引用同步')
        else:
            self.add_pass('✓ 附录为数字编号（附录1、附录2…，无字母）')

    def run_all(self):
        print('=' * 60)
        print('国赛论文格式硬检测')
        print('=' * 60)
        self.check_abstract()
        self.check_keywords()
        self.check_structure()
        self.check_numbering()
        self.check_anonymity()
        self.check_forbidden()
        self.check_ai_disclosure()
        self.check_appendix()
        self.check_pagination_numbering()
        self.check_tex()
        return self.report()

    def report(self):
        high = [i for i in self.issues if i['严重程度'] == 'high']
        mid = [i for i in self.issues if i['严重程度'] == 'mid']
        low = [i for i in self.issues if i['严重程度'] == 'low']
        status = 'BLOCK' if high else ('PASS' if not mid else 'FAIL')
        report = {
            '状态': status, '通过': self.passes, '不通过': self.issues,
            'high': len(high), 'mid': len(mid), 'low': len(low),
        }
        print(f"通过: {len(self.passes)} 项 | 不通过: {len(self.issues)} 项 "
              f"(high={len(high)} mid={len(mid)} low={len(low)})")
        print(f"状态: {status}")
        for i in self.issues:
            print(f"  [{i['严重程度'].upper()}] {i['类别']}: {i['问题']}")
            print(f"      → {i['修正建议']}")
        if status == 'PASS':
            print('\n✅ 全部通过，可输出论文')
        return report


def main():
    if len(sys.argv) < 2:
        print('用法: python format_check.py <论文.md> [论文.tex]')
        sys.exit(2)
    md_path = Path(sys.argv[1])
    tex_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if not md_path.exists():
        print(f'错误：文件不存在 - {md_path}')
        sys.exit(1)
    md = md_path.read_text(encoding='utf-8', errors='replace')
    tex = tex_path.read_text(encoding='utf-8', errors='replace') if tex_path and tex_path.exists() else ''
    checker = PaperFormatChecker(md, tex, md_path=str(md_path))
    checker.run_all()


if __name__ == '__main__':
    main()
