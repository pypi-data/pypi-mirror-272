from .scalarization import ls, mtche, tche, pbi, cosmos, invagg, soft_tche
from ..problem.synthetic import VLMOP1, VLMOP2, ZDT1, ZDT2, ZDT3, ZDT4, ZDT6
from ..problem.synthetic import MAF1
from ..problem.synthetic.dtlz import DTLZ1, DTLZ2, DTLZ3, DTLZ4
from ..problem.synthetic.re import RE21, RE22, RE23, RE24, RE25, RE31, RE37, RE41, RE42


import os
from numpy import array
import torch

FONT_SIZE = 20
solution_eps = 1e-5

agg_dict = {
    'ls' : ls,
    'mtche' : mtche,
    'tche' : tche,
    'pbi' : pbi,
    'cosmos' : cosmos,
    'invagg' : invagg,
    'softtche' : soft_tche,
}
def get_problem(problem, n_var=10):
    problem_dict = {
        'ZDT1': ZDT1(n_var=n_var),
        'ZDT2': ZDT2(n_var=n_var),
        'ZDT3': ZDT3(n_var=n_var),
        'ZDT4': ZDT4(n_var=n_var),
        'ZDT6': ZDT6(n_var=n_var),
        'DTLZ1': DTLZ1(n_var=n_var),
        'DTLZ2': DTLZ2(n_var=n_var),
        'DTLZ3': DTLZ3(n_var=n_var),
        'DTLZ4': DTLZ4(n_var=n_var),
        'VLMOP1': VLMOP1(n_var=n_var),
        'VLMOP2': VLMOP2(n_var=n_var),
        'MAF1': MAF1(n_var=n_var),
        'RE21': RE21(),
        'RE22': RE22(),
        'RE23': RE23(),
        'RE24': RE24(),
        'RE25': RE25(),
        'RE31': RE31(),
        'RE37': RE37(),
        'RE41': RE41(),
        'RE42': RE42(),
    }
    problem_cls = problem_dict[problem]
    return problem_cls


hv_ref_dict = {
    'VLMOP1': array([1.0, 1.0]),
    'adult': array([2.0, 2.0]),
    'VLMOP2': array([4.0, 4.0]),
    'MAF1': array([2.0, 2.0, 2.0]),
    'mnist': array([3.0, 3.0]),
    'fmnist': array([3.0, 3.0]),
}


def get_hv_ref_dict(problem_name):
    if problem_name.startswith('ZDT'):
        ref = array([1.0, 1.0])
    else:
        ref = hv_ref_dict[problem_name]
    return ref + 0.5


root_name = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def is_pref_based(mtd):
    if mtd in ['epo', 'mgda', 'agg', 'pmgda']:
        return True
    else:
        return False


def get_device():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print('cuda is available')
    else:
        device = torch.device("cpu")
        print('cuda is not available')
    return device

def get_param_num(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


color_arr = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'grey', 'black', 'yellow']