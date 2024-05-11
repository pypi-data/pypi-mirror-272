"""
 #  bas-muti :: set-lam 置函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of sets builtin basic-python
"""
# r(import-refs)
#       r.. im
from .depLam         import *

# s
_JC_NYM = 'lam_set'


#   setnDiK_def
def setnDiK_def( ox, fc, ar=NON): ox.setdefault(fc, ar)
def setnDic_def( ox, dx):
    dx.update(ox)
    ox.update(dx)