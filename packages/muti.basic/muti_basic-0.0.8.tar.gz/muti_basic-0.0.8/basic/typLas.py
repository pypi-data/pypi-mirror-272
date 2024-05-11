"""
 #  bas-muti :: typ-las 型类集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Las of type builtin basic-python
"""
import os, sys
# r
from .depLam import * # type: ignore
from .metLas import *
import itertools as _it
from abc     import ABC,\
                    abstractmethod as _am


# s
#_L  =  TYP._1H([TYP.ASX,TYP._1H])
_L   =  TYP.ASX,TYP._0H
_D   =  TYP.TSX
# t
typ  =lambda x  : type(x)


# Las=Oia   XXX
class Lis( list, metaclass =Oia): pass
class Dis( dict, metaclass =Oia): pass
# Las=Num   XXX
class Nus(       metaclass =Num): pass
#class   Ep_(ctypes.Structure):
    #_fields_ = ("field1", ctypes.c_uint)
    #def value(ego): return super().value()
class   NuO(Nus) :
    # 紧凑
    #__slots__= (   )
    # Concrete numeric types must provide their own hash implementation
    __hash__ =  None
    def __init__(ego,zx, *c) :  ego.__ini__( zx, *c)
    def __repr__(ego       ) : return f"{ego.__class__.__name__}({ego._ar})"
    def __bool__(ego       ) : return    ego.__eno__()
    def __ini__(ego, zx, *c) :
        ego.setnALF( zx, *c)
        ego._ar=\
        ego.getrVar( zx, *c)

    def setnALF(ego, zx, *c) :
        ego.cfg_alf={
        (bet,zx,TYC._0O) :           zx     ,
        (bet,zx,TYC._0I) : (ego.ZBI, zx, *c),
        (bet,zx,TYC.A0C) : (    ZBC, zx    )}

    def getrVar(ego, zx, *c) :
        if  bet( zx, NuO): return    zx._ar
        return  betrVaz(ego.cfg_alf)
    
    def ZBI(    ego, zi, qi=NON, fb=FЯB) :
        _qi= qi if  bet( qi,int) and qi>0 else QII(zi)//8 + 1 if fb else (QII(zi)+7)//8 # 无前导0
        try:    return  ZBI( zi,_qi, signed=fb)                                # byteorder="big"
        except: return  TYC._0O(_qi*[ 0XFF]   )
        
    
    def __val__(ego, fb=FЯB):return ZIB(ego._ar, signed= fb) #ego._ar
    def __eq__( ego, od):return ego.__val__()==  od.__val__()
    def __gt__( ego, od):return ego.__val__()>   od.__val__()
    def __lt__( ego, od):return ego.__val__()<   od.__val__()
    def __ne__( ego, od):return ego.__val__()!=  od.__val__()
    def __ge__( ego, od):return ego.__val__()>=  od.__val__()
    def __le__( ego, od):return ego.__val__()<=  od.__val__()
    def __con__(ego, od):return NuO(ego._ar+ego.getrVar( od))
    def __add__(ego, od,
                 fb=FЯB):return NuO(ego.ZBI(ego.__val__( fb)+
                                        ZIB(ego.getrVar( od),signed= fb), 
                                                                fb = fb  ))
    def __sub__(ego, od,
                 fb=FЯB):return NuO(ego.ZBI(ego.__val__( fb)-
                                        ZIB(ego.getrVar( od),signed= fb), 
                                                                fb = fb  ))
    def __eno__(ego    ):return QI_(0x0,ego) == len(ego)
    
#NuO.register(bytes)

class   NuE(NuO):
    FRE=ZBI(0XFF,1)
    FЯE=ZBI(0   ,1)
    
    # 不支持负数
    def setnALF(ego, zx, *c) :
        ego.cfg_alf={
        (bet,zx,TYC._0O) :           zx     ,
        (bet,zx,TYC._0I) : (ego.ZBI, zx, *c),
        (bet,zx,TYC._0F) : (ego.ZBD, zx, *c),
        (bet,zx,TYC.A0C) : (    ZBC, zx    )}

    def ZBD(    ego, zd, qi= 1 ):
        _qi= qi if  bet( qi,int) and qi>0 else 1
        if zd >= 1 : return NuE.FRE#._ar
        if zd <= 0 : return NuE.FЯE#._ar
        return  ZBI(ZFD(zd * l2b(_qi)),_qi)
    def __vah__(ego):  return (ZIB(ego._ar),  len(ego._ar))
    def __val__(ego):
        _ah = ego.__vah__()
        return  _ah[0] / l2b(_ah[1])
    def __add__(ego, od:NuE):
        _ah  =  ego.__vah__()
        _dh  =   od.__vah__()
        _gd  =  _ah[ 1]-_dh[ 1]
        if _gd >= 0: return NuE(_ah[ 0]+_dh[ 0]*q2b( _gd),_ah[1])
        return              NuE(_dh[ 0]+_ah[ 0]*q2b(-_gd),_dh[1])
    def __sub__(ego, od:NuE):
        _ah  =  ego.__vah__()
        _dh  =   od.__vah__()
        if  _ah[0] * l2b(_dh[1]) <= _dh[0] * l2b(_ah[1]): return NuE(NuE.FЯE)
        _gd  =  _ah[ 1]-_dh[ 1]
        if _gd >= 0: return NuE(_ah[ 0]-_dh[ 0]*q2b( _gd),_ah[1])
        return              NuE(_ah[ 0]*q2b(-_gd)-_dh[ 0],_dh[1])
    #def __omline__(ego): return super().__omline__()
#NuO.register(bytes)
#import iterator.cycle as cyc

class Zip():
    def zip( *o,**g):return zip( *o,**g)
    def zid( *o, qi=NON):
        if not bet(qi,int): qi = _ma.lcm(* [len(e) for e in o])
        return zip( *o,**g)
        

    
class Lic(Lis):
    def __init__(ego, *c, qx=NON,**g):
        super().__init__( *c,    **g)
        ego.setnItr(      qx        )
    #   
    def setnItr(ego, qx) : 
        cfg_alf={  (bet, qx,int) : 
                 {((lambda   x: x>0), qx) :   qx,
            FRB : ((lambda o,x:max(len(o)+ x,1)),ego, qx)},
        (bet,qx,TYP._0F) : ((lambda o,x:ZFD(len(o) * x)), ego, qx)}
        _qi=       betrVaz(cfg_alf, oR=sys.maxsize)
        #ego.__iter__ = Itr_Cyc(ego,_qi).__iter__
        ego.itr=        Itr_Cyc(ego,_qi).__iter__
    def cqi(ego, qi=NON) :  ego.setnItr( qi) # 别名


class   Di_(Dis):
    def __init__(      ego, *c,**g):
        #ego._JC  =   ego.ic_(   )
        ego.upd_cfg(**ego.frm( *c))
        ego.upd_cfg(           **g)

    def frm(ego, *c): return c[0] if c and bet(c[0],_D) else {}
    # 增量更新
    def upd(    ego,ox:_D, fc='l'):
        _ox=CP_[fc](ox)
        ego.update(_ox)
    # g is dict
    def upd_cfg(ego,  **g):
        if    g:ego.upd(g)
    @_am
    def update(ego, ox: _D, *c): raise NotImplementedError


# dims
class   Dim(Di_, TYA._YM):
    #for _jc in  ox:  setattr(ego, _jc, ox[_jc])
    def update(ego, ox): setnDic(ego,ox)


# 循环迭代封装
class Itr_SIC():
    def __iter__(ego, qi=float('inf')):

        #return  ego # onl-for array
        return   _it.islice(
                 _it.cycle(ego), qi)

# 循环迭代封装
class Itr_Cyc():
    def __init__(ego, ox, qi = float('inf')):
        ego._ox = ox
        ego._qi = qi
        #ego._li=  0
        #ego._lj=  0
    def __iter__(ego, qi=NON):
        #return  ego # onl-for array
        return  _it.islice(
                _it.cycle(  ego._ox), qi if qi
                            else ego._qi)
    ''' onl-for array
    def __next__(ego):
        if  ego._li  >= ego._qi: raise StopIteration
        ego._li += 1
        ego._lj = (ego._lj + 1) % len(ego._ox)
        return ego._ox[ego._li-1]
    '''
    def zip( *o, qi=NON):
        if not bet(qi,int): qi = _ma.lcm(*[len(e) for e in o])
        return zip(*[e.itr( qi) for e in o])

# dict
class   Dic(Di_, dict):
    def update(ego, ox): super(Di_,ego).update(ox)


# multi-key not tuple key CHECK
class   Dih(Dic):
    def getMore(ego, k):
        if isinstance(k, tuple):
            if len(k) == 1: return ego.getMore(k[0])
            return tuple(ego.getMore(_k) for _k in k)
        if  isinstance(k,list):
            if len(k) == 1: return ego.getMore(k[0])
            _k = k.pop(0)
            return Dic(super().__getitem__(_k)).getMore(k)
        if isinstance(k, str):return super().__getitem__(k)
        
    
    def setMore(ego, k, v):
        if isinstance(k, tuple):
            if len(k) == 1: ego.setMore(k[0], v)
            elif len(v)==len(k):
                for k ,v in zip(k, v): ego.setMore(k, v)
            else: super().__setitem__(k, v)
        elif  isinstance(k,list):
            if len(k) == 0: raise KeyError("Unsupported key type or structure.")
            elif len(k) == 1: ego.setMore(k[0])
            else: 
                ego.setMore(k[0],Dih())
                super().__getitem__(k[0]).setMore(k[1:],v)
        elif isinstance(k, str): super().__setitem__(k,v)
        else: raise KeyError("Unsupported key type or structure.")
    def __getitem__(ego, k):
        return ego.getMore(k)
    def __setitem__(ego, k, v) -> None:
        return ego.setMore(k, v)

# dixt
class   Dix(Dih):
    
    #def __init__( ego, *c,**g): super.__init__(ego, *c,**g)
    def __setattr__(   ego, jc, ox):
        _ZS = ego.__class__ # 方法可继承
        # FIXME SET\OTH FORMAT
        if      brt(ox,_L):    _ox = typ(ox)(_ZS(_ex) if bet(_ex, _D) else _ex for _ex in ox)
        elif    bet(ox, _D):    _ox = _ZS(ox)
        else               :    _ox =     ox
        super().__setattr__( jc,_ox)
        super().__setitem__( jc,_ox)
    __setitem__=__setattr__

    # FIXME set_attr 暂时不管 copy
    def upd(    ego,ox:_D,*arg):
        ego.update( ox)
    #for    _jc  in  ox : setattr(ego,   _jc, ox[_jc]) 
    def update(ego, ox): setnDic(ego,ox)
    # poptItm
    def pop(ego, k, *c):
        if ego.__hasattr__(k): ego.__delattr__(k)
        return   super().pop(k, *c)

if  Her(__name__): h = Dic(ox=1, c=1)