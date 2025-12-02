#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流：全层股东穿透 → 生成股权穿透图
1) 使用 tianyancha_penetration_api.TianyanchaPenetrationAPI 做“所有层级股东”穿透
2) 解析生成的报告文本，绘制完整股权穿透图（股东 → 目标公司），文件名用公司名称

用法：
  python workflow_generate_equity_graph.py "公司名称" --format svg
  python workflow_generate_equity_graph.py --input companies.txt --format svg
  直接运行进入交互模式，逐行输入公司名
"""

import argparse
import re
import os
import graphviz

from tianyancha_penetration_api import TianyanchaPenetrationAPI
from equity_graph_from_report import parse_structure_from_report, build_graph

FONT_NAME = "SimSun"  # 宋体


def sanitize_filename(name: str) -> str:
    s = re.sub(r"[\\/:*?\"<>|]+", "_", name)
    s = s.strip().rstrip('.')
    return s or "equity_structure"


SUFFIXES_TO_REMOVE = [
    "（有限合伙）合伙企业","（有限合伙）","投资合伙企业（有限合伙）","创业投资合伙企业（有限合伙）",
    "股权投资合伙企业（有限合伙）","投资管理合伙企业（有限合伙）","资产管理合伙企业（有限合伙）",
    "合伙企业（有限合伙）","投资合伙企业","创业投资合伙企业","股权投资合伙企业","投资管理合伙企业",
    "资产管理合伙企业","合伙企业","股份有限公司","有限责任公司","有限公司","集团有限公司","控股有限公司"
]


def normalize_company_name(name: str) -> str:
    if not name:
        return name
    s = name.strip()
    changed = True
    while changed:
        changed = False
        for suf in SUFFIXES_TO_REMOVE:
            if s.endswith(suf):
                s = s[: -len(suf)].rstrip()
                changed = True
                break
        s = re.sub(r"[（\(]\s*[）\)]$", "", s).strip()
    return s


def run_for_company(api: TianyanchaPenetrationAPI, company_name: str, fmt: str):
    # 全层穿透
    report = api.penetrate_shareholders(company_name, max_depth=None)
    if not report:
        print(f"❌ 穿透失败: {company_name}")
        return
    # 保存报告，得到txt路径
    json_file, txt_file = api.save_penetration_report(report, company_name)
    # 解析“完整穿透结构”并绘图
    root, edges = parse_structure_from_report(txt_file)
    out_name = sanitize_filename(normalize_company_name(root))
    build_graph(root, edges, out_name, fmt=fmt)


def main():
    parser = argparse.ArgumentParser(description='工作流：全层股东穿透并生成股权穿透图')
    parser.add_argument('company', nargs='?', help='公司名称（单个）')
    parser.add_argument('--input', '-i', help='批量公司文件（UTF-8，每行一个公司名）')
    parser.add_argument('--format', '-f', default='svg', choices=['svg','png'], help='输出格式，默认 svg')
    args = parser.parse_args()

    api = TianyanchaPenetrationAPI()

    targets = []
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            targets = [ln.strip() for ln in f if ln.strip()]
    elif args.company:
        targets = [args.company]
    else:
        print("请输入公司名称（可多行，每行一个；直接回车结束）：")
        targets = []
        try:
            while True:
                line = input().strip()
                if not line:
                    break
                targets.append(line)
        except EOFError:
            pass
        if not targets:
            print("未输入公司名称，已退出。")
            return

    for company in targets:
        run_for_company(api, company, fmt=args.format)


if __name__ == '__main__':
    main()


