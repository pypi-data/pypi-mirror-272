# -*- coding: UTF-8 -*-
# @Author: Zhang Senxin

"""
Functions for bio-analysis
"""

from collections import defaultdict
from functools import reduce
import gzip
import os
import pandas as pd
import numpy as np


# PDB file related infomation
class PDBfilereader(object):
    from collections import defaultdict as __defaultdict
    from collections import namedtuple as __namedtuple

    __columns = ['ATOM', 'serial', 'SPACE1', 'name', 'altLoc', 'resName', 'SPACE1', 'chainID', 'resSeq',
                 'iCode', 'SPACE3', 'x', 'y', 'z', 'occupancy', 'tempFactor', 'SPACE6', 'segID', 'element', 'charge']

    __split = [0, 6, 11, 12, 16, 17, 20, 21, 22, 26, 27,
               30, 38, 46, 54, 60, 66, 72, 76, 78, 80]

    __type = [str, int, str, str, str, str, str, str, int,
              str, str, float, float, float, float, float, str, str, str, str]

    __round = [False, False, False, False, False, False, False, False, False,
               False, False, 3, 3, 3, 2, 2, False, False, False, False]

    __direction = ['left', 'right', 'left', 'middle', 'left', 'left', 'left', 'left', 'right',
                   'left', 'left', 'right', 'right', 'right', 'right', 'right', 'left', 'left', 'right', 'left']

    __info = __namedtuple('pdb_info', ['split_info', 'type_info', 'round_info', 'direction_info'])
    __info_dict = __defaultdict(tuple)
    for __i, __col in enumerate(__columns):
        __info_use = __info(__split[__i: __i + 2], __type[__i], __round[__i], __direction[__i])
        __info_dict[__col] = __info_use

    def __init__(self, silence=False):
        if not silence:
            print('pdb_columns = pdb_file_reader.columns\n'
                  'pdb_split = pdb_file_reader.split\n'
                  'pdb_type = pdb_file_reader.typing\n'
                  'pdb_round = pdb_file_reader.rounding\n'
                  'pdb_direction = pdb_file_reader.direction\n'
                  'pdb_info_dict = pdb_file_reader.info_dict')

    @property
    def columns(self):
        return self.__columns

    @property
    def split(self):
        return self.__split

    @property
    def typing(self):
        return self.__type

    @property
    def rounding(self):
        return self.__round

    @property
    def direction(self):
        return self.__direction

    @property
    def info_dict(self):
        return self.__info_dict


# amino acid related infomation
class Aminoacid(object):
    from collections import defaultdict as __defaultdict

    __seqnum = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
                'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '*']
    __aa_dict = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
        "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G"}

    __nt_dict = __defaultdict(list)
    for __nt in __aa_dict.keys():
        __nt_dict[__aa_dict[__nt]] += [__nt]

    # 三元组的命名为被排除者的后继字母
    __degeneracy = {'W': ['A', 'T'], 'S': ['G', 'C'], 'K': ['G', 'T'], 'M': ['A', 'C'], 'R': ['A', 'G'],
                    'Y': ['C', 'T'],
                    'B': ['T', 'C', 'G'], 'D': ['T', 'A', 'G'], 'H': ['T', 'C', 'A'], 'V': ['A', 'C', 'G'],
                    'N': ['A', 'C', 'T', 'G']}

    __aa_one_three = {'VAL': 'V', 'ILE': 'I', 'LEU': 'L', 'GLU': 'E', 'GLN': 'Q',
                      'ASP': 'D', 'ASN': 'N', 'HIS': 'H', 'TRP': 'W', 'PHE': 'F',
                      'TYR': 'Y', 'ARG': 'R', 'LYS': 'K', 'SER': 'S', 'THR': 'T',
                      'MET': 'M', 'ALA': 'A', 'GLY': 'G', 'PRO': 'P', 'CYS': 'C'}
    three_letter = dict([[v, k] for k, v in __aa_one_three.items()])
    __aa_one_three.update(three_letter)

    def __init__(self, silence=False):
        if not silence:
            print('aa_dict = amino_acid_info.aa_dict\n'
                  'nt_dict = amino_acid_info.nt_dict\n'
                  'degeneracy = amino_acid_info.degeneracy\n'
                  'seqnum = amino_acid_info.seqnum\n'
                  'aa_one_three = amino_acid_info.aa_one_three')

    @property
    def seqnum(self):
        """
        Amino acid list
        :return:
        """
        return self.__seqnum

    @property
    def aa_dict(self):
        """
        Codon to amino acid
        :return:
        """
        return self.__aa_dict

    @property
    def nt_dict(self):
        """
        Amino acid to codon list
        :return:
        """
        return self.__nt_dict

    @property
    def degeneracy(self):
        return self.__degeneracy

    @property
    def aa_one_three(self):
        """
        Amino acid name in 3 letters to 1 letter
        :return:
        """
        return self.__aa_one_three

    def translate(self, dna_reference, silence=False, cut=False):
        return translate(dna_reference, self.__aa_dict, silence=silence, cut=cut)


class SeqDistComp(object):
    """
    A useful sequence distance tool, now only allows same length sequences.
    """

    def __init__(self, seq_list1=None, seq_list2=None,
                 seq_type=None, element=None, encoding='one-hot'):  # , method='hamming', func=None
        if seq_list2 is None:
            seq_list2 = seq_list1

        if seq_type is not None:
            seq_type = seq_type.lower().replace(' ', '')
            if seq_type in ['aa', 'aminoacid', 'protein', 'p']:
                seq_type = 'aa'
            elif seq_type in ['nt', 'nucleotide', 'dna', 'n']:
                seq_type = 'nt'
        elif element is None:
            if seq_list1 is None:
                find_type = {'A', 'T', 'G', 'C', 'N'}
            else:
                find_type = ''.join(seq_list1[:10]) + ''.join(seq_list2[:10])
                find_type = set(list(find_type))

            seq_type = 'aa' if (find_type - {'A', 'T', 'G', 'C', 'N'}) else 'nt'
        else:
            seq_type = 'custom'

        if element is None:
            if seq_type == 'nt':
                element = ['A', 'T', 'G', 'C', 'N']
            else:
                amino_acid_info = Aminoacid(silence=True)
                element = amino_acid_info.seqnum

        encoding = self._encoding_check(encoding)

        self.seq1 = seq_list1
        self.seq2 = seq_list2
        self.seq_type = seq_type
        self.element = element
        self.encoding = encoding

        self.seq1_coding = None
        self.seq2_coding = None

    def _encoding_check(self, encoding):
        if encoding is None:
            encoding = self.encoding

        if encoding.lower() in ['one-hot', 'onehot']:
            encoding = 'one-hot'
        elif encoding.lower() in ['index']:
            encoding = 'index'
        else:
            encoding = 'one-hot'
            print('Warning: encoding name cannot be understood, \'one-hot\' is automatically performed.')

        return encoding

    @classmethod
    def _seq_check(cls, seq1, seq2):
        if (seq1 is None) and (seq2 is None):
            raise ValueError('sequence information is missing.')
        elif seq2 is None:
            seq2 = seq1

        return seq1, seq2

    def _method_check(self, method, encoding):
        if method is None:
            encoding = self._encoding_check(encoding)
            if encoding in 'one-hot':
                method = 'hamming'
                self.method = 'hamming'
            else:
                method = 'euclidean'
                self.method = 'euclidean'
            print('method automatically used', '\'' + method + '\'')

        elif method in 'hamming':
            method = 'hamming'
            self.method = 'hamming'
        elif method in 'euclidean':
            method = 'euclidean'
            self.method = 'euclidean'
        elif method in 'consecutive':
            method = 'consecutive'
            self.method = 'consecutive'

        return method

    def _encoding_seqs(self, seq_, encoding=None, element=None, flatting=False):
        if element is None:
            element = self.element
        encoding = self._encoding_check(encoding)

        if encoding == 'one-hot':
            def default_out():
                return [0] * (len(element) - 1) + [1]

            auto_index = defaultdict(default_out)
            for i_ in range(len(element)):
                aa = [0] * len(element)
                aa[i_] = 1
                auto_index[element[i_]] = aa if flatting else [aa]

        else:
            def default_out():
                return len(element)

            auto_index = defaultdict(default_out)
            for i_ in range(len(element)):
                auto_index[element[i_]] = [i_]

        def chain_encoding(seq__):
            ba = []
            for ab in seq__:
                ba += auto_index[ab]
            return ba

        return np.array([chain_encoding(one_seq) for one_seq in seq_])

    def encoding_seqs(self, seq1=None, seq2=None, encoding=None, flatting=False):
        element = self.element
        if seq1 is None:
            seq1 = self.seq1
        if seq2 is None:
            seq2 = self.seq2
        if encoding is not None:
            self.encoding = encoding

        seq1, seq2 = self._seq_check(seq1, seq2)

        seq1_coding = self._encoding_seqs(seq1, encoding, element=element, flatting=flatting)
        seq2_coding = self._encoding_seqs(seq2, encoding, element=element, flatting=flatting)

        self.seq1_coding = seq1_coding
        self.seq2_coding = seq2_coding

        return seq1_coding, seq2_coding

    @staticmethod
    def consecutive_distance(chain1, chain2):
        chain = abs(chain1 - chain2)
        xa = list(map(str, chain))
        xa = ''.join(xa)
        xb = xa.split(sep='0')
        tt = [len(i_) ** 2 for i_ in xb]
        xc = sum(tt)

        return xc

    @staticmethod
    def hamming_distance_matrix(P, C):
        difference = P.reshape(P.shape[0], 1, P.shape[1]) - C.reshape(1, C.shape[0], C.shape[1])
        distance = np.sum(abs(difference) != 0, axis=2)

        return distance

    @staticmethod
    def hamming_distance(chain1, chain2):
        chain = abs(chain1 - chain2)
        xb = np.sum(chain != 0)

        return xb

    @staticmethod
    def euclidean_distance_matrix(P, C):
        A = (P ** 2).sum(axis=1, keepdims=True)
        B = (C ** 2).sum(axis=1, keepdims=True).T

        return (A + B - 2 * np.dot(P, C.T)) / 2

    @staticmethod
    def euclidean_distance(chain1, chain2):
        return np.sum(abs(chain1 - chain2)) / 2

    @staticmethod
    def coding_check(seq_coding, num_):
        length = set([len(i_) for i_ in seq_coding])
        if len(length) > 1:
            raise ValueError('seq' + num_ + '_coding has multiple length, please check seq' + num_)

    def computing_dist(self, seq1=None, seq2=None, seq1_coding=None,
                       seq2_coding=None, encoding=None, method=None):
        if (seq1_coding is None) and (self.seq1_coding is None) and (seq1 is None) and (self.seq1 is None):
            raise ValueError('Nothing is given.')

        elif seq1_coding is not None:
            seq1_coding, seq2_coding = self._seq_check(seq1_coding, seq2_coding)

        elif seq1 is not None:
            encoding = self._encoding_check(encoding)
            if seq2 is None:
                seq2 = seq1
            seq1_coding, seq2_coding = self.encoding_seqs(seq1=seq1, seq2=seq2, encoding=encoding, flatting=True)

        elif self.seq1_coding is not None:
            seq1_coding = self.seq1_coding
            seq2_coding = self.seq2_coding

        elif self.seq1 is not None:
            encoding = self._encoding_check(encoding)
            if seq1 is None:
                seq1 = self.seq1
            if seq2 is None:
                seq2 = self.seq2
            if seq2 is None:
                seq2 = seq1
            seq1_coding, seq2_coding = self.encoding_seqs(seq1=seq1, seq2=seq2, encoding=encoding, flatting=True)

        self.coding_check(seq1_coding, '1')
        self.coding_check(seq2_coding, '2')

        method = self._method_check(method, encoding)
        if method in 'hamming':
            from .read_write_tools import get_memory
            memory_free = get_memory()
            size_estimate = seq1_coding.shape[0] * seq2_coding.shape[0] * seq2_coding.shape[1] * 4 * 2
            if memory_free > size_estimate:
                distance = self.hamming_distance_matrix(seq1_coding, seq2_coding)
            else:
                from scipy import spatial
                distance = spatial.distance.cdist(seq1_coding, seq2_coding, self.hamming_distance)
                print('Matrix method need', size_estimate, 'now is less than', memory_free, 'so we use loop method')

        elif method in 'euclidean':
            from .read_write_tools import get_memory
            memory_free = get_memory()
            size_estimate = seq1_coding.shape[0] * seq2_coding.shape[0] * seq2_coding.shape[1] * 4 * 2
            if memory_free > size_estimate:
                distance = self.euclidean_distance_matrix(seq1_coding, seq2_coding)
            else:
                from scipy import spatial
                distance = spatial.distance.cdist(seq1_coding, seq2_coding, self.euclidean_distance)
                print('Matrix method need', size_estimate, 'now is less than', memory_free, 'so we use loop method')

        elif method in 'consecutive':
            from scipy import spatial
            distance = spatial.distance.cdist(seq1_coding, seq2_coding, self.consecutive_distance)

        return distance


# PDB file read write
def read_pdb_file(path_, remark_read=False):
    """
    Read pdb file.
    :param path_: pdb file path
    :param remark_read: save remark info
    :return: pdb file
    """

    def read_pdb_line(line__, pdb_columns_, pdb_info_dict_):
        line_info_ = []
        for col__ in pdb_columns_:
            split_info_ = pdb_info_dict_[col__].split_info
            type_info_ = pdb_info_dict_[col__].type_info

            try:
                info_ = type_info_(line__[split_info_[0]: split_info_[1]].strip(' '))
            except ValueError:
                info_ = ''

            line_info_ += [info_]

        return line_info_

    pdb_file_reader = PDBfilereader(silence=True)
    pdb_columns = pdb_file_reader.columns
    pdb_info_dict = pdb_file_reader.info_dict

    data_ = []
    if remark_read:
        from .read_write_tools import wc_py
        from .basic_tools import remove_duplicate_list
        _num = wc_py(path_)
        remark_dict = {'lines': _num, 'file_type': 'simple'}
        remark_order = 0
        remark_info = []

    with open(path_, 'r+') as pdb_file_:
        for line_ in pdb_file_:
            if ('ATOM' not in line_) and ('HETATM' not in line_):
                if remark_read and 'REMARK' in line_:
                    line_ = line_.strip('\n').strip('REMARK   ')
                    remark_info += [line_]

            else:
                if remark_read:
                    equal_line = [remark_ for remark_ in remark_info if '=' in remark_]
                    if len(equal_line) >= 2:
                        # remark_info = [remark_ for remark_ in remark_info if '=' not in remark_] + equal_line[-1:]
                        remark_dict['file_type'] = 'multiple'
                        remark_info = remove_duplicate_list(remark_info)

                    for remark_ in remark_info:
                        if '=' not in remark_:
                            remark_order += 1
                            if remark_order >= 4:
                                break
                            remark_dict['REMARK_' + str(remark_order)] = remark_
                        else:
                            remark_ = remark_.split(' ')
                            chain_info = [i_ for i_ in remark_ if '=' not in i_]
                            if '5' in chain_info:
                                chain_info.remove('5')
                            if 'REMARK_chain_tyoe' not in remark_dict.keys():
                                remark_dict['REMARK_chain_type'] = ' '.join(chain_info)
                            else:
                                remark_dict['REMARK_chain_type'] += ',' + ' '.join(chain_info)

                            chain_name = [i_.split('=') for i_ in remark_ if '=' in i_]
                            for key, name in chain_name:
                                if key not in remark_dict.keys():
                                    remark_dict[key] = name
                                else:
                                    remark_dict[key] += ',' + name

                if remark_read == 'only':
                    break
                line_ = line_.strip('\n')
                data_ += [read_pdb_line(line_, pdb_columns, pdb_info_dict)]

    data_ = pd.DataFrame(data_, columns=pdb_columns)

    if remark_read == 'only':
        return remark_dict
    elif remark_read:
        return data_, remark_dict
    else:
        return data_


def write_pdb_file(path_, data_):
    """
    Save df to pdb file (Format requirements are strict)
    :param path_: save path
    :param data_: pdb df
    :return: None
    """
    from .basic_tools import exactly_round

    def write_pdb_block(string__, value__, col__, i__, pdb_info_dict_):
        split_info = pdb_info_dict_[col__].split_info
        round_info = pdb_info_dict_[col__].round_info
        direction_info = pdb_info_dict_[col__].direction_info

        if round_info:
            try:
                value__ = exactly_round(value__, round_info)
            except ValueError:
                value__ = ''

        value__ = str(value__)
        length_exp = split_info[1] - split_info[0]
        length_true = len(value__)
        if length_true == length_exp:
            string__ += value__
        elif length_true > length_exp:
            raise ValueError('Value in row \'' + str(i__) + '\' and in col \'' +
                             col__ + '\' (\'' + value__ + '\') is too long to be set in a PDB file.')
        else:
            diff = length_exp - length_true
            if direction_info == 'right':
                value__ = ' ' * diff + value__
            elif direction_info == 'left':
                value__ = value__ + ' ' * diff
            elif direction_info == 'middle':
                value__ = ' ' + value__ + ' ' * (diff - 1)
            string__ += value__

        return string__

    pdb_file_reader = PDBfilereader(silence=True)
    pdb_info_dict = pdb_file_reader.info_dict

    with open(path_, 'w+') as pdb_file_:
        for i_ in range(data_.shape[0]):
            string_ = ''
            for j_, col_ in enumerate(data_.columns):
                value_ = data_.iloc[i_, j_]
                string_ = write_pdb_block(string_, value_, col_, i_, pdb_info_dict)

            pdb_file_.write(string_ + '\n')


# will be deleted in next version ###!!!
def amino_acid():
    """
    Replaced by class Aminoacid()
    :return: amino acid related infomation
    """
    seqnum = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '*']
    aa_dict = {
        'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
        'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
        'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
        'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
        'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
        'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
        'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
        "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G"}

    nt_dict = defaultdict(list)
    for nt in aa_dict.keys():
        nt_dict[aa_dict[nt]] += [nt]

    # 三元组的命名为被排除者的后继字母
    other_name = {'W': ['A', 'T'], 'S': ['G', 'C'], 'K': ['G', 'T'], 'M': ['A', 'C'], 'R': ['A', 'G'], 'Y': ['C', 'T'],
                  'B': ['T', 'C', 'G'], 'D': ['T', 'A', 'G'], 'H': ['T', 'C', 'A'], 'V': ['A', 'C', 'G']}

    return seqnum, aa_dict, nt_dict, other_name


def design_motif(motif_name_):
    """
    Use nucleotide degeneracy name to design motifs. For example, 'WRC' motif equal to ['AAC', 'AGC', 'TAC', 'TGC']
    :param motif_name_: str, degeneracy name
    :return: list of nucleotide motif
    """
    from .basic_tools import fn

    amino_acid_info_ = Aminoacid(silence=True)
    degeneracy_ = amino_acid_info_.degeneracy

    motif_list_ = []
    for alphabet_ in motif_name_:
        if alphabet_ in degeneracy_.keys():
            motif_list_ += [degeneracy_[alphabet_]]
        else:
            motif_list_ += [[alphabet_]]

    return fn(motif_list_)


# dna to amino acid
def translate(dna_reference, aa_dictionary, silence=False, cut=False):
    """
    Translate nucleotide (DNA) sequence to amino acid (protein) sequence
    :param dna_reference: DNA sequence
    :param aa_dictionary: dict, keys are dna codons, values are amino acid names.
    :param silence: print warning message or not
    :param cut:
    :return: amino acid sequence
    """
    length = len(dna_reference)
    if length % 3 != 0:
        if cut:
            cut_length = length % 3
            dna_reference = dna_reference[: - cut_length]
        else:
            if silence:
                return None
            else:
                return print('DNA length can not be divided by 3.')

    return ''.join(aa_dictionary[dna_reference[3 * i: 3 * (i + 1)]] for i in range(length // 3))


def find_motif(sequence_, motif_, mot_p=2):
    """
    To find motif positions in such sequence
    :param sequence_: str, using sequence
    :param motif_: list, motif that designed by design_motif()
    :param mot_p: position start with the i_th nucleotide of the motif
    :return: list of positions that exist the motif
    """
    result_ = []
    mot_l = len(motif_[0])
    for i_ in range(len(sequence_) - len(motif_[0]) + 1):
        mot_ = sequence_[i_: i_ + mot_l]
        if mot_ in motif_:
            result_ += [i_ + mot_p]

    return result_


def count_motif(sequence_, motif_):
    """
    To calculate the number of motif in such sequence
    :param sequence_: str, using sequence
    :param motif_: list, motif that designed by design_motif()
    :return: int, motif counts
    """
    num_ = 0
    mot_l = len(motif_[0])
    if type(motif_) == str:
        motif_ = [motif_]
    for i_ in range(len(sequence_) - len(motif_[0]) + 1):
        mot_ = sequence_[i_: i_ + mot_l]
        if mot_ in motif_:
            num_ += 1

    return num_


def count_motif_list(sequence_, motif_):
    """
    To calculate the number of a list-motif in such sequence
    :param sequence_: str, using sequence
    :param motif_: list, motif that designed by design_motif()
    :return: dict that save motif counts
    """
    mot_l = len(motif_[0])
    if type(motif_) == str:
        motif_ = [motif_]
    num_dict_ = defaultdict(int)

    for i_ in range(len(sequence_) - len(motif_[0]) + 1):
        mot_ = sequence_[i_: i_ + mot_l]
        if mot_ in motif_:
            num_dict_[mot_] += 1

    return num_dict_


def extract_motif(sequence_, motif_, extract_1=6, extract_2=False):
    """

    :param sequence_:
    :param motif_:
    :param extract_1:
    :param extract_2:
    :return:
    """
    start = extract_1
    end = int(len(sequence_)) - (extract_2 + n_ - 1)
    n_ = len(motif_[0])

    result_ = []
    for i_ in range(start, end):
        mot = sequence_[i_: i_ + n_]
        if mot in motif_:
            seq_out = sequence_[i_ - extract_1: i_ + extract_2 + n_]
            seq_left = seq_out[: extract_1]
            seq_mid = seq_out[extract_1: extract_1 + n_]
            seq_end = seq_out[extract_1 + n_:]

            result_ += [[seq_left, seq_mid, seq_end]]

    return result_


def get_unique_clonotype(clonotype_data_):
    """

    :param clonotype_data_:
    :return:
    """
    iloc_ind = []
    ind_use = set()
    for ind in clonotype_data_.index:
        if ind not in ind_use:
            iloc_ind += [True]
            ind_use.add(ind)
        else:
            iloc_ind += [False]

    return clonotype_data_.iloc[iloc_ind]


# useless function
def get_chr_seq(chr_path):
    data_ = read_fasta(chr_path)

    return data_.iloc[:, 0].to_dict()


def read_fasta(path_, split=None):
    """
    Read fasta file as a df
    :param path_: fasta file path
    :param split: id info will split by the given separation and keep the front part
    :return: df, index is id, and only one column is sequence
    """

    fasta = []
    lines = []
    _string = ''

    with open(path_, 'r') as file_:
        for line_ in file_:
            line_ = line_.strip("\n\r")

            if '>' in line_:
                lines += [_string]
                fasta += [lines]
                _string = ''
                lines = [line_.split('>', 1)[-1].split(split)[0]]  # need more parameter
            else:
                _string += line_

    lines += [_string]
    fasta = fasta[1:] + [lines]
    fasta = pd.DataFrame(fasta, columns=['ID', 'seq']).set_index('ID')

    return fasta


def write_fasta(path_, data__):
    """
    Save fasta file
    :param path_: save path
    :param data__: df
    :return: None
    """
    data_ = data__.copy()
    if data_.shape[1] == 1:
        data_ = data_.reset_index()
    elif data_.shape[1] > 2:
        data_ = data_.iloc[:, :2]

    with open(path_, 'w+') as file_:
        for i in range(data_.shape[0]):
            file_.write('>' + str(data_.iloc[i, 0]) + '\n')
            file_.write(str(data_.iloc[i, 1]) + '\n')


def read_fasta_gz(path_, split=None, num_limit=0, decode='utf-8'):
    """
    Read fasta.gz file as a df
    :param path_: fasta file path
    :param split: id info will split by the given separation and keep the front part
    :param num_limit: stop reading at which line
    :param decode: decode parameter
    :return: df, index is id, and three columns for sequence, addition info, and sequencing quality
    """

    fasta = []
    lines = []
    _string = ''
    if num_limit == 0:
        num_limit = 99999999

    try:
        from xopen import xopen

        with xopen(path_, 'r') as file_:
            for i, line_ in enumerate(file_):
                line_ = line_.strip("\n\r")
                if ('\x00' in line_) and i > 0:
                    continue

                if '>' in line_:
                    lines += [_string]
                    fasta += [lines]
                    _string = ''
                    lines = [line_.split('>', 1)[-1].split(split)[0]]  # need more parameter
                else:
                    _string += line_

                if i == num_limit * 4:
                    break

    except ModuleNotFoundError:
        with gzip.open(path_, 'r+') as file_:
            for i, line_ in enumerate(file_):
                line_ = line_.decode(decode).strip("\n\r")
                if ('\x00' in line_) and i > 0:
                    continue

                if '>' in line_:
                    lines += [_string]
                    fasta += [lines]
                    _string = ''
                    lines = [line_.split('>', 1)[-1].split(split)[0]]  # need more parameter
                else:
                    _string += line_

                if i == num_limit * 4:
                    break

    lines += [_string]
    fasta = fasta[1:] + [lines]
    fasta = pd.DataFrame(fasta, columns=['ID', 'seq']).set_index('ID')

    return fasta


def write_fasta_gz(path_, data__):
    """
    Save fasta.gz file
    :param path_: save path
    :param data__: df
    :return: None
    """
    if data__.shape[1] == 1:
        data_ = data__.reset_index()
    elif data__.shape[1] > 2:
        data_ = data__.iloc[:, :2]
    else:
        data_ = data__

    try:
        from xopen import xopen

        with xopen(path_, 'w') as file_:
            for i in range(data_.shape[0]):
                file_.write('>' + str(data_.iloc[i, 0]) + '\n')
                file_.write(str(data_.iloc[i, 1]) + '\n')

    except ModuleNotFoundError:
        with gzip.open(path_, 'w+') as file_:
            for i in range(data_.shape[0]):
                file_.write(('>' + str(data_.iloc[i, 0]) + '\n').encode())
                file_.write((str(data_.iloc[i, 1]) + '\n').encode())


def read_fastq(path_, split=None):
    """
    Read fastq file as a df
    :param path_: fastq file path
    :param split: id info will split by the given separation and keep the front part
    :return: df, index is id, and three columns for sequence, addition info, and sequencing quality
    """
    fastq = []
    lines = []
    with open(path_, 'r+') as file:
        for i_, line_ in enumerate(file):
            line_ = line_.strip("\n\r")
            if i_ % 4 == 0:
                fastq += [lines]
                lines = [line_.split('@', 1)[-1].split(split)[0]]  # more parameter
            else:
                lines += [line_]

        fastq = fastq[1:] + [lines]
        fastq = pd.DataFrame(fastq, columns=['ID', 'seq', '+', 'qua']).set_index('ID')

    return fastq


def write_fastq(path_, data__):
    """
    Save fastq file
    :param path_: save path
    :param data__: df
    :return: None
    """
    if data__.shape[1] == 3:
        data_ = data__.reset_index()
    elif data__.shape[1] > 4:
        data_ = data__.iloc[:, :4]
    else:
        data_ = data__
    with open(path_, 'w+') as file_:
        for i in range(data_.shape[0]):
            file_.write('@' + str(data_.iloc[i, 0]) + '\n')
            file_.write(str(data_.iloc[i, 1]) + '\n')
            file_.write(str(data_.iloc[i, 2]) + '\n')
            file_.write(str(data_.iloc[i, 3]) + '\n')


def read_fastq_gz(path, split='.', num_limit=0, decode='utf-8'):
    """
    Read fastq.gz file as a df
    :param path: fastq file path
    :param split: id info will split by the given separation and keep the front part
    :param num_limit: stop reading at which line
    :param decode: decode parameter
    :return: df, index is id, and three columns for sequence, addition info, and sequencing quality
    """
    fastq = []
    lines = []
    if num_limit == 0:
        num_limit = 99999999

    try:
        from xopen import xopen

        with xopen(path, 'r') as file_:
            for i, line_ in enumerate(file_):
                line_ = line_.strip("\n\r")
                if ('\x00' in line_) and i > 0:
                    continue

                if i % 4 == 0:
                    fastq += [lines]
                    lines = [line_.split('@', 1)[-1].split(split)[0]]  # more parameter

                else:
                    lines += [line_]

                if i == num_limit * 4:
                    break

    except ModuleNotFoundError:
        with gzip.open(path, 'r') as file_:
            for i, line_ in enumerate(file_):
                line_ = line_.decode(decode).strip("\n\r")
                if ('\x00' in line_) and i > 0:
                    continue

                if i % 4 == 0:
                    fastq += [lines]
                    lines = [line_.split('@', 1)[-1].split(split)[0]]  # more parameter
                else:
                    lines += [line_]

                if i == num_limit * 4:
                    break

    fastq = fastq[1:] + [lines]
    fastq = pd.DataFrame(fastq, columns=['ID', 'seq', '+', 'qua']).set_index('ID')

    return fastq


def write_fastq_gz(path_, data_):
    """
    Save fastq.gz file
    :param path_: save path
    :param data_: df
    :return: None
    """
    if data_.shape[1] == 3:
        data_ = data_.reset_index()

    try:
        from xopen import xopen

        with xopen(path_, 'w') as file_:
            for i in range(data_.shape[0]):
                file_.write('@' + str(data_.iloc[i, 0]) + '\n')
                file_.write(str(data_.iloc[i, 1]) + '\n')
                file_.write(str(data_.iloc[i, 2]) + '\n')
                file_.write(str(data_.iloc[i, 3]) + '\n')

    except ModuleNotFoundError:
        with gzip.open(path_, 'w+') as file_:
            for i in range(data_.shape[0]):
                file_.write(('@' + str(data_.iloc[i, 0]) + '\n').encode())
                file_.write((str(data_.iloc[i, 1]) + '\n').encode())
                file_.write((str(data_.iloc[i, 2]) + '\n').encode())
                file_.write((str(data_.iloc[i, 3]) + '\n').encode())


def read_fq_as_fa(path_, split='.'):
    """
    Read fastq.gz file as a fasta file
    :param path_: fastq file path
    :param split: id info will split by the given separation and keep the front part
    :return:
    """
    fasta = []
    lines = []

    with open(path_, 'r+') as f1:
        for i, line in enumerate(f1):
            line = line.strip("\n\r")
            if i % 4 == 0:
                fasta += [lines]
                lines = [line.split('@')[-1].split(split)[0]]  # more parameter
            elif i % 4 == 1:
                lines += [line]

    fasta = fasta[1:] + [lines]
    fasta = pd.DataFrame(fasta, columns=['ID', 'seq']).set_index('ID')

    return fasta


def read_fq_gz_as_fa(path_, split='.', num_limit=0, decode=None):
    """
    Read fastq.gz file as a fasta file
    :param path_: fastq file path
    :param split: id info will split by the given separation and keep the front part
    :param num_limit: stop reading at which line.
    :param decode: decode parameter
    :return:
    """
    fasta = []
    lines = []

    if num_limit == 0:
        num_limit = 99999999

    try:
        from xopen import xopen

        with xopen(path_, 'r') as f1:
            for i, line in enumerate(f1):
                line = line.strip("\n\r")
                if ('\x00' in line) and i > 0:
                    continue

                if i % 4 == 0:
                    fasta += [lines]
                    lines = [line.split('@')[-1].split(split)[0]]  # more parameter
                elif i % 4 == 1:
                    lines += [line]

                if i == num_limit * 4:
                    break

    except ModuleNotFoundError:
        with gzip.open(path_, 'r') as f1:
            for i, line in enumerate(f1):
                line = line.decode(decode).strip("\n\r")
                if ('\x00' in line) and i > 0:
                    continue

                if i % 4 == 0:
                    fasta += [lines]
                    lines = [line.split('@')[-1].split(split)[0]]  # more parameter
                elif i % 4 == 1:
                    lines += [line]

                if i == num_limit * 4:
                    break

    fasta = fasta[1:] + [lines]
    fasta = pd.DataFrame(fasta, columns=['ID', 'seq']).set_index('ID')

    return fasta


def get_reverse_complementary(sequence_, reverse=True):
    """
    Reverse and complementary the sequence
    :param sequence_: sequence
    :param reverse: reverse or not
    :return: processed sequence
    """

    complementary_dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
                          'W': 'W', 'S': 'S',
                          'K': 'M', 'M': 'K',
                          'R': 'Y', 'Y': 'R',
                          'B': 'V', 'V': 'B',
                          'D': 'H', 'H': 'D',
                          'N': 'N'}

    if reverse:
        sequence_ = sequence_[::-1]

    return ''.join([complementary_dict[nt_] for nt_ in sequence_])


# keep #
complementary = get_reverse_complementary


# keep #


def mutation(seq_, max_num_=3, element=None):
    """
    random mutate sequence
    :param seq_:
    :param max_num_:
    :param element:
    :return:
    """
    seq_new = list(seq_)
    if element is None:
        element = ['A', 'G', 'C', 'T']

    num_ = np.random.randint(1, max_num_)
    pos_s = random.sample(range(len(seq_)), num_)
    for pos in pos_s:
        nt = random.sample(element, 1)[0]
        seq_new[pos] = nt

    return ''.join(seq_new)
