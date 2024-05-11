"""
 #  bas-muti :: par-lam 析函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of part builtin basic-python
"""
# r(import-refs)
#       r.. im
from   .typLas       import *

import argparse as arg
import json
import yaml  # ruamel.yaml pyyaml
import importlib.util as pyt
# s
_JC_NYM = 'lam_par'


partArp = dict(
     j  = json.loads,
     y  = yaml.safe_load
)
def partArg( fh, zc, fb_las=FЯB):
    _or_par  = arg.ArgumentParser(description=zc)
    for _li in  range(  len( fh)):
        _fh_cfg  =   fh[_li]
        if not _fh_cfg[2]: _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1])
        elif isinstance(_fh_cfg[2], ):
            if   len(_fh_cfg[2]) == 1: _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], action = 'store_'+_fh_cfg[2][0])
            elif len(_fh_cfg[2]) == 2 and _fh_cfg[2][1] in ['+',',']:
                _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], type = _fh_cfg[2][0], nargs=_fh_cfg[2][1])
            else:
                _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], choices = _fh_cfg[2])
        else:    # elif afc_cfg_tmp[1] is class (else: choices)
            _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], type = _fh_cfg[2])
    if fb_las: return  _or_par.parse_args()
    return  _or_par.parse_args().__dict__



# json
def Imp_Cfp( lc, fc, fg={'f':'r','c':'utf-8'}):
    _fc  =   fc[ 0]
    #_fb  = FRB if len(fc) == 2 else FЯB
    return  partArp[_fc](OIF( lc, fg['f'], encoding=fg['c']).read()) # read_text()

# 必须是 .py 结尾
def Imp_Cfg( lc, *c,**g):
    _jc  =  os.path.basename(                    lc)
    #_lc =  os.path.dirname(                     lc)
    spe  = pyt.spec_from_file_location(_jc[:-4], lc)       # 创建规范
    cfg  = pyt.module_from_spec(                spe)       # 规载模块
    spe.loader.exec_module(                     cfg)       # 执行模块
    if hasattr(cfg,'getrArg')   :return partArg(cfg.getrArg( ), *c,**g)
    for _jc_lam,lam in  RΞ_(    cfg,BTW):
     if _jc_lam[:3] in['get']   :
        ret  =  lam()
        if  not bet(ret,TYP.TUX):return         ret
        try                     :return     Dix(ret)
        except                  :return         ret        # 不可皮壳
    raise   NotImplementedError

#  a = Imp_Arg,
Imp_ = dict(
   p = Imp_Cfg,
   j = Imp_Cfp,
   y = Imp_Cfp)

def Imp( lc, fc, *c,**g):
    #if lc[1] not in [':','h']:
    return Imp_[fc](lc, fc, *c,**g)

_LC_HER = os.getcwd()

_JC_TOK_={
    'r' :['rut','root','/','\\'],
    'a' :['aut','ares','~','D:'],
    'b' :['but','base','_','..'],
    'c' :['cut','cwdb','.','__']}

_LC_RUT = os.path.abspath(os.sep)
_LC_HOM = os.path.expanduser("~")
# 得到合法的 lc/jc 路径, 若 fb 且 lc不存在 则创建
def Pth( jc, lc=NON, fb=FRB) :
    _lc                              =  os.path.dirname(             jc) # '' 或 jc前缀
    _jc                              =  os.path.basename(            jc)
    if  bet( lc,NON):           _lc  =  os.path.abspath(            _lc)\
                                    if  os.path.isdir(              _lc)\
                                   else ZCL(os.getcwd(),   _lc)
    elif lc  in _JC_TOK_['r']:  _lc  =  ZCL(_LC_RUT    ,   _lc)
    elif lc  in _JC_TOK_['a']:  _lc  =  ZCL(_LC_HOM    ,   _lc)
    elif lc  in _JC_TOK_['b']:  _lc  =  ZCL(os.getcwd(),   _lc) 
    elif lc  in _JC_TOK_['c']:  _lc  =  ZCL(os.getcwd(),   _lc) #os.getcwdb()
    else:                       _lc  =  ZCL(os.path.abspath(lc),_lc)
    if fb and not os.path.isdir(_lc) :  os.makedirs( _lc)
    return        ZCL( _lc,_jc)

def lam_per( am, *c):return lambda o: am( o, *c)
lam_get = lambda *c: lam_per(GΞ_, *c)
lam_del = lambda *c: lam_per(ƋΞ_, *c)
lam_set = lambda *c: lam_per(SΞ_, *c)
def lamAset( jc): return lambda o,v: SΞ_( o, jc, v)

def getrGSD(jd):
    return lam_get(jd),lam_set(jd),lam_del(jd)

#   setProperty on var
def SP_( ox, jc, fg={'a':(getrGSD,'_jc')}):
    dic = {}
    if 'a' in fg:
        dic['fget'], dic['fset'], dic['fdel'] = fg['a'][0](fg['a'][1])
    else:
        if 'g' in fg: dic['fget'] = fg['g'][0](*fg['g'][1:])
        if 's' in fg: dic['fset'] = fg['s'][0](*fg['s'][1:])
        if 'd' in fg: dic['fdel'] = fg['d'][0](*fg['d'][1:])
    SΞ_( ox, jc, ZPM(**dic))

# FIXME
def Atr_inJ( ox, fg):
    for jc,fc in fg.items(): SP_( ox, jc, {'a':(getrGSD,fc)})

if  Her(__name__):
    pass