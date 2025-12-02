#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整的GUI测试 - 模拟真实的查询流程
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
from bs4 import BeautifulSoup

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianyancha_treeview import TianyanchaAPI

def create_test_gui():
    """创建测试GUI"""
    
    root = tk.Tk()
    root.title("天眼查GUI测试 - 基础信息显示")
    root.geometry("1000x700")
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 配置网格权重
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(2, weight=1)
    
    # 标题
    title_label = ttk.Label(main_frame, text="天眼查基础信息显示测试", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, pady=(0, 10))
    
    # 状态标签
    status_label = ttk.Label(main_frame, text="准备就绪", foreground="blue")
    status_label.grid(row=1, column=0, pady=(0, 10))
    
    # 创建基础信息表格
    columns = ("字段", "值")
    basic_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=25)
    
    # 配置列
    basic_tree.heading("字段", text="字段")
    basic_tree.heading("值", text="值")
    basic_tree.column("字段", width=200, anchor="w")
    basic_tree.column("值", width=600, anchor="w")
    
    # 添加滚动条
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=basic_tree.yview)
    basic_tree.configure(yscrollcommand=scrollbar.set)
    
    # 布局
    basic_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
    
    def update_basic_info(basic_info):
        """更新基本信息表格 - 模拟tianyancha_treeview.py的逻辑"""
        # 清空现有数据
        for item in basic_tree.get_children():
            basic_tree.delete(item)

        if not basic_info:
            status_label.config(text="❌ 没有基础信息数据", foreground="red")
            return

        # 定义显示项目和对应的键名（与tianyancha_treeview.py完全一致）
        info_items = [
            ("🏢 公司名称", "公司名称"),
            ("🌐 英文名称", "英文名称"),
            ("📋 统一社会信用代码", "统一社会信用代码"),
            ("👤 法定代表人", "法定代表人"),
            ("💰 注册资本", "注册资本"),
            ("📅 成立日期", "成立日期"),
            ("✅ 经营状态", "经营状态"),
            ("📍 注册地址", "注册地址"),
            ("🏛️ 登记机关", "登记机关"),
            ("🏭 所属行业", "所属行业"),
            ("📊 企业规模", "企业规模"),
            ("👥 员工人数", "员工人数"),
            ("📞 联系电话", "联系电话"),
            ("📧 邮箱", "邮箱"),
            ("🌐 网址", "网址"),
            ("📝 经营范围", "经营范围")
        ]

        displayed_count = 0
        for display_name, key in info_items:
            value = basic_info.get(key, "")
            if value:  # 只显示有值的字段
                # 对于经营范围，如果太长则适当截断
                if key == "经营范围" and len(str(value)) > 300:
                    value = str(value)[:300] + "..."
                basic_tree.insert("", tk.END, values=(display_name, value))
                displayed_count += 1

        status_label.config(text=f"✅ 成功显示 {displayed_count} 个字段", foreground="green")
    
    def load_test_data():
        """加载测试数据"""
        try:
            status_label.config(text="🔍 正在加载测试数据...", foreground="orange")
            root.update()
            
            # 读取HTML文件
            html_file = "2320855868"
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 创建BeautifulSoup对象
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 创建API实例并提取信息
            default_cookies = "CUID=62b3804415cb2ef97572b27cdb7c519c; TYCID=e7f47650f4e911efa23e1f6dbaa18f88"
            api = TianyanchaAPI(default_cookies)
            
            status_label.config(text="🔍 正在提取基础信息...", foreground="orange")
            root.update()
            
            basic_info = api._extract_basic_info_from_html(soup)
            
            print(f"📊 提取到的基础信息:")
            for key, value in basic_info.items():
                print(f"  {key}: {value}")
            
            # 更新GUI显示
            update_basic_info(basic_info)
            
        except Exception as e:
            status_label.config(text=f"❌ 加载失败: {str(e)}", foreground="red")
            print(f"加载数据时出错: {e}")
            import traceback
            traceback.print_exc()
    
    # 添加测试按钮
    test_btn = ttk.Button(main_frame, text="加载测试数据", command=load_test_data)
    test_btn.grid(row=3, column=0, pady=(10, 0))
    
    # 自动加载数据
    root.after(500, load_test_data)
    
    return root

if __name__ == "__main__":
    print("🚀 启动完整GUI测试...")
    
    try:
        root = create_test_gui()
        print("✅ GUI创建成功，启动界面...")
        root.mainloop()
    except Exception as e:
        print(f"❌ GUI测试失败: {e}")
        import traceback
        traceback.print_exc()
