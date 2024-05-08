# -*- coding: UTF-8 -*-
# @Author: Zhang Senxin

"""
unclassified code
now only comtain NPS summary
"""

import pandas as pd


def summary_system(pathout, summary):
    isExists = os.path.exists(pathout + 'summary.txt')
    if isExists:
        summary0 = []
        for line in open(pathout + 'summary.txt'):
            summary0 += line.strip('\n').split('\t')
        if not (summary[0] in summary0):
            summary0 += summary
    else:
        summary0 = summary
    summary0 = pd.DataFrame(summary0)
    summary0.to_csv(pathout + "summary.txt", sep='\t', index=False, header=False)


def path_found(root_path_, file_name_, target='v3j', nps_target='total'):
    """
    BCR-Rep data path find system.
    :param root_path_: '/sibcb2/mengfeilonglab4/zhangsenxin/ZYW/'
    :param file_name_: target sample name
    :param target: 'v3j', 'igblast', 'NPS_pipeline'
    :param nps_target: 'total', 'select'
    :return: full path
    """
    run = file_name_.split('_', 1)[0]

    if 'RNA' in file_name_ or 'DNA' in file_name_:
        out_path_ = root_path_ + 'RNA/' + run + '/'
    else:
        out_path_ = root_path_ + 'NPS/human/' + run + '/'

    if target in 'v3j':
        out_path_ += 'v3j/' + file_name_ + '_IgH_v3j_clonotype.txt'
    elif target in 'igblast':
        out_path_ += 'igblast/' + file_name_ + '_IgH_blast_extract.txt'

    elif target in 'NPS_pipeline':
        if nps_target in 'total':
            out_path_ += 'NPS_pipeline/' + file_name_ + '/Intermediate_out/' + \
                         file_name_ + '_pair_alignment_select_t.csv'
        elif nps_target in 'igblast':
            out_path_1 = out_path_ + 'igblast/' + file_name_ + '_IgH_blast_extract.txt'
            out_path_2 = out_path_ + 'igblast/' + file_name_ + '_IgL_blast_extract.txt'
            out_path_ = [out_path_1, out_path_2]
        elif nps_target in 'full_length':
            out_path_1 = out_path_ + 'selec_alignment/' + file_name_ + '_IgH_alignment.txt'
            out_path_2 = out_path_ + 'selec_alignment/' + file_name_ + '_IgL_alignment.txt'
            out_path_ = [out_path_1, out_path_2]
        else:
            out_path_ += 'NPS_pipeline/' + file_name_ + '/C1_bitest_HLpair.csv'

    return out_path_


def reform_nps_data(nps_data):
    """
    Trans NPS cluster data to standard phylogenetic tree plot data.
    :param nps_data: NPS cluster data
    :return: standard phylogenetic tree plot data
    """
    raw_data = nps_data.copy()
    raw_data.loc[:, 'seq'] = [raw_data.loc[ab, 'H_CDR3'] + raw_data.loc[ab, 'L_CDR3'] for ab in raw_data.index]
    raw_data.loc[:, 'class'] = raw_data.loc[:, 'Ig_Class']
    raw_data.loc[:, 'counts'] = raw_data.loc[:, 'repeat']

    return raw_data
