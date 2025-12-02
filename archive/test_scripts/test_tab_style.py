#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试标签页样式的脚本
"""

import tkinter as tk
from tianyancha_treeview import ModernTianyanchaGUI

def main():
    """测试现代化GUI的标签页样式"""
    print("🎨 测试标签页样式...")
    print("主要改进：")
    print("- 选中标签页更大更突出")
    print("- 使用微软雅黑字体")
    print("- 选中时字体加粗")
    print("- 更大的内边距")
    
    # 创建主窗口
    root = tk.Tk()
    
    # 创建现代化GUI应用
    app = ModernTianyanchaGUI(root)
    
    print("✅ GUI已启动，请查看标签页样式效果！")
    
    # 启动GUI主循环
    root.mainloop()

if __name__ == "__main__":
    main()
