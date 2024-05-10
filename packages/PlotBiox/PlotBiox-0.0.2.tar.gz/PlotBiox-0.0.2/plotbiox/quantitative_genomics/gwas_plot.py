import matplotlib.pyplot as plt
import numpy as np

def quantile_quantile_plot(p_value, title=None, ax=None, filter_zero_point=True):
    p_value = np.array(p_value)

    if ax is None:
        fig, ax = plt.subplots()

    if filter_zero_point:
        # 计算 -np.log10(p_value)
        log_p_value = -np.log10(p_value)
        # 找出 -np.log10(p_value) 不等于 0 的值
        mask = log_p_value != 0
        # 使用 mask 来筛选 p_value
        p_value = p_value[mask]

    # 计算理论分位数
    n = len(p_value)

    expected = -np.log10(np.linspace(1/n, 1, n))

    max_value = max(np.max(expected), np.max(-np.log10(p_value)))

    # 绘图
    ax.scatter(expected, -np.log10(np.sort(p_value)), s=20, c="#000000")

    lim = (0 - max_value*0.1, max_value*1.1)
    ax.plot(lim, lim, c="#FB0324")

    # 设置 x 轴和 y 轴的范围
    ax.set_xlim(0 - np.max(expected)*0.1, np.max(expected)*1.1)
    ax.set_ylim(0 - np.max(-np.log10(p_value))*0.1, np.max(-np.log10(p_value))*1.1)

    # 设置 x 轴和 y 轴的标签
    ax.set_xlabel('Expected $-log_{10}(p)$')
    ax.set_ylabel('Observed $-log_{10}(p)$')

    # 设置标题
    if title is not None:
        ax.set_title(title)

    if ax is None:
        plt.show()


def manhattan_plot(manhattan_df, chr_list, chr_length_dict, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(16,9))

    chr_coord_dict = {}
    total_length = 0
    for i in chr_list:
        chr_coord_dict[i] = total_length
        total_length += chr_length_dict[i]

    # 设置ax
    ax.set_xlim(0 - total_length*0.05, total_length*1.05)
    max_y = np.max(-np.log10(manhattan_df.pval))
    ax.set_ylim(0, max_y*1.1)

    # 设置 x 轴和 y 轴的标签
    ax.set_xlabel('Chromosome')
    ax.set_ylabel('$-log_{10}(p)$')

    # 隐藏坐标轴的上边框和右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 绘图
    c1 = "#617EB8"
    c2 = "#84B8D0"
    n = 0
    chr_ticks = []  # 用于存储每个染色体中点的位置
    chr_labels = []  # 用于存储染色体的编号
    for chr_id in chr_list:
        c = c1 if n % 2 == 0 else c2
        chr_df = manhattan_df.loc[manhattan_df['chr'] == chr_id]
        ax.scatter(chr_df.pos + chr_df.chr.map(chr_coord_dict), -np.log10(chr_df.pval), s=10, c=c)
        # 计算染色体的中点位置并添加到列表中
        chr_ticks.append((chr_df.pos + chr_df.chr.map(chr_coord_dict)).mean())
        chr_labels.append(chr_id)
        n += 1

    # 设置 x 轴的刻度标签
    ax.set_xticks(chr_ticks)
    ax.set_xticklabels(chr_labels)

    if ax is None:
        plt.show()