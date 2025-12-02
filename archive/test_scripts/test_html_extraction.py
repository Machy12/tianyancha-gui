#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试HTML提取脚本
用于分析天眼查页面HTML结构变化
"""

from bs4 import BeautifulSoup
import re

def analyze_html_structure(html_file):
    """分析HTML结构，提取基本信息"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    print("🔍 开始分析HTML结构...")
    print("=" * 60)
    
    # 分析公司名称
    print("\n📋 公司名称提取:")
    name_elem = soup.find('h1', class_='index_company-name__LqKlo')
    if name_elem:
        name_span = name_elem.find('span', class_='index_name__dz4jY')
        if name_span:
            company_name = name_span.get_text(strip=True)
            print(f"✅ 找到公司名称: {company_name}")
        else:
            print("❌ 未找到公司名称span")
    else:
        print("❌ 未找到公司名称h1元素")
    
    # 分析统一社会信用代码
    print("\n🆔 统一社会信用代码提取:")
    credit_code_elem = soup.find('span', class_='index_detail-credit-code__fH1Ny')
    if credit_code_elem:
        code_span = credit_code_elem.find('span')
        if code_span:
            credit_code = code_span.get_text(strip=True)
            print(f"✅ 找到统一社会信用代码: {credit_code}")
        else:
            print("❌ 未找到信用代码span")
    else:
        print("❌ 未找到信用代码元素")
    
    # 分析法定代表人
    print("\n👤 法定代表人提取:")
    legal_person_elem = soup.find('div', class_='index_legal-person-root__THrdz')
    if legal_person_elem:
        link_elem = legal_person_elem.find('a', class_='index_link-click__NmHxP')
        if link_elem:
            legal_person = link_elem.get_text(strip=True)
            print(f"✅ 找到法定代表人: {legal_person}")
        else:
            print("❌ 未找到法定代表人链接")
    else:
        print("❌ 未找到法定代表人元素")
    
    # 分析详细信息项
    print("\n📊 详细信息项提取:")
    detail_items = soup.find_all('div', class_='index_detail-info-item__oAOqL')
    print(f"找到 {len(detail_items)} 个详细信息项")
    
    extracted_info = {}
    
    for i, item in enumerate(detail_items):
        label_elem = item.find('span', class_='index_detail-label__oRf2J')
        if label_elem:
            label_text = label_elem.get_text(strip=True)
            print(f"  项目 {i+1}: {label_text}")
            
            # 根据标签提取对应的值
            if '注册资本' in label_text:
                value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                if value_elem:
                    value = value_elem.get_text(strip=True)
                    extracted_info['注册资本'] = value
                    print(f"    ✅ 值: {value}")
                    
            elif '成立日期' in label_text:
                value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                if value_elem:
                    value = value_elem.get_text(strip=True)
                    extracted_info['成立日期'] = value
                    print(f"    ✅ 值: {value}")
                    
            elif '电话' in label_text:
                # 电话可能有多种格式
                tel_elem = item.find('span', class_='index_detail-tel__fgpsE')
                if tel_elem:
                    value = tel_elem.get_text(strip=True)
                    extracted_info['联系电话'] = value
                    print(f"    ✅ 值: {value}")
                else:
                    print("    ❌ 未找到电话值")
                    
            elif '邮箱' in label_text:
                email_elem = item.find('a', class_='index_detail-email__B_1Tq')
                if email_elem:
                    value = email_elem.get_text(strip=True)
                    extracted_info['邮箱'] = value
                    print(f"    ✅ 值: {value}")
                else:
                    print("    ❌ 未找到邮箱值")
                    
            elif '网址' in label_text:
                website_elem = item.find('a', class_='index_detail-website__n2yst')
                if website_elem:
                    value = website_elem.get_text(strip=True)
                    extracted_info['网址'] = value
                    print(f"    ✅ 值: {value}")
                else:
                    print("    ❌ 未找到网址值")
                    
            elif '地址' in label_text:
                # 地址提取的新逻辑
                address_elem = item.find('span', class_='index_detail-address-moretext__9R_Z1')
                if address_elem:
                    address_span = address_elem.find('span', class_='index_inline-flex__QLDiW')
                    if address_span:
                        value = address_span.get_text(strip=True)
                        extracted_info['注册地址'] = value
                        print(f"    ✅ 值: {value}")
                    else:
                        print("    ❌ 未找到地址内部span")
                else:
                    # 备用选择器
                    address_elem = item.find('span', class_='index_inline-flex__QLDiW')
                    if address_elem:
                        value = address_elem.get_text(strip=True)
                        # 过滤掉标签文本
                        if value and '地址：' not in value and len(value) > 10:
                            extracted_info['注册地址'] = value
                            print(f"    ✅ 值: {value}")
                        else:
                            print(f"    ❌ 地址值无效: {value}")
                    else:
                        print("    ❌ 未找到地址值")
                    
            elif '国标行业' in label_text:
                value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                if value_elem:
                    value = value_elem.get_text(strip=True)
                    extracted_info['所属行业'] = value
                    print(f"    ✅ 值: {value}")
                else:
                    print("    ❌ 未找到行业值")
                    
            elif '企业规模' in label_text:
                value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                if value_elem:
                    value = value_elem.get_text(strip=True)
                    extracted_info['企业规模'] = value
                    print(f"    ✅ 值: {value}")
                else:
                    print("    ❌ 未找到企业规模值")
                    
            elif '员工人数' in label_text:
                value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                if value_elem:
                    value = value_elem.get_text(strip=True)
                    extracted_info['员工人数'] = value
                    print(f"    ✅ 值: {value}")
                else:
                    print("    ❌ 未找到员工人数值")
    
    # 分析经营状态
    print("\n📈 经营状态提取:")
    status_elem = soup.find('div', class_='index_company-tag__ZcJFV index_header-company-tag__WaTgu')
    if status_elem:
        status = status_elem.get_text(strip=True)
        extracted_info['经营状态'] = status
        print(f"✅ 找到经营状态: {status}")
    else:
        # 尝试其他选择器
        status_elem = soup.find('div', class_='index_reg-status-tag__ES7dF')
        if status_elem:
            tag_elem = status_elem.find('div', class_='index_company-tag__ZcJFV')
            if tag_elem:
                status = tag_elem.get_text(strip=True)
                extracted_info['经营状态'] = status
                print(f"✅ 找到经营状态(备用): {status}")
            else:
                print("❌ 未找到经营状态标签")
        else:
            print("❌ 未找到经营状态")
    
    # 输出提取结果汇总
    print("\n" + "=" * 60)
    print("📋 提取结果汇总:")
    print("=" * 60)
    
    if company_name:
        extracted_info['公司名称'] = company_name
    if credit_code:
        extracted_info['统一社会信用代码'] = credit_code
    if legal_person:
        extracted_info['法定代表人'] = legal_person
    
    for key, value in extracted_info.items():
        print(f"  {key}: {value}")
    
    print(f"\n✅ 总共提取到 {len(extracted_info)} 个字段")
    
    return extracted_info

if __name__ == "__main__":
    # 分析HTML文件
    html_file = "2320855868"  # 当前HTML文件
    
    try:
        result = analyze_html_structure(html_file)
        print(f"\n🎉 分析完成！提取到 {len(result)} 个字段")
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
