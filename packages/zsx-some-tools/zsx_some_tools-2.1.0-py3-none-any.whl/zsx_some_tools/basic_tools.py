# -*- coding: UTF-8 -*-
# @Author: Zhang Senxin

"""
Functions for producing data
"""

import numpy as np
import pandas as pd
from collections import defaultdict, namedtuple
from functools import reduce


class LinearMapping(object):
    def __init__(self, x1, x2, y1, y2):
        """
        Mapping range to range: (x1, x1) <-> (y1, y2)
        :param x1: range1 start
        :param x2: range1 end
        :param y1: range2 start
        :param y2: range2 end
        """
        x_d = x2 - x1
        y_d = y2 - y1

        if not x_d:
            print('Warning: x_d = 0')
            self.ok = False
        elif not y_d:
            print('Warning: y_d = 0')
            self.ok = False
        else:
            self.ok = True

        self.x1 = x1
        self.y1 = y1
        self.k = y_d / x_d

    def map_x2y(self, x_new):
        if self.ok:
            return (x_new - self.x1) * self.k + self.y1
        else:
            return None

    def map_y2x(self, y_new):
        if self.ok:
            return (y_new - self.y1) / self.k + self.x1
        else:
            return None


# 全排列函数
fn = lambda x, code='': reduce(lambda y, z: [str(i) + code + str(j) for i in y for j in z], x)


def count_list(list_like_, sort=False, ascending=True, dict_out=False):
    """
    Perform a fast and decent calculation of the element frequency number.
    :param list_like_: iterable object (Any)
    :param sort: sort the result or not
    :param ascending: sort by ascending or not
    :param dict_out: output as dictionary or a pandas.DataFrame form.
    :return: summary of the given list.
    """
    if not len(list_like_):
        print('Warning: nothing in input.')
        if dict_out:
            return defaultdict(int)
        else:
            return pd.DataFrame(None, columns=[0, 1])

    if dict_out:
        countlist = defaultdict(int)
        for i in list_like_:
            countlist[i] += 1

        return countlist

    else:
        s_list = list(set(list_like_))
        if len(s_list) > 12 or type(list_like_) != list:
            countlist = defaultdict(int)
            for i in list_like_:
                countlist[i] += 1
            countlist = pd.DataFrame.from_dict(countlist, orient='index')
            countlist = countlist.reset_index()

        else:
            countlist = [[i, list_like_.count(i)] for i in s_list]
            countlist = pd.DataFrame(countlist)

        countlist.columns = [0, 1]

        if sort:
            countlist = countlist.sort_values(by=countlist.columns[1], ascending=ascending)

        return countlist


# keep the same order
def sort_set_list(list_data__):
    """
    Export a sorted result after perform set() function.
    :param list_data__: data neet to be set and sort
    :return: list that remove duplicates and sorted as the original order.
    """
    list_data_ = list(list_data__)
    set_list_ = list(set(list_data_))
    set_list_.sort(key=list_data_.index)

    return set_list_


# Normalize to normal distribution
def normalize_df(data_, axis=0):
    """
    Normalize the df to normal distribution.
    :param data_: pandas.DataFrame object
    :param axis: perform normalize under columns/rows independently or not, use axis=0, 1, or 'all'.
    Default is 'all'.
    :return: Normalized df
    """
    data__ = data_.copy()
    if type(axis) == int:
        data__ = (data__ - np.mean(data__, axis=axis)) / np.std(data__, axis=axis)

    elif axis == 'all':
        data__ = (data__ - np.mean(np.mean(data__))) / \
                 np.std(np.array(data__.values).reshape(data__.shape[0] * data__.shape[1], 1))

    else:
        raise ValueError('parameter \'axis\' should be set among 0, 1 and \'all\'.')

    return data__


# Normalize to separately [0, 1]
def double_norm(data_, axis='all'):
    """
    Normalize the df separately for those values are positive number (0.5, 1] or negative number [0, 0.5),
    while zero to 0.5. Usually used for heatmap plotting.
    :param data_: pandas.DataFrame object
    :param axis: perform double normalize under columns/rows independently or not, use axis=0, 1, or 'all'.
    Default is 'all'.
    :return: Double normalized df
    """
    data__ = data_.copy()
    if type(axis) == int:
        max_value_ = np.max(data__, axis=axis)
        min_value_ = -np.min(data__, axis=axis)
        if axis == 0:
            data__[data__ >= 0] = data__[data__ >= 0] / max_value_ / 2 + 0.5
            data__[data__ < 0] = data__[data__ < 0] / min_value_ / 2 + 0.5
        else:
            data__ = data__.T
            data__[data__ >= 0] = data__[data__ >= 0] / max_value_ / 2 + 0.5
            data__[data__ < 0] = data__[data__ < 0] / min_value_ / 2 + 0.5
            data__ = data__.T

    elif axis == 'all':
        max_value_ = np.max(np.max(data__))
        min_value_ = - np.min(np.min(data__))
        data__[data__ >= 0] = data__[data__ >= 0] / max_value_ / 2 + 0.5
        data__[data__ < 0] = data__[data__ < 0] / min_value_ / 2 + 0.5

    else:
        raise ValueError('parameter \'axis\' should be set among 0, 1 and \'all\'.')

    return data__


# test data set follows normal distribution or not
def normal_test(p_data_):
    """
    Perform Normal test.
    :param p_data_: data to be tested
    :return: p-value
    """
    from scipy import stats

    stat_ = []
    for i in range(p_data_.shape[1]):
        data_ = p_data_.loc[p_data_.iloc[:, i] != -1].iloc[:, i]
        data_ = data_.astype(float)
        stat_ += [stats.shapiro(data_)[1]]

    norm_ = False if np.max(stat_) > 0.1 else True

    return norm_


# trans p value
def mark_pval(p_v_):
    """
    Trans p-value to '*' marks
    :param p_v_: p-value
    :return: 'Ns', '.', or '*' * n
    """
    if p_v_ < 0.0001:
        return '****'
    elif p_v_ < 0.001:
        return '***'
    elif p_v_ < 0.01:
        return '**'
    elif p_v_ < 0.05:
        return '*'
    elif p_v_ < 0.1:
        return '·'
    else:
        return 'Ns'


def effect_size_hedges_g(test_data_, test_data2_, summary=True, rounding=False, rounding_int=False):
    """
    Served for the effect size
    :param test_data_:
    :param test_data2_:
    :param summary:
    :param rounding:
    :param rounding_int:
    :return:
    """
    n1_ = len(test_data_)
    n2_ = len(test_data2_)
    m1_ = np.mean(test_data_)
    m2_ = np.mean(test_data2_)
    me1_ = np.quantile(test_data_, 0.5)
    me2_ = np.quantile(test_data2_, 0.5)
    sd1_ = np.std(test_data_)
    sd2_ = np.std(test_data2_)

    sd_star_ = ((sd1_ ** 2 * (n1_ - 1) + sd2_ ** 2 * (n2_ - 1)) / (n1_ + n2_ - 2)) ** 0.5
    g_size_ = (m1_ - m2_) / sd_star_

    if summary:
        info_ = [g_size_, n1_, n2_, m1_, m2_, me1_, me2_, sd1_, sd2_, sd_star_]
        if rounding_int:
            info_ = [np.round(i_, rounding) for i_ in info_]
        return info_
    else:
        if rounding_int:
            g_size_ = np.round(g_size_, rounding)
        return g_size_


def simple_test(test_data, test_data2=False, is_pair=False, summary=False, one_tail=True,
                norm_fix=None, equal_var=None, rounding=4):
    """
    Perform auto-test on two given samples.
    :param test_data: sample1
    :param test_data2: sample2
    :param is_pair: If paired-test will be performed.
    :param summary: output detailed test infomation or only P-value
    :param one_tail: do one-tail or two-tail test
    :param norm_fix: If the test fixes normal distribution or not.
    Default is None, then will perform normal distribution test to determine it.
    If True, normal distribution is directly determined, vice versa.
    :param equal_var: If the test fixes equal_var or not, only used when t test is performed.
    :param rounding: numpy.round(obj, rounding) will be performed for P-value
    :return: Test result.
    """
    from scipy import stats

    # if len(test_data.shape) == 1:
    #     dim = 1
    if len(test_data.shape) == 2:
        if test_data.shape[1] != 1:
            print('Error! Dim of data input is larger than 1!')
            return
    if type(test_data2) == bool:
        print('Sorry Error! Single sample test is not supported now!')
        return

    if one_tail:
        larger = 1 if np.mean(test_data) > np.mean(test_data2) else 0

    rounding_int = 1 if (not rounding and type(rounding) == int) else rounding

    if norm_fix is None:
        norm1 = stats.shapiro(test_data)[1]
        norm2 = stats.shapiro(test_data2)[1]

        norm = False if min([norm1, norm2]) <= 0.05 else True

    elif norm_fix:
        norm1 = 1
        norm2 = 1
        norm = True
    else:
        norm1 = 0
        norm2 = 0
        norm = False

    is_equal_var = 'None'

    if is_pair:
        if len(test_data) != len(test_data2):
            print('Jian Gui Error! unpaired length of data input can not do paired test!')
            return

        if norm:
            stat = stats.ttest_rel(test_data, test_data2)[1]
            name = 'Paired t-test'
            if one_tail:
                stat = stat / 2

        else:
            name = 'Wilcoxon signed rank test'
            if one_tail:
                if larger:
                    stat = stats.wilcoxon(test_data, test_data2, alternative='greater')[1]
                else:
                    stat = stats.wilcoxon(test_data2, test_data, alternative='greater')[1]
            else:
                stat = stats.wilcoxon(test_data, test_data2, alternative='two-sided')[1]

    else:
        if norm:
            if equal_var is None:
                var_p_ = stats.levene(test_data, test_data2)[1]
            elif equal_var:
                var_p_ = 0.1
            else:
                var_p_ = 0.01

            if var_p_ > 0.05:
                is_equal_var = True
                name = 'Homogeneity of variance unpaired t-test'
            else:
                is_equal_var = False
                name = 'Heterogeneity of variance unpaired t-test'

            stat = stats.ttest_ind(test_data, test_data2, equal_var=is_equal_var)[1]
            if one_tail:
                stat = stat / 2

        else:
            name = 'Mann-Whitney U test'
            if one_tail:
                if larger:
                    stat = stats.mannwhitneyu(test_data, test_data2, alternative='greater')[1]
                else:
                    stat = stats.mannwhitneyu(test_data2, test_data, alternative='greater')[1]
            else:
                stat = stats.mannwhitneyu(test_data, test_data2, alternative='two-sided')[1]

    if not summary:
        if rounding_int:
            return np.round(stat, rounding)
        else:
            return stat

    else:
        effect_size_info = effect_size_hedges_g(test_data, test_data2, summary=True,
                                                rounding=rounding, rounding_int=rounding_int)

        if stat >= 0.1:
            larger_res = ' = '
        elif one_tail:
            larger_res = ' > ' if larger else ' < '
        else:
            larger_res = ' != '

        symbol = mark_pval(stat)

        summary = namedtuple('test_summary', ['p_value', 'relationship', 'symbol', 'normal', 'pair',
                                              'equal_var', 'name', 'effect_size', 'n1', 'n2', 'm1',
                                              'm2', 'me1', 'me2', 'sd1', 'sd2', 'sd_star'])

        if rounding_int:
            summary_info = [np.round(stat, rounding), larger_res, symbol,
                            {'normal': str(norm), 'data1_p': np.round(norm1, rounding),
                             'data2_p': np.round(norm2, rounding)},
                            str(is_pair), str(is_equal_var), name] + effect_size_info
        else:
            summary_info = [stat, larger_res, symbol, {'normal': str(norm), 'data1_p': norm1, 'data2_p': norm2},
                            str(is_pair), str(is_equal_var), name] + effect_size_info

        return summary._make(summary_info)


def permutation_test(sample1_, sample2_, iter_num=10000, summary=False, one_tail=False, rounding=4):
    """
    Perform permutation test on two given samples.
    :param sample1_: sample1
    :param sample2_: sample2
    :param iter_num: cycle number to divide mixed sample randomly that is the core link of the test.
    :param summary: output detailed test infomation or only P-value
    :param one_tail: do one-tail or two-tail test
    :param rounding: numpy.round(obj, rounding) will be performed for P-value
    :return: Test result.
    """
    import math
    import random
    from collections import namedtuple

    n1 = len(sample1_)
    n2 = len(sample2_)

    rounding_int = 1 if (not rounding and type(rounding) == int) else rounding

    if math.comb(n1 + n2, n1) < iter_num:
        return 'so easy!'

    d0_ = np.mean(sample1_) - np.mean(sample2_)
    if not one_tail:
        d0_ = abs(d0_)

    all_sample_ = list(sample1_) + list(sample2_)

    new_distribution = []
    for _ in range(iter_num):
        random.shuffle(all_sample_)
        d1_ = sum(all_sample_[: n1]) / n1 - sum(all_sample_[n1:]) / n2
        if not one_tail:
            d1_ = abs(d1_)
        new_distribution += [d1_]

    p_ = np.count_nonzero(d0_ >= new_distribution) / iter_num
    larger = 0
    if p_ > 0.5:
        p_ = 1 - p_
        larger = 1

    if not one_tail:
        p_ = p_ * 2

    if not summary:
        if rounding_int:
            return np.round(p_, rounding)
        else:
            return p_

    else:
        if p_ >= 0.1:
            larger_res = ' = '
        elif one_tail:
            larger_res = ' > ' if larger else ' < '
        else:
            larger_res = ' != '

    symbol = mark_pval(p_)
    summary = namedtuple('test_summary', ['p_value', 'relationship', 'symbol', 'name'])

    if rounding_int:
        return summary(np.round(p_, rounding), larger_res, symbol, {'two-tail': not one_tail})
    else:
        return summary(p_, larger_res, symbol, {'two-tail': not one_tail})


# input function to test computing time
def comput_time(func, *args, iter_num=100, round_num=4, **kwargs):
    """
    Test function time used.
    :param func: function name
    :param args: function args if necessary
    :param iter_num: cycle number
    :param round_num: numpy.round(obj, round_num) will be performed before output time info
    :param kwargs: function keyword args if necessary
    :return: mean time used per cycle
    """
    import time

    t1 = time.time()
    for _ in range(iter_num):
        func(*args, **kwargs)

    t2 = time.time()

    return np.round(t2 - t1, round_num)


def exactly_round(float_like_, round_num_):
    """
    Round number to a string form in a given decimal places.
    :param float_like_: float or int object
    :param round_num_: round the given number
    :return: string number
    """
    float_like_ = str(np.round(float(float_like_), round_num_))
    length_ = len(float_like_.split('.')[1])

    if length_ == round_num_:
        return float_like_
    else:
        diff = round_num_ - length_

        return float_like_ + '0' * diff


def time_trans(seconds_, second_round_num=2):
    """
    Trans time in a decent form.
    :param seconds_: int or float object indicates pure seconds
    :param second_round_num: out second will do np.round()
    :return: time in hour (if necessary), minute (if necessary) and seconds
    """
    if seconds_ == 0:
        return '0s'

    out_ = []
    m_, s_ = divmod(seconds_, 60)
    h_, m_ = divmod(m_, 60)
    s_ = np.round(s_, second_round_num)

    if h_:
        out_ += [str(h_) + 'h']
    if m_:
        out_ += [str(m_) + 'm']
    if s_:
        if 10 < seconds_ < 30:
            s_ = np.round(s_, 1)
        elif seconds_ > 30:
            s_ = int(s_)
        out_ += [str(s_) + 's']

    if not out_:
        return '0s'

    return ' '.join(out_)


def list_selection(list_like_, target='', exception=False, sep=False, logic_and=True):
    """
    Used for list with only str element.
    :param list_like_: 1d iterable object with str element
    :param target: element with such string will be selected (cooperated with param 'sep' and 'logic_and')
    :param exception: element with such string will not be selected (cooperated with param 'sep' and 'logic_and')
    :param sep: param 'target' and 'exception' will be split by sep
    :param logic_and: split param 'target' and 'exception' will be used in the logic 'and', 'or'
    :return: list after selected
    """

    if sep:
        target = target.split(sep)
    else:
        target = [target]

    if logic_and:
        list_like_ = [i for i in list_like_ if (not sum([0 if tar in i else 1 for tar in target]))]
    else:
        list_like_ = [i for i in list_like_ if sum([1 if tar in i else 0 for tar in target])]

    if exception:
        if sep:
            exception = exception.split(sep)
        else:
            exception = [exception]

        if logic_and:
            list_like_ = [i for i in list_like_ if not sum([1 if exc in i else 0 for exc in exception])]
        else:
            list_like_ = [i for i in list_like_ if sum([0 if exc in i else 1 for exc in exception])]

    return list_like_


# md5 check
def get_md5(file_path_, hash_type='md5', ram=4000000):
    """
    Perform hash algorithm for file, default is md5.
    :param file_path_: file path
    :param hash_type: type of hash algorithm, default is md5
    :param ram: ram using
    :return: hash value
    """
    import hashlib

    hash_type_list = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s']
    if hash_type not in hash_type_list:
        raise ValueError('hash_type only support md5, sha1, sha224, sha256, sha384, sha512, blake2b, and blake2s')

    string_ = 'm_ = hashlib.' + hash_type + '()'
    exec(string_, None, globals())
    # m_ = hashlib.md5()
    with open(file_path_, 'rb') as fobj:
        while True:
            data_ = fobj.read(ram)
            if not data_:
                break
            m_.update(data_)

    return m_.hexdigest()


def get_order_ind(list_like_, ascending=True):
    """
    get sort_index
    :param list_like_:
    :param ascending:
    :return:
    """
    list_like_ind_ = list(range(len(list_like_)))
    process_obj = pd.DataFrame([list_like_ind_, list_like_]).T
    process_obj = process_obj.sort_values(by=1, ascending=ascending)
    process_obj = process_obj.reset_index(drop=True)

    order_dict_ = {}
    for order_, id_ in zip(process_obj.index, process_obj.iloc[:, 0]):
        order_dict_[order_] = int(id_)

    return order_dict_


def get_first_x_ind(list_like_, order=0, ascending=True):
    """

    :param list_like_:
    :param order:
    :param ascending:
    :return:
    """
    order_dict_ = get_order_ind(list_like_, ascending=ascending)
    try:
        return [order_dict_[i_] for i_ in order]
    except TypeError:
        return order_dict_[order]


def remove_list(list_, value_):
    """

    :param list_:
    :param value_:
    :return:
    """
    while value_ in list_:
        list_.remove(value_)

    return list_


def remove_duplicate_list(list_):
    """
    Remove duplicates from input list_like and keep each identity's first order
    :param list_: list_like
    :return: list
    """
    _dict = {}
    try:
        for _i in list_:
            _dict[_i] = ''

        return list(_dict.keys())

    except TypeError:
        str_list = [str(i) for i in list_]
        for _i in str_list:
            _dict[_i] = ''

        res_ = []
        for info_ in _dict.keys():
            string = 'a_ = ' + info_
            exec(string, None, globals())
            res_ += [a_]

        return res_


def trans_number(num_):
    """
    change 10000000 to 10,000,000
    :param num_: int number
    :return:
    """
    string_num = str(num_)
    if len(string_num) <= 3:
        return string_num

    string_num_out = ''
    for i_ in range(0, len(string_num) - 3, 3):
        if i_ == 0:
            string_num_out = ',' + string_num[-3:] + string_num_out
        else:
            string_num_out = ',' + string_num[-(i_ + 3): -i_] + string_num_out

    string_num_out = string_num[:-(i_ + 3)] + string_num_out

    return string_num_out


def assign_tasks(weight_list, weight_label=None, max_volume=100, summary=False):
    """

    :param weight_list:
    :param weight_label:
    :param max_volume:
    :param summary:
    :return:
    """
    if weight_label is None:
        weight_label = list(range(len(weight_list)))

    perform_df = pd.DataFrame([weight_list, weight_label]).T.sort_values(0, ascending=False)
    if perform_df.iloc[0, 0] > max_volume:
        raise ValueError('the single obj is higher than \'max_volume\'')

    min_bucket = sum(weight_list) // max_volume

    assign_df = pd.DataFrame([max_volume] * min_bucket)
    assign_dict = {}
    now_bucket = min_bucket - 1

    for weight, label in perform_df.values:
        max_space = np.max(assign_df.iloc[:, 0])
        if max_space >= weight:
            use_bucket = np.argmax(assign_df.iloc[:, 0] >= weight)
            assign_dict[label] = use_bucket
            assign_df.iloc[use_bucket, 0] -= weight
        else:
            now_bucket += 1
            assign_dict[label] = now_bucket
            assign_df = pd.concat([assign_df, pd.DataFrame([max_volume - weight], index=[now_bucket])])

    if summary:
        return assign_dict, assign_df
    else:
        return assign_dict


def has_chinese(string):
    """
    Check is chinese existed in given string
    :param string:
    :return:
    """
    if re.search('[\\u4e00-\\u9fff]', string):
        return True
    return False


def screen_search(search_paths, confidence=0.8, break_threshold=60, search_interval=1):
    """
    Search given picture(s) in iteration.
    :param search_paths: string or list object
    :param confidence:
    :param break_threshold: times
    :param search_interval: seconds
    :return:
    """
    import pyautogui

    if type(search_paths) is str:
        search_paths = [search_paths]

    length = len(search_paths)
    break_time = 0
    while True:
        break_time += 1
        for i_, search_path in enumerate(search_paths):
            try:
                location_ = pyautogui.locateOnScreen(search_path, confidence=confidence)
            except pyautogui.ImageNotFoundException:
                pass
            else:
                if location_ is not None:
                    return location_, i_

            time.sleep(search_interval / length)

        if break_time > break_threshold:
            raise TimeoutError('Out of time limit!')


# A function to determine the row and column position of a certain element in a two-dimensional array or df
def find_2d_pos(target_2d, target_element, get_order=None, default_return=None):
    """

    :param target_2d:
    :param target_element:
    :param get_order:
    :param default_return:
    :return:
    """
    bool_array = target_2d == target_element
    counts = np.sum(bool_array)
    if not counts:
        return default_return

    shape = target_2d.shape
    row_number = np.array(list(range(shape[0])) * shape[1]).reshape([shape[1], shape[0]]).T
    col_number = np.array(list(range(shape[1])) * shape[0]).reshape(shape) / 10 ** len(str(shape[1]))

    pos_array = row_number + col_number

    target_pos = pos_array[bool_array]

    if get_order is not None:
        return [int(i_) for i_ in str(target_pos[get_order]).split('.')]
    else:
        return [[int(i_) for i_ in str(j_).split('.')] for j_ in target_pos]


# split y axis in two range
def split_2_ranges(value_, max_value, threshold1=0.5, threshold2=1, thres_value=0.05):
    if value_ < 0:
        value_ = -value_
        fu = True
    else:
        fu = False

    if value_ <= thres_value:
        value_new = (value_ / thres_value) * threshold1
    else:
        ratio = (value_ - thres_value) / (max_value - thres_value)
        value_new = (threshold2 - threshold1) * ratio + threshold1

    if fu:
        value_new = - value_new

    return value_new