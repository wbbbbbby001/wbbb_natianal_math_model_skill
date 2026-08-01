"""
==========================================
wbbb_math_skill 代码可运行性验证脚本
用法：
  python verify_code.py [code目录]
  示例: python verify_code.py code
流程：
  1) 语法编译检查（py_compile）—— 硬门禁，任一失败即 FAIL
  2) import 冒烟测试 —— 软门禁，报告每个模块能否导入
  3) 可选：运行 main_solver.py（超时 90s）
输出：PASS / FAIL + 详细报告
==========================================
"""
import os
import py_compile
import subprocess
import sys
from pathlib import Path


def find_py_files(code_dir: Path):
    return sorted(p for p in code_dir.rglob('*.py') if '__pycache__' not in str(p))


def syntax_check(py_files):
    """硬门禁：所有 .py 语法编译通过。"""
    failures = []
    for f in py_files:
        try:
            py_compile.compile(str(f), doraise=True)
        except py_compile.PyCompileError as e:
            failures.append((f, str(e)))
    return failures


def import_smoke(code_dir: Path, py_files):
    """软门禁：每个顶层模块尝试 import。"""
    python = sys.executable
    results = []
    for f in py_files:
        if f.name == '__init__.py':
            continue
        mod = f.stem
        try:
            r = subprocess.run(
                [python, '-c', f'import {mod}'],
                cwd=str(code_dir), capture_output=True, text=True, timeout=60,
            )
            if r.returncode == 0:
                results.append((mod, 'OK', ''))
            else:
                tail = (r.stderr or r.stdout or '').strip().splitlines()
                err = tail[-1] if tail else 'unknown error'
                results.append((mod, 'FAIL', err))
        except subprocess.TimeoutExpired:
            results.append((mod, 'TIMEOUT', 'import 超时 60s'))
    return results


def run_main(code_dir: Path):
    """可选：运行 main_solver.py。"""
    main = code_dir / 'main_solver.py'
    if not main.exists():
        return None
    python = sys.executable
    try:
        r = subprocess.run(
            [python, 'main_solver.py'], cwd=str(code_dir),
            capture_output=True, text=True, timeout=90,
        )
        if r.returncode == 0:
            return ('OK', '')
        tail = (r.stderr or r.stdout or '').strip().splitlines()
        return ('FAIL', tail[-1] if tail else 'exit != 0')
    except subprocess.TimeoutExpired:
        return ('TIMEOUT', 'main_solver 运行超时 90s')


def main():
    code_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('code')
    if not code_dir.exists():
        print(f'错误：目录不存在 - {code_dir}')
        sys.exit(2)

    print('=' * 60)
    print(f'代码可运行性验证：{code_dir}')
    print('=' * 60)

    py_files = find_py_files(code_dir)
    if not py_files:
        print('未找到 .py 文件')
        sys.exit(2)
    print(f'发现 {len(py_files)} 个 .py 文件\n')

    # 1) 语法硬门禁
    print('[1/3] 语法编译检查（硬门禁）...')
    failures = syntax_check(py_files)
    if failures:
        print(f'  ✗ {len(failures)} 个文件语法错误：')
        for f, e in failures:
            print(f'    - {f.name}: {e}')
        print('\n状态: FAIL（语法错误，必须先修复）')
        sys.exit(1)
    print('  ✓ 全部语法通过')

    # 2) import 冒烟
    print('\n[2/3] import 冒烟测试（软门禁）...')
    smoke = import_smoke(code_dir, py_files)
    ok = sum(1 for _, s, _ in smoke if s == 'OK')
    for mod, s, err in smoke:
        print(f'  {"✓" if s == "OK" else "✗"} {mod}: {s}' + (f' — {err[:120]}' if s != 'OK' else ''))
    print(f'  import 通过 {ok}/{len(smoke)}')

    # 3) 运行 main_solver
    print('\n[3/3] main_solver.py 运行...')
    run = run_main(code_dir)
    if run is None:
        print('  - 未找到 main_solver.py，跳过')
        final_ok = ok == len(smoke)
    else:
        s, err = run
        print(f'  {"✓ 运行成功" if s == "OK" else "✗ " + s} ' + (f'— {err[:200]}' if s != 'OK' else ''))
        final_ok = s == 'OK' and ok == len(smoke)

    print('\n' + '=' * 60)
    print(f'状态: {"PASS" if final_ok else "FAIL（存在不可导入模块，检查依赖/路径）"}')
    print('=' * 60)
    sys.exit(0 if final_ok else 1)


if __name__ == '__main__':
    main()
