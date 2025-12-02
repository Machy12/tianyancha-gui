# 天眼查HTML提取修复报告

## 问题描述
用户反馈基础信息页面不显示了，数据源能获取到，但需要检查HTML提取方式是否有变化。

## 问题分析
通过分析用户提供的HTML文件（2320855868），发现：
1. 地址提取逻辑有问题，只能提取到"地址："标签而不是实际地址
2. 经营状态提取失败，使用的CSS选择器不正确
3. 部分字段提取不完整

## 修复内容

### 1. 地址提取修复
**问题：** 原来的选择器只能提取到标签文本"地址："
**修复：** 
```python
# 原代码
address_elem = item.find('span', class_='index_inline-flex__QLDiW')

# 修复后
address_elem = item.find('span', class_='index_detail-address-moretext__9R_Z1')
if address_elem:
    address_span = address_elem.find('span', class_='index_inline-flex__QLDiW')
    if address_span:
        info['注册地址'] = address_span.get_text(strip=True)
else:
    # 备用选择器
    address_elem = item.find('span', class_='index_inline-flex__QLDiW')
    if address_elem:
        address_text = address_elem.get_text(strip=True)
        if address_text and '地址：' not in address_text and len(address_text) > 10:
            info['注册地址'] = address_text
```

### 2. 经营状态提取修复
**问题：** 原选择器无法找到经营状态元素
**修复：**
```python
# 原代码
status_elem = soup.find('div', class_='index_company-tag__ZcJFV index_header-company-tag__WaTgu')

# 修复后 - 添加备用选择器
status_elem = soup.find('div', class_='index_company-tag__ZcJFV index_header-company-tag__WaTgu')
if status_elem:
    info['经营状态'] = status_elem.get_text(strip=True)
else:
    # 尝试其他选择器
    status_elem = soup.find('div', class_='index_reg-status-tag__ES7dF')
    if status_elem:
        tag_elem = status_elem.find('div', class_='index_company-tag__ZcJFV')
        if tag_elem:
            info['经营状态'] = tag_elem.get_text(strip=True)
```

### 3. 联系电话提取优化
**修复：**
```python
# 原代码
value_elem = item.find('span', class_='link-hover-click')

# 修复后 - 使用更准确的选择器
tel_elem = item.find('span', class_='index_detail-tel__fgpsE')
if tel_elem:
    info['联系电话'] = tel_elem.get_text(strip=True)
else:
    # 备用选择器
    value_elem = item.find('span', class_='link-hover-click')
    if value_elem:
        info['联系电话'] = value_elem.get_text(strip=True)
```

### 4. 新增网址提取
**新增：**
```python
elif '网址' in label_text:
    website_elem = item.find('a', class_='index_detail-website__n2yst')
    if website_elem:
        info['网址'] = website_elem.get_text(strip=True)
```

## 修复结果

### 修复前
- 提取字段数量：约10个
- 地址提取：失败（只显示"地址："）
- 经营状态：失败
- 联系信息：部分缺失

### 修复后
- ✅ 提取字段数量：16个
- ✅ 地址提取：成功（"浙江省杭州市临平区临平经济开发区五洲路116号"）
- ✅ 经营状态：成功（"存续"）
- ✅ 联系信息：完整（电话、邮箱、网址）

### 完整提取字段列表
1. 公司名称：浙江春风动力股份有限公司
2. 统一社会信用代码：91330100757206158J
3. 法定代表人：赖民杰
4. 经营状态：存续
5. 注册资本：15,257.7663万人民币
6. 成立日期：2003-12-09
7. 联系电话：0571-89265620
8. 邮箱：wuyiqing@cfmoto.com
9. 网址：www.cfmoto.com
10. 注册地址：浙江省杭州市临平区临平经济开发区五洲路116号
11. 所属行业：城市轨道交通设备制造
12. 企业规模：大型
13. 员工人数：6911人
14. 英文名称：Zhejiang CFMOTO Power Co.,Ltd.
15. 登记机关：浙江省市场监督管理局
16. 经营范围：完整的经营范围信息

## 测试验证
- ✅ 创建了专门的测试脚本验证修复效果
- ✅ 所有关键字段都能正确提取
- ✅ 地址和经营状态修复验证通过
- ✅ 联系信息提取完整（3/3个字段）

## 结论
HTML提取功能已完全修复，现在能够正确提取16个字段的基础信息，包括之前无法提取的地址和经营状态。修复后的代码具有更好的容错性，使用了多个备用选择器来应对页面结构的变化。
