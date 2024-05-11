"""
 #  bas-muti :: get-lam 取函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of gets builtin basic-python
"""
# r(import-refs)
#       r.. im
from .depLam         import *
from .parLam         import Imp, Pth
from .setLam         import *
from .typLas         import Dix
from threading       import Thread
#       r.. as
import     random        as _rd
import      numpy        as _np
import      torch        as _tc
import  itertools        as _it
import os
import re
# s
_JC_NYM = 'lam_get'




_KY_ = ['dtype','device']

def isn_Lis( ox, ex): return ex in ox
def ism_Lis( ox,aex): return [ex in ox for ex in aex]
def ish_Lis( ox,aex): return all(ish_Lis( ox,aex))
def isx_Lis( ox,aex): return any(ish_Lis( ox,aex))

_JP_IS_ = ['n','m','h','x']
_JP_ISD = _JP_IS_ + ['e']
#_JP_DIC= ['_','K','V']
_JP_DIC = {'_':'items','K':'keys','V':'values'}
_JP_DI_ = list(_JP_DIC.keys())
_FC_AT_ = ['_','E','1']
def Lis_Dic( ox, fc='_'):
  if  fc == '_': return list(ox.items())
  if  fc == 'K': return list(ox.keys())
  if  fc == 'V': return list(ox.values())
  return   [ list(ox.keys()), list(ox.values())]


# FIXME PARALL #TAL('is'+_jk[0]+_jk[1]+'Dic')=lambda ox, ex:TAL('is'+_jk[0]+'_Lis')(Lis_Dic( ox, _jk[1]), ex)
for _jk  in _it.product(_JP_IS_,_JP_DI_):
    _fc_hea  =  'is'   +_jk[0]
    _fcMhea  =  _fc_hea+_jk[1]
    _fc_hea +=  '_'
    TAL[_fcMhea+'Dic']= lambda ox,ex: TAL(_fc_hea+'Lis')(GΞ_(ox,_JP_DIC(_jk[1]))(), ex)
    TAL[_fcMhea+'Las']= lambda ox,ex: TAL(_fcMhea+'Dic')(        ox.__dict__,           ex)

def iseKDic( ox, ex)      : return  True  if ex in ox.keys() and ox[ex] is not NON else False
iseKLas                   = lambda ox,ex:              iseKDic(          ox.__dict__,           ex)

def Var_DiK( ox, fc, ar=NON):
    if      bet( fc,TYP.ASX):
        if  bet( ar,TYP.TSX):
            return [Var_DiK( ox,_fc, ar.get(_fc,NON)) for _fc in  fc]
        return     [Var_DiK( ox,_fc, ar)              for _fc in  fc]
    return           ox.get(     fc, ar)

# FIXME GI_(fh,im[0]) 依次GI_ 等价于 GUN(GI_(fh,dd)for dd in im)
@MUNX(GIT)
def grt(): pass


def VarEDiK( ox, fc, ar= 0 ):
    if      bet( fc,TYP.ASX):
        if  bet( ar,TYP.TSX):
            return [Var_DiK( ox,_fc, ar.get(_fc,NON)) for _fc in  fc]
        return     [Var_DiK( ox,_fc, ar)              for _fc in  fc]
    var        =     ox.get(     fc, ar)
    return    ar if var is NON else var # 也许有，但是元素就是None，那就替补


# 
def Var1DiK( ox, fc, ar=NON):
    _fc        = fc
    if      bet( fc,TYP.ASX):
        _fc    = fc.pop(   )
        if  len( fc): return Var1DiK(
             ox, fc, ar=Var1DiK( ox, _fc, ar))
    
    return   ox.get(_fc, ar)

# FIXME PARALL
for _fc in _FC_AT_: TAL[ 'Xar'+_fc+'LaK'] =lambda ox, ex:TAL('Xar'+_fc+'DiK')(ox.__dict__, ex)

#   setmDiK_def
def DiK_def(     ox, fc, ar=NON):
    setnDiK_def( ox, fc, ar)
    return       ox

#   setmDic_def
def Dic_def(     ox, dx):
    setnDic_def( ox, dx)
    return       ox

def ENC( fc='PD'):
    if fc =='PD': return VAR['PRINT'] or VAR['DEBUG']
    if fc =='P' : return VAR['PRINT'] 
    if fc =='D' : return VAR['DEBUG']
    if fc =='E' : return VAR['ERROR']
    if fc =='W' : return VAR['WARN']

#   遍【扫符线fc】, 适【取数入空表】, 返【表】
def A0I_str( zc:TYP.A0C) ->TYP.A0I: return [int(_re) for _re in re.findall(r'\d+', zc)]
#   遍【扫符线fc】, 适【取止数第一】, 返【数以整，否则NON】
def N0I_str( zc:TYP.A0C) ->TYP.N0I:
    ret  =   re.search(r'\d+', zc)
    return  int(ret) if ret else None

_ZC_BSC = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789_'
def N0C_int( ri= range( 1 ), fe:TYP._0F=FRB, zc:TYP.A0C=_ZC_BSC):
  _zc = ''
  _gi = len( zc)       -1 if fb else len( zc)
  _zc = sum([zc[_rd.randint(0, _gi)] for _ in ri]) if fb\
    else sum([zc[_rd.randint(0, _gi)] if _rd.randint(0, _gi) < _gi-1 else '' for _ in li])
  return _zc

_LC_HER = CWD()

TZR['f_deb'] = 'R'
# input configs
def Inp( jc, lc=_LC_HER, fb=FRB):
    _lc  =  Pth( jc, lc)
    _jh  =  ACL(     jc)
    _jc  =  _jh[ 0]
    _fc  =  _jh[-1][ 1]
    # fb_deb
    if VZR('f_deb'): print(_lc)
    return  Dix(Imp(_lc,_fc)) if fb else Imp(_lc,_fc) # 边角逻辑

def Him(imp):
    print('pause')
    pass

#if __name__ == "__main__":
if  Her(__name__):
    
    #him()
    Him(Inp('tests.yml','..'))