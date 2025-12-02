#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
调试tianyancha_complete_api.py中的basic_info获取功能
展示详细的获取过程和结果
"""

from bs4 import BeautifulSoup
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianyancha_complete_api import TianyanchaAPI

def debug_basic_info_extraction():
    """调试basic_info提取过程"""
    
    print("🔍 调试tianyancha_complete_api.py中的basic_info获取功能")
    print("=" * 80)
    
    # 读取HTML文件
    html_file = "2320855868"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"📄 成功读取HTML文件: {html_file}")
        print(f"📄 HTML文件大小: {len(html_content)} 字符")
        
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, 'html.parser')
        print(f"✅ 成功创建BeautifulSoup对象")
        
        # 创建API实例（tianyancha_complete_api.py中的构造函数不需要参数）
        api = TianyanchaAPI()
        print(f"✅ 成功创建TianyanchaAPI实例")
        
        print("\n" + "=" * 80)
        print("🔍 开始调用_extract_basic_info_from_html函数...")
        print("=" * 80)
        
        # 调用提取方法
        basic_info = api._extract_basic_info_from_html(soup)
        
        print("\n" + "=" * 80)
        print("📊 提取结果详细分析")
        print("=" * 80)
        
        print(f"📈 提取结果类型: {type(basic_info)}")
        print(f"📈 提取字段总数: {len(basic_info)}")
        print(f"📈 是否为空: {'是' if not basic_info else '否'}")
        
        if basic_info:
            print(f"\n🎯 详细字段内容:")
            print("-" * 80)
            
            # 按类别分组显示
            basic_fields = ["公司名称", "统一社会信用代码", "法定代表人", "经营状态"]
            registration_fields = ["注册资本", "成立日期", "注册地址", "登记机关"]
            contact_fields = ["联系电话", "邮箱", "网址"]
            business_fields = ["所属行业", "企业规模", "员工人数", "英文名称"]
            scope_fields = ["经营范围"]
            
            def display_fields(category_name, field_list):
                print(f"\n📋 {category_name}:")
                found_any = False
                for field in field_list:
                    if field in basic_info and basic_info[field]:
                        value = str(basic_info[field])
                        if len(value) > 100:
                            display_value = value[:100] + "..."
                        else:
                            display_value = value
                        print(f"  ✅ {field}: {display_value}")
                        found_any = True
                    else:
                        print(f"  ❌ {field}: [未获取到]")
                
                if not found_any:
                    print(f"  ⚠️  该类别下没有获取到任何信息")
            
            # 分类显示
            display_fields("基本信息", basic_fields)
            display_fields("注册信息", registration_fields)
            display_fields("联系信息", contact_fields)
            display_fields("经营信息", business_fields)
            display_fields("经营范围", scope_fields)
            
            # 检查是否有其他字段
            all_expected_fields = basic_fields + registration_fields + contact_fields + business_fields + scope_fields
            extra_fields = [field for field in basic_info.keys() if field not in all_expected_fields]
            
            if extra_fields:
                print(f"\n📋 其他字段:")
                for field in extra_fields:
                    value = str(basic_info[field])
                    if len(value) > 100:
                        display_value = value[:100] + "..."
                    else:
                        display_value = value
                    print(f"  ➕ {field}: {display_value}")
            
            print(f"\n" + "=" * 80)
            print("📊 统计信息")
            print("=" * 80)
            
            # 统计各类别的获取情况
            categories = [
                ("基本信息", basic_fields),
                ("注册信息", registration_fields),
                ("联系信息", contact_fields),
                ("经营信息", business_fields),
                ("经营范围", scope_fields)
            ]
            
            total_expected = 0
            total_obtained = 0
            
            for category_name, field_list in categories:
                expected = len(field_list)
                obtained = len([f for f in field_list if f in basic_info and basic_info[f]])
                total_expected += expected
                total_obtained += obtained
                
                percentage = (obtained / expected * 100) if expected > 0 else 0
                print(f"  {category_name}: {obtained}/{expected} ({percentage:.1f}%)")
            
            overall_percentage = (total_obtained / total_expected * 100) if total_expected > 0 else 0
            print(f"\n🎯 总体获取率: {total_obtained}/{total_expected} ({overall_percentage:.1f}%)")
            
            # 质量评估
            print(f"\n📈 数据质量评估:")
            if overall_percentage >= 90:
                print(f"  🟢 优秀 - 数据获取非常完整")
            elif overall_percentage >= 70:
                print(f"  🟡 良好 - 大部分数据获取成功")
            elif overall_percentage >= 50:
                print(f"  🟠 一般 - 部分数据获取成功")
            else:
                print(f"  🔴 较差 - 数据获取不完整")
        
        else:
            print(f"\n❌ 没有获取到任何基本信息！")
            print(f"可能的原因:")
            print(f"  1. HTML结构发生变化")
            print(f"  2. CSS选择器不匹配")
            print(f"  3. 页面内容为空或错误")
        
        return basic_info
        
    except Exception as e:
        print(f"❌ 调试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_with_expected():
    """与预期结果进行对比"""
    
    print(f"\n" + "=" * 80)
    print("🔄 与预期结果对比")
    print("=" * 80)
    
    # 预期应该获取到的字段（基于之前的成功测试）
    expected_fields = {
        "公司名称": "浙江春风动力股份有限公司",
        "统一社会信用代码": "91330100757206158J",
        "法定代表人": "赖民杰",
        "经营状态": "存续",
        "注册资本": "15,257.7663万人民币",
        "成立日期": "2003-12-09",
        "联系电话": "0571-89265620",
        "邮箱": "wuyiqing@cfmoto.com",
        "网址": "www.cfmoto.com",
        "注册地址": "浙江省杭州市临平区临平经济开发区五洲路116号",
        "所属行业": "城市轨道交通设备制造",
        "企业规模": "大型",
        "员工人数": "6911人",
        "英文名称": "Zhejiang CFMOTO Power Co.,Ltd.",
        "登记机关": "浙江省市场监督管理局",
        "经营范围": "一般项目：摩托车零配件制造..."
    }
    
    # 获取实际结果
    actual_result = debug_basic_info_extraction()
    
    if actual_result:
        print(f"\n📊 字段对比结果:")
        print("-" * 80)
        
        match_count = 0
        total_count = len(expected_fields)
        
        for field, expected_value in expected_fields.items():
            actual_value = actual_result.get(field, "")
            
            if actual_value:
                if field == "经营范围":
                    # 经营范围只比较前50个字符
                    match = expected_value[:50] in actual_value[:50]
                else:
                    match = str(actual_value) == str(expected_value)
                
                if match:
                    print(f"  ✅ {field}: 匹配")
                    match_count += 1
                else:
                    print(f"  ⚠️  {field}: 不匹配")
                    print(f"      预期: {expected_value}")
                    print(f"      实际: {actual_value}")
            else:
                print(f"  ❌ {field}: 缺失")
        
        match_percentage = (match_count / total_count * 100) if total_count > 0 else 0
        print(f"\n🎯 匹配率: {match_count}/{total_count} ({match_percentage:.1f}%)")
        
        if match_percentage >= 90:
            print(f"🎉 结果优秀！tianyancha_complete_api.py工作正常")
        elif match_percentage >= 70:
            print(f"👍 结果良好！大部分功能正常")
        else:
            print(f"⚠️  结果需要改进！存在较多问题")

if __name__ == "__main__":
    print("🚀 开始调试tianyancha_complete_api.py的basic_info获取功能...")
    compare_with_expected()
    print(f"\n🏁 调试完成！")
