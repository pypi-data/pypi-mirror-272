"""
 #  bas-muti :: typ-lam 型函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Las of type builtin basic-python
"""
# r
#from depLam import *
import basic as bas
from  typing import TypeVar,Generic

a = (str, int)


def Lar( jc:str, ox:a.d, *at):
    locals()[jc] = TypeVar( jc, *at)

if  bas.Her(__name__):
    Lar('_D',  1,int)
    
    print(Lar)