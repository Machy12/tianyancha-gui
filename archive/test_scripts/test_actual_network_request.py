#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试实际的网络请求，查看获取到的HTML内容
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianyancha_complete_api import TianyanchaAPI

def test_actual_network_request():
    """测试实际的网络请求"""
    
    print("🌐 测试实际网络请求获取HTML内容")
    print("=" * 80)
    
    try:
        # 创建API实例
        api = TianyanchaAPI()
        print("✅ 成功创建TianyanchaAPI实例")
        
        # 先搜索公司获取GID
        company_name = "浙江春风动力股份有限公司"
        print(f"🔍 搜索公司: {company_name}")
        
        search_result = api.search_company(company_name)
        
        if search_result and 'gid' in search_result:
            gid = search_result['gid']
            print(f"✅ 获取到GID: {gid}")
            
            # 获取基本信息（这会保存实际的HTML文件）
            print(f"\n🌐 开始获取基本信息页面...")
            basic_info = api.get_basic_info(gid)
            
            print(f"\n📊 网络请求结果分析:")
            print(f"  提取字段数量: {len(basic_info)}")
            
            if basic_info:
                print(f"  ✅ 成功提取到基本信息")
                print(f"  📋 提取到的字段:")
                for key, value in basic_info.items():
                    if len(str(value)) > 50:
                        print(f"    {key}: {str(value)[:50]}...")
                    else:
                        print(f"    {key}: {value}")
            else:
                print(f"  ❌ 未能提取到基本信息")
                print(f"  💡 请检查保存的HTML文件: debug_actual_page_{gid}.html")
                
                # 检查是否生成了调试文件
                debug_file = f"debug_actual_page_{gid}.html"
                if os.path.exists(debug_file):
                    print(f"  📄 调试文件已生成: {debug_file}")
                    
                    # 读取并分析HTML内容
                    with open(debug_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    print(f"  📊 HTML内容分析:")
                    print(f"    文件大小: {len(html_content)} 字符")
                    
                    # 检查常见的问题标识
                    if "登录" in html_content or "login" in html_content.lower():
                        print(f"    ⚠️  包含登录相关内容")
                    if "验证码" in html_content or "captcha" in html_content.lower():
                        print(f"    ⚠️  包含验证码相关内容")
                    if "访问被拒绝" in html_content or "access denied" in html_content.lower():
                        print(f"    ⚠️  包含访问被拒绝内容")
                    if "index_detail-info-item__oAOqL" in html_content:
                        print(f"    ✅ 包含预期的CSS类名")
                    else:
                        print(f"    ❌ 不包含预期的CSS类名")
                    
                    # 检查页面标题
                    if "<title>" in html_content:
                        title_start = html_content.find("<title>") + 7
                        title_end = html_content.find("</title>", title_start)
                        if title_end > title_start:
                            title = html_content[title_start:title_end]
                            print(f"    📄 页面标题: {title}")
                    
                    # 检查是否包含公司名称
                    if company_name in html_content:
                        print(f"    ✅ 包含公司名称")
                    else:
                        print(f"    ❌ 不包含公司名称")
                else:
                    print(f"  ❌ 调试文件未生成")
            
        else:
            print(f"❌ 搜索公司失败，无法获取GID")
            if search_result:
                print(f"搜索结果: {search_result}")
            
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

def analyze_html_structure():
    """分析HTML结构差异"""
    
    print(f"\n" + "=" * 80)
    print("🔍 分析HTML结构差异")
    print("=" * 80)
    
    # 检查是否有调试文件
    debug_files = [f for f in os.listdir('.') if f.startswith('debug_actual_page_') and f.endswith('.html')]
    
    if debug_files:
        debug_file = debug_files[0]  # 使用第一个找到的调试文件
        print(f"📄 分析文件: {debug_file}")
        
        try:
            with open(debug_file, 'r', encoding='utf-8') as f:
                actual_html = f.read()
            
            # 与测试HTML文件对比
            test_html_file = "2320855868"
            if os.path.exists(test_html_file):
                with open(test_html_file, 'r', encoding='utf-8') as f:
                    test_html = f.read()
                
                print(f"📊 结构对比:")
                print(f"  实际页面大小: {len(actual_html)} 字符")
                print(f"  测试页面大小: {len(test_html)} 字符")
                
                # 检查关键CSS类名
                key_classes = [
                    "index_detail-info-item__oAOqL",
                    "index_detail-label__oRf2J", 
                    "index_detail-text__Ac9Py",
                    "index_company-name__LqKlo",
                    "index_name__dz4jY"
                ]
                
                print(f"  关键CSS类名对比:")
                for css_class in key_classes:
                    in_actual = css_class in actual_html
                    in_test = css_class in test_html
                    status = "✅" if in_actual else "❌"
                    print(f"    {status} {css_class}: 实际页面{'有' if in_actual else '无'}, 测试页面{'有' if in_test else '无'}")
                
            else:
                print(f"❌ 测试HTML文件不存在: {test_html_file}")
                
        except Exception as e:
            print(f"❌ 分析HTML结构时出错: {e}")
    else:
        print(f"❌ 没有找到调试HTML文件")
        print(f"请先运行网络请求测试")

if __name__ == "__main__":
    print("🚀 开始测试实际网络请求...")
    
    # 测试网络请求
    test_actual_network_request()
    
    # 分析HTML结构
    analyze_html_structure()
    
    print(f"\n🏁 测试完成！")
    print(f"💡 如果提取失败，请检查生成的debug_actual_page_*.html文件")
    print(f"💡 对比该文件与测试文件2320855868的结构差异")
