#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试GUI界面显示
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianyancha_complete_api import TianyanchaAPI
from bs4 import BeautifulSoup

def create_test_gui():
    """创建测试GUI界面"""
    
    root = tk.Tk()
    root.title("天眼查信息提取测试")
    root.geometry("800x600")
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 配置网格权重
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    
    # 标题
    title_label = ttk.Label(main_frame, text="天眼查基础信息提取测试", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, pady=(0, 10))
    
    # 创建Treeview表格
    columns = ("字段", "值")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
    
    # 配置列
    tree.heading("字段", text="字段")
    tree.heading("值", text="值")
    tree.column("字段", width=150, anchor="w")
    tree.column("值", width=500, anchor="w")
    
    # 添加滚动条
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # 布局
    tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
    
    # 状态标签
    status_label = ttk.Label(main_frame, text="正在加载数据...", foreground="blue")
    status_label.grid(row=2, column=0, pady=(10, 0))
    
    def load_data():
        """加载测试数据"""
        try:
            # 读取HTML文件
            html_file = "2320855868"
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 创建BeautifulSoup对象
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 创建API实例并提取信息
            api = TianyanchaAPI()
            basic_info = api._extract_basic_info_from_html(soup)
            
            # 清空现有数据
            for item in tree.get_children():
                tree.delete(item)
            
            # 添加数据到表格
            if basic_info:
                for key, value in basic_info.items():
                    # 如果值太长，截断显示
                    display_value = str(value)
                    if len(display_value) > 100:
                        display_value = display_value[:100] + "..."
                    
                    tree.insert("", tk.END, values=(key, display_value))
                
                status_label.config(text=f"✅ 成功加载 {len(basic_info)} 个字段", foreground="green")
            else:
                status_label.config(text="❌ 未能提取到数据", foreground="red")
                
        except Exception as e:
            status_label.config(text=f"❌ 加载失败: {str(e)}", foreground="red")
            print(f"加载数据时出错: {e}")
            import traceback
            traceback.print_exc()
    
    # 延迟加载数据
    root.after(100, load_data)
    
    return root

if __name__ == "__main__":
    print("🧪 启动GUI测试...")
    
    try:
        root = create_test_gui()
        print("✅ GUI创建成功，启动界面...")
        root.mainloop()
    except Exception as e:
        print(f"❌ GUI测试失败: {e}")
        import traceback
        traceback.print_exc()
