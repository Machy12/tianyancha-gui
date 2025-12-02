#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行GUI并查看调试输出
"""

import tkinter as tk
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianyancha_treeview import TianyanchaTreeviewGUI

def main():
    print("🚀 启动tianyancha_treeview.py GUI...")
    print("=" * 60)
    
    try:
        root = tk.Tk()
        app = TianyanchaTreeviewGUI(root)
        
        print("✅ GUI创建成功")
        print("📝 请在GUI中输入公司名称进行测试")
        print("📝 建议测试公司: 浙江春风动力股份有限公司")
        print("📝 观察控制台输出的调试信息")
        print("=" * 60)
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
