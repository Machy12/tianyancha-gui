#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试tianyancha_treeview.py的字段映射和GUI显示
"""

from bs4 import BeautifulSoup
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianyancha_treeview import TianyanchaAPI

def test_field_mapping():
    """测试字段映射"""
    
    print("🧪 测试tianyancha_treeview.py字段映射")
    print("=" * 60)
    
    # 读取HTML文件
    html_file = "2320855868"
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 创建API实例（使用默认cookies）
        default_cookies = "CUID=62b3804415cb2ef97572b27cdb7c519c; TYCID=e7f47650f4e911efa23e1f6dbaa18f88"
        api = TianyanchaAPI(default_cookies)
        
        # 调用提取方法
        print("🔍 调用_extract_basic_info_from_html方法...")
        basic_info = api._extract_basic_info_from_html(soup)
        
        print(f"\n📊 提取结果:")
        print(f"总共提取到 {len(basic_info)} 个字段")
        
        # 显示所有提取到的字段
        print(f"\n🔍 提取到的字段:")
        for key, value in basic_info.items():
            if len(str(value)) > 100:
                print(f"  {key}: {str(value)[:100]}...")
            else:
                print(f"  {key}: {value}")
        
        # 检查GUI期望的字段
        print(f"\n🎯 GUI期望的字段映射:")
        gui_expected_fields = [
            "公司名称", "英文名称", "统一社会信用代码", "法定代表人",
            "注册资本", "成立日期", "经营状态", "注册地址", "登记机关",
            "所属行业", "企业规模", "员工人数", "联系电话", "邮箱", "网址", "经营范围"
        ]
        
        missing_fields = []
        present_fields = []
        
        for field in gui_expected_fields:
            if field in basic_info and basic_info[field]:
                present_fields.append(field)
                print(f"  ✅ {field}: 已提取")
            else:
                missing_fields.append(field)
                print(f"  ❌ {field}: 缺失")
        
        print(f"\n📈 字段统计:")
        print(f"  成功提取: {len(present_fields)}/{len(gui_expected_fields)} 个字段")
        print(f"  缺失字段: {len(missing_fields)} 个")
        
        if missing_fields:
            print(f"\n⚠️  缺失的字段: {', '.join(missing_fields)}")
        
        # 检查是否有额外的字段
        extra_fields = [field for field in basic_info.keys() if field not in gui_expected_fields]
        if extra_fields:
            print(f"\n➕ 额外提取的字段: {', '.join(extra_fields)}")
        
        return len(present_fields) >= 10  # 至少要有10个字段才算成功
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_display_simulation():
    """模拟GUI显示逻辑"""
    
    print(f"\n" + "=" * 60)
    print("🖥️  模拟GUI显示逻辑")
    print("=" * 60)
    
    try:
        # 读取HTML文件
        html_file = "2320855868"
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        default_cookies = "CUID=62b3804415cb2ef97572b27cdb7c519c; TYCID=e7f47650f4e911efa23e1f6dbaa18f88"
        api = TianyanchaAPI(default_cookies)
        basic_info = api._extract_basic_info_from_html(soup)
        
        # 模拟update_basic_info函数的逻辑
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
        
        print("🎯 GUI将显示的内容:")
        displayed_count = 0
        
        for display_name, key in info_items:
            value = basic_info.get(key, "")
            if value:  # 只显示有值的字段
                # 对于经营范围，如果太长则适当截断
                if key == "经营范围" and len(str(value)) > 300:
                    value = str(value)[:300] + "..."
                print(f"  {display_name}: {value}")
                displayed_count += 1
            else:
                print(f"  {display_name}: [空值，不显示]")
        
        print(f"\n📊 GUI显示统计:")
        print(f"  将显示 {displayed_count} 个字段")
        print(f"  空值字段 {len(info_items) - displayed_count} 个")
        
        return displayed_count > 0
        
    except Exception as e:
        print(f"❌ GUI显示模拟失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 开始测试tianyancha_treeview.py...")
    
    # 测试字段映射
    field_test_success = test_field_mapping()
    
    # 测试GUI显示模拟
    gui_test_success = test_gui_display_simulation()
    
    print(f"\n" + "=" * 60)
    print("📋 测试总结:")
    print(f"  字段映射测试: {'✅ 通过' if field_test_success else '❌ 失败'}")
    print(f"  GUI显示测试: {'✅ 通过' if gui_test_success else '❌ 失败'}")
    
    if field_test_success and gui_test_success:
        print(f"\n🎉 所有测试通过！tianyancha_treeview.py应该能正常显示基础信息")
    else:
        print(f"\n💥 测试失败！需要进一步检查问题")
