#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从穿透报告(txt)中解析“完整穿透结构”并生成股权穿透图。
特性：
- 白色背景，宋体（SimSun），直角连接线
- 持股比例标注在线上
- 处理一个股东持有多个主体（同名节点去重复用）
使用：
  python equity_graph_from_report.py --input tianyancha_penetration_*.txt --output equity_structure
"""

import re
import os
import argparse
from collections import defaultdict
import graphviz

FONT_NAME = "SimSun"  # 宋体

# 需要剔除的公司后缀（尾部匹配，包含常见合伙/有限公司/股份有限公司等）
SUFFIXES_TO_REMOVE = [
    "（有限合伙）合伙企业","（有限合伙）","投资合伙企业（有限合伙）","创业投资合伙企业（有限合伙）",
    "股权投资合伙企业（有限合伙）","投资管理合伙企业（有限合伙）","资产管理合伙企业（有限合伙）",
    "合伙企业（有限合伙）","投资合伙企业","创业投资合伙企业","股权投资合伙企业","投资管理合伙企业",
    "资产管理合伙企业","合伙企业",
    # 有限公司/股份有限公司及其常见组合
    "集团股份有限公司","控股股份有限公司","投资股份有限公司","实业股份有限公司","贸易股份有限公司",
    "科技股份有限公司","发展股份有限公司","建设股份有限公司","工程股份有限公司","咨询股份有限公司",
    "服务股份有限公司","管理股份有限公司","置业股份有限公司","地产股份有限公司","房地产股份有限公司",
    "物业股份有限公司","教育股份有限公司","文化股份有限公司","传媒股份有限公司","广告股份有限公司",
    "设计股份有限公司","装饰股份有限公司","建筑股份有限公司","制造股份有限公司","生产股份有限公司",
    "加工股份有限公司","销售股份有限公司","经营股份有限公司","运营股份有限公司","物流股份有限公司",
    "运输股份有限公司","仓储股份有限公司","电子股份有限公司","网络股份有限公司","信息股份有限公司",
    "数据股份有限公司","软件股份有限公司","技术股份有限公司","研发股份有限公司","创新股份有限公司",
    "智能股份有限公司","自动化股份有限公司","机械股份有限公司","设备股份有限公司","器械股份有限公司",
    "仪器股份有限公司","材料股份有限公司","化工股份有限公司","医药股份有限公司","生物股份有限公司",
    "环保股份有限公司","能源股份有限公司","电力股份有限公司","水务股份有限公司","燃气股份有限公司",
    "供热股份有限公司","交通股份有限公司","航空股份有限公司","海运股份有限公司","港口股份有限公司",
    "码头股份有限公司","船务股份有限公司","货运股份有限公司","快递股份有限公司","邮政股份有限公司",
    "通信股份有限公司","电信股份有限公司","移动股份有限公司","联通股份有限公司","广播股份有限公司",
    "电视股份有限公司","影视股份有限公司","娱乐股份有限公司","体育股份有限公司","健身股份有限公司",
    "旅游股份有限公司","酒店股份有限公司","餐饮股份有限公司","食品股份有限公司","饮料股份有限公司",
    "农业股份有限公司","林业股份有限公司","渔业股份有限公司","畜牧股份有限公司","种植股份有限公司",
    "养殖股份有限公司","园艺股份有限公司","花卉股份有限公司","苗木股份有限公司","果业股份有限公司",
    "粮油股份有限公司","副食股份有限公司","商贸股份有限公司","百货股份有限公司","超市股份有限公司",
    "连锁股份有限公司","零售股份有限公司","批发股份有限公司","代理股份有限公司","经销股份有限公司",
    "分销股份有限公司","配送股份有限公司","供应股份有限公司","采购股份有限公司","进出口股份有限公司",
    "外贸股份有限公司","国际股份有限公司",
    # 有限公司系列
    "股份有限公司","有限责任公司","集团有限公司","控股有限公司","投资有限公司","实业有限公司",
    "贸易有限公司","科技有限公司","发展有限公司","建设有限公司","工程有限公司","咨询有限公司",
    "服务有限公司","管理有限公司","置业有限公司","地产有限公司","房地产有限公司","物业有限公司",
    "教育有限公司","文化有限公司","传媒有限公司","广告有限公司","设计有限公司","装饰有限公司",
    "建筑有限公司","制造有限公司","生产有限公司","加工有限公司","销售有限公司","经营有限公司",
    "运营有限公司","物流有限公司","运输有限公司","仓储有限公司","电子有限公司","网络有限公司",
    "信息有限公司","数据有限公司","软件有限公司","技术有限公司","研发有限公司","创新有限公司",
    "智能有限公司","自动化有限公司","机械有限公司","设备有限公司","器械有限公司","仪器有限公司",
    "材料有限公司","化工有限公司","医药有限公司","生物有限公司","环保有限公司","能源有限公司",
    "电力有限公司","水务有限公司","燃气有限公司","供热有限公司","交通有限公司","航空有限公司",
    "海运有限公司","港口有限公司","码头有限公司","船务有限公司","货运有限公司","快递有限公司",
    "邮政有限公司","通信有限公司","电信有限公司","移动有限公司","联通有限公司","广播有限公司",
    "电视有限公司","影视有限公司","娱乐有限公司","体育有限公司","健身有限公司","旅游有限公司",
    "酒店有限公司","餐饮有限公司","食品有限公司","饮料有限公司","农业有限公司","林业有限公司",
    "渔业有限公司","畜牧有限公司","种植有限公司","养殖有限公司","园艺有限公司","花卉有限公司",
    "苗木有限公司","果业有限公司","粮油有限公司","副食有限公司","商贸有限公司","百货有限公司",
    "超市有限公司","连锁有限公司","零售有限公司","批发有限公司","代理有限公司","经销有限公司",
    "分销有限公司","配送有限公司","供应有限公司","采购有限公司","进出口有限公司","外贸有限公司",
    # 常见城市/地域字样保留，由业务自行选择是否裁剪
]

def normalize_company_name(name: str) -> str:
    """规范化公司名称：去除常见后缀（仅裁剪末尾出现的后缀）。"""
    if not name:
        return name
    s = name.strip()
    # 反复裁剪，直到不再变化
    changed = True
    while changed:
        changed = False
        for suf in SUFFIXES_TO_REMOVE:
            if s.endswith(suf):
                s = s[: -len(suf)].rstrip()
                changed = True
                break
        # 去掉尾部成对空括号
        s = re.sub(r"[（\(]\s*[）\)]$", "", s).strip()
    return s


def parse_structure_from_report(path):
    """解析报告txt中的“完整穿透结构”部分，返回根公司名与边列表。
    边：[(上级, 下级, 比例文本)]
    """
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 定位“完整穿透结构:”段落
    m = re.search(r"🌳 完整穿透结构:\s*(.+)$", text, re.S)
    if not m:
        raise ValueError("未找到 '完整穿透结构' 段落")
    block = m.group(1).strip()

    lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]

    # 识别每行的缩进级别与实体+比例
    # 行示例：
    # "🏢 重庆博奥实业（集团）有限公司 (14.0082%, 实际14.01%)"
    # "👤 汪武扬 (95.0%, 实际13.17%)"
    node_stack = []  # [(level, name)]
    edges = []       # (parent, child, label)
    root = None

    def level_of(line):
        # 两空格为一个层级
        leading = len(line) - len(line.lstrip(' '))
        return leading // 2

    def extract_name_ratio(line):
        # 去除前导空格与图标
        s = line.lstrip()
        s = re.sub(r"^[🏢👤]\s*", "", s)
        # 名称与括号中的 declared 百分比
        name_part = re.sub(r"\([^()]*%[^()]*\)\s*$", "", s).strip()
        name_part = normalize_company_name(name_part)
        ratio_m = re.search(r"\(([^()]*?)\)$", s)
        label = ""
        if ratio_m:
            label = ratio_m.group(1)
            # 只取声明比例（第一个百分数）
            pct_m = re.search(r"([0-9]+(?:\.[0-9]+)?)%", label)
            if pct_m:
                label = pct_m.group(1) + "%"
        return name_part, label

    for ln in lines:
        lvl = level_of(ln)
        name, pct = extract_name_ratio(ln)
        if root is None:
            root = name
        # 维护栈到同级
        while node_stack and node_stack[-1][0] >= lvl:
            node_stack.pop()
        # 若栈有父，则连边
        if node_stack:
            parent = node_stack[-1][1]
            edges.append((parent, name, pct))
        node_stack.append((lvl, name))

    return root, edges


def build_graph(root, edges, output_basename, fmt="svg", avoid_overlap=True, ranksep=1.0, nodesep=0.6, concentrate=False):
    g_attrs = {
        'rankdir': 'TB',
        'splines': 'ortho',
        'bgcolor': 'white',
        'ranksep': str(ranksep),
        'nodesep': str(nodesep),
        'concentrate': 'true' if concentrate else 'false'
    }
    if avoid_overlap:
        g_attrs['overlap'] = 'false'
        g_attrs['pack'] = 'true'
        g_attrs['packmode'] = 'node'

    dot = graphviz.Digraph(
        'EquityGraph',
        graph_attr=g_attrs,
        node_attr={'fontname': FONT_NAME, 'shape': 'box', 'style': 'rounded'},
        # 使用 xlabel 居中标注比例，避免折线导致的偏移；适当加大最小边长
        edge_attr={'fontname': FONT_NAME, 'labelfontname': FONT_NAME, 'labelfontsize': '10', 'labelfloat': 'true', 'minlen': '2'}
    )

    # 去重节点
    seen_nodes = set()
    def add_node(n):
        if n in seen_nodes:
            return
        seen_nodes.add(n)
        dot.node(n, n)

    add_node(root)
    for u, v, lbl in edges:
        add_node(u)
        add_node(v)
        # 反向连边：股东(上层 v) 指向 被投(下层 u / 根方向)，箭头向下指向目标公司
        # 用 xlabel 让比例文本尽量居中贴近边
        if lbl:
            dot.edge(v, u, xlabel=f" {lbl} ")
        else:
            dot.edge(v, u)

    # 输出为指定格式（svg 适合 PPT 矢量）
    out = dot.render(output_basename, format=fmt, view=False, cleanup=True)
    print(f"✅ 已生成: {out}")


def main():
    parser = argparse.ArgumentParser(description='从穿透报告生成股权穿透图')
    parser.add_argument('--input', '-i', required=True, help='穿透报告txt路径')
    parser.add_argument('--output', '-o', default='equity_structure', help='输出文件基名(不含扩展名)')
    parser.add_argument('--format', '-f', default='svg', choices=['svg','png'], help='输出格式，默认 svg')
    parser.add_argument('--no-overlap', dest='avoid_overlap', action='store_true', default=True,
                       help='尽量避免节点/边遮挡（默认开启）')
    parser.add_argument('--allow-overlap', dest='avoid_overlap', action='store_false',
                       help='允许重叠（更紧凑）')
    parser.add_argument('--ranksep', type=float, default=1.0, help='层级间距，默认 1.0')
    parser.add_argument('--nodesep', type=float, default=0.6, help='同层节点间距，默认 0.6')
    parser.add_argument('--concentrate', action='store_true', help='合并平行边，降低线条杂乱（可能影响标签位置）')
    args = parser.parse_args()

    root, edges = parse_structure_from_report(args.input)
    build_graph(
        root, edges, args.output, fmt=args.format,
        avoid_overlap=args.avoid_overlap, ranksep=args.ranksep, nodesep=args.nodesep,
        concentrate=args.concentrate
    )


if __name__ == '__main__':
    main()


