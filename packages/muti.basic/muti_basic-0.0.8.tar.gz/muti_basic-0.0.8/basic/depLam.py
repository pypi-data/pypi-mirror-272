"""
 #  bas-muti :: dep-lam 公函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of deps builtin basic-python
"""
# r
from .__deps__ import *
# 
#exptNon = lambda _or, *cfg, **tfg: try: return _or(*cfg, **tfg); except: return None
def dddfOut_cfc(_or_, fc,*cfg,**tfg): return       _or_[fc](     *cfg,**tfg)
def dddfOut_afc(_or_,afc,*cfg,**tfg): return {fc : _or_[fc](     *cfg,**tfg) for fc     in afc                 } 
def dddfOut_tfc(_or_,tfc,*cfg,**tfg): return {fc : _or_[fc]( jc ,*cfg,**tfg) for fc, jc in tfc.items(         )}
def dddfOut_nfc(_or_,nfc,*cfg,**tfg): return {fc : _or_[fc]( jc ,*cfg,**tfg) for fc, jc in nfc.__dict__.items()}
def dddfOut_mfc(_or_,nfc,*cfg,**tfg): raise  NotImplementedError
dddfOut_ = {
   'str' :  dddfOut_cfc,
   'lis' :  dddfOut_afc,
   'tup' :  dddfOut_afc,
   'dic' :  dddfOut_tfc,
   'JYM' :  dddfOut_nfc}
# FIXME tuple, namespace: parallel
def dddfOut(    _or_,_fc,*cfg,**tfg): return dddfOut_[type(_fc).__name__[:3]](_or_,_fc,*cfg,**tfg)
def dntfOut(    _or_,_fc,*cfg,**tfg): # HERE-4 # for DEBUG
  try    :                                   return dddfOut_[type(_fc).__name__[:3]](_or_,_fc,*cfg,**tfg)
  except :                                   return     None
# pass: not do any work here. FIXME tuple, namespace: parallel
def dptfOut(    _or_,_fc,*cfg,**tfg):
  if   isinstance(_fc, str):
    try     :return      _or_[_fc](     *cfg,**tfg)  # FIXME HERE-4
    except  :return      None
  elif isinstance(_fc, dict):
    tfg_ret = {}    # events-like, return not nessary
    for   fc,jc in  _fc.items() :
      try   :tfg_ret[fc]=_or_[ fc]( jc ,*cfg,**tfg)
      except:pass
    return tfg_ret
  elif isinstance(_fc,(list ,tuple)):
    tfg_ret = {}    # events-like, return not nessary
    for   fc    in  _fc:
      try   :tfg_ret[fc]=_or_[ fc](     *cfg,**tfg)
      except:pass
    return tfg_ret  # get 方法..

# [HERE-5] MODD [ARES] 
def dddd(_or_):
  return lambda fc, *cfg, **tfg: dddfOut(_or_, fc ,*cfg, **tfg)

def dptfOnt(    _or_,_fc,*cfg,**tfg):
  # not do any work here
  if   isinstance(  _fc, dict):
    tfg_ret = {}    # events-like, return not nessary
    for   fc,jc in  _fc.items() :
      try   :tfg_ret[fc]=_or_[ fc]( jc, *cfg, tfg[ jc])
      except:pass
    return tfg_ret
  elif isinstance(  _fc,(list ,tuple)):
    tfg_ret = {}    # events-like, return not nessary
    for   fc    in  _fc:
      try   :tfg_ret[fc]=_or_[ fc](     *cfg,  tfg[ fc])
      except:pass
    return tfg_ret  # get 方法..
  else:
    try     :return      _or_[_fc](     *cfg,  tfg[_fc])
    except  :return      None


#
MYF = lambda  lam:lambda  o, fc =[], fg ={}, *c, **g: lam(o,fc,fg)



TYB.MDE = lambda zm=Z__: lambda f :  lambda t,*c,**g: TAM["G"]()[zm(t)]



@TYB.MDE(lambda t:'BE'+t)
def BE_(): pass

def bex( ox, ft):
  if BT_(ft,TYB.A0C): return BE_(ft, ox)
  # todo ft(ox)
  return FЯB
   

def bet( ox, ft):
  if BT_(ft,(TYA._OT,TYP._OT,TYP.ΛOT)):return BT_( ox, ft)
  if BT_(ft,TYB.A0C):  #str-ft
    if SYA._jc(        ox )==ft :return FRB # None True False
    if SYP._jc(TYA._OT(ox))==ft :return FRB
    # TODO BE_Dict
    return bex( ox, ft)
  if ox is ft: return FRB
  return FЯB

@MUNX(bex, um=any) # FIXME BIG-PARALL
def brx(): pass
@MUNX(bet, um=any) # FIXME BIG-PARALL # any:=lambda x,*h:isinstance(x,tuple(h))
def brt(): pass


xtndTYP=TYB.TSX(
    ASX= lambda  ox, ux, am=TYB.ASX: OUL( ox, am( ux)), # list
    TSX= lambda  ox, ux, am=TYB.TSX: OUD( ox, am( ux))) # dict

# 并(Merge)：按栗一之型，若禁同，按栗二之要 extend
def xtndSaf( ox, ux, am=(Z__,SI_)):
    _ox = am[0]( ox)
    xtndTYP[Jyp( ox)](ox, ux, am[1])
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    elif isinstance(a, tuple) and isinstance(b, tuple):
        return a + b
    elif isinstance(a, str) and isinstance(b, str):
        return a + b
    elif isinstance(a, dict) and isinstance(b, dict):
        return {**a, **b}
    elif hasattr(a, 'merge') and callable(GΞ_(a, 'merge')) and hasattr(b, 'merge') and callable(GΞ_(b, 'merge')):
        return a.merge(b)
    else:
        raise TypeError(f"Unsupported types for merging: {type(a)} and {type(b)}")

MYFX=lambda _c=[],_g={}:lambda w:lambda o,fc=_c,fg=_g,*c,**g: w(o,updfSaf(fc,c),fg)

def getrLar( jc, fx=TAL): return fx[jc] if BEI(fx) else ZCO(fx)[jc]
#BEI(fx) Dic_=Lar_arg 时间小偷
def Lar_arg( *c, fx=NON , jc=NON):
    _fg = OFC().f_back.f_globals if bet( fx,NON) else fx if BEI(fx)else ZCO( fx)
    _jc = JYM(_fg)               if bet( jc,NON) else jc
    return {y:_fg[_jc+y] for y in c}

def Lar_idx( *c, fx=TAL, jc=NON):
    _fg = fx if BEI(fx)else ZCO( fx)
    _jc = JYM[_fg] if not bet( jc,NON) else jc
    return [  _fg[_jc+y] for y in c]
def rec(  a=[ ], *c): pass
 
def r1c( *c,  f=NON):
    if f is NON     : f  =   c[0] is not NON
    return    c[0] if f else c[1]

def rtc( *c,  f=NON):
    if f is NON     : f  =   c[0] is not NON
    return    c[0] if f else c[1](c[0])






# FIXME TYP._FH 要求第第二个数后续可作为第一个数的变长参数传入
def Val_f0H( oh:TYP._FH, *c,**g):
    if   oh:_am,*_c= oh
    else   :_am,*_c=ASS,NON
    return  _am(*_c,     *c,**g)
# fixme TYC._0H -> TYC.Laz 懒惰计算
def getrLaz( ox        ):
    if  bet( ox,TYC._0H):return Val_f0H( ox)
    #if bet( ox,CALABLE):return          ox() # 无元素Laz语句默认用 (fun,) 表示，以避免需要返回本体的情况
    return   ox
# # BET函数，key: if elif else if-else
NAP  = (ASS,NON)
#[ if-lif-bet] func, not [ if-nif-bet]需要考虑无返回的情况
def betrVaz( ox:TYP.TSX, oR=NAP):
    for e in ox.items():
        if  betrVaz(e[0],oR=FЯB) if bet(e[0],TYP.TSX) else getrLaz(e[0]):\
    return  betrVaz(e[1],oR= oR) if bet(e[1],TYP.TSX) else getrLaz(e[1])
    return               oR
#[ if-lif-bet] 不是 Lar 是因为有可能是函数头 
def betrVar( ox:TYP.TSX, oR=NON):
    for e in ox:
        if e[0]:\
    return  betrVar(e[1],oR= oR) if bet(e[1],TYP.TSX) else e[1]
    return               oR



@MIFX()
def mif(): pass

@MIFX(vd=EXM)
def mdf(): pass

##[if-else] func
#def betrLam( ox:TYP.TSX, oR=ASS): return betrVar( ox, oR)
#[if-else] func()
#def betmLam( ox:TYP.TSX, oR=ASS):
#    Xar  =  betrVar( ox, oR)
#    if bet(Xar, TYC._FH):return Val_f0H(Xar)
    #if bet(Xar, 'lam') :return         Xar() # 无元素函数默认用 (fun,) 表示
#    return Xar


TAL['W'] = 1.0

def warnMsg( ox:str, *c: object, ar:TYP.WAR, fi:int = 1):
    _li_war= VAR("_LI_WAR")
    if  bet(_li_war,int):
      if    _li_war ==0 :      WAR("\033[WARN: {ox % c}\033[0m", category=ar, stacklevel=fi+ 1)
      elif  _li_war <=VAR('W'):WAR("\033[WARN: {ox % c}\033[0m", category=ar, stacklevel=fi+ 1)

def updtDic_rcs( ox:TYP.TCX, od:TYP.TCX):
    for _jc,_ex  in  od.items():
     if bet(_ex,dict) and _jc in ox:
            updtDic_rcs( ox[_jc], _ex )
     else: ox[_jc] = _ex 

def setnDic( od, ox):
    for _eh  in  ox.items():  setattr(od, *_eh)

def q2b( qi): return 2**(qi*8)
def l2b( qi): return 2**(qi*8)-1