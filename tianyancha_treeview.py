#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天眼查GUI工具 - Treeview表格版本
使用真正的表格控件展示企业信息
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import json
import time
import re
import threading
import os
import pickle

# ==================== 原始GUI代码 (已注释) ====================
"""
原始的传统GUI实现已被注释，保留以供参考。
新的现代化GUI实现在下方的ModernTianyanchaGUI类中。

原始GUI特点：
- 使用传统的ttk样式
- 基础的颜色方案
- 标准的布局和组件
- 功能完整但界面较为朴素

如需恢复原始GUI，可以取消注释下方的TianyanchaTreeviewGUI类，
并在main函数中使用TianyanchaTreeviewGUI替代ModernTianyanchaGUI。
"""

# class TianyanchaTreeviewGUI:
#     """原始传统GUI类 - 已注释保留"""
#     def __init__(self, root):
#         pass  # 原始实现已注释

# ==================== 现代化GUI实现 ====================

class ModernTianyanchaGUI:
    """现代化的天眼查GUI - 清新简洁的设计风格"""

    def __init__(self, root):
        self.root = root
        self.root.title("🔍 天眼查企业信息查询工具 - 现代版 | Machy@HTSC")
        self.root.geometry("1500x950")

        # 设置现代化的颜色主题
        self.colors = {
            'primary': '#2563eb',      # 蓝色主色调
            'primary_light': '#3b82f6',
            'secondary': '#64748b',    # 灰蓝色
            'success': '#10b981',      # 绿色
            'warning': '#f59e0b',      # 橙色
            'danger': '#ef4444',       # 红色
            'background': '#f8fafc',   # 浅灰背景
            'surface': '#ffffff',      # 白色表面
            'text_primary': '#1e293b', # 深色文字
            'text_secondary': '#64748b', # 次要文字
            'border': '#e2e8f0',       # 边框色
            'hover': '#f1f5f9'         # 悬停色
        }

        # 配置现代化样式
        self.setup_modern_style()

        # 默认cookies - 更新为有效的cookies
        self.default_cookies = "CUID=fb5e88e52fd728716c8198eb6ba8ea2a; jsid=SEO-BING-ALL-SY-000001; TYCID=0abfc5307ad811f09f5f8b4d203646f6; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22237696749%22%2C%22first_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk4YjQ2MDUwMjExMzktMDY2Mzk3MzY0YTRlODU0LTI2MDExMDUxLTEzOTUzOTYtMTk4YjQ2MDUwMjI0NjUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIyMzc2OTY3NDkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22237696749%22%7D%2C%22%24device_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2215904922578%22%2C%22userId%22%3A%22237696749%22%7D; tyc-user-info-save-time=1756966779039; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTkwNDkyMjU3OCIsImlhdCI6MTc1Njk2Njc4MywiZXhwIjoxNzU5NTU4NzgzfQ.y0E08y-FkpMHgxVcdF3W0EQG3UQhZpW49DAScvqlgmhwVUgc8BSCQybsWEQ3OpCH1WpLzEp54zoRkjWLiYIYBw; ssuid=7644527464; bannerFlag=true; HWWAFSESID=42b601301cf9cc76a7a; HWWAFSESTIME=1757594260820; csrfToken=Axgtjv95gX1OwqzJf4s7gLbX"

        # 存储查询结果
        self.current_company_data = {}

        # 初始化cookies变量
        self.cookies_text = None

        # 配置文件路径
        self.config_file = "tianyancha_config.pkl"

        # 加载保存的配置
        self.load_config()

        # 如果没有保存的配置，使用默认值
        if not hasattr(self, 'current_auth_token') or not self.current_auth_token:
            self.current_auth_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTkwNDkyMjU3OCIsImlhdCI6MTc1NTM3NTI1MSwiZXhwIjoxNzU3OTY3MjUxfQ.1zIzw4KvTX6t1MovGzUrigh7pnZaEc708q1jyHOpGzLNfFiHl86P5DP0qxx5SJIC6qMHBRBo4ZG6Q-StF0BFoA"

        self.setup_ui()
        self.setup_shortcuts()

    def setup_modern_style(self):
        """设置现代化的样式主题"""
        style = ttk.Style()

        # 设置主题
        style.theme_use('clam')

        # 配置现代化的样式
        style.configure('Modern.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=0)

        style.configure('Header.TFrame',
                       background=self.colors['primary'],
                       relief='flat',
                       borderwidth=0)

        style.configure('Modern.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       font=('Microsoft YaHei', 10))

        style.configure('Header.TLabel',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Microsoft YaHei', 12, 'bold'))

        style.configure('Title.TLabel',
                       background=self.colors['surface'],
                       foreground=self.colors['primary'],
                       font=('Microsoft YaHei', 14, 'bold'))

        style.configure('Modern.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Microsoft YaHei', 10),
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 8))

        style.map('Modern.TButton',
                 background=[('active', self.colors['primary_light']),
                           ('pressed', self.colors['primary'])])

        style.configure('Secondary.TButton',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Microsoft YaHei', 10),
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(15, 6))

        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['surface'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       focuscolor=self.colors['primary'],
                       font=('Microsoft YaHei', 11),
                       padding=(12, 8))

        style.configure('Modern.Treeview',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['surface'],
                       borderwidth=1,
                       relief='solid',
                       font=('Microsoft YaHei', 10))

        style.configure('Modern.Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Microsoft YaHei', 10, 'bold'),
                       relief='flat',
                       borderwidth=0)

        style.map('Modern.Treeview',
                 background=[('selected', self.colors['primary_light'])],
                 foreground=[('selected', 'white')])

        style.configure('Modern.TNotebook',
                       background=self.colors['background'],
                       borderwidth=0,
                       tabmargins=[2, 2, 2, 0])

        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['surface'],
                       foreground=self.colors['text_primary'],
                       font=('Microsoft YaHei', 12),
                       padding=[25, 15],
                       borderwidth=1,
                       relief='solid')

        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['hover'])],
                 foreground=[('selected', 'white'),
                           ('active', self.colors['text_primary'])],
                 padding=[('selected', [30, 18]),
                         ('active', [25, 15])],
                 font=[('selected', ('Microsoft YaHei', 13, 'bold')),
                      ('active', ('Microsoft YaHei', 12))])

        # 设置根窗口背景
        self.root.configure(bg=self.colors['background'])

    def setup_ui(self):
        """设置现代化用户界面"""
        # 主容器 - 使用现代化样式
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # 顶部标题栏
        self.create_header(main_container)

        # 主内容区域
        content_frame = ttk.Frame(main_container, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # 查询区域
        self.create_search_section(content_frame)

        # 数据展示区域
        self.create_data_section(content_frame)

        # 底部状态栏
        self.create_status_bar(main_container)

    def create_header(self, parent):
        """创建现代化的头部区域"""
        header_frame = ttk.Frame(parent, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=0)

        # 左侧标题
        title_frame = ttk.Frame(header_frame, style='Header.TFrame')
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)

        title_label = ttk.Label(title_frame,
                               text="🔍 天眼查企业信息查询",
                               style='Header.TLabel')
        title_label.pack(side=tk.LEFT)

        subtitle_label = ttk.Label(title_frame,
                                  text="现代版 - 专业企业数据分析工具",
                                  font=('Microsoft YaHei', 10),
                                  foreground='#e2e8f0',
                                  background=self.colors['primary'])
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0))

        # 右侧作者信息
        author_frame = ttk.Frame(header_frame, style='Header.TFrame')
        author_frame.pack(side=tk.RIGHT, padx=20, pady=15)

        author_label = ttk.Label(author_frame,
                                text="Powered by Machy@HTSC",
                                font=('Microsoft YaHei', 9),
                                foreground='#cbd5e1',
                                background=self.colors['primary'])
        author_label.pack()

    def create_search_section(self, parent):
        """创建现代化的搜索区域"""
        search_frame = ttk.Frame(parent, style='Modern.TFrame')
        search_frame.pack(fill=tk.X, pady=(20, 25))

        # 搜索卡片
        search_card = ttk.Frame(search_frame, style='Modern.TFrame', relief='solid', borderwidth=1)
        search_card.pack(fill=tk.X, padx=10, pady=10)

        # 内部填充
        search_inner = ttk.Frame(search_card, style='Modern.TFrame')
        search_inner.pack(fill=tk.X, padx=25, pady=20)

        # 搜索标题
        search_title = ttk.Label(search_inner,
                                text="🏢 企业信息查询",
                                style='Title.TLabel')
        search_title.pack(anchor=tk.W, pady=(0, 15))

        # 搜索输入区域
        input_frame = ttk.Frame(search_inner, style='Modern.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 15))

        # 输入标签
        input_label = ttk.Label(input_frame,
                               text="企业名称",
                               style='Modern.TLabel',
                               font=('Microsoft YaHei', 11, 'bold'))
        input_label.pack(anchor=tk.W, pady=(0, 8))

        # 输入框和按钮容器
        input_container = ttk.Frame(input_frame, style='Modern.TFrame')
        input_container.pack(fill=tk.X)

        # 搜索输入框
        self.company_entry = ttk.Entry(input_container,
                                      style='Modern.TEntry',
                                      font=('Microsoft YaHei', 12),
                                      width=50)
        self.company_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))

        # 按钮组
        button_frame = ttk.Frame(input_container, style='Modern.TFrame')
        button_frame.pack(side=tk.RIGHT)

        # 查询按钮
        self.query_btn = ttk.Button(button_frame,
                                   text="🔍 开始查询",
                                   style='Modern.TButton',
                                   command=self.start_query)
        self.query_btn.pack(side=tk.LEFT, padx=(0, 10))

        # 配置按钮
        config_btn = ttk.Button(button_frame,
                               text="⚙️ 配置",
                               style='Secondary.TButton',
                               command=self.show_config)
        config_btn.pack(side=tk.LEFT)

    def create_data_section(self, parent):
        """创建数据展示区域"""
        # 数据容器
        data_frame = ttk.Frame(parent, style='Modern.TFrame')
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # 创建现代化的Notebook
        self.notebook = ttk.Notebook(data_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建各个标签页
        self.create_basic_info_tab()
        self.create_shareholders_tab()
        self.create_personnel_tab()
        self.create_financial_tab()
        self.create_investment_tab()

    def create_status_bar(self, parent):
        """创建现代化的状态栏"""
        status_frame = ttk.Frame(parent, style='Modern.TFrame', relief='solid', borderwidth=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # 内部容器
        status_inner = ttk.Frame(status_frame, style='Modern.TFrame')
        status_inner.pack(fill=tk.X, padx=20, pady=12)

        # 状态信息
        self.status_label = ttk.Label(status_inner,
                                     text="✅ 系统就绪",
                                     style='Modern.TLabel',
                                     font=('Microsoft YaHei', 10),
                                     foreground=self.colors['success'])
        self.status_label.pack(side=tk.LEFT)

        # 快捷键提示
        shortcut_text = "💡 快捷键: Enter-查询 | F1-配置 | 1-5-切换页面 | Ctrl+A-全选 | Ctrl+C-复制"
        shortcut_label = ttk.Label(status_inner,
                                  text=shortcut_text,
                                  style='Modern.TLabel',
                                  font=('Microsoft YaHei', 9),
                                  foreground=self.colors['text_secondary'])
        shortcut_label.pack(side=tk.RIGHT)

    def update_status(self, message, color="blue"):
        """更新现代化状态信息"""
        # 状态颜色映射
        color_map = {
            "blue": self.colors['primary'],
            "green": self.colors['success'],
            "orange": self.colors['warning'],
            "red": self.colors['danger'],
            "gray": self.colors['text_secondary']
        }

        # 状态图标映射
        icon_map = {
            "blue": "🔄",
            "green": "✅",
            "orange": "⚠️",
            "red": "❌",
            "gray": "ℹ️"
        }

        final_color = color_map.get(color, color)
        icon = icon_map.get(color, "ℹ️")

        self.status_label.config(text=f"{icon} {message}", foreground=final_color)

        # 3秒后恢复到就绪状态
        if color != "green" or "就绪" not in message:
            self.root.after(3000, lambda: self.status_label.config(
                text="✅ 系统就绪",
                foreground=self.colors['success']
            ))

    def create_basic_info_tab(self):
        """创建现代化的基本信息标签页"""
        basic_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(basic_frame, text="📋 基本信息")

        # 内容容器
        content_frame = ttk.Frame(basic_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(content_frame,
                               text="📋 企业基本信息",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        # 表格容器
        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建现代化的Treeview
        columns = ("项目", "内容")
        self.basic_tree = ttk.Treeview(table_frame,
                                      columns=columns,
                                      show="headings",
                                      height=20,
                                      selectmode="extended",
                                      style='Modern.Treeview')

        # 设置列标题
        self.basic_tree.heading("项目", text="信息项目")
        self.basic_tree.heading("内容", text="详细内容")

        # 设置列宽
        self.basic_tree.column("项目", width=220, minwidth=180)
        self.basic_tree.column("内容", width=800, minwidth=600)

        # 添加现代化滚动条
        basic_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.basic_tree.yview)
        self.basic_tree.configure(yscrollcommand=basic_scrollbar.set)

        # 布局
        self.basic_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        basic_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定事件
        self.basic_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.basic_tree))
        self.basic_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.basic_tree))
        self.basic_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.basic_tree))
        
    def create_shareholders_tab(self):
        """创建现代化的股东信息标签页"""
        shareholders_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(shareholders_frame, text="👥 股东信息")

        # 内容容器
        content_frame = ttk.Frame(shareholders_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(content_frame,
                               text="👥 股东持股信息",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        # 表格容器
        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建现代化的Treeview
        columns = ("序号", "股东名称", "持股比例", "认缴出资", "股东类型")
        self.shareholders_tree = ttk.Treeview(table_frame,
                                            columns=columns,
                                            show="headings",
                                            height=15,
                                            selectmode="extended",
                                            style='Modern.Treeview')

        # 设置列标题和宽度
        headers = {"序号": 80, "股东名称": 350, "持股比例": 140, "认缴出资": 180, "股东类型": 140}
        for col, width in headers.items():
            self.shareholders_tree.heading(col, text=col)
            self.shareholders_tree.column(col, width=width, minwidth=width-20)

        # 添加现代化滚动条
        shareholders_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.shareholders_tree.yview)
        self.shareholders_tree.configure(yscrollcommand=shareholders_scrollbar.set)

        # 布局
        self.shareholders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        shareholders_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定事件
        self.shareholders_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.shareholders_tree))
        self.shareholders_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.shareholders_tree))
        self.shareholders_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.shareholders_tree))
        self.shareholders_tree.bind("<Control-Button-1>", lambda e: self.ctrl_click_search(e, self.shareholders_tree, "股东名称"))
        
    def create_personnel_tab(self):
        """创建现代化的主要人员标签页"""
        personnel_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(personnel_frame, text="👤 主要人员")

        # 内容容器
        content_frame = ttk.Frame(personnel_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(content_frame,
                               text="👤 主要管理人员",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        # 表格容器
        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建现代化的Treeview
        columns = ("姓名", "职位", "详细信息")
        self.personnel_tree = ttk.Treeview(table_frame,
                                         columns=columns,
                                         show="headings",
                                         height=15,
                                         selectmode="extended",
                                         style='Modern.Treeview')

        # 设置列标题和宽度
        headers = {"姓名": 180, "职位": 250, "详细信息": 500}
        for col, width in headers.items():
            self.personnel_tree.heading(col, text=col)
            self.personnel_tree.column(col, width=width, minwidth=width-20)

        # 添加现代化滚动条
        personnel_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.personnel_tree.yview)
        self.personnel_tree.configure(yscrollcommand=personnel_scrollbar.set)

        # 布局
        self.personnel_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        personnel_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定事件
        self.personnel_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.personnel_tree))
        self.personnel_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.personnel_tree))
        self.personnel_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.personnel_tree))
        
    def create_financial_tab(self):
        """创建现代化的财务数据标签页"""
        financial_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(financial_frame, text="💰 财务数据")

        # 内容容器
        content_frame = ttk.Frame(financial_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(content_frame,
                               text="💰 财务数据分析",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        # 表格容器
        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建现代化的动态列Treeview
        self.financial_tree = ttk.Treeview(table_frame,
                                         show="headings",
                                         height=15,
                                         selectmode="extended",
                                         style='Modern.Treeview')

        # 添加现代化滚动条
        financial_scrollbar_v = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.financial_tree.yview)
        financial_scrollbar_h = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.financial_tree.xview)
        self.financial_tree.configure(yscrollcommand=financial_scrollbar_v.set, xscrollcommand=financial_scrollbar_h.set)

        # 布局
        self.financial_tree.grid(row=0, column=0, sticky="nsew")
        financial_scrollbar_v.grid(row=0, column=1, sticky="ns")
        financial_scrollbar_h.grid(row=1, column=0, sticky="ew")

        # 配置grid权重
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # 绑定事件
        self.financial_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.financial_tree))
        self.financial_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.financial_tree))
        self.financial_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.financial_tree))

    def create_investment_tab(self):
        """创建现代化的对外投资标签页"""
        investment_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(investment_frame, text="💼 对外投资")

        # 内容容器
        content_frame = ttk.Frame(investment_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        title_label = ttk.Label(content_frame,
                               text="� 对外投资信息",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        # 表格容器
        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 创建现代化的Treeview
        columns = ("序号", "被投资企业名称", "投资比例", "投资金额", "成立日期", "注册状态", "法定代表人", "所在地区")
        self.investment_tree = ttk.Treeview(table_frame,
                                          columns=columns,
                                          show="headings",
                                          height=15,
                                          selectmode="extended",
                                          style='Modern.Treeview')

        # 设置列标题和宽度
        headers = {
            "序号": 80,
            "被投资企业名称": 280,
            "投资比例": 120,
            "投资金额": 140,
            "成立日期": 120,
            "注册状态": 100,
            "法定代表人": 140,
            "所在地区": 180
        }
        for col, width in headers.items():
            self.investment_tree.heading(col, text=col)
            self.investment_tree.column(col, width=width, minwidth=width-20)

        # 添加现代化滚动条
        investment_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.investment_tree.yview)
        self.investment_tree.configure(yscrollcommand=investment_scrollbar.set)

        # 布局
        self.investment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        investment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 绑定事件
        self.investment_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.investment_tree))
        self.investment_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.investment_tree))
        self.investment_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.investment_tree))
        self.investment_tree.bind("<Control-Button-1>", lambda e: self.ctrl_click_search(e, self.investment_tree, "被投资企业名称"))
        
    # ==================== 原始方法实现 (已注释保留) ====================
    # 以下是原始GUI的所有方法实现，已注释保留以供参考
    # 现代化GUI继承了所有这些方法的功能，但使用了更现代的样式

    def show_context_menu(self, event, tree):
        """显示右键菜单"""
        # 检查点击的项目
        item = tree.identify_row(event.y)

        # 只有在点击的项目没有被选中时，才重新选择
        # 这样可以保持多行选择状态
        if item and item not in tree.selection():
            tree.selection_set(item)

        # 创建右键菜单
        context_menu = tk.Menu(self.root, tearoff=0)

        # 根据选择状态显示不同的菜单项
        selection = tree.selection()
        if selection:
            if len(selection) == 1:
                context_menu.add_command(label="📋 复制选中行（Word格式）", command=lambda: self.copy_for_word(tree))
                context_menu.add_command(label="📊 复制选中行（Excel格式）", command=lambda: self.copy_for_excel(tree))
            else:
                context_menu.add_command(label=f"📋 复制{len(selection)}行（Word格式）", command=lambda: self.copy_for_word(tree))
                context_menu.add_command(label=f"📊 复制{len(selection)}行（Excel格式）", command=lambda: self.copy_for_excel(tree))

        context_menu.add_separator()
        context_menu.add_command(label="🔍 全选", command=lambda: tree.selection_set(tree.get_children()))
        context_menu.add_command(label="❌ 取消选择", command=lambda: tree.selection_remove(tree.selection()))

        # 显示菜单
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
                
    def copy_selected(self, tree):
        """复制选中的单元格内容"""
        selection = tree.selection()
        if selection:
            item = selection[0]
            # 获取当前焦点列
            focus_column = tree.focus_get()
            if hasattr(tree, 'identify_column'):
                col = tree.identify_column(tree.winfo_pointerx() - tree.winfo_rootx())
                if col:
                    col_index = int(col.replace('#', '')) - 1
                    values = tree.item(item)['values']
                    if col_index < len(values):
                        self.root.clipboard_clear()
                        self.root.clipboard_append(str(values[col_index]))
                        self.update_status("已复制到剪贴板")
                        
    def copy_row(self, tree):
        """复制整行内容"""
        selection = tree.selection()
        if selection:
            item = selection[0]
            values = tree.item(item)['values']
            row_text = '\t'.join(str(v) for v in values)
            self.root.clipboard_clear()
            self.root.clipboard_append(row_text)
            self.update_status("已复制整行到剪贴板")
            
    def copy_for_word(self, tree):
        """复制为Word友好格式（表格格式）"""
        selection = tree.selection()
        if not selection:
            self.update_status("请先选择要复制的行", "orange")
            return

        try:
            copied_data = []

            # 获取列标题和列宽信息
            columns = tree['columns']
            if columns:
                headers = []
                col_widths = []
                for col in columns:
                    header_text = tree.heading(col)['text']
                    headers.append(header_text)
                    # 估算列宽（中文字符按2个字符宽度计算）
                    width = max(len(header_text), 8)  # 最小宽度8
                    col_widths.append(width)

                # 检查数据行，调整列宽
                for item in selection[:5]:  # 只检查前5行来估算宽度
                    values = tree.item(item, 'values')
                    for i, v in enumerate(values):
                        if i < len(col_widths):
                            str_v = str(v) if v else '-'
                            # 计算显示宽度（中文字符宽度x2）
                            display_width = sum(2 if ord(c) > 127 else 1 for c in str_v)
                            col_widths[i] = max(col_widths[i], min(display_width, 20))  # 最大宽度20

                # 创建表格分隔线
                separator = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'

                # 添加表格标题
                copied_data.append(separator)
                header_row = '|'
                for i, header in enumerate(headers):
                    padded_header = f" {header:<{col_widths[i]}} "
                    header_row += padded_header + '|'
                copied_data.append(header_row)
                copied_data.append(separator)

            # 获取选中行的数据，格式化为表格
            for item in selection:
                values = tree.item(item, 'values')
                row = '|'
                for i, v in enumerate(values):
                    if i < len(col_widths):
                        str_v = str(v).strip() if v else '-'
                        # 处理特殊字符
                        str_v = str_v.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                        # 限制长度
                        if len(str_v) > col_widths[i]:
                            str_v = str_v[:col_widths[i]-3] + '...'
                        padded_value = f" {str_v:<{col_widths[i]}} "
                        row += padded_value + '|'
                copied_data.append(row)

            # 添加底部分隔线
            if columns:
                copied_data.append(separator)

            if copied_data:
                clipboard_text = '\n'.join(copied_data)
                self.root.clipboard_clear()
                self.root.clipboard_append(clipboard_text)
                data_rows = len(selection)
                self.update_status(f"已复制 {data_rows} 行数据（Word表格格式），粘贴到Word后选中文本转换为表格", "green")

        except Exception as e:
            self.update_status(f"复制失败: {str(e)}", "red")

    def copy_for_excel(self, tree):
        """复制为Excel友好格式"""
        selection = tree.selection()
        if not selection:
            self.update_status("请先选择要复制的行", "orange")
            return

        try:
            copied_data = []

            # 获取列标题
            columns = tree['columns']
            if columns:
                headers = []
                for col in columns:
                    headers.append(tree.heading(col)['text'])
                copied_data.append('\t'.join(headers))

            # 获取选中行的数据，优化Excel显示
            for item in selection:
                values = tree.item(item, 'values')
                processed_values = []
                for v in values:
                    if v is None or v == '':
                        processed_values.append('')
                    else:
                        str_v = str(v)
                        # Excel格式：如果包含特殊字符，用引号包围
                        if '\t' in str_v or '\n' in str_v or '"' in str_v:
                            str_v = '"' + str_v.replace('"', '""') + '"'
                        processed_values.append(str_v)
                copied_data.append('\t'.join(processed_values))

            if copied_data:
                clipboard_text = '\n'.join(copied_data)
                self.root.clipboard_clear()
                self.root.clipboard_append(clipboard_text)
                data_rows = len(copied_data) - 1
                self.update_status(f"已复制 {data_rows} 行数据（Excel格式），可直接粘贴到Excel", "green")

        except Exception as e:
            self.update_status(f"复制失败: {str(e)}", "red")

    def export_to_excel(self):
        """导出数据到Excel"""
        # TODO: 实现Excel导出功能
        messagebox.showinfo("提示", "Excel导出功能开发中...")
        
    def setup_shortcuts(self):
        """设置快捷键"""
        self.company_entry.bind('<Return>', lambda event: self.start_query())
        self.root.bind('<F1>', lambda event: self.show_config())
        self.root.bind('<Control-q>', lambda event: self.root.quit())

        # 数字键1-5快速切换标签页
        self.root.bind('<Key-1>', lambda event: self.switch_to_tab(0))
        self.root.bind('<Key-2>', lambda event: self.switch_to_tab(1))
        self.root.bind('<Key-3>', lambda event: self.switch_to_tab(2))
        self.root.bind('<Key-4>', lambda event: self.switch_to_tab(3))
        self.root.bind('<Key-5>', lambda event: self.switch_to_tab(4))

        # ESC键退出
        self.root.bind('<Escape>', lambda event: self.root.quit())

        # 为所有Treeview添加Ctrl+A全选功能
        self.root.bind('<Control-a>', lambda event: self.select_all_in_current_tab(event))

    def switch_to_tab(self, tab_index):
        """切换到指定标签页"""
        try:
            if tab_index < self.notebook.index("end"):
                self.notebook.select(tab_index)
                tab_names = ["基本信息", "股东信息", "主要人员", "财务数据", "对外投资"]
                if tab_index < len(tab_names):
                    self.update_status(f"已切换到: {tab_names[tab_index]}", "green")
        except Exception as e:
            pass

    def select_all_in_current_tab(self, event):
        """在当前标签页中全选所有行"""
        try:
            # 获取当前活动的标签页
            current_tab = self.notebook.select()
            tab_text = self.notebook.tab(current_tab, "text")

            # 根据标签页确定对应的Treeview
            if "基本信息" in tab_text:
                tree = self.basic_tree
            elif "股东信息" in tab_text:
                tree = self.shareholders_tree
            elif "主要人员" in tab_text:
                tree = self.personnel_tree
            elif "财务数据" in tab_text:
                tree = self.financial_tree
            elif "对外投资" in tab_text:
                tree = self.investment_tree
            else:
                return

            # 全选当前Treeview的所有行
            tree.selection_set(tree.get_children())
            self.update_status(f"已全选 {len(tree.get_children())} 行数据", "green")

        except Exception as e:
            self.update_status(f"全选失败: {str(e)}", "red")

    def ctrl_click_search(self, event, tree, target_column):
        """Ctrl+点击搜索企业名称"""
        try:
            # 获取点击的项目
            item = tree.identify_row(event.y)
            if not item:
                return

            # 获取该行的数据
            values = tree.item(item, 'values')
            if not values:
                return

            # 根据不同的表格确定企业名称的位置
            company_name = ""
            if target_column == "股东名称":
                # 股东信息表格：股东名称在第2列（索引1）
                if len(values) > 1:
                    company_name = str(values[1]).strip()
            elif target_column == "被投资企业名称":
                # 对外投资表格：被投资企业名称在第2列（索引1）
                if len(values) > 1:
                    company_name = str(values[1]).strip()

            if company_name and company_name != "-" and company_name != "":
                # 更新搜索框
                self.company_entry.delete(0, tk.END)
                self.company_entry.insert(0, company_name)

                # 开始搜索
                self.update_status(f"正在搜索: {company_name}", "blue")
                self.start_query()
            else:
                self.update_status("未找到有效的企业名称", "orange")

        except Exception as e:
            self.update_status(f"搜索失败: {str(e)}", "red")

    def load_config(self):
        """加载保存的配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'rb') as f:
                    config = pickle.load(f)
                    self.default_cookies = config.get('cookies', self.default_cookies)
                    self.current_auth_token = config.get('auth_token', '')
                    print(f"已加载配置文件: {self.config_file}")
        except Exception as e:
            print(f"加载配置失败: {str(e)}")

    def save_config_to_file(self):
        """保存配置到文件"""
        try:
            config = {
                'cookies': self.default_cookies,
                'auth_token': getattr(self, 'current_auth_token', '')
            }
            with open(self.config_file, 'wb') as f:
                pickle.dump(config, f)
            print(f"配置已保存到: {self.config_file}")
        except Exception as e:
            print(f"保存配置失败: {str(e)}")

    def copy_cell_on_double_click(self, event, tree):
        """双击复制单元格内容"""
        try:
            # 获取点击位置的项目和列
            item = tree.identify_row(event.y)
            column = tree.identify_column(event.x)

            if item and column:
                # 获取列索引
                col_index = int(column.replace('#', '')) - 1
                if col_index >= 0:
                    # 获取该行的值
                    values = tree.item(item, 'values')
                    if col_index < len(values):
                        cell_value = str(values[col_index])
                        # 复制到剪贴板
                        self.root.clipboard_clear()
                        self.root.clipboard_append(cell_value)
                        self.update_status(f"已复制: {cell_value[:50]}{'...' if len(cell_value) > 50 else ''}", "green")
        except Exception as e:
            self.update_status(f"复制失败: {str(e)}", "red")

    def copy_selected_cells(self, event, tree):
        """Ctrl+C复制选中的行（支持多行选择，格式适合Word/Excel）"""
        try:
            selection = tree.selection()
            if selection:
                copied_data = []

                # 获取列标题
                columns = tree['columns']
                if columns:
                    headers = []
                    for col in columns:
                        headers.append(tree.heading(col)['text'])
                    copied_data.append('\t'.join(headers))

                # 获取选中行的数据
                for item in selection:
                    values = tree.item(item, 'values')
                    # 处理空值和特殊字符，优化Word显示
                    processed_values = []
                    for v in values:
                        if v is None or v == '':
                            processed_values.append('-')  # 空值用-表示，在Word中更清晰
                        else:
                            str_v = str(v).strip()  # 去除首尾空格
                            # 替换可能影响格式的字符
                            str_v = str_v.replace('\n', ' ').replace('\r', ' ')  # 换行符替换为空格
                            str_v = str_v.replace('\t', ' ')  # 制表符替换为空格
                            processed_values.append(str_v)
                    copied_data.append('\t'.join(processed_values))

                if copied_data:
                    clipboard_text = '\n'.join(copied_data)
                    self.root.clipboard_clear()
                    self.root.clipboard_append(clipboard_text)

                    # 显示更详细的复制信息
                    data_rows = len(copied_data) - 1  # 减去标题行
                    if data_rows > 0:
                        self.update_status(f"已复制 {data_rows} 行数据（含标题），可粘贴到Word/Excel", "green")
                    else:
                        self.update_status("已复制标题行", "green")
        except Exception as e:
            self.update_status(f"复制失败: {str(e)}", "red")

    def show_config(self):
        """显示配置窗口"""
        config_window = tk.Toplevel(self.root)
        config_window.title("配置设置")
        config_window.geometry("700x500")
        config_window.transient(self.root)
        config_window.grab_set()

        # Cookies配置
        ttk.Label(config_window, text="Cookies配置:").pack(anchor=tk.W, padx=10, pady=(10, 5))

        cookies_frame = ttk.Frame(config_window)
        cookies_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.cookies_text = tk.Text(cookies_frame, height=10, wrap=tk.WORD)
        cookies_scrollbar = ttk.Scrollbar(cookies_frame, orient=tk.VERTICAL, command=self.cookies_text.yview)
        self.cookies_text.configure(yscrollcommand=cookies_scrollbar.set)

        self.cookies_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cookies_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 设置默认cookies
        self.cookies_text.insert(tk.END, self.default_cookies)

        # Auth Token配置
        ttk.Label(config_window, text="Auth Token配置 (用于对外投资等高级功能):").pack(anchor=tk.W, padx=10, pady=(10, 5))

        token_frame = ttk.Frame(config_window)
        token_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.auth_token_text = tk.Text(token_frame, height=4, wrap=tk.WORD)
        token_scrollbar = ttk.Scrollbar(token_frame, orient=tk.VERTICAL, command=self.auth_token_text.yview)
        self.auth_token_text.configure(yscrollcommand=token_scrollbar.set)

        self.auth_token_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        token_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 设置默认auth token（如果有的话）
        if hasattr(self, 'current_auth_token') and self.current_auth_token:
            self.auth_token_text.insert(tk.END, self.current_auth_token)

        # 按钮框架
        btn_frame = ttk.Frame(config_window)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(btn_frame, text="保存", command=lambda: self.save_config(config_window)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="取消", command=config_window.destroy).pack(side=tk.RIGHT)
        
    def save_config(self, window):
        """保存配置"""
        if self.cookies_text:
            self.default_cookies = self.cookies_text.get("1.0", tk.END).strip()
        if hasattr(self, 'auth_token_text') and self.auth_token_text:
            self.current_auth_token = self.auth_token_text.get("1.0", tk.END).strip()

        # 保存到文件
        self.save_config_to_file()

        window.destroy()
        self.update_status("配置已保存并同步到本地", "green")
        
    def update_status(self, message, color="blue"):
        """更新状态信息"""
        self.status_label.config(text=message, foreground=color)
        self.root.after(3000, lambda: self.status_label.config(text="就绪", foreground="green"))
        
    def get_current_cookies(self):
        """获取当前的cookies"""
        if self.cookies_text and hasattr(self.cookies_text, 'get'):
            return self.cookies_text.get(1.0, tk.END).strip()
        else:
            return self.default_cookies

    def start_query(self):
        """开始查询"""
        company_name = self.company_entry.get().strip()
        if not company_name:
            messagebox.showwarning("警告", "请输入企业名称")
            return

        # 禁用查询按钮
        self.query_btn.config(state='disabled')
        self.update_status("正在查询...", "orange")

        # 在新线程中执行查询
        thread = threading.Thread(target=self.query_company, args=(company_name,))
        thread.daemon = True
        thread.start()

    def query_company(self, company_name):
        """查询企业信息"""
        try:
            # 获取当前cookies和auth token
            cookies = self.get_current_cookies()
            auth_token = getattr(self, 'current_auth_token', '') if hasattr(self, 'current_auth_token') else ''

            # 创建API客户端
            api = TianyanchaAPI(cookies, auth_token)

            # 搜索企业
            search_result = api.search_company(company_name)
            if not search_result:
                self.root.after(0, lambda: self.update_status("未找到企业信息", "red"))
                return

            gid = search_result.get('gid')
            if not gid:
                self.root.after(0, lambda: self.update_status("获取企业ID失败", "red"))
                return

            # 获取详细信息
            print(f"🔍 开始获取详细信息，gid: {gid}")
            basic_info = api.get_basic_info(gid)
            print(f"📊 获取到basic_info: {basic_info}")
            print(f"📊 basic_info类型: {type(basic_info)}, 长度: {len(basic_info) if basic_info else 0}")

            shareholders = api.get_shareholders(gid)
            personnel = api.get_key_personnel(gid)
            financial = api.get_financial_data(gid)
            investments = api.get_investment_info(gid)

            # 更新界面
            print(f"🎯 准备更新界面...")
            self.root.after(0, lambda: self.update_display(basic_info, shareholders, personnel, financial, investments))

        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"查询失败: {str(e)}", "red"))
        finally:
            self.root.after(0, lambda: self.query_btn.config(state='normal'))

    def update_display(self, basic_info, shareholders, personnel, financial, investments):
        """更新显示内容"""
        print(f"🎯 update_display 被调用")
        print(f"🎯 basic_info参数: {basic_info}")

        # 更新基本信息
        self.update_basic_info(basic_info)

        # 更新股东信息
        self.update_shareholders(shareholders)

        # 更新人员信息
        self.update_personnel(personnel)

        # 更新财务数据
        self.update_financial(financial)

        # 更新对外投资
        self.update_investments(investments)

        self.update_status("查询完成", "green")

    def update_basic_info(self, basic_info):
        """更新基本信息表格"""
        print(f"🎯 update_basic_info 被调用，basic_info类型: {type(basic_info)}")
        print(f"🎯 basic_info内容: {basic_info}")

        # 清空现有数据
        for item in self.basic_tree.get_children():
            self.basic_tree.delete(item)

        if not basic_info:
            print("❌ basic_info为空，直接返回")
            return

        print(f"✅ basic_info有数据，包含 {len(basic_info)} 个字段")

        # 定义显示项目和对应的键名
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
            ("🌐 网址", "网址"),  # 添加网址字段
            ("📝 经营范围", "经营范围")
        ]

        for display_name, key in info_items:
            value = basic_info.get(key, "")
            if value:  # 只显示有值的字段
                # 对于经营范围，如果太长则适当截断
                if key == "经营范围" and len(str(value)) > 300:
                    value = str(value)[:300] + "..."
                self.basic_tree.insert("", tk.END, values=(display_name, value))

    def update_shareholders(self, shareholders):
        """更新股东信息表格"""
        # 清空现有数据
        for item in self.shareholders_tree.get_children():
            self.shareholders_tree.delete(item)

        if not shareholders:
            return

        for i, shareholder in enumerate(shareholders, 1):
            values = (
                i,
                shareholder.get('name', ''),
                shareholder.get('ratio', ''),
                shareholder.get('capital', ''),
                shareholder.get('type', '')
            )
            self.shareholders_tree.insert("", tk.END, values=values)

    def update_personnel(self, personnel):
        """更新人员信息表格"""
        # 清空现有数据
        for item in self.personnel_tree.get_children():
            self.personnel_tree.delete(item)

        if not personnel:
            return

        for person in personnel:
            values = (
                person.get('name', ''),
                person.get('position', ''),
                person.get('details', '')
            )
            self.personnel_tree.insert("", tk.END, values=values)

    def update_financial(self, financial):
        """更新财务数据表格 - 显示所有财务指标"""
        # 清空现有数据
        for item in self.financial_tree.get_children():
            self.financial_tree.delete(item)

        if not financial:
            return

        # 如果financial是原始API数据格式
        if isinstance(financial, dict) and 'titleList' in financial:
            title_list = financial.get('titleList', [])
            attr_list = financial.get('attrList', [])
            column_list = financial.get('columnList', [])

            if not title_list or not attr_list or not column_list:
                return

            # 动态设置列 - 财务指标名称 + 各个报告期
            columns = ['财务指标'] + title_list[:8]  # 最多显示8个报告期
            self.financial_tree['columns'] = columns
            self.financial_tree['show'] = 'headings'

            # 设置列标题和宽度
            self.financial_tree.heading('财务指标', text='财务指标')
            self.financial_tree.column('财务指标', width=200, minwidth=150)

            for title in title_list[:8]:
                self.financial_tree.heading(title, text=title)
                self.financial_tree.column(title, width=120, minwidth=100)

            # 添加所有财务指标数据
            for i, attr in enumerate(attr_list):
                attr_name = attr.get('name', '')
                if not attr_name:
                    continue

                # 构建该指标在各个报告期的数据
                row_values = [attr_name]

                for j, column in enumerate(column_list[:8]):  # 最多8个报告期
                    value_list = column.get('valueList', [])
                    if i < len(value_list):
                        value = value_list[i]
                        row_values.append(str(value) if value and value != "" else "-")
                    else:
                        row_values.append("-")

                self.financial_tree.insert("", tk.END, values=row_values)
        else:
            # 如果是处理过的简化格式（向后兼容）
            columns = ("报告期", "营业收入", "净利润", "总资产", "净资产", "资产负债率")
            self.financial_tree['columns'] = columns
            self.financial_tree['show'] = 'headings'

            for col in columns:
                self.financial_tree.heading(col, text=col)
                self.financial_tree.column(col, width=150, minwidth=120)

            for data in financial:
                values = (
                    data.get('period', ''),
                    data.get('revenue', ''),
                    data.get('profit', ''),
                    data.get('total_assets', ''),
                    data.get('net_assets', ''),
                    data.get('debt_ratio', '')
                )
                self.financial_tree.insert("", tk.END, values=values)

    def update_investments(self, investments):
        """更新对外投资表格"""
        # 清空现有数据
        for item in self.investment_tree.get_children():
            self.investment_tree.delete(item)

        if not investments:
            return

        for i, investment in enumerate(investments, 1):
            values = (
                i,
                investment.get('被投资企业名称', ''),
                investment.get('投资比例', ''),
                investment.get('投资金额', ''),
                investment.get('成立日期', ''),
                investment.get('注册状态', ''),
                investment.get('法定代表人', ''),
                investment.get('所在地区', '')
            )
            self.investment_tree.insert("", tk.END, values=values)

# TianyanchaAPI 类将在文件末尾定义


class TianyanchaAPI:
    def __init__(self, cookies, auth_token=None):
        """初始化API客户端"""
        self.session = requests.Session()
        self.cookies = cookies
        self.auth_token = auth_token

        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6",
            "connection": "keep-alive",
            "content-type": "application/json",
            "cookie": cookies,
            "host": "capi.tianyancha.com",
            "origin": "https://www.tianyancha.com",
            "referer": "https://www.tianyancha.com/",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "version": "TYC-Web",
            "x-tycid": "0abfc5307ad811f09f5f8b4d203646f6"
        }

        # 如果有auth token，添加到headers中
        if auth_token:
            self.base_headers["x-auth-token"] = auth_token

    def search_company(self, company_name):
        """搜索公司获取基本信息"""
        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/cloud-tempest/search/suggest/company/main?_={timestamp}"

        payload = {"keyword": company_name}

        try:
            response = self.session.post(url, json=payload, headers=self.base_headers, timeout=10)

            if response.status_code == 200:
                result = response.json()

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    company_list = data.get('companySuggestList', [])

                    if company_list:
                        first_company = company_list[0]
                        search_info = {
                            'gid': str(first_company.get('id', '')),
                            'graphId': str(first_company.get('graphId', '')),
                            'name': first_company.get('comName', ''),
                            'alias': first_company.get('alias', ''),
                            'taxCode': first_company.get('taxCode', ''),
                            'regStatus': first_company.get('regStatus', 0)
                        }
                        return search_info
            return None
        except Exception as e:
            return None

    def get_basic_info(self, gid):
        """获取基本信息"""
        try:
            url = f"https://www.tianyancha.com/company/{gid}"
            print(f"🔍 正在获取基本信息: {url}")

            # 设置访问网页的headers，包含cookies
            web_headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6",
                "cache-control": "no-cache",
                "connection": "keep-alive",
                "cookie": self.cookies,
                "host": "www.tianyancha.com",
                "pragma": "no-cache",
                "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            }

            response = self.session.get(url, headers=web_headers, timeout=10)
            print(f"📡 HTTP状态码: {response.status_code}")

            if response.status_code == 200:
                # 保存HTML文件用于调试
                html_filename = f"debug_company_{gid}.html"
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"💾 已保存HTML文件: {html_filename}")

                soup = BeautifulSoup(response.text, 'html.parser')
                basic_info = self._extract_basic_info_from_html(soup)
                print(f"📊 提取到基本信息字段数量: {len(basic_info)}")
                for key, value in basic_info.items():
                    print(f"   {key}: {value}")
                return basic_info
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"❌ 响应内容: {response.text[:500]}")
            return {}
        except Exception as e:
            print(f"❌ 获取基本信息失败: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def _extract_basic_info_from_html(self, soup):
        """从HTML中提取基本信息 - 优化版本"""
        info = {}

        try:
            print("🔍 开始提取基本信息...")

            # 1. 公司名称
            name_elem = soup.find('h1', class_='index_company-name__LqKlo')
            if name_elem:
                name_span = name_elem.find('span', class_='index_name__dz4jY')
                if name_span:
                    info['公司名称'] = name_span.get_text(strip=True)
                    print(f"✅ 公司名称: {info['公司名称']}")

            # 如果上面没找到，尝试其他选择器
            if '公司名称' not in info:
                name_elem = soup.find('h1')
                if name_elem:
                    info['公司名称'] = name_elem.get_text(strip=True)
                    print(f"✅ 公司名称(备用): {info['公司名称']}")

            # 2. 统一社会信用代码
            credit_code_elem = soup.find('span', class_='index_detail-credit-code__fH1Ny')
            if credit_code_elem:
                code_span = credit_code_elem.find('span')
                if code_span:
                    info['统一社会信用代码'] = code_span.get_text(strip=True)
                    print(f"✅ 统一社会信用代码: {info['统一社会信用代码']}")

            # 3. 法定代表人
            legal_person_elem = soup.find('div', class_='index_legal-person-root__THrdz')
            if legal_person_elem:
                link_elem = legal_person_elem.find('a', class_='index_link-click__NmHxP')
                if link_elem:
                    info['法定代表人'] = link_elem.get_text(strip=True)
                    print(f"✅ 法定代表人: {info['法定代表人']}")

            # 4. 经营状态
            status_elem = soup.find('div', class_='index_company-tag__ZcJFV index_header-company-tag__WaTgu')
            if status_elem:
                info['经营状态'] = status_elem.get_text(strip=True)
                print(f"✅ 经营状态: {info['经营状态']}")
            else:
                # 尝试其他选择器
                status_elem = soup.find('div', class_='index_reg-status-tag__ES7dF')
                if status_elem:
                    tag_elem = status_elem.find('div', class_='index_company-tag__ZcJFV')
                    if tag_elem:
                        info['经营状态'] = tag_elem.get_text(strip=True)
                        print(f"✅ 经营状态(备用): {info['经营状态']}")

            # 5. 详细信息项提取
            print("📊 开始提取详细信息项...")
            detail_items = soup.find_all('div', class_='index_detail-info-item__oAOqL')
            print(f"找到 {len(detail_items)} 个详细信息项")

            for item in detail_items:
                label_elem = item.find('span', class_='index_detail-label__oRf2J')
                if label_elem:
                    label_text = label_elem.get_text(strip=True)

                    if '注册资本' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['注册资本'] = value_elem.get_text(strip=True)
                            print(f"✅ 注册资本: {info['注册资本']}")

                    elif '成立日期' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['成立日期'] = value_elem.get_text(strip=True)
                            print(f"✅ 成立日期: {info['成立日期']}")

                    elif '电话' in label_text:
                        # 电话的新选择器
                        tel_elem = item.find('span', class_='index_detail-tel__fgpsE')
                        if tel_elem:
                            info['联系电话'] = tel_elem.get_text(strip=True)
                            print(f"✅ 联系电话: {info['联系电话']}")
                        else:
                            # 备用选择器
                            value_elem = item.find('span', class_='link-hover-click')
                            if value_elem:
                                info['联系电话'] = value_elem.get_text(strip=True)
                                print(f"✅ 联系电话(备用): {info['联系电话']}")

                    elif '邮箱' in label_text:
                        email_elem = item.find('a', class_='index_detail-email__B_1Tq')
                        if email_elem:
                            info['邮箱'] = email_elem.get_text(strip=True)
                            print(f"✅ 邮箱: {info['邮箱']}")

                    elif '网址' in label_text:
                        website_elem = item.find('a', class_='index_detail-website__n2yst')
                        if website_elem:
                            info['网址'] = website_elem.get_text(strip=True)
                            print(f"✅ 网址: {info['网址']}")

                    elif '地址' in label_text:
                        # 地址提取的优化逻辑
                        address_elem = item.find('span', class_='index_detail-address-moretext__9R_Z1')
                        if address_elem:
                            address_span = address_elem.find('span', class_='index_inline-flex__QLDiW')
                            if address_span:
                                info['注册地址'] = address_span.get_text(strip=True)
                                print(f"✅ 注册地址: {info['注册地址']}")
                        else:
                            # 备用选择器
                            address_elem = item.find('span', class_='index_inline-flex__QLDiW')
                            if address_elem:
                                address_text = address_elem.get_text(strip=True)
                                # 过滤掉标签文本
                                if address_text and '地址：' not in address_text and len(address_text) > 10:
                                    info['注册地址'] = address_text
                                    print(f"✅ 注册地址(备用): {info['注册地址']}")

                    elif '国标行业' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['所属行业'] = value_elem.get_text(strip=True)
                            print(f"✅ 所属行业: {info['所属行业']}")

                    elif '企业规模' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['企业规模'] = value_elem.get_text(strip=True)
                            print(f"✅ 企业规模: {info['企业规模']}")

                    elif '员工人数' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['员工人数'] = value_elem.get_text(strip=True)
                            print(f"✅ 员工人数: {info['员工人数']}")

            # 6. 从表格中提取更多信息（经营范围、英文名称、登记机关等）
            print("📋 开始从表格提取更多信息...")
            business_scope = None

            table_rows = soup.find_all('tr')
            for row in table_rows:
                cells = row.find_all('td')
                for i, cell in enumerate(cells):
                    cell_text = cell.get_text(strip=True)

                    if '经营范围' in cell_text and i + 1 < len(cells):
                        scope_cell = cells[i + 1]
                        copy_text_elem = scope_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            business_scope = copy_text_elem.get_text(strip=True)
                            print(f"✅ 经营范围: {business_scope[:100]}...")
                        else:
                            # 尝试直接获取单元格文本
                            scope_text = scope_cell.get_text(strip=True)
                            if scope_text and len(scope_text) > 20:
                                business_scope = scope_text
                                print(f"✅ 经营范围(备用): {business_scope[:100]}...")

                    elif '注册地址' in cell_text and i + 1 < len(cells) and '注册地址' not in info:
                        addr_cell = cells[i + 1]
                        copy_text_elem = addr_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['注册地址'] = copy_text_elem.get_text(strip=True)
                            print(f"✅ 注册地址(表格): {info['注册地址']}")
                        else:
                            addr_text = addr_cell.get_text(strip=True)
                            if addr_text and len(addr_text) > 10:
                                info['注册地址'] = addr_text
                                print(f"✅ 注册地址(表格备用): {info['注册地址']}")

                    elif '英文名称' in cell_text and i + 1 < len(cells):
                        en_cell = cells[i + 1]
                        copy_text_elem = en_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['英文名称'] = copy_text_elem.get_text(strip=True)
                            print(f"✅ 英文名称: {info['英文名称']}")
                        else:
                            en_text = en_cell.get_text(strip=True)
                            if en_text and len(en_text) > 5:
                                info['英文名称'] = en_text
                                print(f"✅ 英文名称(备用): {info['英文名称']}")

                    elif '登记机关' in cell_text and i + 1 < len(cells):
                        reg_cell = cells[i + 1]
                        copy_text_elem = reg_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['登记机关'] = copy_text_elem.get_text(strip=True)
                            print(f"✅ 登记机关: {info['登记机关']}")
                        else:
                            reg_text = reg_cell.get_text(strip=True)
                            if reg_text and len(reg_text) > 5:
                                info['登记机关'] = reg_text
                                print(f"✅ 登记机关(备用): {info['登记机关']}")

            # 7. 如果经营范围还没找到，尝试其他方法
            if not business_scope:
                print("🔍 尝试其他方法提取经营范围...")

                # 方法1：查找简介中的经营范围
                intro_elem = soup.find('div', class_='introduceRich_collapse-left__5Vvd5')
                if intro_elem:
                    intro_text = intro_elem.get_text(strip=True)
                    if len(intro_text) > 100:  # 简介通常比较长
                        business_scope = intro_text
                        print(f"✅ 经营范围(简介): {business_scope[:100]}...")

                # 方法2：查找其他可能的选择器
                if not business_scope:
                    scope_elems = soup.find_all('div', string=re.compile(r'经营范围'))
                    for elem in scope_elems:
                        parent = elem.parent
                        if parent:
                            text_elem = parent.find_next('span') or parent.find_next('div')
                            if text_elem:
                                scope_text = text_elem.get_text(strip=True)
                                if len(scope_text) > 50:
                                    business_scope = scope_text
                                    print(f"✅ 经营范围(其他): {business_scope[:100]}...")
                                    break

            if business_scope:
                info['经营范围'] = business_scope

            # 8. 输出提取结果汇总
            print(f"\n📊 提取完成，共获得 {len(info)} 个字段:")
            for key, value in info.items():
                if key == '经营范围' and len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:100]}...")
                else:
                    print(f"  {key}: {value}")

            return info

        except Exception as e:
            print(f"❌ HTML解析错误: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def get_shareholders(self, gid):
        """获取股东信息"""
        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/cloud-company-background/companyV2/dim/holder/latest/announcement?_={timestamp}"

        payload = {
            "benefitSharesType": 1,
            "gid": gid,
            "historyType": None,
            "keyword": "",
            "pageNum": 1,
            "pageSize": 50,
            "percentLevel": "-100",
            "_unUseParam": 0
        }

        try:
            response = self.session.post(url, json=payload, headers=self.base_headers, timeout=10)
            print(f"股东信息请求状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"股东信息响应状态: {result.get('state')}")

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    holders = data.get('result', [])

                    shareholders = []
                    for holder in holders:
                        shareholder_name = holder.get('shareHolderName', '') or holder.get('name', '')
                        percent = holder.get('percent', '')
                        total_capital = holder.get('totalCapital', '') or holder.get('amount', '')
                        shareholder_type = holder.get('shareHolderTypeOnPage', '')

                        # 处理持股比例，避免重复添加%符号
                        if percent:
                            if isinstance(percent, str) and percent.endswith('%'):
                                ratio_display = percent
                            else:
                                ratio_display = f"{percent}%"
                        else:
                            ratio_display = ''

                        shareholder = {
                            'name': shareholder_name,
                            'ratio': ratio_display,
                            'capital': total_capital,
                            'type': shareholder_type
                        }
                        shareholders.append(shareholder)

                    print(f"解析到股东数量: {len(shareholders)}")
                    return shareholders
                else:
                    print(f"股东信息API返回错误: {result.get('message', '未知错误')}")
            else:
                print(f"股东信息HTTP请求失败: {response.status_code}")
            return []
        except Exception as e:
            print(f"获取股东信息失败: {e}")
            return []

    def get_key_personnel(self, gid):
        """获取主要人员信息"""
        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/cloud-company-background/company/dim/staff/announcement?_={timestamp}&gid={gid}&pageSize=20&pageNum=1&stockType=0"

        try:
            response = self.session.get(url, headers=self.base_headers, timeout=10)
            print(f"主要人员请求状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"主要人员响应状态: {result.get('state')}")

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    staff_list = data.get('result', [])

                    personnel = []
                    for staff in staff_list:
                        name = staff.get('name', '') or staff.get('personName', '')
                        position = staff.get('typeJoin', '') or staff.get('position', '')
                        staff_type = staff.get('type', '')

                        person_info = {
                            'name': name,
                            'position': position,
                            'details': f"类型: {staff_type}" if staff_type else ''
                        }
                        personnel.append(person_info)

                    print(f"解析到人员数量: {len(personnel)}")
                    return personnel
                else:
                    print(f"主要人员API返回错误: {result.get('message', '未知错误')}")
            else:
                print(f"主要人员HTTP请求失败: {response.status_code}")
            return []
        except Exception as e:
            print(f"主要人员查询异常: {str(e)}")
            return []

    def get_financial_data(self, gid):
        """获取上市公司财务数据"""
        try:
            timestamp = int(time.time() * 1000)
            url = f"https://capi.tianyancha.com/cloud-newdim/listedCompany/financial/listV2?_={timestamp}"

            data = {
                "gid": gid,
                "timeType": "QUARTER",
                "dataType": "FINANCIAL",
                "companyType": "A",
                "codeType": "HB",
                "amountUnit": 0,
                "decimal": 2,
                "hideLine": False,
                "quarterList": [5, 4],
                "showBasis": False,
                "timeSort": 0
            }

            response = self.session.post(url, json=data, headers=self.base_headers, timeout=10)
            print(f"财务数据请求状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"财务数据响应状态: {result.get('state')}")

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    print(f"获取到财务数据: {len(data.get('columnList', []))}个报告期")

                    # 获取财务数据结构
                    title_list = data.get('titleList', [])
                    attr_list = data.get('attrList', [])
                    column_list = data.get('columnList', [])

                    print(f"标题数量: {len(title_list)}, 指标数量: {len(attr_list)}, 列数量: {len(column_list)}")

                    # 直接返回原始数据，让update_financial方法处理显示
                    return data
                else:
                    print(f"财务数据API返回错误: {result.get('message', '未知错误')}")
                    return []
            else:
                print(f"财务数据HTTP请求失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"财务数据查询异常: {str(e)}")
            return []

    def get_investment_info(self, gid):
        """获取对外投资信息"""
        try:
            timestamp = int(time.time() * 1000)
            url = f"https://capi.tianyancha.com/cloud-company-background/company/investListV2?_={timestamp}"

            payload = {
                "gid": gid,
                "pageSize": 10,
                "pageNum": 1,
                "benefitSharesType": 1
            }

            response = self.session.post(url, json=payload, headers=self.base_headers, timeout=10)
            print(f"对外投资请求状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"对外投资响应状态: {result.get('state')}")

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    investments = []

                    for item in data.get('result', []):
                        # 处理成立日期（从时间戳转换为日期）
                        establish_time = item.get('estiblishTime', '')
                        if establish_time and isinstance(establish_time, (int, float)):
                            try:
                                import datetime
                                establish_date = datetime.datetime.fromtimestamp(establish_time / 1000).strftime('%Y-%m-%d')
                            except:
                                establish_date = str(establish_time)
                        else:
                            establish_date = str(establish_time) if establish_time else ''

                        investment = {
                            '被投资企业名称': item.get('name', ''),
                            '投资比例': item.get('percent', ''),
                            '投资金额': item.get('amount', ''),
                            '成立日期': establish_date,
                            '注册状态': item.get('regStatus', ''),
                            '法定代表人': item.get('legalPersonName', ''),
                            '所在地区': item.get('region', '')
                        }
                        investments.append(investment)

                    print(f"解析到投资数量: {len(investments)}")
                    return investments
                else:
                    print(f"对外投资API返回错误: {result.get('message', '未知错误')}")
            else:
                print(f"对外投资HTTP请求失败: {response.status_code}")
            return []
        except Exception as e:
            print(f"对外投资查询异常: {str(e)}")
            return []

if __name__ == "__main__":
    root = tk.Tk()
    # 使用现代化GUI
    app = ModernTianyanchaGUI(root)
    # 如需使用原始GUI，请取消注释下行并注释上行
    # app = TianyanchaTreeviewGUI(root)
    root.mainloop()
