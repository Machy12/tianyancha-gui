#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天眼查股东穿透查询工具
基于现有API实现多层股东穿透功能
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import sys
import random
from collections import defaultdict, deque
class TianyanchaPenetrationAPI:
    def __init__(self):
        """初始化天眼查股东穿透API客户端"""
        self.session = requests.Session()
        self.base_headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6",
            "connection": "keep-alive",
            "content-type": "application/json",
            "cookie": "CUID=62b3804415cb2ef97572b27cdb7c519c; TYCID=e7f47650f4e911efa23e1f6dbaa18f88; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1740647092; HWWAFSESID=40c29112c61098450cf; HWWAFSESTIME=1755375185394; csrfToken=R8gKyDTjSz45Lx-d9M_0CKPb; ssuid=4092267612; bannerFlag=true; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22237696749%22%2C%22first_id%22%3A%2219546a6ce6d75a-0612ae99879ecc-26011a51-1382400-19546a6ce6e1244%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.bing.com%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk1NDZhNmNlNmQ3NWEtMDYxMmFlOTk4NzllY2MtMjYwMTFhNTEtMTM4MjQwMC0xOTU0NmE2Y2U2ZTEyNDQiLCIkaWRlbnRpdHlfbG9naW5faWQiOiIyMzc2OTY3NDkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22237696749%22%7D%2C%22%24device_id%22%3A%2219546a6ce6d75a-0612ae99879ecc-26011a51-1382400-19546a6ce6e1244%22%7D; tyc-user-info={%22state%22:%220%22%2C%22vipManager%22:%220%22%2C%22mobile%22:%2215904922578%22%2C%22userId%22:%22237696749%22}; tyc-user-info-save-time=1755375251805; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTkwNDkyMjU3OCIsImlhdCI6MTc1NTM3NTI1MSwiZXhwIjoxNzU3OTY3MjUxfQ.1zIzw4KvTX6t1MovGzUrigh7pnZaEc708q1jyHOpGzLNfFiHl86P5DP0qxx5SJIC6qMHBRBo4ZG6Q-StF0BFoA; tyc-user-phone=%255B%252215904922578%2522%255D",
            "host": "capi.tianyancha.com",
            "origin": "https://www.tianyancha.com",
            "referer": "https://www.tianyancha.com/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "version": "TYC-Web",
            "x-tycid": "e7f47650f4e911efa23e1f6dbaa18f88"
        }
        
        # 穿透查询相关配置
        self.visited_companies = set()  # 防止循环查询
        self.penetration_results = {}   # 存储穿透结果
        self.max_depth = None            # 深度不固定；仅作兜底（None 表示不限）
        self.delay_between_requests = 1 # 兼容旧参数：固定请求间隔（秒），若设置了范围将被忽略
        self.min_delay = 0.5            # 随机最小延迟（秒）
        self.max_delay = 2.5            # 随机最大延迟（秒），强制不超过3秒

        # 终止关键词（可通过命令行追加/文件覆盖）
        self.overseas_indicators = [
            # 香港相关
            "香港", "Hong Kong", "HK", "港",
            # 开曼相关
            "开曼", "Cayman", "开曼群岛",
            # 英属维尔京群岛
            "BVI", "British Virgin", "维尔京",
            # 新加坡
            "新加坡", "Singapore", "SG",
            # 其他常见离岸地
            "百慕大", "Bermuda", "毛里求斯", "Mauritius",
            # 地址或注册地标识
            "(香港)", "(开曼)", "(新加坡)", "(BVI)",
            "荷兰", "比利时", "卢森堡"
        ]
        self.stop_keywords = [
            "国务院", "国资委", "资产监督管理委员会", "财政部", "国有资产", "人民政府", "财政厅", "发改委", "办公室", "办事处", "管委会", "管理委员会","中央结算","中国证券金融股份有限公司","财政局","CHINA INTERNATIONAL CAPITAL","证券投资基金","中央汇金",
        ]
        
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
        print(f"🔍 搜索公司: {company_name}")
        
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
                        first_company = company_list[0]
                        search_info = {
                            'gid': str(first_company.get('id', '')),
                            'graphId': str(first_company.get('graphId', '')),
                            'name': first_company.get('comName', ''),
                            'alias': first_company.get('alias', ''),
                            'taxCode': first_company.get('taxCode', ''),
                            'regStatus': first_company.get('regStatus', 0)
                        }
                        
                        print(f"✅ 找到公司: {search_info['name']} (GID: {search_info['gid']})")
                        return search_info
                    else:
                        print(f"❌ 未找到匹配的公司: {company_name}")
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
    
    def get_shareholders_info(self, gid, company_name=""):
        """
        获取股东信息
        
        Args:
            gid (str): 公司GID
            company_name (str): 公司名称（用于日志显示）
        
        Returns:
            list: 股东信息列表
        """
        if company_name:
            print(f"👥 获取股东信息: {company_name} (GID: {gid})")
        else:
            print(f"👥 获取股东信息: GID {gid}")
        
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
                        shareholder_name = holder.get('shareHolderName', '') or holder.get('name', '')
                        percent = holder.get('percent', '')
                        total_capital = holder.get('totalCapital', '') or holder.get('amount', '')
                        shareholder_type = (
                            holder.get('shareHolderTypeOnPage', '') or
                            holder.get('type', '') or
                            holder.get('shareholderType', '')
                        )
                        shareholder_gid = holder.get('shareHolderGid', '')

                        # 自然人/企业判定：优先使用类型字段；其次基于名称关键词
                        type_text = str(shareholder_type)
                        is_natural_person = ('自然人' in type_text) or ('个人' in type_text)
                        company_keywords = [
                            '公司','集团','有限','股份','银行','合伙','企业','合作社','事务所','中心','研究院','基金','基金会','大学','学院',
                            # 政府/机构类关键词，视作“机构主体”，避免误判为自然人
                            '政府','人民政府','委员会','管理委员会','资产监督管理','国资','国有资产','财政厅','财政部','发展和改革','发改委','办公室','办事处','管委会','管理委员会','中央结算','中国证券金融股份有限公司','财政局','CHINA INTERNATIONAL CAPITAL','证券投资基金','中央汇金',
                        ]
                        name_looks_company = any(k in str(shareholder_name) for k in company_keywords)
                        is_company = (not is_natural_person) and (('企业' in type_text) or ('公司' in type_text) or name_looks_company)

                        shareholder_info = {
                            '股东名称': shareholder_name,
                            '持股比例': percent,
                            '认缴出资额': total_capital,
                            '股东类型': shareholder_type,
                            '股东GID': shareholder_gid,
                            '别名': holder.get('alias', ''),
                            # 注意：人名可能也有GID，这里严格基于类型和名称判断
                            '是否为企业': is_company
                        }
                        shareholders.append(shareholder_info)
                    
                    print(f"✅ 获取到 {len(shareholders)} 个股东")
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
    
    def penetrate_shareholders(self, company_name, max_depth=None, min_percentage=0.01):
        """
        多层股东穿透查询
        
        Args:
            company_name (str): 起始公司名称
            max_depth (int): 最大穿透深度
            min_percentage (float): 最小持股比例阈值（百分比）
        
        Returns:
            dict: 完整的穿透结果
        """
        print("🔍 天眼查股东穿透查询工具")
        print("=" * 80)
        print(f"🎯 目标公司: {company_name}")
        if max_depth is not None:
            print(f"📊 最大深度: {max_depth} 层")
        print(f"📈 最小持股比例: {min_percentage}%")
        print("=" * 80)
        
        # 重置状态
        self.visited_companies.clear()
        self.penetration_results.clear()
        self.max_depth = max_depth
        
        # 搜索起始公司
        start_company = self.search_company(company_name)
        if not start_company:
            print("❌ 无法找到起始公司，穿透查询结束")
            return None
        
        # 开始穿透查询
        penetration_tree = self._recursive_penetrate(
            start_company['gid'], 
            start_company['name'], 
            depth=0, 
            min_percentage=min_percentage,
            parent_percentage=100.0
        )
        
        # 生成穿透报告
        report = self._generate_penetration_report(start_company, penetration_tree)
        
        print(f"\n🎉 股东穿透查询完成！ 共查询了 {len(self.visited_companies)} 家公司")
        
        return report
    
    def _recursive_penetrate(self, gid, company_name, depth=0, min_percentage=0.0, parent_percentage=100.0):
        """
        递归穿透查询股东
        
        Args:
            gid (str): 公司GID
            company_name (str): 公司名称
            depth (int): 当前深度
            min_percentage (float): 最小持股比例阈值
            parent_percentage (float): 父级持股比例
        
        Returns:
            dict: 当前层级的穿透结果
        """
        # 如果设置了最大深度才限制；默认不限深
        if self.max_depth is not None and depth >= self.max_depth:
            print(f"⚠️ 已达到最大穿透深度 {self.max_depth}，停止查询: {company_name}")
            return {'company_name': company_name, 'gid': gid, 'depth': depth, 'shareholders': [], 'stop_reason': '达到最大深度'}
        
        # 检查是否已访问过（防止循环）
        if gid in self.visited_companies:
            print(f"⚠️ 检测到循环引用，跳过: {company_name} (GID: {gid})")
            return {'company_name': company_name, 'gid': gid, 'depth': depth, 'shareholders': [], 'stop_reason': '循环引用'}
        
        # 标记为已访问
        self.visited_companies.add(gid)
        
        # 显示当前查询进度
        indent = "  " * depth
        print(f"{indent}🏢 [{depth}层] 查询: {company_name}")
        
        # 获取股东信息
        shareholders = self.get_shareholders_info(gid, company_name)
        
        if not shareholders:
            print(f"{indent}⚠️ 未获取到股东信息")
            return {'company_name': company_name, 'gid': gid, 'depth': depth, 'shareholders': [], 'stop_reason': '无股东信息'}
        
        # 请求间隔：使用随机延迟，最大不超过3秒
        delay = self.delay_between_requests if self.delay_between_requests > 0 else 0
        # 如果设置了范围，则使用范围内随机延迟（覆盖固定延迟）
        if self.min_delay is not None and self.max_delay is not None:
            max_cap = min(float(self.max_delay), 3.0)
            min_cap = max(0.0, float(self.min_delay))
            if max_cap < min_cap:
                max_cap = min_cap
            delay = random.uniform(min_cap, max_cap)
        if delay > 0:
            time.sleep(delay)
        
        # 处理每个股东
        penetrated_shareholders = []
        for shareholder in shareholders:
            shareholder_name = shareholder['股东名称']
            percentage_str = shareholder['持股比例']
            
            # 解析持股比例
            try:
                if percentage_str and percentage_str != '-':
                    percentage = float(percentage_str.replace('%', ''))
                else:
                    percentage = 0.0
            except:
                percentage = 0.0
            
            # 计算实际持股比例（考虑上级持股）
            actual_percentage = (percentage * parent_percentage) / 100.0
            
            # 检查是否满足最小持股比例要求
            if actual_percentage < min_percentage:
                print(f"{indent}  ⏭️ 跳过低持股比例股东: {shareholder_name} ({percentage}%)")
                continue
            
            # 准备股东信息
            shareholder_result = {
                'shareholder_name': shareholder_name,
                'percentage': percentage,
                'actual_percentage': actual_percentage,
                'capital': shareholder['认缴出资额'],
                'type': shareholder['股东类型'],
                'gid': shareholder['股东GID'],
                'is_company': shareholder['是否为企业'],
                'sub_shareholders': []
            }
            
            print(f"{indent}  👤 股东: {shareholder_name} ({percentage}%, 实际{actual_percentage:.2f}%)")
            
            # 终止条件：自然人、命中“海外或政府/财政相关”关键词
            combined_stops = set(self.overseas_indicators + self.stop_keywords)
            is_stop_entity = (not shareholder['是否为企业']) or any(k in shareholder_name for k in combined_stops)

            # 如果是企业股东且有GID，并且不属于终止实体，继续穿透
            if (not is_stop_entity) and shareholder['股东GID'] and shareholder['股东GID'] != '0':
                try:
                    sub_result = self._recursive_penetrate(
                        shareholder['股东GID'],
                        shareholder_name,
                        depth + 1,
                        min_percentage,
                        actual_percentage
                    )
                    shareholder_result['sub_shareholders'] = sub_result
                    print(f"{indent}  ✅ 完成穿透: {shareholder_name}")
                except Exception as e:
                    print(f"{indent}  ❌ 穿透失败: {shareholder_name} - {e}")
                    shareholder_result['penetration_error'] = str(e)
            else:
                if not shareholder['是否为企业']:
                    print(f"{indent}  👨 自然人股东（终止）")
                elif any(k in shareholder_name for k in combined_stops):
                    print(f"{indent}  ⛔ 终止点: {shareholder_name}")
                else:
                    print(f"{indent}  ⚠️ 企业股东但无GID，无法继续穿透")
            
            penetrated_shareholders.append(shareholder_result)
        
        return {
            'company_name': company_name,
            'gid': gid,
            'depth': depth,
            'shareholders': penetrated_shareholders,
            'total_shareholders': len(shareholders),
            'penetrated_shareholders': len(penetrated_shareholders)
        }
    
    def _generate_penetration_report(self, start_company, penetration_tree):
        """
        生成穿透报告
        
        Args:
            start_company (dict): 起始公司信息
            penetration_tree (dict): 穿透结果树
        
        Returns:
            dict: 完整的穿透报告
        """
        # 统计信息
        stats = self._calculate_penetration_stats(penetration_tree)
        
        # 生成最终受益人列表
        ultimate_beneficiaries = self._extract_ultimate_beneficiaries(penetration_tree)
        
        # 生成持股路径
        shareholding_paths = self._generate_shareholding_paths(penetration_tree)
        
        report = {
            'query_info': {
                'target_company': start_company['name'],
                'company_gid': start_company['gid'],
                'query_time': time.strftime("%Y-%m-%d %H:%M:%S"),
                'max_depth': self.max_depth,
                'total_companies_queried': len(self.visited_companies)
            },
            'penetration_tree': penetration_tree,
            'statistics': stats,
            'ultimate_beneficiaries': ultimate_beneficiaries,
            'shareholding_paths': shareholding_paths,
            'data_source': '天眼查API'
        }
        
        return report
    
    def _calculate_penetration_stats(self, tree):
        """计算穿透统计信息"""
        stats = {
            'total_levels': 0,
            'total_shareholders': 0,
            'company_shareholders': 0,
            'individual_shareholders': 0,
            'max_individual_percentage': 0.0,
            'total_percentage_covered': 0.0
        }
        
        def traverse(node, level=0):
            stats['total_levels'] = max(stats['total_levels'], level)
            
            if 'shareholders' in node:
                for shareholder in node['shareholders']:
                    stats['total_shareholders'] += 1
                    
                    if shareholder['is_company']:
                        stats['company_shareholders'] += 1
                        if 'sub_shareholders' in shareholder:
                            traverse(shareholder['sub_shareholders'], level + 1)
                    else:
                        stats['individual_shareholders'] += 1
                        stats['max_individual_percentage'] = max(
                            stats['max_individual_percentage'],
                            shareholder['actual_percentage']
                        )
                    
                    if level == 0:  # 只统计第一层的持股比例
                        stats['total_percentage_covered'] += shareholder['percentage']
        
        traverse(tree)
        return stats
    
    def _extract_ultimate_beneficiaries(self, tree):
        """提取最终受益人（自然人股东）"""
        beneficiaries = []
        
        def traverse(node, path=[]):
            if 'shareholders' in node:
                for shareholder in node['shareholders']:
                    current_path = path + [{
                        'company': node['company_name'],
                        'shareholder': shareholder['shareholder_name'],
                        'percentage': shareholder['percentage']
                    }]
                    
                    if not shareholder['is_company']:
                        # 自然人股东
                        beneficiaries.append({
                            'name': shareholder['shareholder_name'],
                            'final_percentage': shareholder['actual_percentage'],
                            'path': current_path,
                            'path_length': len(current_path)
                        })
                    elif 'sub_shareholders' in shareholder:
                        traverse(shareholder['sub_shareholders'], current_path)
        
        traverse(tree)
        
        # 按最终持股比例排序
        beneficiaries.sort(key=lambda x: x['final_percentage'], reverse=True)
        
        return beneficiaries
    
    def _generate_shareholding_paths(self, tree):
        """生成持股路径"""
        paths = []
        
        def traverse(node, current_path="", current_percentage=100.0):
            # 兼容多种节点形态：dict 或 list
            if isinstance(node, list):
                for sub in node:
                    traverse(sub, current_path, current_percentage)
                return

            if not isinstance(node, dict):
                return

            company_name = node.get('company_name', '')

            if 'shareholders' in node and isinstance(node['shareholders'], list):
                for shareholder in node['shareholders']:
                    shareholder_name = shareholder['shareholder_name']
                    percentage = shareholder['percentage']
                    
                    path = f"{current_path} → {shareholder_name}({percentage}%)" if current_path else f"{company_name} → {shareholder_name}({percentage}%)"
                    final_percentage = (current_percentage * percentage) / 100.0
                    
                    if not shareholder['is_company']:
                        # 到达自然人，记录完整路径
                        paths.append({
                            'path': path,
                            'final_beneficiary': shareholder_name,
                            'final_percentage': final_percentage,
                            'path_length': path.count('→')
                        })
                    elif 'sub_shareholders' in shareholder:
                        traverse(shareholder['sub_shareholders'], path, final_percentage)
        
        traverse(tree)
        
        # 按最终持股比例排序
        paths.sort(key=lambda x: x['final_percentage'], reverse=True)
        
        return paths
    
    def print_penetration_tree(self, tree, indent=0, show_company_header=True):
        """打印穿透结果树；支持节点为 dict 或 list；为避免同名公司重复一层，子节点不再重复打印公司抬头"""
        # 兼容 list：逐个打印
        if isinstance(tree, list):
            for sub in tree:
                self.print_penetration_tree(sub, indent, show_company_header)
            return

        if not isinstance(tree, dict):
            return

        prefix = "  " * indent
        company_name = tree.get('company_name', '未知公司')

        if show_company_header:
            print(f"{prefix}🏢 {company_name}")

        shareholders = tree.get('shareholders')
        if isinstance(shareholders, list):
            for shareholder in shareholders:
                shareholder_name = shareholder['shareholder_name']
                percentage = shareholder['percentage']
                actual_percentage = shareholder['actual_percentage']

                if shareholder['is_company']:
                    print(f"{prefix}  🏢 {shareholder_name} ({percentage}%, 实际{actual_percentage:.2f}%)")
                    if 'sub_shareholders' in shareholder:
                        # 子树不再重复打印公司抬头，直接进入其股东列表
                        self.print_penetration_tree(shareholder['sub_shareholders'], indent + 2, show_company_header=False)
                else:
                    print(f"{prefix}  👤 {shareholder_name} ({percentage}%, 实际{actual_percentage:.2f}%)")
    
    def save_penetration_report(self, report, filename_prefix="tianyancha_penetration"):
        """保存穿透报告"""
        if not report:
            print("❌ 无报告数据可保存")
            return
        
        timestamp = int(time.time())
        company_name = report['query_info']['target_company']
        
        # 保存JSON格式的完整报告
        json_filename = f"{filename_prefix}_{timestamp}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"💾 完整报告已保存到: {json_filename}")
        
        # 保存可读性强的文本报告
        txt_filename = f"{filename_prefix}_{timestamp}.txt"
        with open(txt_filename, "w", encoding="utf-8") as f:
            self._write_readable_report(f, report)
        
        print(f"📄 可读报告已保存到: {txt_filename}")
        
        return json_filename, txt_filename
    
    def _write_readable_report(self, file, report):
        """写入可读性强的报告"""
        query_info = report['query_info']
        stats = report['statistics']
        beneficiaries = report['ultimate_beneficiaries']
        paths = report['shareholding_paths']
        
        file.write(f"天眼查股东穿透查询报告\n")
        file.write("=" * 80 + "\n\n")
        
        # 查询信息
        file.write("📝 查询信息:\n")
        file.write(f"  目标公司: {query_info['target_company']}\n")
        file.write(f"  公司GID: {query_info['company_gid']}\n")
        file.write(f"  查询时间: {query_info['query_time']}\n")
        file.write(f"  最大深度: {query_info['max_depth']} 层\n")
        file.write(f"  查询公司数: {query_info['total_companies_queried']} 家\n\n")
        
        # 统计信息
        file.write("📊 统计信息:\n")
        file.write(f"  穿透层数: {stats['total_levels']} 层\n")
        file.write(f"  股东总数: {stats['total_shareholders']} 个\n")
        file.write(f"  企业股东: {stats['company_shareholders']} 个\n")
        file.write(f"  个人股东: {stats['individual_shareholders']} 个\n")
        file.write(f"  最大个人持股: {stats['max_individual_percentage']:.2f}%\n")
        file.write(f"  第一层覆盖率: {stats['total_percentage_covered']:.2f}%\n\n")
        
        # 最终受益人
        file.write("👤 最终受益人 (按持股比例排序):\n")
        for i, beneficiary in enumerate(beneficiaries[:20], 1):  # 只显示前20个
            file.write(f"  {i:2d}. {beneficiary['name']} - {beneficiary['final_percentage']:.2f}% (路径长度: {beneficiary['path_length']})\n")
        
        if len(beneficiaries) > 20:
            file.write(f"  ... 还有 {len(beneficiaries) - 20} 个受益人\n")
        file.write("\n")
        
        # 主要持股路径
        file.write("🔗 主要持股路径 (按最终持股比例排序):\n")
        for i, path in enumerate(paths[:15], 1):  # 只显示前15条路径
            file.write(f"  {i:2d}. {path['path']} (最终: {path['final_percentage']:.2f}%)\n")
        
        if len(paths) > 15:
            file.write(f"  ... 还有 {len(paths) - 15} 条路径\n")
        file.write("\n")
        
        # 穿透结构树
        file.write("🌳 完整穿透结构:\n")
        self._write_tree_structure(file, report['penetration_tree'])
    
    def _write_tree_structure(self, file, tree, indent=0, show_company_header=True):
        """写入树形结构；支持节点为 dict 或 list；子树不重复打印公司抬头，避免同名公司重复一层"""
        # 兼容 list：逐个写入
        if isinstance(tree, list):
            for sub in tree:
                self._write_tree_structure(file, sub, indent, show_company_header)
            return

        if not isinstance(tree, dict):
            return

        prefix = "  " * indent
        company_name = tree.get('company_name', '未知公司')

        if show_company_header:
            file.write(f"{prefix}🏢 {company_name}\n")

        shareholders = tree.get('shareholders')
        if isinstance(shareholders, list):
            for shareholder in shareholders:
                shareholder_name = shareholder['shareholder_name']
                percentage = shareholder['percentage']
                actual_percentage = shareholder['actual_percentage']

                if shareholder['is_company']:
                    file.write(f"{prefix}  🏢 {shareholder_name} ({percentage}%, 实际{actual_percentage:.2f}%)\n")
                    if 'sub_shareholders' in shareholder:
                        self._write_tree_structure(file, shareholder['sub_shareholders'], indent + 2, show_company_header=False)
                else:
                    file.write(f"{prefix}  👤 {shareholder_name} ({percentage}%, 实际{actual_percentage:.2f}%)\n")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='天眼查股东穿透查询工具')
    parser.add_argument('company_name', nargs='?', default="海南玮峻思投资合伙企业（有限合伙）",
                       help='要查询的公司名称')
    parser.add_argument('--depth', '-d', type=int, default=10,
                       help='最大穿透深度（固定10层，本参数将被忽略）')
    parser.add_argument('--min-percentage', '-p', type=float, default=0.01,
                       help='最小“实际持股比例”阈值（按链路递推后的实际比例）。低于此比例将跳过 (默认: 0.01%)')
    parser.add_argument('--delay', type=float, default=0.0,
                       help='固定请求间隔（秒）。若设置 --min-delay/--max-delay 则忽略本参数')
    parser.add_argument('--min-delay', type=float, default=0.5,
                       help='最小随机延迟（秒），默认0.5')
    parser.add_argument('--max-delay', type=float, default=2.5,
                       help='最大随机延迟（秒），上限3秒，默认2.5')
    parser.add_argument('--print-tree', action='store_true',
                       help='在控制台打印完整的穿透结构树')
    parser.add_argument('--input', '-i', type=str,
                       help='批量公司输入文件（每行一个公司名）')
    parser.add_argument('--output-csv', '-o', type=str,
                       help='将穿透结果汇总导出为CSV文件路径')
    parser.add_argument('--add-stop', type=str, nargs='*',
                       help='追加终止关键词（空格分隔，多词可写多项）')
    parser.add_argument('--stop-file', type=str,
                       help='从文件加载终止关键词（每行一个，UTF-8）')

    args = parser.parse_args()

    # 创建穿透API客户端
    api_client = TianyanchaPenetrationAPI()
    api_client.delay_between_requests = args.delay
    api_client.min_delay = args.min_delay
    api_client.max_delay = min(args.max_delay, 3.0)

    # 固定穿透深度为10层（忽略命令行传入的 --depth 值）
    # 现在不固定：若未指定则不限
    if args.depth and args.depth <= 0:
        args.depth = None

    # 处理终止关键词扩展
    if args.add_stop:
        api_client.stop_keywords.extend(args.add_stop)
    if args.stop_file:
        try:
            with open(args.stop_file, 'r', encoding='utf-8') as sf:
                extra = [line.strip() for line in sf if line.strip()]
                api_client.stop_keywords.extend(extra)
        except Exception as e:
            print(f"⚠️ 读取终止关键词文件失败: {e}")

    def flatten_rows(company_name, report):
        rows = []
        if not report:
            return rows

        def walk(node, parent_path, parent_actual):
            if isinstance(node, list):
                for sub in node:
                    walk(sub, parent_path, parent_actual)
                return

            if not isinstance(node, dict):
                return

            for sh in node.get('shareholders', []):
                row = {
                    'root_company': report['query_info']['target_company'],
                    'node_company': node.get('company_name', ''),
                    'shareholder_name': sh['shareholder_name'],
                    'is_company': 1 if sh['is_company'] else 0,
                    'declared_percentage': sh['percentage'],
                    'actual_percentage': sh['actual_percentage'],
                    'capital': sh.get('capital', ''),
                    'path': ' / '.join(parent_path + [sh['shareholder_name']])
                }
                rows.append(row)
                if sh['is_company'] and 'sub_shareholders' in sh:
                    walk(sh['sub_shareholders'], parent_path + [sh['shareholder_name']], sh['actual_percentage'])

        walk(report['penetration_tree'], [report['query_info']['target_company']], 100.0)
        return rows

    all_rows = []
    targets = []
    # 交互模式：如果没有传任何参数（直接运行脚本），单步读取多行公司名
    interactive = len(sys.argv) == 1
    if interactive:
        print("请输入公司名称（可多行，每行一个；直接回车结束）：")
        try:
            while True:
                line = input().strip()
                if not line:
                    break
                targets.append(line)
        except EOFError:
            pass
        if not targets:
            print("未输入公司名称，已退出。")
            return
    else:
        if args.input:
            with open(args.input, 'r', encoding='utf-8') as f:
                targets = [line.strip() for line in f if line.strip()]
        else:
            targets = [args.company_name]

    for target in targets:
        report = api_client.penetrate_shareholders(
            target,
            max_depth=args.depth,
            min_percentage=args.min_percentage
        )
        if report:
            all_rows.extend(flatten_rows(target, report))

    if all_rows:
        # 打印摘要信息
        print("\n📊 穿透查询摘要:")
        print("-" * 60)
        stats = report['statistics']
        print(f"穿透层数: {stats['total_levels']} 层")
        print(f"股东总数: {stats['total_shareholders']} 个")
        print(f"最终受益人: {stats['individual_shareholders']} 个")
        
        if report['ultimate_beneficiaries']:
            print(f"最大个人持股: {stats['max_individual_percentage']:.2f}%")
            print("\n🏆 前5名最终受益人:")
            for i, beneficiary in enumerate(report['ultimate_beneficiaries'][:5], 1):
                print(f"  {i}. {beneficiary['name']} - {beneficiary['final_percentage']:.2f}%")
        
        # 可选：打印完整树结构
        if args.print_tree and len(targets) == 1 and report:
            print("-" * 60)
            api_client.print_penetration_tree(report['penetration_tree'])
        
        # 保存报告
        # 如需保存最后一次的报告文件
        if report:
            json_file, txt_file = api_client.save_penetration_report(report)
        else:
            json_file = txt_file = ''

        # 导出CSV
        if args.output_csv:
            import csv
            with open(args.output_csv, 'w', encoding='utf-8', newline='') as csvf:
                writer = csv.DictWriter(csvf, fieldnames=[
                    'root_company','node_company','shareholder_name','is_company',
                    'declared_percentage','actual_percentage','capital','path'
                ])
                writer.writeheader()
                writer.writerows(all_rows)
            print(f"📄 CSV已导出: {args.output_csv} (共 {len(all_rows)} 行)")
        
        print(f"\n✅ 穿透查询完成！")
        print(f"📁 报告文件: {json_file}, {txt_file}")
        
    else:
        print("❌ 穿透查询失败")


if __name__ == "__main__":
    main()
