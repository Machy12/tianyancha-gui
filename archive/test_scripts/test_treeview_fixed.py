#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 tianyancha_treeview.py 修复后的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tianyancha_treeview import TianyanchaAPI

def test_treeview_api():
    """测试 tianyancha_treeview.py 中的API功能"""
    print("🚀 开始测试 tianyancha_treeview.py 修复后的功能...")
    print("=" * 80)
    
    try:
        # 使用更新后的cookies创建API实例
        cookies = "CUID=fb5e88e52fd728716c8198eb6ba8ea2a; jsid=SEO-BING-ALL-SY-000001; TYCID=0abfc5307ad811f09f5f8b4d203646f6; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22237696749%22%2C%22first_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk4YjQ2MDUwMjExMzktMDY2Mzk3MzY0YTRlODU0LTI2MDExMDUxLTEzOTUzOTYtMTk4YjQ2MDUwMjI0NjUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIyMzc2OTY3NDkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22237696749%22%7D%2C%22%24device_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2215904922578%22%2C%22userId%22%3A%22237696749%22%7D; tyc-user-info-save-time=1756966779039; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTkwNDkyMjU3OCIsImlhdCI6MTc1Njk2Njc4MywiZXhwIjoxNzU5NTU4NzgzfQ.y0E08y-FkpMHgxVcdF3W0EQG3UQhZpW49DAScvqlgmhwVUgc8BSCQybsWEQ3OpCH1WpLzEp54zoRkjWLiYIYBw; ssuid=7644527464; bannerFlag=true; HWWAFSESID=42b601301cf9cc76a7a; HWWAFSESTIME=1757594260820; csrfToken=Axgtjv95gX1OwqzJf4s7gLbX"

        api = TianyanchaAPI(cookies)
        print("✅ 成功创建TianyanchaAPI实例")
        
        # 测试公司搜索
        company_name = "浙江春风动力股份有限公司"
        print(f"🔍 搜索公司: {company_name}")
        
        search_results = api.search_company(company_name)
        
        if search_results and len(search_results) > 0:
            print(f"✅ 找到 {len(search_results)} 个匹配结果")
            
            # 选择第一个结果
            first_result = search_results[0]
            print(f"📋 选择公司: {first_result.get('name', 'Unknown')}")
            print(f"🆔 公司GID: {first_result.get('gid', 'Unknown')}")
            
            # 获取基本信息
            gid = first_result.get('gid')
            if gid:
                print(f"\n🌐 开始获取基本信息页面...")
                basic_info = api.get_basic_info(gid)
                
                if basic_info:
                    print("✅ 成功获取基本信息")
                    print(f"📊 提取字段数量: {len(basic_info)}")
                    
                    # 显示关键字段
                    key_fields = ['公司名称', '统一社会信用代码', '法定代表人', '经营状态', '注册资本', '成立日期']
                    print("\n📋 关键字段:")
                    for field in key_fields:
                        if field in basic_info:
                            value = basic_info[field]
                            if len(str(value)) > 50:
                                value = str(value)[:50] + "..."
                            print(f"  ✅ {field}: {value}")
                        else:
                            print(f"  ❌ {field}: 未找到")
                    
                    print(f"\n📊 完整字段列表:")
                    for i, (key, value) in enumerate(basic_info.items(), 1):
                        if len(str(value)) > 60:
                            value = str(value)[:60] + "..."
                        print(f"  {i:2d}. {key}: {value}")
                    
                    return True
                else:
                    print("❌ 获取基本信息失败")
                    return False
            else:
                print("❌ 无法获取GID")
                return False
        else:
            print("❌ 搜索结果为空")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🔧 tianyancha_treeview.py 功能测试")
    print("=" * 80)
    
    success = test_treeview_api()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 测试成功！tianyancha_treeview.py 修复完成")
        print("💡 现在可以运行GUI界面测试基本信息显示功能")
    else:
        print("❌ 测试失败，请检查cookies和请求头设置")
        print("💡 可能需要进一步更新cookies或检查网络连接")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
