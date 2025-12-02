#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修复后的HTML提取功能
"""

from bs4 import BeautifulSoup
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入主程序中的TianyanchaAPI类
from tianyancha_treeview import TianyanchaAPI

def test_html_extraction():
    """测试HTML提取功能"""
    
    print("🧪 测试修复后的HTML提取功能")
    print("=" * 50)
    
    # 读取HTML文件
    html_file = "2320855868"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 创建API实例（用于调用提取方法）
        api = TianyanchaAPI({}, "")
        
        # 调用提取方法
        basic_info = api._extract_basic_info_from_html(soup)
        
        print(f"✅ 成功提取基本信息")
        print(f"📊 提取到字段数量: {len(basic_info)}")
        print("\n📋 提取结果:")
        print("-" * 50)
        
        # 显示提取结果
        for key, value in basic_info.items():
            print(f"  {key}: {value}")
        
        # 验证关键字段
        required_fields = ['公司名称', '统一社会信用代码', '法定代表人', '注册资本', '成立日期']
        missing_fields = []
        
        for field in required_fields:
            if field not in basic_info or not basic_info[field]:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"\n⚠️  缺失关键字段: {', '.join(missing_fields)}")
        else:
            print(f"\n✅ 所有关键字段都已提取")
        
        # 验证特定修复
        print(f"\n🔧 修复验证:")
        
        # 验证地址修复
        if '注册地址' in basic_info and basic_info['注册地址']:
            if '地址：' not in basic_info['注册地址'] and len(basic_info['注册地址']) > 10:
                print(f"  ✅ 地址提取修复成功: {basic_info['注册地址']}")
            else:
                print(f"  ❌ 地址提取仍有问题: {basic_info['注册地址']}")
        else:
            print(f"  ❌ 地址未提取到")
        
        # 验证经营状态修复
        if '经营状态' in basic_info and basic_info['经营状态']:
            print(f"  ✅ 经营状态提取修复成功: {basic_info['经营状态']}")
        else:
            print(f"  ❌ 经营状态未提取到")
        
        # 验证联系信息
        contact_fields = ['联系电话', '邮箱', '网址']
        extracted_contact = [field for field in contact_fields if field in basic_info and basic_info[field]]
        print(f"  ✅ 联系信息提取: {len(extracted_contact)}/{len(contact_fields)} 个字段")
        
        return basic_info
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_html_extraction()
    
    if result:
        print(f"\n🎉 测试完成！成功提取 {len(result)} 个字段")
    else:
        print(f"\n💥 测试失败！")
