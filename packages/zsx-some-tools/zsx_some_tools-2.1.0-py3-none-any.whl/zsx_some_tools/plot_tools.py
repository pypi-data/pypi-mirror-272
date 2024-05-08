# -*- coding: UTF-8 -*-
# @Author: Zhang Senxin

"""
Functions mainly for plotting
contain simple test
"""

import numpy as np
from collections import namedtuple
from .basic_tools import mark_pval, simple_test
import math


class DecentColor(object):
    def __init__(self):
        self.c_orange = np.array([255, 180, 160, 255]) / 255
        self.c_purple = np.array([181, 170, 210, 255]) / 255
        self.c_green = np.array([163, 218, 202, 255]) / 255
        self.c_blue = np.array([70, 169, 224, 255]) / 255
        self.c_red = np.array([239, 92, 85, 255]) / 255


# 设置字体
# 后续改写为类
def set_plt_backend():
    """
    ctex library has sth wrong now.
    :return: None
    """
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib import rcParams

    matplotlib.use("pgf")
    pgf_config = {
        "font.family": 'serif',
        "font.size": 20,
        "pgf.rcfonts": False,
        "text.usetex": True,
        "pgf.preamble": "\n".join([
            r"\usepackage{unicode-math}",
            r"\setmathfont{XITS Math}",
            r"\setmainfont{Arial}",
            r"\usepackage{xeCJK}",
            # r"\xeCJKsetup{CJKmath=true}",
            r"\setCJKmainfont{SimSun}",
        ]),
    }
    rcParams.update(pgf_config)

    matplotlib.use('module://ipykernel.pylab.backend_inline')


# 自动换行
def line_feed(txt, max_len, lines=False):
    """
    Add '\t' automatically, support Chinese and English.
    :param txt: str, text
    :param max_len: the max number of string in one line
    :param lines: to control the max lines and auto_change max_len
    :return: text with '\t' insertion
    """
    new_txt = ''

    if not lines:
        txt_s = txt.split(' ')
        length = [len(t) for t in txt_s]
        step_len = 0
        step_txt = ''
        for i in range(len(txt_s)):
            step_len += length[i]
            step_txt += txt_s[i] + ' '
            if step_len > max_len:
                new_txt += step_txt.strip(' ') + '\n'
                step_len = 0
                step_txt = ''
            elif i == len(txt_s) - 1:
                new_txt += step_txt.strip(' ')

    elif type(lines) == int:
        max_len = len(txt) // lines
        length = [max_len] * lines
        rest = len(txt) % lines
        for i in range(rest):
            length[i] += 1
        length = [0] + [sum(length[:(i + 1)]) for i in range(len(length))]
        for i in range(lines):
            new_txt += txt[length[i]:length[i + 1]] + '\n'
        new_txt = new_txt.strip('\n')

    return new_txt


def mark_significance(plt_, data1_, data2_, x1_, x2_, height='max', rounding=4, y_axis_ran=False,
                      color_font='black', block_ratio=30, block_ratio_p=30, one_tail=True, norm_fix=False,
                      vertical_ratio=1, alpha_p=0.05, size_txt_=15, test_pair=False, **kwargs):
    """
    Automatically do test and plot significance mark.
    :param plt_: plot canvas or subplot canvas obj
    :param data1_: sample1
    :param data2_: sample2
    :param x1_: x coordinate for sample1
    :param x2_: x coordinate for sample2
    :param height: y coordinate to mark line, default is 'max', use the max(sample1) as height,
    while 'mean' and int or float obj are also supported.
    :param rounding: numpy.round(obj, rounding) will be performed for P-value
    :param y_axis_ran: determine the max range of y coordinate, which is related to the block info.
    default is False, will call the max range of y coordinate now.
    :param color_font: text color
    :param block_ratio: the block ratio between the mark and data present
    :param block_ratio_p: the block ratio between the mark and p-value text
    :param one_tail: do one-tail or two-tail test
    :param norm_fix: If the test fixes normal distribution or not.
    Default is None, then will perform normal distribution test to determine it.
    If True, normal distribution is directly determined, vice versa.
    :param vertical_ratio: to change the height of vertical length of mark
    :param alpha_p: Significant level
    :param size_txt_: text fontsize
    :param test_pair: if paired-test will be performed.
    :param kwargs: plt.plot()'s keyword arguments
    :return: x list for plot mark, y list for plot mark, test summary name tuple, y_axis_ran
    """
    import numpy as np_

    if not y_axis_ran:
        yaxis_ = plt_.yticks()
        y_axis_ran = max(yaxis_[0]) - min(yaxis_[0])

    # 标注折线x
    if height == 'max':
        y_max = max([max(data1_), max(data2_)])
    elif height == 'mean':
        y_max = max([np_.mean(data1_), np_.mean(data2_)])
    elif type(height) == float or type(height) == int:
        y_max = height

    if x1_ > x2_:
        x1_, x2_ = x2_, x1_

    block_y = y_axis_ran / block_ratio
    block_p = y_axis_ran / block_ratio_p
    dia_y = block_y / vertical_ratio

    y1_ = y_max + block_y
    y2_ = y_max + block_y + dia_y

    x_ = [x1_, x1_, x2_, x2_]
    y_ = [y1_, y2_, y2_, y1_]

    plt_.plot(x_, y_, **kwargs)

    # 标注显著性
    test_ = simple_test(np_.array(data1_), np_.array(data2_), summary=True, rounding=rounding, norm_fix=norm_fix,
                        is_pair=test_pair, one_tail=one_tail)
    p_value_ = test_.p_value
    symbol_ = test_.symbol
    if p_value_ <= alpha_p:
        txt_ = symbol_
    else:
        txt_ = str(np_.round(p_value_, 3))

    plt_.text((x1_ + x2_) / 2, y2_ + block_p, txt_, rotation=0, rotation_mode='anchor', color=color_font,
              fontsize=size_txt_, verticalalignment="center", horizontalalignment="center")

    # 用于扩充figure自适应范围
    plt__ = plt_.scatter((x1_ + x2_) / 2, y2_ + dia_y)
    plt__.set_visible(False)

    return x_, y_, test_, y_axis_ran


# 十六进制、RGB、RGBA颜色转换
def hex_2_rgb(value_):
    """
    hex to rgb color
    :param value_: hex color
    :return: numpy.array, rgb color
    """
    value_ = value_.lstrip('#')
    lv_ = len(value_)

    return np.array(int(value_[i: i + lv_ / 3], 16) for i in range(0, lv_, lv_ / 3))


def rgb_2_hex(rgb_):
    """
    rgb to hex color
    :param rgb_: rgb color
    :return: str, hex color
    """
    return "#" + "".join([i[2:] if len(i[2:]) > 1 else '0' + i[2:] for i in [hex(rgb_[0]), hex(rgb_[1]), hex(rgb_[2])]])


def rgba_2_rgb(rgba_, background_color_=None):
    """
    rgba to rgb color
    :param rgba_: rgba color
    :param background_color_: only rgb color is allowed
    :return: numpy.array, rgb color
    """
    if type(None) == type(background_color_):
        background_color_ = [1, 1, 1]

    rgba__ = rgba_.copy()
    if len(rgba__) == 1:
        rgba__ = rgba__[0]

    rgb = np.array(rgba__[:3]) * rgba__[3] + np.array(background_color_) * (1 - rgba__[3])

    return rgb


def set_base_color(plt_, base_color_):
    """
    Set the axis color. Note that line.set_color did not reflect, so just set invisible for the scale line.
    :param plt_: plot canvas or subplot canvas obj
    :param base_color_: axis color
    :return: plot canvas or subplot canvas obj
    """
    ax1_ = plt_.gca()
    ax1_.spines['top'].set_color(base_color_)
    ax1_.spines['right'].set_color(base_color_)
    ax1_.spines['bottom'].set_color(base_color_)
    ax1_.spines['left'].set_color(base_color_)

    # line.set_color did not reflect, so just neglect
    for line in ax1_.yaxis.get_ticklines():
        line.set_visible(False)
    for line in ax1_.xaxis.get_ticklines():
        line.set_visible(False)

    return ax1_


def set_spines(plt_, lw=2):
    """
    Set top and right spines invisible, and set the linewidth of bottom and left spines.
    :param plt_: plot canvas obj
    :param lw: linewidth of bottom and left spines
    :return: plot canvas obj
    """
    ax1_ = plt_.gca()
    ax1_.spines['top'].set_visible(False)
    ax1_.spines['right'].set_visible(False)
    ax1_.spines['bottom'].set_linewidth(lw)  # 设置底部坐标轴的粗细
    ax1_.spines['left'].set_linewidth(lw)  # 设置左边坐标轴的粗细

    return ax1_


def mod_fun(array_):
    """
    get mod of an array
    :param array_:
    :return:
    """
    return np.dot(array_, array_) ** 0.5


def circle_curve_plot(ax, x1, x2, y1=0, y2=0, up_down='up', alpha=180, epsilon=1000, **kwargs):
    """
    need math
    """
    up_down = 1 if up_down in 'up' else -1

    alpha0 = alpha / 180 * math.pi
    l = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    h = (l / 2) * (1 / math.tan(alpha0 / 2))

    beta = math.atan((y2 - y1) / (x2 - x1)) if x2 != x1 else math.pi / 2

    gamma = abs(math.pi / 2 - beta)

    if beta == 0:
        dieta_x = 0
    elif beta <= math.pi / 2:
        dieta_x = h * math.cos(gamma)
    elif beta > math.pi / 2:
        dieta_x = - h * math.cos(gamma)

    dieta_y = - (h * math.sin(gamma)) if (beta != math.pi / 2) else 0

    x0 = (x1 + x2) / 2 + up_down * dieta_x
    y0 = (y1 + y2) / 2 + up_down * dieta_y

    r = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

    array1 = np.array([x1 - x0, y1 - y0])
    array2 = np.array([x2 - x0, y2 - y0])
    x_axis = np.array([1, 0])

    alpha1 = math.acos(np.dot(array1, x_axis) / (mod_fun(array1) * mod_fun(x_axis)))
    alpha2 = math.acos(np.dot(array2, x_axis) / (mod_fun(array2) * mod_fun(x_axis)))

    alpha1 = alpha1 if array1[1] >= 0 else 2 * math.pi - alpha1
    alpha2 = alpha2 if array2[1] >= 0 else 2 * math.pi - alpha2

    alpha1, alpha2 = min([alpha1, alpha2]), max([alpha1, alpha2])

    # circle
    cis = True if up_down == 1 else False
    if alpha2 - alpha1 < math.pi:
        cis = True

    elif alpha2 - alpha1 > math.pi:
        cis = False

    elif beta == math.pi / 2:
        pass

    elif alpha1 > math.pi / 2:
        cis = not cis

    if cis:
        alpha_range1 = np.arange(alpha1, alpha2, math.pi / epsilon)
    else:
        alpha_range1_1 = np.arange(alpha2, 2 * math.pi, math.pi / epsilon)
        alpha_range1_2 = np.arange(math.pi / epsilon, alpha1, math.pi / epsilon)
        alpha_range1 = np.concatenate([alpha_range1_1, alpha_range1_2])

    x_list = [r * math.cos(angle) + x0 for angle in alpha_range1]
    y_list = [r * math.sin(angle) + y0 for angle in alpha_range1]

    ax.plot(x_list, y_list, **kwargs)


def box_plot_decent(ax, data_, positions,
                    widths=0.4, whis=99,
                    box_edge_color='gray', box_edge_alpha=0.7,
                    box_face_color=(1, 0, 0, 0), lw=2,
                    scatter=True, scatter_color='gray',
                    random_props=3, s=10, alpha=1, edgecolors='none'):
    """

    :param ax:
    :param data_:
    :param positions:
    :param widths:
    :param whis:
    :param box_edge_color:
    :param box_edge_alpha:
    :param box_face_color:
    :param lw:
    :param scatter:
    :param scatter_color:
    :param random_props:
    :param s:
    :param alpha:
    :param edgecolors:
    :return:
    """
    ax.boxplot(data_,
               positions=positions, widths=widths, whis=whis, patch_artist=True, showfliers=False,
               boxprops={'color': box_edge_color, 'facecolor': box_face_color, 'linewidth': lw},
               whiskerprops={'color': box_edge_color, 'alpha': box_edge_alpha, 'linewidth': lw},
               capprops={'color': box_edge_color, 'alpha': box_edge_alpha, 'linewidth': lw},
               medianprops={'linestyle': '--', 'color': box_edge_color, 'alpha': box_edge_alpha, 'linewidth': lw})

    if scatter:
        if random_props is None:
            x_list = positions * len(data_)
        else:
            x_list = positions * len(data_) + (np.random.random(len(data_)) - 0.5) / random_props

        ax.scatter(x_list, data_, c=scatter_color, s=s, alpha=alpha, edgecolors=edgecolors)


def framework_plot(x0_, x1_, y0, y1):
    plt.plot([x0_, x0_], [y0, y1], c='black')
    plt.plot([x1_, x1_], [y0, y1], c='black')
    plt.plot([x0_, x1_], [y0, y0], c='black')
    plt.plot([x0_, x1_], [y1, y1], c='black')
