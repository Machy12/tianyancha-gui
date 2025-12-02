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
import ctypes

# DPI高分屏适配
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass


class ModernTianyanchaGUI:
    """现代化的天眼查GUI - 清新简洁的设计风格"""

    def __init__(self, root):
        self.root = root
        self.root.title("天眼查企业信息查询工具 | Machy@HTSC")
        self.root.geometry("1600x1000")
        self.root.state('zoomed')

        # 设置现代化的颜色主题
        self.colors = {
            'primary': '#2563eb',
            'primary_light': '#3b82f6',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'text_primary': '#1e293b',
            'text_secondary': '#64748b',
            'border': '#e2e8f0',
            'hover': '#f1f5f9'
        }

        # 配置现代化样式
        self.setup_modern_style()

        # 默认cookies
        self.default_cookies = ""
        self.current_company_data = {}
        self.cookies_text = None
        self.config_file = "tianyancha_config.pkl"
        
        # 查询历史和候选企业
        self.query_history = []
        self.current_query_index = -1
        self.candidate_companies = []

        # 加载保存的配置
        self.load_config()

        if not hasattr(self, 'current_auth_token'):
            self.current_auth_token = ""

        self.setup_ui()
        self.setup_shortcuts()

    def setup_modern_style(self):
        """设置现代化的样式主题"""
        style = ttk.Style()
        style.theme_use('clam')

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
                       font=('Microsoft YaHei', 10),
                       rowheight=28)

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

        self.root.configure(bg=self.colors['background'])

    def setup_ui(self):
        """设置现代化用户界面"""
        main_container = ttk.Frame(self.root, style='Modern.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.create_header(main_container)

        content_frame = ttk.Frame(main_container, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.create_search_section(content_frame)
        self.create_data_section(content_frame)
        self.create_status_bar(main_container)

    def create_header(self, parent):
        """创建现代化的头部区域"""
        header_frame = ttk.Frame(parent, style='Header.TFrame')
        header_frame.pack(fill=tk.X, pady=0)

        title_frame = ttk.Frame(header_frame, style='Header.TFrame')
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)

        title_label = ttk.Label(title_frame,
                               text="🔍 天眼查企业信息查询",
                               style='Header.TLabel')
        title_label.pack(side=tk.LEFT)

        subtitle_label = ttk.Label(title_frame,
                                  text="专业企业数据分析工具",
                                  font=('Microsoft YaHei', 10),
                                  foreground='#e2e8f0',
                                  background=self.colors['primary'])
        subtitle_label.pack(side=tk.LEFT, padx=(15, 0))

        # 快捷键提示
        shortcut_frame = ttk.Frame(header_frame, style='Header.TFrame')
        shortcut_frame.pack(side=tk.LEFT, padx=(30, 0), pady=15)
        
        shortcut_text = "快捷键: Enter搜索 | ↓进入列表 | 双击/Enter查询 | Alt+←返回 | 1-5切换页 | Ctrl+C复制"
        shortcut_label = ttk.Label(shortcut_frame,
                                  text=shortcut_text,
                                  font=('Microsoft YaHei', 9),
                                  foreground='#cbd5e1',
                                  background=self.colors['primary'])
        shortcut_label.pack()

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
        search_frame.pack(fill=tk.X, pady=(20, 15))

        search_card = ttk.Frame(search_frame, style='Modern.TFrame', relief='solid', borderwidth=1)
        search_card.pack(fill=tk.X, padx=10, pady=10)

        search_inner = ttk.Frame(search_card, style='Modern.TFrame')
        search_inner.pack(fill=tk.X, padx=25, pady=20)

        search_title = ttk.Label(search_inner,
                                text="🏢 企业信息查询",
                                style='Title.TLabel')
        search_title.pack(anchor=tk.W, pady=(0, 15))

        input_frame = ttk.Frame(search_inner, style='Modern.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 15))

        input_label = ttk.Label(input_frame,
                               text="企业名称",
                               style='Modern.TLabel',
                               font=('Microsoft YaHei', 11, 'bold'))
        input_label.pack(anchor=tk.W, pady=(0, 8))

        input_container = ttk.Frame(input_frame, style='Modern.TFrame')
        input_container.pack(fill=tk.X)

        self.company_entry = ttk.Entry(input_container,
                                      style='Modern.TEntry',
                                      font=('Microsoft YaHei', 12),
                                      width=50)
        self.company_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))

        button_frame = ttk.Frame(input_container, style='Modern.TFrame')
        button_frame.pack(side=tk.RIGHT)

        self.query_btn = ttk.Button(button_frame,
                                   text="🔍 搜索企业",
                                   style='Modern.TButton',
                                   command=self.search_companies)
        self.query_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.back_btn = ttk.Button(button_frame,
                                  text="⬅ 返回",
                                  style='Secondary.TButton',
                                  command=self.go_back_query)
        self.back_btn.pack(side=tk.LEFT, padx=(0, 10))

        config_btn = ttk.Button(button_frame,
                               text="⚙️ 配置",
                               style='Secondary.TButton',
                               command=self.show_config)
        config_btn.pack(side=tk.LEFT)

        # 候选企业列表区域
        candidate_frame = ttk.Frame(search_inner, style='Modern.TFrame')
        candidate_frame.pack(fill=tk.X, pady=(10, 0))

        candidate_label = ttk.Label(candidate_frame,
                                   text="📋 候选企业列表（双击或按Enter查询详情）",
                                   style='Modern.TLabel',
                                   font=('Microsoft YaHei', 10))
        candidate_label.pack(anchor=tk.W, pady=(0, 5))

        candidate_table_frame = ttk.Frame(candidate_frame, style='Modern.TFrame')
        candidate_table_frame.pack(fill=tk.X)

        columns = ("序号", "企业名称", "法定代表人", "注册状态", "成立日期")
        self.candidate_tree = ttk.Treeview(candidate_table_frame,
                                          columns=columns,
                                          show="headings",
                                          height=5,
                                          selectmode="browse",
                                          style='Modern.Treeview')

        headers = {"序号": 60, "企业名称": 400, "法定代表人": 120, "注册状态": 100, "成立日期": 120}
        for col, width in headers.items():
            self.candidate_tree.heading(col, text=col)
            self.candidate_tree.column(col, width=width, minwidth=width-20)

        candidate_scrollbar = ttk.Scrollbar(candidate_table_frame, orient=tk.VERTICAL, command=self.candidate_tree.yview)
        self.candidate_tree.configure(yscrollcommand=candidate_scrollbar.set)

        self.candidate_tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
        candidate_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.candidate_tree.bind("<Double-Button-1>", self.on_candidate_select)
        self.candidate_tree.bind("<Return>", self.on_candidate_select)

    def create_data_section(self, parent):
        """创建数据展示区域"""
        data_frame = ttk.Frame(parent, style='Modern.TFrame')
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.notebook = ttk.Notebook(data_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_basic_info_tab()
        self.create_shareholders_tab()
        self.create_personnel_tab()
        self.create_financial_tab()
        self.create_investment_tab()

    def create_status_bar(self, parent):
        """创建现代化的状态栏"""
        status_frame = ttk.Frame(parent, style='Modern.TFrame', relief='solid', borderwidth=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        status_inner = ttk.Frame(status_frame, style='Modern.TFrame')
        status_inner.pack(fill=tk.X, padx=20, pady=12)

        self.status_label = ttk.Label(status_inner,
                                     text="✅ 系统就绪",
                                     style='Modern.TLabel',
                                     font=('Microsoft YaHei', 10),
                                     foreground=self.colors['success'])
        self.status_label.pack(side=tk.LEFT)

    def update_status(self, message, color="blue"):
        """更新现代化状态信息"""
        color_map = {
            "blue": self.colors['primary'],
            "green": self.colors['success'],
            "orange": self.colors['warning'],
            "red": self.colors['danger'],
            "gray": self.colors['text_secondary']
        }

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


    def create_basic_info_tab(self):
        """创建现代化的基本信息标签页"""
        basic_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(basic_frame, text="📋 基本信息")

        content_frame = ttk.Frame(basic_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(content_frame,
                               text="📋 企业基本信息",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("项目", "内容")
        self.basic_tree = ttk.Treeview(table_frame,
                                      columns=columns,
                                      show="headings",
                                      height=20,
                                      selectmode="extended",
                                      style='Modern.Treeview')

        self.basic_tree.heading("项目", text="信息项目")
        self.basic_tree.heading("内容", text="详细内容")
        self.basic_tree.column("项目", width=220, minwidth=180)
        self.basic_tree.column("内容", width=800, minwidth=600)

        basic_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.basic_tree.yview)
        self.basic_tree.configure(yscrollcommand=basic_scrollbar.set)

        self.basic_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        basic_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.basic_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.basic_tree))
        self.basic_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.basic_tree))
        self.basic_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.basic_tree))

    def create_shareholders_tab(self):
        """创建现代化的股东信息标签页"""
        shareholders_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(shareholders_frame, text="👥 股东信息")

        content_frame = ttk.Frame(shareholders_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(content_frame,
                               text="👥 股东持股信息",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("序号", "股东名称", "持股比例", "认缴出资", "股东类型")
        self.shareholders_tree = ttk.Treeview(table_frame,
                                            columns=columns,
                                            show="headings",
                                            height=18,
                                            selectmode="extended",
                                            style='Modern.Treeview')

        headers = {"序号": 80, "股东名称": 350, "持股比例": 140, "认缴出资": 180, "股东类型": 140}
        for col, width in headers.items():
            self.shareholders_tree.heading(col, text=col)
            self.shareholders_tree.column(col, width=width, minwidth=width-20)

        shareholders_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.shareholders_tree.yview)
        self.shareholders_tree.configure(yscrollcommand=shareholders_scrollbar.set)

        self.shareholders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        shareholders_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.shareholders_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.shareholders_tree))
        self.shareholders_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.shareholders_tree))
        self.shareholders_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.shareholders_tree))
        self.shareholders_tree.bind("<Control-Button-1>", lambda e: self.ctrl_click_search(e, self.shareholders_tree, "股东名称"))

    def create_personnel_tab(self):
        """创建现代化的主要人员标签页"""
        personnel_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(personnel_frame, text="👤 主要人员")

        content_frame = ttk.Frame(personnel_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(content_frame,
                               text="👤 主要管理人员",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("姓名", "职位", "详细信息")
        self.personnel_tree = ttk.Treeview(table_frame,
                                         columns=columns,
                                         show="headings",
                                         height=18,
                                         selectmode="extended",
                                         style='Modern.Treeview')

        headers = {"姓名": 180, "职位": 250, "详细信息": 500}
        for col, width in headers.items():
            self.personnel_tree.heading(col, text=col)
            self.personnel_tree.column(col, width=width, minwidth=width-20)

        personnel_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.personnel_tree.yview)
        self.personnel_tree.configure(yscrollcommand=personnel_scrollbar.set)

        self.personnel_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        personnel_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.personnel_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.personnel_tree))
        self.personnel_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.personnel_tree))
        self.personnel_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.personnel_tree))

    def create_financial_tab(self):
        """创建现代化的财务数据标签页"""
        financial_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(financial_frame, text="💰 财务数据")

        content_frame = ttk.Frame(financial_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(content_frame,
                               text="💰 财务数据分析",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.financial_tree = ttk.Treeview(table_frame,
                                         show="headings",
                                         height=18,
                                         selectmode="extended",
                                         style='Modern.Treeview')

        financial_scrollbar_v = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.financial_tree.yview)
        financial_scrollbar_h = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.financial_tree.xview)
        self.financial_tree.configure(yscrollcommand=financial_scrollbar_v.set, xscrollcommand=financial_scrollbar_h.set)

        self.financial_tree.grid(row=0, column=0, sticky="nsew")
        financial_scrollbar_v.grid(row=0, column=1, sticky="ns")
        financial_scrollbar_h.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.financial_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.financial_tree))
        self.financial_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.financial_tree))
        self.financial_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.financial_tree))

    def create_investment_tab(self):
        """创建现代化的对外投资标签页"""
        investment_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(investment_frame, text="💼 对外投资")

        content_frame = ttk.Frame(investment_frame, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(content_frame,
                               text="💼 对外投资信息",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W, pady=(0, 15))

        table_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("序号", "被投资企业名称", "投资比例", "投资金额", "成立日期", "注册状态", "法定代表人", "所在地区")
        self.investment_tree = ttk.Treeview(table_frame,
                                          columns=columns,
                                          show="headings",
                                          height=18,
                                          selectmode="extended",
                                          style='Modern.Treeview')

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

        investment_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.investment_tree.yview)
        self.investment_tree.configure(yscrollcommand=investment_scrollbar.set)

        self.investment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        investment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.investment_tree.bind("<Button-3>", lambda e: self.show_context_menu(e, self.investment_tree))
        self.investment_tree.bind("<Double-Button-1>", lambda e: self.copy_cell_on_double_click(e, self.investment_tree))
        self.investment_tree.bind("<Control-c>", lambda e: self.copy_selected_cells(e, self.investment_tree))
        self.investment_tree.bind("<Control-Button-1>", lambda e: self.ctrl_click_search(e, self.investment_tree, "被投资企业名称"))


    def show_context_menu(self, event, tree):
        """显示右键菜单"""
        item = tree.identify_row(event.y)
        if item and item not in tree.selection():
            tree.selection_set(item)

        context_menu = tk.Menu(self.root, tearoff=0)
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

        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def copy_for_word(self, tree):
        """复制为Word友好格式（HTML表格格式）"""
        selection = tree.selection()
        if not selection:
            self.update_status("请先选择要复制的行", "orange")
            return

        try:
            columns = tree['columns']
            headers = [tree.heading(col)['text'] for col in columns]
            
            # 构建HTML表格
            html = '<table border="1" cellspacing="0" cellpadding="5">\n'
            html += '<tr>'
            for header in headers:
                html += f'<th style="background-color:#2563eb;color:white;font-weight:bold;">{header}</th>'
            html += '</tr>\n'
            
            for item in selection:
                values = tree.item(item, 'values')
                html += '<tr>'
                for v in values:
                    cell_value = str(v) if v else '-'
                    html += f'<td>{cell_value}</td>'
                html += '</tr>\n'
            
            html += '</table>'
            
            # 尝试使用HTML剪贴板格式
            if self._copy_html_to_clipboard(html):
                self.update_status(f"已复制 {len(selection)} 行数据（HTML表格格式），可直接粘贴到Word", "green")
            else:
                # 回退到纯文本格式
                text_data = ['\t'.join(headers)]
                for item in selection:
                    values = tree.item(item, 'values')
                    text_data.append('\t'.join(str(v) if v else '-' for v in values))
                self.root.clipboard_clear()
                self.root.clipboard_append('\n'.join(text_data))
                self.update_status(f"已复制 {len(selection)} 行数据（文本格式）", "green")

        except Exception as e:
            self.update_status(f"复制失败: {str(e)}", "red")

    def _copy_html_to_clipboard(self, html):
        """将HTML内容复制到剪贴板（支持Word粘贴）"""
        try:
            import win32clipboard
            
            # HTML剪贴板格式头
            html_header = (
                "Version:0.9\r\n"
                "StartHTML:{:08d}\r\n"
                "EndHTML:{:08d}\r\n"
                "StartFragment:{:08d}\r\n"
                "EndFragment:{:08d}\r\n"
            )
            
            prefix = "<!DOCTYPE html><html><body><!--StartFragment-->"
            suffix = "<!--EndFragment--></body></html>"
            
            # 计算偏移量
            header_len = len(html_header.format(0, 0, 0, 0))
            start_html = header_len
            start_fragment = start_html + len(prefix)
            end_fragment = start_fragment + len(html.encode('utf-8'))
            end_html = end_fragment + len(suffix)
            
            # 构建完整的HTML剪贴板数据
            cf_html = html_header.format(start_html, end_html, start_fragment, end_fragment)
            cf_html += prefix + html + suffix
            
            # 注册HTML格式
            CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")
            
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(CF_HTML, cf_html.encode('utf-8'))
            
            # 同时设置纯文本格式作为备用
            text_lines = []
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            for row in soup.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                text_lines.append('\t'.join(cell.get_text() for cell in cells))
            win32clipboard.SetClipboardText('\n'.join(text_lines))
            
            win32clipboard.CloseClipboard()
            return True
        except ImportError:
            return False
        except Exception as e:
            print(f"HTML剪贴板复制失败: {e}")
            return False

    def copy_for_excel(self, tree):
        """复制为Excel友好格式"""
        selection = tree.selection()
        if not selection:
            self.update_status("请先选择要复制的行", "orange")
            return

        try:
            copied_data = []
            columns = tree['columns']
            if columns:
                headers = [tree.heading(col)['text'] for col in columns]
                copied_data.append('\t'.join(headers))

            for item in selection:
                values = tree.item(item, 'values')
                processed_values = []
                for v in values:
                    if v is None or v == '':
                        processed_values.append('')
                    else:
                        str_v = str(v)
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

    def copy_cell_on_double_click(self, event, tree):
        """双击复制单元格内容"""
        try:
            item = tree.identify_row(event.y)
            column = tree.identify_column(event.x)

            if item and column:
                col_index = int(column.replace('#', '')) - 1
                if col_index >= 0:
                    values = tree.item(item, 'values')
                    if col_index < len(values):
                        cell_value = str(values[col_index])
                        self.root.clipboard_clear()
                        self.root.clipboard_append(cell_value)
                        self.update_status(f"已复制: {cell_value[:50]}{'...' if len(cell_value) > 50 else ''}", "green")
        except Exception as e:
            self.update_status(f"复制失败: {str(e)}", "red")

    def copy_selected_cells(self, event, tree):
        """Ctrl+C复制选中的行（HTML表格格式）"""
        self.copy_for_word(tree)


    def setup_shortcuts(self):
        """设置快捷键"""
        self.company_entry.bind('<Return>', lambda event: self.search_companies())
        self.company_entry.bind('<Down>', lambda event: self.focus_candidate_list())
        self.root.bind('<F1>', lambda event: self.show_config())
        self.root.bind('<Control-q>', lambda event: self.root.quit())
        self.root.bind('<Alt-Left>', lambda event: self.go_back_query())

        # 数字键1-5快速切换标签页
        self.root.bind('<Key-1>', lambda event: self.switch_to_tab(0))
        self.root.bind('<Key-2>', lambda event: self.switch_to_tab(1))
        self.root.bind('<Key-3>', lambda event: self.switch_to_tab(2))
        self.root.bind('<Key-4>', lambda event: self.switch_to_tab(3))
        self.root.bind('<Key-5>', lambda event: self.switch_to_tab(4))

        self.root.bind('<Escape>', lambda event: self.focus_search_entry())
        self.root.bind('<Control-a>', lambda event: self.select_all_in_current_tab(event))

    def focus_candidate_list(self):
        """焦点移到候选列表"""
        children = self.candidate_tree.get_children()
        if children:
            self.candidate_tree.focus_set()
            self.candidate_tree.selection_set(children[0])
            self.candidate_tree.focus(children[0])

    def focus_search_entry(self):
        """焦点移到搜索框"""
        self.company_entry.focus_set()
        self.company_entry.select_range(0, tk.END)

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
            current_tab = self.notebook.select()
            tab_text = self.notebook.tab(current_tab, "text")

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

            tree.selection_set(tree.get_children())
            self.update_status(f"已全选 {len(tree.get_children())} 行数据", "green")

        except Exception as e:
            self.update_status(f"全选失败: {str(e)}", "red")

    def ctrl_click_search(self, event, tree, target_column):
        """Ctrl+点击直接查询企业详情"""
        try:
            item = tree.identify_row(event.y)
            if not item:
                return

            values = tree.item(item, 'values')
            if not values:
                return

            company_name = ""
            if target_column == "股东名称":
                if len(values) > 1:
                    company_name = str(values[1]).strip()
            elif target_column == "被投资企业名称":
                if len(values) > 1:
                    company_name = str(values[1]).strip()

            if company_name and company_name != "-" and company_name != "":
                self.company_entry.delete(0, tk.END)
                self.company_entry.insert(0, company_name)
                self.update_status(f"正在查询: {company_name}", "blue")
                # 直接查询，不显示候选列表
                self._direct_query_company(company_name)
            else:
                self.update_status("未找到有效的企业名称", "orange")

        except Exception as e:
            self.update_status(f"搜索失败: {str(e)}", "red")

    def _direct_query_company(self, company_name):
        """直接查询企业详情（跳过候选列表）"""
        self.query_btn.config(state='disabled')
        
        def query_thread():
            try:
                cookies = self.get_current_cookies()
                auth_token = getattr(self, 'current_auth_token', '')
                api = TianyanchaAPI(cookies, auth_token)
                
                # 搜索获取第一个匹配的企业
                result = api.search_company(company_name)
                
                if result:
                    gid = result.get('gid', '')
                    name = result.get('name', company_name)
                    
                    if gid:
                        # 添加到历史记录
                        self.query_history.append({'gid': gid, 'name': name})
                        self.current_query_index = len(self.query_history) - 1
                        
                        # 获取详细信息
                        basic_info = api.get_basic_info(gid)
                        shareholders = api.get_shareholders(gid)
                        personnel = api.get_key_personnel(gid)
                        financial = api.get_financial_data(gid)
                        investments = api.get_investment_info(gid)
                        
                        self.root.after(0, lambda: self.update_display(basic_info, shareholders, personnel, financial, investments))
                    else:
                        self.root.after(0, lambda: self.update_status("未找到企业信息", "orange"))
                else:
                    self.root.after(0, lambda: self.update_status("未找到企业信息", "orange"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.update_status(f"查询失败: {str(e)}", "red"))
            finally:
                self.root.after(0, lambda: self.query_btn.config(state='normal'))
        
        thread = threading.Thread(target=query_thread)
        thread.daemon = True
        thread.start()

    def load_config(self):
        """加载保存的配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'rb') as f:
                    config = pickle.load(f)
                    self.default_cookies = config.get('cookies', self.default_cookies)
                    self.current_auth_token = config.get('auth_token', '')
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
        except Exception as e:
            print(f"保存配置失败: {str(e)}")

    def get_current_cookies(self):
        """获取当前的cookies"""
        if self.cookies_text and hasattr(self.cookies_text, 'get'):
            return self.cookies_text.get(1.0, tk.END).strip()
        else:
            return self.default_cookies

    def show_config(self):
        """显示配置窗口"""
        config_window = tk.Toplevel(self.root)
        config_window.title("配置设置")
        config_window.geometry("700x500")
        config_window.transient(self.root)
        config_window.grab_set()

        ttk.Label(config_window, text="Cookies配置:").pack(anchor=tk.W, padx=10, pady=(10, 5))

        cookies_frame = ttk.Frame(config_window)
        cookies_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.cookies_text = tk.Text(cookies_frame, height=10, wrap=tk.WORD)
        cookies_scrollbar = ttk.Scrollbar(cookies_frame, orient=tk.VERTICAL, command=self.cookies_text.yview)
        self.cookies_text.configure(yscrollcommand=cookies_scrollbar.set)

        self.cookies_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cookies_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cookies_text.insert(tk.END, self.default_cookies)

        ttk.Label(config_window, text="Auth Token配置:").pack(anchor=tk.W, padx=10, pady=(10, 5))

        token_frame = ttk.Frame(config_window)
        token_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.auth_token_text = tk.Text(token_frame, height=4, wrap=tk.WORD)
        token_scrollbar = ttk.Scrollbar(token_frame, orient=tk.VERTICAL, command=self.auth_token_text.yview)
        self.auth_token_text.configure(yscrollcommand=token_scrollbar.set)

        self.auth_token_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        token_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        if hasattr(self, 'current_auth_token') and self.current_auth_token:
            self.auth_token_text.insert(tk.END, self.current_auth_token)

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

        self.save_config_to_file()
        window.destroy()
        self.update_status("配置已保存", "green")


    def search_companies(self):
        """搜索企业列表"""
        company_name = self.company_entry.get().strip()
        if not company_name:
            messagebox.showwarning("警告", "请输入企业名称")
            return

        self.query_btn.config(state='disabled')
        self.update_status("正在搜索...", "blue")

        thread = threading.Thread(target=self._search_companies_thread, args=(company_name,))
        thread.daemon = True
        thread.start()

    def _search_companies_thread(self, company_name):
        """搜索企业线程"""
        try:
            cookies = self.get_current_cookies()
            auth_token = getattr(self, 'current_auth_token', '')
            api = TianyanchaAPI(cookies, auth_token)

            result = api.search_company_list(company_name)
            
            if result:
                self.candidate_companies = result
                self.root.after(0, lambda: self._update_candidate_list(result))
                self.root.after(0, lambda: self.update_status(f"找到 {len(result)} 个候选企业", "green"))
            else:
                self.root.after(0, lambda: self.update_status("未找到匹配的企业", "orange"))

        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"搜索失败: {str(e)}", "red"))
        finally:
            self.root.after(0, lambda: self.query_btn.config(state='normal'))

    def _update_candidate_list(self, companies):
        """更新候选企业列表"""
        for item in self.candidate_tree.get_children():
            self.candidate_tree.delete(item)

        for i, company in enumerate(companies, 1):
            values = (
                i,
                company.get('name', ''),
                company.get('legalPerson', ''),
                company.get('regStatus', ''),
                company.get('establishTime', '')
            )
            self.candidate_tree.insert("", tk.END, values=values, tags=(str(i-1),))

        if companies:
            first_item = self.candidate_tree.get_children()[0]
            self.candidate_tree.selection_set(first_item)

    def on_candidate_select(self, event):
        """候选企业选择事件"""
        selection = self.candidate_tree.selection()
        if not selection:
            return

        item = selection[0]
        item_index = self.candidate_tree.index(item)
        
        if item_index < len(self.candidate_companies):
            company = self.candidate_companies[item_index]
            gid = company.get('gid', '')
            company_name = company.get('name', '')
            
            if gid:
                # 添加到历史记录
                self.query_history.append({
                    'gid': gid,
                    'name': company_name
                })
                self.current_query_index = len(self.query_history) - 1
                
                self.start_query(gid, company_name)

    def go_back_query(self):
        """返回上一个查询"""
        if self.current_query_index > 0:
            self.current_query_index -= 1
            history_item = self.query_history[self.current_query_index]
            gid = history_item.get('gid', '')
            company_name = history_item.get('name', '')
            
            if gid:
                self.company_entry.delete(0, tk.END)
                self.company_entry.insert(0, company_name)
                self.start_query(gid, company_name)
                self.update_status(f"返回: {company_name}", "blue")
        else:
            self.update_status("已经是第一个查询", "orange")

    def start_query(self, gid=None, company_name=None):
        """开始查询企业详情"""
        if not gid:
            # 兼容旧的调用方式
            company_name = self.company_entry.get().strip()
            if not company_name:
                messagebox.showwarning("警告", "请输入企业名称")
                return
            self.search_companies()
            return

        self.query_btn.config(state='disabled')
        self.update_status(f"正在查询: {company_name}...", "blue")

        thread = threading.Thread(target=self._query_company_thread, args=(gid, company_name))
        thread.daemon = True
        thread.start()

    def _query_company_thread(self, gid, company_name):
        """查询企业详情线程"""
        try:
            cookies = self.get_current_cookies()
            auth_token = getattr(self, 'current_auth_token', '')
            api = TianyanchaAPI(cookies, auth_token)

            basic_info = api.get_basic_info(gid)
            shareholders = api.get_shareholders(gid)
            personnel = api.get_key_personnel(gid)
            financial = api.get_financial_data(gid)
            investments = api.get_investment_info(gid)

            self.root.after(0, lambda: self.update_display(basic_info, shareholders, personnel, financial, investments))

        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"查询失败: {str(e)}", "red"))
        finally:
            self.root.after(0, lambda: self.query_btn.config(state='normal'))

    def update_display(self, basic_info, shareholders, personnel, financial, investments):
        """更新显示内容"""
        self.update_basic_info(basic_info)
        self.update_shareholders(shareholders)
        self.update_personnel(personnel)
        self.update_financial(financial)
        self.update_investments(investments)
        # 切换到基本信息标签页
        self.notebook.select(0)
        self.update_status("查询完成", "green")

    def update_basic_info(self, basic_info):
        """更新基本信息表格"""
        for item in self.basic_tree.get_children():
            self.basic_tree.delete(item)

        if not basic_info:
            return

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

        for display_name, key in info_items:
            value = basic_info.get(key, "")
            if value:
                if key == "经营范围" and len(str(value)) > 300:
                    value = str(value)[:300] + "..."
                self.basic_tree.insert("", tk.END, values=(display_name, value))

    def update_shareholders(self, shareholders):
        """更新股东信息表格"""
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
        """更新财务数据表格"""
        for item in self.financial_tree.get_children():
            self.financial_tree.delete(item)

        if not financial:
            return

        if isinstance(financial, dict) and 'titleList' in financial:
            title_list = financial.get('titleList', [])
            attr_list = financial.get('attrList', [])
            column_list = financial.get('columnList', [])

            if not title_list or not attr_list or not column_list:
                return

            columns = ['财务指标'] + title_list[:8]
            self.financial_tree['columns'] = columns
            self.financial_tree['show'] = 'headings'

            self.financial_tree.heading('财务指标', text='财务指标')
            self.financial_tree.column('财务指标', width=200, minwidth=150)

            for title in title_list[:8]:
                self.financial_tree.heading(title, text=title)
                self.financial_tree.column(title, width=120, minwidth=100)

            for i, attr in enumerate(attr_list):
                attr_name = attr.get('name', '')
                if not attr_name:
                    continue

                row_values = [attr_name]
                for j, column in enumerate(column_list[:8]):
                    value_list = column.get('valueList', [])
                    if i < len(value_list):
                        value = value_list[i]
                        row_values.append(str(value) if value and value != "" else "-")
                    else:
                        row_values.append("-")

                self.financial_tree.insert("", tk.END, values=row_values)
        else:
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

        if auth_token:
            self.base_headers["x-auth-token"] = auth_token

    def search_company_list(self, company_name):
        """搜索公司列表，返回多个候选企业"""
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
                    
                    companies = []
                    for company in company_list[:10]:
                        establish_time = company.get('estiblishTime', '')
                        if establish_time and isinstance(establish_time, (int, float)):
                            try:
                                import datetime
                                establish_time = datetime.datetime.fromtimestamp(establish_time / 1000).strftime('%Y-%m-%d')
                            except:
                                establish_time = str(establish_time)
                        
                        companies.append({
                            'gid': str(company.get('id', '')),
                            'graphId': str(company.get('graphId', '')),
                            'name': company.get('comName', ''),
                            'legalPerson': company.get('legalPersonName', ''),
                            'regStatus': '存续' if company.get('regStatus', 0) == 1 else '其他',
                            'establishTime': establish_time
                        })
                    return companies
            return []
        except Exception as e:
            print(f"搜索企业列表失败: {e}")
            return []

    def search_company(self, company_name):
        """搜索公司获取基本信息（兼容旧接口）"""
        companies = self.search_company_list(company_name)
        if companies:
            return companies[0]
        return None

    def get_basic_info(self, gid):
        """获取基本信息"""
        try:
            url = f"https://www.tianyancha.com/company/{gid}"

            web_headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
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

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                basic_info = self._extract_basic_info_from_html(soup)
                return basic_info
            return {}
        except Exception as e:
            print(f"获取基本信息失败: {e}")
            return {}

    def _extract_basic_info_from_html(self, soup):
        """从HTML中提取基本信息"""
        info = {}

        try:
            # 公司名称
            name_elem = soup.find('h1', class_='index_company-name__LqKlo')
            if name_elem:
                name_span = name_elem.find('span', class_='index_name__dz4jY')
                if name_span:
                    info['公司名称'] = name_span.get_text(strip=True)

            if '公司名称' not in info:
                name_elem = soup.find('h1')
                if name_elem:
                    info['公司名称'] = name_elem.get_text(strip=True)

            # 统一社会信用代码
            credit_code_elem = soup.find('span', class_='index_detail-credit-code__fH1Ny')
            if credit_code_elem:
                code_span = credit_code_elem.find('span')
                if code_span:
                    info['统一社会信用代码'] = code_span.get_text(strip=True)

            # 法定代表人
            legal_person_elem = soup.find('div', class_='index_legal-person-root__THrdz')
            if legal_person_elem:
                link_elem = legal_person_elem.find('a', class_='index_link-click__NmHxP')
                if link_elem:
                    info['法定代表人'] = link_elem.get_text(strip=True)

            # 经营状态
            status_elem = soup.find('div', class_='index_company-tag__ZcJFV index_header-company-tag__WaTgu')
            if status_elem:
                info['经营状态'] = status_elem.get_text(strip=True)

            # 详细信息项提取
            detail_items = soup.find_all('div', class_='index_detail-info-item__oAOqL')
            for item in detail_items:
                label_elem = item.find('span', class_='index_detail-label__oRf2J')
                if label_elem:
                    label_text = label_elem.get_text(strip=True)

                    if '注册资本' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['注册资本'] = value_elem.get_text(strip=True)

                    elif '成立日期' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['成立日期'] = value_elem.get_text(strip=True)

                    elif '电话' in label_text:
                        tel_elem = item.find('span', class_='index_detail-tel__fgpsE')
                        if tel_elem:
                            info['联系电话'] = tel_elem.get_text(strip=True)

                    elif '邮箱' in label_text:
                        email_elem = item.find('a', class_='index_detail-email__B_1Tq')
                        if email_elem:
                            info['邮箱'] = email_elem.get_text(strip=True)

                    elif '网址' in label_text:
                        website_elem = item.find('a', class_='index_detail-website__n2yst')
                        if website_elem:
                            info['网址'] = website_elem.get_text(strip=True)

                    elif '地址' in label_text:
                        address_elem = item.find('span', class_='index_detail-address-moretext__9R_Z1')
                        if address_elem:
                            address_span = address_elem.find('span', class_='index_inline-flex__QLDiW')
                            if address_span:
                                info['注册地址'] = address_span.get_text(strip=True)

                    elif '国标行业' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['所属行业'] = value_elem.get_text(strip=True)

                    elif '企业规模' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['企业规模'] = value_elem.get_text(strip=True)

                    elif '员工人数' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['员工人数'] = value_elem.get_text(strip=True)

            # 从表格中提取更多信息
            table_rows = soup.find_all('tr')
            for row in table_rows:
                cells = row.find_all('td')
                for i, cell in enumerate(cells):
                    cell_text = cell.get_text(strip=True)

                    if '经营范围' in cell_text and i + 1 < len(cells):
                        scope_cell = cells[i + 1]
                        copy_text_elem = scope_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['经营范围'] = copy_text_elem.get_text(strip=True)
                        else:
                            scope_text = scope_cell.get_text(strip=True)
                            if scope_text and len(scope_text) > 20:
                                info['经营范围'] = scope_text

                    elif '英文名称' in cell_text and i + 1 < len(cells):
                        en_cell = cells[i + 1]
                        copy_text_elem = en_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['英文名称'] = copy_text_elem.get_text(strip=True)

                    elif '登记机关' in cell_text and i + 1 < len(cells):
                        reg_cell = cells[i + 1]
                        copy_text_elem = reg_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['登记机关'] = copy_text_elem.get_text(strip=True)

            return info

        except Exception as e:
            print(f"HTML解析错误: {e}")
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

            if response.status_code == 200:
                result = response.json()

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    holders = data.get('result', [])

                    shareholders = []
                    for holder in holders:
                        shareholder_name = holder.get('shareHolderName', '') or holder.get('name', '')
                        percent = holder.get('percent', '')
                        total_capital = holder.get('totalCapital', '') or holder.get('amount', '')
                        shareholder_type = holder.get('shareHolderTypeOnPage', '')

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

                    return shareholders
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

            if response.status_code == 200:
                result = response.json()

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

                    return personnel
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

            if response.status_code == 200:
                result = response.json()

                if result.get('state') == 'ok' and 'data' in result:
                    return result['data']
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

            if response.status_code == 200:
                result = response.json()

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    investments = []

                    for item in data.get('result', []):
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

                    return investments
            return []
        except Exception as e:
            print(f"对外投资查询异常: {str(e)}")
            return []


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTianyanchaGUI(root)
    root.mainloop()
