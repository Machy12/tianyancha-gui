import graphviz
import os

# 设置中文字体，避免生成图片时中文乱码
# SimHei 是一个常见的中文字体，如果您的系统没有，可以换成如 'Microsoft YaHei' 等
# 对于macOS，可以是 'PingFang.ttc'
FONT_NAME = "SimHei" 

# 如果Graphviz没有在系统PATH中，可以手动指定路径
# 例如：os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

def draw_orthogonal_equity_chart(filename="equity_structure"):
    """
    使用 Graphviz 绘制具有直角连接线的股权结构图 (PNG格式)。
    """
    # 1. 初始化图表
    # rankdir='TB' -> Top to Bottom, 从上到下布局
    # splines='ortho' -> 这是实现直角线的关键！
    dot = graphviz.Digraph(
        'EquityStructure',
        graph_attr={'rankdir': 'TB', 'splines': 'ortho'},
        node_attr={'fontname': FONT_NAME, 'shape': 'box', 'style': 'rounded'},
        edge_attr={'fontname': FONT_NAME}
    )

    # 2. 定义所有节点 (为了代码清晰，使用简称作为变量名)
    # 第一层 (自然人股东)
    li_jun = "李军"
    xia_zhou_yu = "夏周煜"
    kang_zhuang = "康庄"
    luo_rong = "罗蓉"
    shi_jin_hui = "史锦辉等10名\n股东" # 使用\n进行换行

    # 第二层 (合伙企业)
    hn_hongma = "湖南红马奔腾私募股权投\n资合伙企业（有限合伙）"
    nb_hongsheng = "宁波象保合作区红昇企业\n管理合伙企业（有限合伙）"

    # 第三层
    cq_hongma_center = "重庆红马奔腾投资中\n心（有限合伙）"
    cq_jidian = "重庆机电控股集团信博投资管\n理有限公司等4名股东"

    # 第四层
    cq_gaoxin = "重庆高新创投红马\n资本管理有限公司"

    # 第五层 (最终基金的LP们)
    cq_chanye = "重庆产业引导股权投资\n基金有限责任公司"
    cq_liangjiang_tech = "重庆两江新区科技创新私募股\n权投资基金合伙企业（有限合伙）"

    # 最终层 (目标公司)
    final_fund = "重庆两江红马智能化产业股权投资\n基金合伙企业（有限合伙）"

    # 3. 添加所有边 (持股关系)
    # 第一层的投资
    dot.edge(li_jun, hn_hongma, label=" 40% ")
    dot.edge(xia_zhou_yu, hn_hongma, label=" 30% ")
    dot.edge(kang_zhuang, hn_hongma, label=" 20% ")
    dot.edge(luo_rong, hn_hongma, label=" 10% ")
    
    # 史锦辉 -> 宁波红昇
    dot.edge(shi_jin_hui, nb_hongsheng)

    # 李军 -> 重庆红马投资中心
    dot.edge(li_jun, cq_hongma_center, label=" (GP)\n0.07% ")

    # 湖南红马 -> 重庆红马投资中心
    dot.edge(hn_hongma, cq_hongma_center, label=" (LP)\n70.95% ")
    
    # 重庆红马投资中心 -> 重庆高新创投
    dot.edge(cq_hongma_center, cq_gaoxin, label=" 36.88% ")

    # 重庆机电 -> 重庆高新创投
    dot.edge(cq_jidian, cq_gaoxin, label=" 63.13% ")

    # 各方投资到最终的基金
    dot.edge(cq_gaoxin, final_fund, label=" (GP)\n1.01% ")
    dot.edge(cq_jidian, final_fund, label=" (LP)\n61.64% ")
    dot.edge(nb_hongsheng, final_fund, label=" (LP)\n28.98% ")
    dot.edge(cq_chanye, final_fund, label=" (LP)\n28.02% ")
    dot.edge(cq_liangjiang_tech, final_fund, label=" (LP)\n9.34% ")

    # 4. 渲染并保存为PNG文件
    try:
        # cleanup=True 会在生成图片后删除临时的dot源文件
        dot.render(filename, format='png', view=False, cleanup=True)
        print(f"✅ 股权结构图已成功生成: {filename}.png")
    except graphviz.backend.execute.CalledProcessError:
        print("❌ 生成失败！请确保：")
        print("1. Graphviz 软件已正确安装。")
        print("2. Graphviz 的 bin 目录已添加到系统的 PATH 环境变量中。")
        print("3. 如果问题依旧，请尝试重启您的电脑或IDE。")

# --- 运行主函数 ---
if __name__ == "__main__":
    draw_orthogonal_equity_chart()