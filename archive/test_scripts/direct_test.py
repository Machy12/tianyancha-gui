#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
直接测试HTML提取功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        print("🧪 开始直接测试...")
        
        # 导入必要的模块
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup导入成功")
        
        from tianyancha_treeview import TianyanchaAPI
        print("✅ TianyanchaAPI导入成功")
        
        # 读取HTML文件
        html_file = "2320855868"
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print("✅ HTML文件读取成功")
        
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, 'html.parser')
        print("✅ BeautifulSoup对象创建成功")
        
        # 创建API实例
        api = TianyanchaAPI({}, "")
        print("✅ API实例创建成功")
        
        # 测试提取方法是否存在
        if hasattr(api, '_extract_basic_info_from_html'):
            print("✅ _extract_basic_info_from_html方法存在")
        else:
            print("❌ _extract_basic_info_from_html方法不存在")
            return False
        
        # 调用提取方法
        print("\n🔍 开始调用提取方法...")
        basic_info = api._extract_basic_info_from_html(soup)
        
        print(f"\n🎉 提取完成！")
        print(f"📊 结果类型: {type(basic_info)}")
        print(f"📊 字段数量: {len(basic_info) if basic_info else 0}")
        
        if basic_info:
            print("\n📋 提取的字段:")
            for key, value in basic_info.items():
                if len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:100]}...")
                else:
                    print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 测试成功！")
    else:
        print("\n💥 测试失败！")
