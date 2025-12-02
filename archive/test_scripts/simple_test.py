#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试修复后的HTML提取功能
"""

from bs4 import BeautifulSoup
from tianyancha_treeview import TianyanchaAPI

def main():
    print("🧪 简单测试修复后的HTML提取功能")
    
    # 读取HTML文件
    html_file = "2320855868"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("✅ HTML文件读取成功")
        
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, 'html.parser')
        print("✅ BeautifulSoup对象创建成功")
        
        # 创建API实例
        api = TianyanchaAPI({}, "")
        print("✅ API实例创建成功")
        
        # 调用提取方法
        print("\n🔍 开始提取基本信息...")
        basic_info = api._extract_basic_info_from_html(soup)
        
        print(f"\n🎉 提取完成！共获得 {len(basic_info)} 个字段")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
