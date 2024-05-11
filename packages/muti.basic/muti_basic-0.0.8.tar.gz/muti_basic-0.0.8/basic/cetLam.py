"""
 #  bas-muti :: cet-lam 車函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of cheat builtin basic-python
"""
# r
from typing import Any
from .__deps__ import *

def cet_imp(j='bas', f='__deps__'): return f"{j}.reg({j}.TAM['G'](),{j}.{f}.__dict__)"
# from __deps__ import *
def xec_dix(j='bas'):return f"{j}.reg({j}.TAM['G'](),{j}.__deps__.__dict__)"
def val3tar(j='bas'):return f"{j}.vcr(),{j}.vgr(),{j}.vzr()"

TAG = globals()

# 非直接计算
class   Tar():
    def __new__(ido, *a,**g):
        ids=super().__new__(ido)
        ids._a = ['C','G','Z'] if not a else a
        for _f in ids._a:
            _fc,_jc=ZΓC(_f),Z_C(ZLC(_f))
            SΞ_(ids,_jc,TAG['T'+_fc+'_'](1))
            SΞ_(ido,_fc,TYB._PM(lambda ids:GΞ_(ids,_jc)))
        return  ids


# class Wrp(type):def __new__

class Tar_STR(Tar):
    def __init__(ego, *c,**g): pass
    def __str__(ego): ""
    def __call__(ego, *a):
        _a = ego._a if not a else a
        for f in _a: yield GΞ_(ego,f) if f in ego._a else NON