#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天眼查完整API集成工具
整合搜索、基本信息、股东信息、工商变更、主要人员的完整解决方案
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import sys

class TianyanchaAPI:
    def __init__(self):
        """初始化天眼查API客户端"""
        self.session = requests.Session()
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6",
            "connection": "keep-alive",
            "content-type": "application/json",
            "cookie": "CUID=fb5e88e52fd728716c8198eb6ba8ea2a; jsid=SEO-BING-ALL-SY-000001; TYCID=0abfc5307ad811f09f5f8b4d203646f6; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22237696749%22%2C%22first_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk4YjQ2MDUwMjExMzktMDY2Mzk3MzY0YTRlODU0LTI2MDExMDUxLTEzOTUzOTYtMTk4YjQ2MDUwMjI0NjUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIyMzc2OTY3NDkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22237696749%22%7D%2C%22%24device_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2215904922578%22%2C%22userId%22%3A%22237696749%22%7D; tyc-user-info-save-time=1756966779039; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTkwNDkyMjU3OCIsImlhdCI6MTc1Njk2Njc4MywiZXhwIjoxNzU5NTU4NzgzfQ.y0E08y-FkpMHgxVcdF3W0EQG3UQhZpW49DAScvqlgmhwVUgc8BSCQybsWEQ3OpCH1WpLzEp54zoRkjWLiYIYBw; ssuid=7644527464; bannerFlag=true; HWWAFSESID=42b601301cf9cc76a7a; HWWAFSESTIME=1757594260820; csrfToken=Axgtjv95gX1OwqzJf4s7gLbX",
            "host": "capi.tianyancha.com",
            "origin": "https://www.tianyancha.com",
            "referer": "https://www.tianyancha.com/",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "version": "TYC-Web",
            "x-tycid": "0abfc5307ad811f09f5f8b4d203646f6"
        }
        
        # 初始化session
        self._init_session()
    
    def _init_session(self):
        """初始化session，访问主页"""
        try:
            home_response = self.session.get("https://www.tianyancha.com/", timeout=10)
            if home_response.status_code == 200:
                print("✅ Session初始化成功")
            else:
                print(f"⚠️ Session初始化异常: {home_response.status_code}")
        except Exception as e:
            print(f"⚠️ Session初始化出错: {e}")
    
    def search_company(self, company_name):
        """
        搜索公司获取基本信息
        
        Args:
            company_name (str): 公司名称
        
        Returns:
            dict: 搜索结果信息
        """
        print(f"🔍 第一步：搜索公司 - {company_name}")
        
        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/cloud-tempest/search/suggest/company/main?_={timestamp}"
        
        payload = {"keyword": company_name}
        
        try:
            response = self.session.post(url, json=payload, headers=self.base_headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    company_list = data.get('companySuggestList', [])
                    
                    if company_list:
                        print(f"✅ 找到 {len(company_list)} 个匹配结果")
                        
                        first_company = company_list[0]
                        search_info = {
                            'gid': str(first_company.get('id', '')),
                            'graphId': str(first_company.get('graphId', '')),
                            'name': first_company.get('comName', ''),
                            'alias': first_company.get('alias', ''),
                            'taxCode': first_company.get('taxCode', ''),
                            'regStatus': first_company.get('regStatus', 0)
                        }
                        
                        print(f"📋 选择公司: {search_info['name']}")
                        print(f"🆔 公司GID: {search_info['gid']}")
                        
                        return search_info
                    else:
                        print("❌ 未找到匹配的公司")
                        return None
                else:
                    print(f"❌ 搜索API返回错误: {result.get('message', '未知错误')}")
                    return None
            else:
                print(f"❌ 搜索请求失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 搜索时出错: {e}")
            return None
    
    def get_basic_info(self, gid):
        """
        获取基本信息（从HTML页面）
        
        Args:
            gid (str): 公司GID
        
        Returns:
            dict: 基本信息
        """
        print(f"\n🏢 第二步：获取基本信息 - GID: {gid}")
        
        url = f"https://www.tianyancha.com/company/{gid}"
        
        html_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6",
            "cache-control": "max-age=0",
            "connection": "keep-alive",
            "cookie": "CUID=fb5e88e52fd728716c8198eb6ba8ea2a; jsid=SEO-BING-ALL-SY-000001; TYCID=0abfc5307ad811f09f5f8b4d203646f6; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22237696749%22%2C%22first_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk4YjQ2MDUwMjExMzktMDY2Mzk3MzY0YTRlODU0LTI2MDExMDUxLTEzOTUzOTYtMTk4YjQ2MDUwMjI0NjUiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIyMzc2OTY3NDkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22237696749%22%7D%2C%22%24device_id%22%3A%22198b4605021139-066397364a4e854-26011051-1395396-198b4605022465%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2215904922578%22%2C%22userId%22%3A%22237696749%22%7D; tyc-user-info-save-time=1756966779039; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTkwNDkyMjU3OCIsImlhdCI6MTc1Njk2Njc4MywiZXhwIjoxNzU5NTU4NzgzfQ.y0E08y-FkpMHgxVcdF3W0EQG3UQhZpW49DAScvqlgmhwVUgc8BSCQybsWEQ3OpCH1WpLzEp54zoRkjWLiYIYBw; ssuid=7644527464; bannerFlag=true; HWWAFSESID=42b601301cf9cc76a7a; HWWAFSESTIME=1757594260820; csrfToken=Axgtjv95gX1OwqzJf4s7gLbX",
            "host": "www.tianyancha.com",
            "referer": "https://www.tianyancha.com/",
            "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
        
        try:
            response = self.session.get(url, headers=html_headers, timeout=15)
            
            if response.status_code == 200:
                print("✅ 成功获取基本信息页面")

                # 保存HTML文件用于调试
                debug_filename = f"debug_actual_page_{gid}.html"
                with open(debug_filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"💾 已保存实际HTML页面: {debug_filename}")
                print(f"📄 HTML页面大小: {len(response.text)} 字符")

                # 检查页面内容类型
                if "登录" in response.text or "login" in response.text.lower():
                    print("⚠️  检测到登录页面，可能需要更新cookies")
                elif "验证" in response.text or "captcha" in response.text.lower():
                    print("⚠️  检测到验证码页面，可能触发了反爬虫")
                elif "访问被拒绝" in response.text or "access denied" in response.text.lower():
                    print("⚠️  检测到访问被拒绝页面")

                soup = BeautifulSoup(response.text, 'html.parser')
                basic_info = self._extract_basic_info_from_html(soup)

                print(f"📊 最终提取结果: {len(basic_info)} 个字段")
                if basic_info:
                    print("✅ 成功提取到基本信息")
                else:
                    print("❌ 未能提取到任何基本信息，请检查保存的HTML文件")

                return basic_info
            else:
                print(f"❌ 获取基本信息失败: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ 获取基本信息时出错: {e}")
            return {}
    
    def get_shareholders_info(self, gid):
        """
        获取股东信息
        
        Args:
            gid (str): 公司GID
        
        Returns:
            list: 股东信息列表
        """
        print(f"\n👥 第三步：获取股东信息 - GID: {gid}")
        
        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/cloud-company-background/companyV2/dim/holder/latest/announcement?_={timestamp}"
        
        payload = {
            "benefitSharesType": 1,
            "gid": gid,
            "historyType": None,
            "keyword": "",
            "pageNum": 1,
            "pageSize": 50,
            "percentLevel": "-100",
            "_unUseParam": 0
        }
        
        try:
            response = self.session.post(url, json=payload, headers=self.base_headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    holders = data.get('result', [])
                    
                    shareholders = []
                    for holder in holders:
                        # 使用更准确的字段名
                        shareholder_name = holder.get('shareHolderName', '') or holder.get('name', '')
                        percent = holder.get('percent', '')
                        total_capital = holder.get('totalCapital', '') or holder.get('amount', '')
                        shareholder_type = holder.get('shareHolderTypeOnPage', '')

                        shareholder_info = {
                            '股东名称': shareholder_name,
                            '持股比例': percent,
                            '认缴出资额': total_capital,
                            '股东类型': shareholder_type,
                            '股东ID': holder.get('shareHolderGid', ''),
                            '别名': holder.get('alias', '')
                        }
                        shareholders.append(shareholder_info)
                    
                    print(f"✅ 获取到 {len(shareholders)} 个股东信息")
                    return shareholders
                else:
                    print(f"❌ 股东信息API返回错误: {result.get('message', '未知错误')}")
                    return []
            else:
                print(f"❌ 获取股东信息失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 获取股东信息时出错: {e}")
            return []
    
    def get_business_changes(self, gid):
        """
        获取工商变更信息
        
        Args:
            gid (str): 公司GID
        
        Returns:
            list: 工商变更信息列表
        """
        print(f"\n📋 第四步：获取工商变更信息 - GID: {gid}")
        
        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/tyc-enterprise-monitor/monitor/brief/dynamic/list?_={timestamp}"
        
        payload = {
            "gid": gid,
            "entityType": 1
        }
        
        try:
            response = self.session.post(url, json=payload, headers=self.base_headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    changes = data.get('list', [])
                    
                    business_changes = []
                    for change in changes[:10]:  # 只取前10条
                        # 从textList中提取变更内容
                        change_text = ""
                        text_list = change.get('textList', [])
                        if text_list:
                            change_text = text_list[0].get('text', '')

                        change_info = {
                            '变更日期': change.get('dynamicDate', ''),
                            '变更类型': change.get('eventType', ''),
                            '变更内容': change_text,
                            '风险等级': change.get('riskLevel', ''),
                            'UUID': change.get('uuid', '')
                        }
                        business_changes.append(change_info)
                    
                    print(f"✅ 获取到 {len(business_changes)} 条工商变更信息")
                    return business_changes
                else:
                    print(f"❌ 工商变更API返回错误: {result.get('message', '未知错误')}")
                    return []
            else:
                print(f"❌ 获取工商变更信息失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 获取工商变更信息时出错: {e}")
            return []
    
    def get_key_personnel(self, gid):
        """
        获取主要人员信息

        Args:
            gid (str): 公司GID

        Returns:
            list: 主要人员信息列表
        """
        print(f"\n👤 第五步：获取主要人员信息 - GID: {gid}")

        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/cloud-company-background/company/dim/staff/announcement?_={timestamp}&gid={gid}&pageSize=20&pageNum=1&stockType=0"

        try:
            response = self.session.get(url, headers=self.base_headers, timeout=10)

            if response.status_code == 200:
                result = response.json()

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    staff_list = data.get('result', [])

                    personnel = []
                    for staff in staff_list:
                        # 使用更准确的字段名
                        name = staff.get('name', '') or staff.get('personName', '')
                        position = staff.get('typeJoin', '') or staff.get('position', '')
                        staff_type = staff.get('type', '')

                        person_info = {
                            '姓名': name,
                            '职位': position,
                            '类型': staff_type,
                            '人员ID': staff.get('id', ''),
                            '股份类型': staff.get('stockType', '')
                        }
                        personnel.append(person_info)

                    print(f"✅ 获取到 {len(personnel)} 个主要人员信息")
                    return personnel
                else:
                    print(f"❌ 主要人员API返回错误: {result.get('message', '未知错误')}")
                    return []
            else:
                print(f"❌ 获取主要人员信息失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ 获取主要人员信息时出错: {e}")
            return []

    def get_investment_info(self, gid):
        """
        获取对外投资信息

        Args:
            gid (str): 公司GID

        Returns:
            list: 对外投资信息列表
        """
        print(f"\n💰 第六步：获取对外投资信息 - GID: {gid}")

        timestamp = int(time.time() * 1000)
        url = f"https://capi.tianyancha.com/cloud-company-background/company/investListV2?_={timestamp}"

        # 根据您提供的请求信息构建载荷
        payload = {
            "gid": gid,
            "pageSize": 20,
            "pageNum": 1,
            "province": -100,
            "percentLevel": "-100",
            "sortField": "estiblishTime",
            "sortType": -1
        }

        try:
            response = self.session.post(url, json=payload, headers=self.base_headers, timeout=10)

            if response.status_code == 200:
                result = response.json()

                if result.get('state') == 'ok' and 'data' in result:
                    data = result['data']
                    invest_list = data.get('result', [])

                    investments = []
                    for invest in invest_list:
                        investment_info = {
                            '被投资企业名称': invest.get('name', ''),
                            '投资比例': f"{invest.get('percent', 0)}%" if invest.get('percent') else '',
                            '投资金额': invest.get('amount', ''),
                            '成立日期': invest.get('estiblishTime', ''),
                            '经营状态': invest.get('regStatus', ''),
                            '企业类型': invest.get('categoryStr', ''),
                            '注册资本': invest.get('regCapital', ''),
                            '被投资企业ID': invest.get('id', '')
                        }
                        investments.append(investment_info)

                    print(f"✅ 获取到 {len(investments)} 个对外投资信息")
                    return investments
                else:
                    print(f"❌ 对外投资API返回错误: {result.get('message', '未知错误')}")
                    return []
            else:
                print(f"❌ 获取对外投资信息失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ 获取对外投资信息时出错: {e}")
            return []

    def _extract_basic_info_from_html(self, soup):
        """
        从HTML中提取基本信息 - 使用最新的优化逻辑

        Args:
            soup: BeautifulSoup对象

        Returns:
            dict: 基本信息
        """
        info = {}

        try:
            print("🔍 开始提取基本信息...")

            # 1. 公司名称
            name_elem = soup.find('h1', class_='index_company-name__LqKlo')
            if name_elem:
                name_span = name_elem.find('span', class_='index_name__dz4jY')
                if name_span:
                    info['公司名称'] = name_span.get_text(strip=True)
                    print(f"✅ 公司名称: {info['公司名称']}")

            # 如果上面没找到，尝试其他选择器
            if '公司名称' not in info:
                name_elem = soup.find('h1')
                if name_elem:
                    info['公司名称'] = name_elem.get_text(strip=True)
                    print(f"✅ 公司名称(备用): {info['公司名称']}")

            # 2. 统一社会信用代码
            credit_code_elem = soup.find('span', class_='index_detail-credit-code__fH1Ny')
            if credit_code_elem:
                code_span = credit_code_elem.find('span')
                if code_span:
                    info['统一社会信用代码'] = code_span.get_text(strip=True)
                    print(f"✅ 统一社会信用代码: {info['统一社会信用代码']}")

            # 3. 法定代表人
            legal_person_elem = soup.find('div', class_='index_legal-person-root__THrdz')
            if legal_person_elem:
                link_elem = legal_person_elem.find('a', class_='index_link-click__NmHxP')
                if link_elem:
                    info['法定代表人'] = link_elem.get_text(strip=True)
                    print(f"✅ 法定代表人: {info['法定代表人']}")

            # 4. 经营状态
            status_elem = soup.find('div', class_='index_company-tag__ZcJFV index_header-company-tag__WaTgu')
            if status_elem:
                info['经营状态'] = status_elem.get_text(strip=True)
                print(f"✅ 经营状态: {info['经营状态']}")
            else:
                # 尝试其他选择器
                status_elem = soup.find('div', class_='index_reg-status-tag__ES7dF')
                if status_elem:
                    tag_elem = status_elem.find('div', class_='index_company-tag__ZcJFV')
                    if tag_elem:
                        info['经营状态'] = tag_elem.get_text(strip=True)
                        print(f"✅ 经营状态(备用): {info['经营状态']}")

            # 5. 详细信息项提取
            print("📊 开始提取详细信息项...")
            detail_items = soup.find_all('div', class_='index_detail-info-item__oAOqL')
            print(f"找到 {len(detail_items)} 个详细信息项")

            for item in detail_items:
                label_elem = item.find('span', class_='index_detail-label__oRf2J')
                if label_elem:
                    label_text = label_elem.get_text(strip=True)

                    if '注册资本' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['注册资本'] = value_elem.get_text(strip=True)
                            print(f"✅ 注册资本: {info['注册资本']}")

                    elif '成立日期' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['成立日期'] = value_elem.get_text(strip=True)
                            print(f"✅ 成立日期: {info['成立日期']}")

                    elif '电话' in label_text:
                        # 电话的新选择器
                        tel_elem = item.find('span', class_='index_detail-tel__fgpsE')
                        if tel_elem:
                            info['联系电话'] = tel_elem.get_text(strip=True)
                            print(f"✅ 联系电话: {info['联系电话']}")
                        else:
                            # 备用选择器
                            value_elem = item.find('span', class_='link-hover-click')
                            if value_elem:
                                info['联系电话'] = value_elem.get_text(strip=True)
                                print(f"✅ 联系电话(备用): {info['联系电话']}")

                    elif '邮箱' in label_text:
                        email_elem = item.find('a', class_='index_detail-email__B_1Tq')
                        if email_elem:
                            info['邮箱'] = email_elem.get_text(strip=True)
                            print(f"✅ 邮箱: {info['邮箱']}")

                    elif '网址' in label_text:
                        website_elem = item.find('a', class_='index_detail-website__n2yst')
                        if website_elem:
                            info['网址'] = website_elem.get_text(strip=True)
                            print(f"✅ 网址: {info['网址']}")

                    elif '地址' in label_text:
                        # 地址提取的优化逻辑
                        address_elem = item.find('span', class_='index_detail-address-moretext__9R_Z1')
                        if address_elem:
                            address_span = address_elem.find('span', class_='index_inline-flex__QLDiW')
                            if address_span:
                                info['注册地址'] = address_span.get_text(strip=True)
                                print(f"✅ 注册地址: {info['注册地址']}")
                        else:
                            # 备用选择器
                            address_elem = item.find('span', class_='index_inline-flex__QLDiW')
                            if address_elem:
                                address_text = address_elem.get_text(strip=True)
                                # 过滤掉标签文本
                                if address_text and '地址：' not in address_text and len(address_text) > 10:
                                    info['注册地址'] = address_text
                                    print(f"✅ 注册地址(备用): {info['注册地址']}")

                    elif '国标行业' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['所属行业'] = value_elem.get_text(strip=True)
                            print(f"✅ 所属行业: {info['所属行业']}")

                    elif '企业规模' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['企业规模'] = value_elem.get_text(strip=True)
                            print(f"✅ 企业规模: {info['企业规模']}")

                    elif '员工人数' in label_text:
                        value_elem = item.find('span', class_='index_detail-text__Ac9Py')
                        if value_elem:
                            info['员工人数'] = value_elem.get_text(strip=True)
                            print(f"✅ 员工人数: {info['员工人数']}")

            # 6. 从表格中提取更多信息（经营范围、英文名称、登记机关等）
            print("📋 开始从表格提取更多信息...")
            business_scope = None

            table_rows = soup.find_all('tr')
            for row in table_rows:
                cells = row.find_all('td')
                for i, cell in enumerate(cells):
                    cell_text = cell.get_text(strip=True)

                    if '经营范围' in cell_text and i + 1 < len(cells):
                        scope_cell = cells[i + 1]
                        copy_text_elem = scope_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            business_scope = copy_text_elem.get_text(strip=True)
                            print(f"✅ 经营范围: {business_scope[:100]}...")
                        else:
                            # 尝试直接获取单元格文本
                            scope_text = scope_cell.get_text(strip=True)
                            if scope_text and len(scope_text) > 20:
                                business_scope = scope_text
                                print(f"✅ 经营范围(备用): {business_scope[:100]}...")

                    elif '注册地址' in cell_text and i + 1 < len(cells) and '注册地址' not in info:
                        addr_cell = cells[i + 1]
                        copy_text_elem = addr_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['注册地址'] = copy_text_elem.get_text(strip=True)
                            print(f"✅ 注册地址(表格): {info['注册地址']}")
                        else:
                            addr_text = addr_cell.get_text(strip=True)
                            if addr_text and len(addr_text) > 10:
                                info['注册地址'] = addr_text
                                print(f"✅ 注册地址(表格备用): {info['注册地址']}")

                    elif '英文名称' in cell_text and i + 1 < len(cells):
                        en_cell = cells[i + 1]
                        copy_text_elem = en_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['英文名称'] = copy_text_elem.get_text(strip=True)
                            print(f"✅ 英文名称: {info['英文名称']}")
                        else:
                            en_text = en_cell.get_text(strip=True)
                            if en_text and len(en_text) > 5:
                                info['英文名称'] = en_text
                                print(f"✅ 英文名称(备用): {info['英文名称']}")

                    elif '登记机关' in cell_text and i + 1 < len(cells):
                        reg_cell = cells[i + 1]
                        copy_text_elem = reg_cell.find('span', class_='index_copy-text__ri7W6')
                        if copy_text_elem:
                            info['登记机关'] = copy_text_elem.get_text(strip=True)
                            print(f"✅ 登记机关: {info['登记机关']}")
                        else:
                            reg_text = reg_cell.get_text(strip=True)
                            if reg_text and len(reg_text) > 5:
                                info['登记机关'] = reg_text
                                print(f"✅ 登记机关(备用): {info['登记机关']}")

            # 7. 如果经营范围还没找到，尝试其他方法
            if not business_scope:
                print("🔍 尝试其他方法提取经营范围...")

                # 方法1：查找简介中的经营范围
                intro_elem = soup.find('div', class_='introduceRich_collapse-left__5Vvd5')
                if intro_elem:
                    intro_text = intro_elem.get_text(strip=True)
                    if len(intro_text) > 100:  # 简介通常比较长
                        business_scope = intro_text
                        print(f"✅ 经营范围(简介): {business_scope[:100]}...")

                # 方法2：查找其他可能的选择器
                if not business_scope:
                    scope_elems = soup.find_all('div', string=re.compile(r'经营范围'))
                    for elem in scope_elems:
                        parent = elem.parent
                        if parent:
                            text_elem = parent.find_next('span') or parent.find_next('div')
                            if text_elem:
                                scope_text = text_elem.get_text(strip=True)
                                if len(scope_text) > 50:
                                    business_scope = scope_text
                                    print(f"✅ 经营范围(其他): {business_scope[:100]}...")
                                    break

            if business_scope:
                info['经营范围'] = business_scope

            # 8. 输出提取结果汇总
            print(f"\n📊 提取完成，共获得 {len(info)} 个字段:")
            for key, value in info.items():
                if key == '经营范围' and len(str(value)) > 100:
                    print(f"  {key}: {str(value)[:100]}...")
                else:
                    print(f"  {key}: {value}")

            return info

        except Exception as e:
            print(f"❌ HTML解析错误: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def get_complete_company_info(self, company_name):
        """
        获取完整的公司信息

        Args:
            company_name (str): 公司名称

        Returns:
            dict: 完整的公司信息
        """
        print("🏢 天眼查完整信息获取工具")
        print("=" * 60)
        print(f"🔍 目标公司: {company_name}")
        print("=" * 60)

        # 第一步：搜索公司
        search_info = self.search_company(company_name)
        if not search_info:
            print("❌ 搜索失败，流程结束")
            return None

        gid = search_info['gid']

        # 第二步：获取基本信息
        basic_info = self.get_basic_info(gid)

        # 如果HTML解析没有获取到公司名称，使用搜索信息中的名称
        if not basic_info.get('公司名称') or basic_info.get('公司名称') == '天眼查-商业查询平台':
            basic_info['公司名称'] = search_info['name']

        # 从搜索信息中补充统一社会信用代码
        if not basic_info.get('统一社会信用代码') and search_info.get('taxCode'):
            basic_info['统一社会信用代码'] = search_info['taxCode']

        # 第三步：获取股东信息
        shareholders = self.get_shareholders_info(gid)

        # 第四步：获取工商变更信息
        business_changes = self.get_business_changes(gid)

        # 第五步：获取主要人员信息
        key_personnel = self.get_key_personnel(gid)

        # 从主要人员中补充法定代表人信息
        if not basic_info.get('法定代表人') and key_personnel:
            for person in key_personnel:
                positions = person.get('职位', [])
                if isinstance(positions, list):
                    # 查找董事长或总经理
                    if '董事长' in positions or '总经理' in positions:
                        basic_info['法定代表人'] = person.get('姓名', '')
                        break

        # 第六步：获取对外投资信息
        investments = self.get_investment_info(gid)

        # 整合所有信息
        complete_info = {
            "搜索信息": search_info,
            "基本信息": basic_info,
            "股东信息": shareholders,
            "工商变更": business_changes,
            "主要人员": key_personnel,
            "对外投资": investments,
            "提取时间": time.strftime("%Y-%m-%d %H:%M:%S"),
            "数据来源": "天眼查API"
        }

        return complete_info

def main():
    """
    主函数
    """
    import argparse

    parser = argparse.ArgumentParser(description='天眼查完整API工具 - 获取公司全面信息')
    parser.add_argument('company_name', nargs='?', default="哈尔滨鼎晟恒泰投资管理有限公司",
                       help='要查询的公司名称')

    args = parser.parse_args()

    # 创建API客户端
    api_client = TianyanchaAPI()

    # 获取完整信息
    complete_info = api_client.get_complete_company_info(args.company_name)

    if complete_info:
        print(f"\n🎉 信息获取完成!")
        print("=" * 60)

        # 显示摘要信息
        basic_info = complete_info.get('基本信息', {})
        shareholders = complete_info.get('股东信息', [])
        business_changes = complete_info.get('工商变更', [])
        key_personnel = complete_info.get('主要人员', [])
        investments = complete_info.get('对外投资', [])

        print("📋 信息摘要:")
        print(f"  公司名称: {basic_info.get('公司名称', '未知')}")
        print(f"  法定代表人: {basic_info.get('法定代表人', '未知')}")
        print(f"  注册资本: {basic_info.get('注册资本', '未知')}")
        print(f"  股东数量: {len(shareholders)}")
        print(f"  工商变更: {len(business_changes)} 条")
        print(f"  主要人员: {len(key_personnel)} 人")
        print(f"  对外投资: {len(investments)} 家企业")

        # 保存完整信息
        timestamp = int(time.time())
        gid = complete_info['搜索信息']['gid']

        json_filename = f"tianyancha_complete_{gid}_{timestamp}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(complete_info, f, ensure_ascii=False, indent=2)

        print(f"\n💾 完整信息已保存到: {json_filename}")

        # 保存简化的文本版本
        txt_filename = f"tianyancha_summary_{gid}_{timestamp}.txt"
        with open(txt_filename, "w", encoding="utf-8") as f:
            f.write(f"天眼查公司完整信息 - {args.company_name}\n")
            f.write("=" * 60 + "\n\n")

            f.write("基本信息:\n")
            for key, value in basic_info.items():
                f.write(f"  {key}: {value}\n")

            f.write(f"\n股东信息 ({len(shareholders)} 个):\n")
            for i, shareholder in enumerate(shareholders, 1):
                f.write(f"  {i}. {shareholder.get('股东名称', '')} - {shareholder.get('持股比例', '')}\n")

            f.write(f"\n主要人员 ({len(key_personnel)} 人):\n")
            for i, person in enumerate(key_personnel, 1):
                f.write(f"  {i}. {person.get('姓名', '')} - {person.get('职位', '')}\n")

            f.write(f"\n对外投资 ({len(investments)} 家企业):\n")
            for i, investment in enumerate(investments, 1):
                f.write(f"  {i}. {investment.get('被投资企业名称', '')} - {investment.get('投资比例', '')}\n")

            f.write(f"\n工商变更 ({len(business_changes)} 条):\n")
            for i, change in enumerate(business_changes, 1):
                f.write(f"  {i}. {change.get('变更日期', '')} - {change.get('变更类型', '')}\n")
                if change.get('变更内容'):
                    f.write(f"     {change.get('变更内容', '')}\n")

        print(f"📄 摘要信息已保存到: {txt_filename}")

    else:
        print("❌ 信息获取失败")

if __name__ == "__main__":
    main()
