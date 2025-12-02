import requests
import json
import re
from urllib.parse import urlencode

def get_x_pid(key_no, name, oper_id, oper_name):
    """
    通过访问结构图页面来获取动态的 X-Pid

    Args:
        key_no (str): 企业关键编号
        name (str): 公司名称
        oper_id (str): 操作员ID
        oper_name (str): 操作员名称

    Returns:
        str: 获取到的 X-Pid，失败则返回 None
    """
    print(f"正在为 keyNo: {key_no} 获取 X-Pid...")
    base_url = "https://graph.qcc.com/web/charts/structure-chart"
    params = {
        "keyNo": key_no,
        "name": name,
        "operId": oper_id,
        "operName": oper_name
    }
    url = f"{base_url}?{urlencode(params)}"
    print(f"请求PID的URL: {url}")

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6",
        "Cookie": "qcc_did=9655fb82-1796-4322-9e48-b28267ac1501; tfstk=gTIKT52h45VH4CSpI9ziriSy7tyg1PxFLE5Iq0xktP191tlntTTHwQdOaBYHAgQZ2tWPxJ-uLHWe43N0ioxRL9-rWzvuT5X_FL-Jdf2zgUWe43Nipe58395eGSp5d3w9fL9pN39IAdw9eKdWVBTS1V9X13tWR0T_fKvxN09SARB6_LtWN_t7BhOwFAFqJQuBi0Q4V9KmsPhJmHs9pedfBroo4NoDJI1H60NfXpIWG9OtV0dI4k4lB9VK0OxFmspctlidMT6VPFI-1SdPXOsCPOlLNd75thOHcyM9xMWClUsba41vv_LfAFH7e9XB9hp1c802sGdhNML_nmLkfiYXAN4atUxpH_sF9Yn5GOXcYFS8MfOP-K-6egyjyQL54VIcD11miIpoRRetz48BQy9wIqPzNcPMBI2GI4uyWPJ9iRetz48BQdd0IC0rzFUN.; _c_WBKFRo=IXI6f4UMfpt2oxOj7dNBZvvio3uZ3sEIgNeN4Z15; QCCSESSID=cf8f152e13e29add9859d18dd6; acw_tc=0a472f4a17569666757265292e45e6198a95e2b42fa09848a4d3986f03f55c",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()

        match = re.search(r"window\.pid\s*=\s*'([a-f0-9]+)';", response.text)
        if match:
            pid = match.group(1)
            print(f"成功获取到 X-Pid: {pid}")
            return pid
        else:
            print("错误: 在HTML响应中未找到 X-Pid。")
            return None

    except requests.exceptions.RequestException as e:
        print(f"获取 X-Pid 时发生网络错误: {e}")
        return None

def get_holders_data(key_no, x_pid, referer_params, level=1, is_first=False):
    """
    获取企业股东信息
    """
    url = "https://graph.qcc.com/api/charts/getHolders"
    referer_url = f"https://graph.qcc.com/web/charts/structure-chart?{urlencode(referer_params)}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,fr;q=0.6",
        "Content-Type": "application/json",
        "Cookie": "qcc_did=9655fb82-1796-4322-9e48-b28267ac1501; tfstk=gTIKT52h45VH4CSpI9ziriSy7tyg1PxFLE5Iq0xktP191tlntTTHwQdOaBYHAgQZ2tWPxJ-uLHWe43N0ioxRL9-rWzvuT5X_FL-Jdf2zgUWe43Nipe58395eGSp5d3w9fL9pN39IAdw9eKdWVBTS1V9X13tWR0T_fKvxN09SARB6_LtWN_t7BhOwFAFqJQuBi0Q4V9KmsPhJmHs9pedfBroo4NoDJI1H60NfXpIWG9OtV0dI4k4lB9VK0OxFmspctlidMT6VPFI-1SdPXOsCPOlLNd75thOHcyM9xMWClUsba41vv_LfAFH7e9XB9hp1c802sGdhNML_nmLkfiYXAN4atUxpH_sF9Yn5GOXcYFS8MfOP-K-6egyjyQL54VIcD11miIpoRRetz48BQy9wIqPzNcPMBI2GI4uyWPJ9iRetz48BQdd0IC0rzFUN.; _c_WBKFRo=IXI6f4UMfpt2oxOj7dNBZvvio3uZ3sEIgNeN4Z15; QCCSESSID=cf8f152e13e29add9859d18dd6; acw_tc=0a472f4a17569666757265292e45e6198a95e2b42fa09848a4d3986f03f55c",
        "Origin": "https://graph.qcc.com",
        "Priority": "u=1, i",
        "Referer": referer_url,
        "Sec-Ch-Ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "X-Pid": x_pid,
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "keyNo": key_no,
        "level": level,
        "isFirst": is_first
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return None

def main():
    """
    主函数，演示如何使用API
    """
    # --- 参数配置 ---
    # 用于获取PID的页面参数
    pid_params = {
        "keyNo": "5e2ae9ef92d6c16f2a195155d02eb718",
        "name": "海南玮峻思投资合伙企业（有限合伙）",
        "operId": "pd818f5bdd0b6c2f900ed9c49c89096c",
        "operName": "潘思链"
    }
    # 真正要查询股东信息的目标公司keyNo
    target_key_no = "6e61c95e2a45a9241d1583b7f3429950"
    # ----------------

    # 1. 获取 X-Pid
    x_pid = get_x_pid(
        pid_params["keyNo"],
        pid_params["name"],
        pid_params["operId"],
        pid_params["operName"]
    )

    if not x_pid:
        print("获取 X-Pid 失败，无法继续执行。")
        return

    # 2. 请求股东信息
    print("\n正在获取股东信息...")
    data = get_holders_data(target_key_no, x_pid, referer_params=pid_params)

    if data:
        print("请求成功！")
        print("=" * 50)
        if 'gd' in data:
            gd_info = data['gd']
            print(f"公司名称: {gd_info.get('CompanyName', 'N/A')}")
            print(f"更新时间: {gd_info.get('UpdateTime', 'N/A')}")
            print(f"股东详情数量: {gd_info.get('DetailCount', 'N/A')}")
            print("=" * 50)
            if 'EquityShareDetail' in gd_info:
                print("股东信息:")
                for i, shareholder in enumerate(gd_info['EquityShareDetail'], 1):
                    print(f"\n股东 {i}:")
                    print(f"  名称: {shareholder.get('Name', 'N/A')}")
                    print(f"  持股比例: {shareholder.get('Percent', 'N/A')}")
                    print(f"  出资额: {shareholder.get('ShouldCapi', 'N/A')}")
                    print(f"  企业类型: {shareholder.get('EconKind', 'N/A')}")
                    print(f"  状态: {shareholder.get('ShortStatus', 'N/A')}")
                    print(f"  统一社会信用代码: {shareholder.get('CreditCode', 'N/A')}")

        with open('qcc_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n完整数据已保存到 qcc_response.json 文件")

    else:
        print("请求失败，请检查网络连接或参数设置")

if __name__ == "__main__":
    main()
