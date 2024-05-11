"""
 #  bas-muti :: deps_basic 公集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  __deps__ builtin basic-python 只述知，不应算
"""

import   os,sys
import builtins                        as _bt
import     time                        as _ti
import     copy                        as _cp
import     math                        as _ma
import operator                        as _op
import   pickle                        as _pk
from       enum import Enum            as _um,\
                       EnumMeta        as _ut
from   argparse import Namespace       as _ym
from frozendict import frozendict      #FrozenDict ImmutableDict
import                 inspect         as _in
import                 types           as _ty
import                 numbers         as _nm
import                 typing          as _tp
import                 ctypes          as _tq
import                 collections     as _ts
import                 collections.abc as _tc
import                 warnings        as war
import                 functools       as _fm
from        abc import ABC             as _ax,\
                       ABCMeta         as _at,\
                       abstractmethod 

__all__ = []

# 幻方初：重载 Built-in Functions
def initKam():
  # TODO: 上下文管理、序列化、比较、拷贝、反射等 __special__
  OBP = breakpoint
  OCO = compile
  OCN =   print
  OIN =   input
  OIF =    open
  VDO =    eval
  #LIX=      id # HEL=help del
  ZAC =   ascii
  #ZCI,ZIC,ZhI,ZoI,ZIP,ZBC=chr,ord,hex,oct,zip,bin
  #FRL,FRO,ZRL,ZЯL,ZUL,ZQL=all,any,max,min,sum,len
  ZFD =   round
  ZHD =  divmod
  #VAB,POW=abs,pow TODO: 运算符重载
  ZCR =  format
  STD =  sorted
  ZHX =    hash
  DET =    iter
  NXT =    next
  NXD =lambda x:next(iter(x))
  # any-Exs
  JXN =    repr
  T_R =    vars
  TCR =  locals
  TGR = globals
  VZR = os.getenv
  TZR = os.environ
  TZ_ =lambda*c: TZR
  SΞ_ = setattr
  GΞ_ = getattr
  ƋΞ_ = delattr
  BΞ_ = hasattr
  #BΞL=lambda o: BΞ_(o,'__len__'    )# Quanable
  BEI =lambda o:BΞ_(o,'__getitem__' )# Indyable
  BEΞ =lambda o:BΞ_(o,'__getattr__' )# Ξtrbable
  BES =lambda o:BΞ_(o,'__getstate__')# Statable
  BEC =callable                      # Callable
  SI_ =lambda o,*x :o.__setitem__(*x)
  GI_ =lambda o, k :o.__getitem__( k)
  ƋI_ =lambda o, k :o.__delitem__( k)
  VAL =lambda o:GΞ_(o, 'value' ,None)
  JYM =lambda o:GΞ_(o,'__name__','_')   # _jc _jc_nym
  NYM =lambda o:GΞ_(o,  'name'  ,'_')   # nym [0].hed
  GIF =     sys._getframe
  TGF =lambda o:o.f_globals
  TCF =lambda o:o.f_locals
  ZFB =lambda o:o.f_back
  CWD =      os.getcwd
  GST =     _ti.time
  ZCL = os.path.join    # join 除格转 有他辑排异
  ACL = os.path.splitext
  AC_ =lambda c,x='_': c.split(x)
  FCL = os.path.basename
  JCL =lambda c:ACL(FCL(c))[0]
  TG_ =lambda i:TGF(GIF(i))
  TC_ =lambda i:TCF(GIF(i))
  #LCL= os.path.dirname
  # Z系 : 纯格转,无事务
  Z__ =lambda*x:x if len(x)>1 else x[0]if len(x)else None 
  #ZCX=     str
  ZBC =     str.encode
  ZCB =   bytes.decode
  ZLC =     str.lower
  ZΓC =     str.upper
  Z_C =lambda c,x='_': x+c
  ZCA =lambda*c,x='_': x.join([str(i) for i in c])
  ZCO =lambda o:o.__str__()
  ZCQ =lambda o:o.__class__.__str__()
  ZTO =lambda o:dict(o.__dict__)
  ZTQ =lambda o:dict(o.__class__.__dict__)
  Z_O =lambda o,c:o.__dict__[c]
  ZBO =     _pk.dumps
  ZOB =     _pk.loads
  ZIB =     int.from_bytes
  ZBI =     int.to_bytes
  QII =     int.bit_length
  QI1 =     int.bit_count
  GIT =lambda o,*c:o.get(*c) # 
  RVT =    dict.values
  RCT =    dict.keys
  RGT =    dict.items
  SED =    dict.setdefault
  ACT =lambda o:list(RCT(o)) # lambda 不带属性
  AVT =lambda o:list(RVT(o))
  AGT =lambda o:list(RGT(o))
  WAR =     war.warn
  RΞ_ =     _in.getmembers
  OFC =     _in.currentframe
  OS_ =     _in.stack
  # B系：Bool判断
  BT_ =         isinstance
  BB_ =         issubclass
  BTS =     _in.isclass
  BTW =     _in.isfunction   # callable
  BTM =     _in.ismethod
  BTF =     _in.isframe
  BTD =     _in.ismodule
  BTG =     _in.isgenerator
  BTB =     _in.isbuiltin
  BTQ =     _in.iscode
  BPC =lambda t,c='__': str.startswith(t,c)
  # COPY
  CPY =     _cp.copy
  CPD =     _cp.deepcopy
  CPL =lambda o:ZOB(ZBO( o ))
  CP_ = dict(
    _ = CPY,
    l = CPL,
    d = CPD)
  # V系 : 纯运算
  #VUI=     set.intersection
  #VUE=     set.union
  #VUB=     set.difference
  #VUD=     set.symmetric_difference
  # O系 : 纯操作,轻返回
  ODO =    exec
  # NPCALL
  ONA =lambda o,d:ODO("o +=d")
  ONB =lambda o,d:ODO("o -=d")
  ONC =lambda o,d:ODO("o *=d")
  OND =lambda o,d:ODO("o /=d")
  ONE =lambda o,d:ODO("o |=d")
  ONP =lambda o,d:ODO("o//=d")
  ONF =lambda o,d:ODO("o %=d")
  ONX =lambda o,d:ODO("o ^=d")
  ONI =lambda o,d:ODO("o &=d")
  ONЯ =lambda o,d:ODO("o<<=d")
  ONR =lambda o,d:ODO("o>>=d")
  # UPDATE
  OUA =lambda o,d:o.append(d) # list
  OUB =lambda o,d:o.remove(d)
  OUC =lambda o:  o.clear(  )
  OUD =lambda o,d:o.update(d) # if BT_(n,dict,set)
  OUL =    list.extend
  OUP =lambda o,d:  o.push( )
  OUT =lambda o, *c:o.pop(*c)
  BU_ =     set.issubset
  BUT =     set.issuperset  # BU‾
  RXN =lambda o  :  o.iter(  )
  QI_ =lambda e,o:  o.count(e)
  CPT =lambda t: {c: v for c, v in RGT(t) if not BPC(c)}
  NOM =lambda*c: None
  EXM =lambda*c:  ...
  FRM =lambda*c: True
  FЯM =lambda*c:False

  # Map of abitems
  TAM = dict(
    C =lambda     : TCF(ZFB(OFC())) ,  #inspect.currentframe().f_back.f_locals
    G =lambda     : TGF(ZFB(OFC())) ,  #inspect.currentframe().f_back.fglobals
    C_=lambda x=1 : TCF(OS_()[x][0]),  #inspect.stack(  )[ x ][ 0   ].f_locals
    G_=lambda x=1 : TGF(OS_()[x][0]),  #inspect.stack(  )[ x ][ 0   ].fglobals
    #A=vars()
    Z =lambda     : TZR              ) #     os.environ
  #MAXX= {f:lambda _:v for f,v in TAM.items()} # LAMBDA表达式v不计算 一直指向global v
  MAXX=lambda F:lambda _:TAM[F]
  @MAXX("Z")
  def vzr(): pass
  @MAXX("G")
  def vgr(): pass
  @MAXX("C")
  def vcr(): pass
  
  

  def updlSaf( ox, ux, ig='__', am=(Z__,SI_)): # TODO PALL  (ZTO,SΞ_)
    _od          = am[0](ux)
    def _sm( jc) : am[1](ox, jc, _od[jc])
    if not ig:
      for _jc in _od.keys(): _sm(_jc)
    else:
      for _jc in _od.keys():
        if not BPC(_jc,ig): _sm( _jc)
  def updfSaf(ox, ux, ig='__', am=(Z__,SI_)):
    updlSaf( ox, ux, ig=ig, am=am)
    return ox

  Cal = lambda m,*c,**g: m(*c,**g)
  Her = lambda c=__name__: c=="__main__" # betrHer default False
  def ASS(*c,**g): pass
  def _me(c=__file__,q=7): OCN(f"[{JCL(c)[:q]:_^7}] : 此 {c}")
  
  
  # 注册尾
  def reg(o,d=TAM["C"]()): # 括号打在哪层是哪层
    OUL(__all__,ACT(d))
    #OUD(  o   ,CPT(d))
    updlSaf(o,      d)
  #return reg
  reg(TAM["G"](),TAM["C"]())

__g=initKam() #__g()

# 国象初：归集
def initDep():
  #To-nYm-Abs 类  LAS or LAM (LAR)
  class TYA(_ym):
    _OT = type     # 型类  纇 isinstance
    _OM = object   # 象类  類 isinstance
    #LAM= function # 函类   
    _AT = _at      # 虚类  ABCMeta
    _AX = _ax      # 虚伪  ABC
    _UT = _ut      # 常型  
    _UM = _um      # 常象  enum AOH  值互斥
    _YM = _ym      # 变象  namespace 
    # TODO: fll pyt,byd pyt
  #To-nYm-Bas 基   .__class__ or .__bases__ is from TYA
  class TYB(TYA._YM):
    #   TypeBase
    #L__= ellipsis
    #NOT= NoneType
    #ObjectBase
    _0B=bool
    _0I=int
    _0F=float
    #OD= dreal    # num by performence (not embedding) 
    _0K= complex
    _0O= bytes
    _0H= tuple    # 由于不可变，不是组织容器
    _0Q= frozenset
    _0G= _ty.MappingProxyType
    ASX= list     # _0X仅由0X元素组成
    TSX= dict
    USX= set
    A0C= str      # code 没有 0C
    MAP= map
    A0O= bytearray
    TOC= _ts.namedtuple('TOC', ['nid','nym'])
    FUP= _ts.namedtuple('FUP', ['lam','ifc','ifg']) # FIXME Name
    RSI= range
    ASI= slice
    FIL= filter
    VOO= memoryview
    #HM=    cache,..   #属法 の 饰
    _HM=_fm.lru_cache  #Holdmθd Map
    _PM=   property    #Proprty Map
    _CM=   classmethod #Clasmθd Map
    _SM=  staticmethod #Statmθd Map
    _AM=abstractmethod #Abstmθd Map
    RIT= reversed
    ENU= enumerate    # FIXNAME
    SOX= super
    _ON= BaseException
    # TODO: contextlib.ContextManager


  # To-nYm-Collection
  class TYC(TYA._YM):
    _EN = Exception
    MOX = _ty.MethodType
    _QX = _tq.Structure
    _2H = _ts.namedtuple
    _CB = _tq.c_bool
    _CI = _tq.c_int
    _CF = _tq.c_float
    _CD = _tq.c_double
    #_CK= _tq.c_complex
    _CC = _tq.c_char
    _CG = _tq.c_char_p
    _CH = _tq.c_float
    _CU = _tq.c_uint
    _CO = _tq.c_ubyte
    _CA = _tq.c_ushort
    A2X = _ts.deque
    TDX = _ts.defaultdict
    T2X = _ts.OrderedDict
    T3X = _ts.ChainMap
    CCC = _ts.Counter
    _ET = TypeError

  class MUT(TYA._UT):
    def __new__(ido,las,bas,cig):
      cig['_jc']=TYB._CM(lambda ego,val:NYM(ego._value2member_map_.get(val)))
      cig['_ug']=TYB._PM(lambda ego:tuple(_eg for _eg in ego if not BPC(NYM(_eg),'_')))
      return super().__new__(ido,las,bas,cig)
    
  class EUA(TYA._UM, metaclass =MUT): pass

  # So-nYm-A # 搜名
  class SYA(EUA):
    # 无
    EXS = Ellipsis # 有
    NON = None     # 冇
    FRB = True     # 右
    FЯB =False     # 左
    NIN = NotImplemented
    # 伪
    ZRO =   0      # 口 0X00
    ZRI =   1      # ZЯO 工(!= 0)
    ZЯO =   0XFF   # 
    ZRC =  '_'     #
    ZЯC =  '-'     #
    NAC ='nan'     #
    MRC ='inf'     #

  class SYB(EUA):
    JRO = TYB._0O([VAL(SYA.ZRO)])# B满 # 容(0~255)
    JЯO = TYB._0O([VAL(SYA.ZЯO)])# B空 FIXME != 0
    NAN = TYB._0F( VAL(SYA.NAC) )
    MRF = TYB._0F( VAL(SYA.MRC) )
    MЯF = TYB._0F( VAL(SYA.ZЯC)+VAL(SYA.MRC))

  class SYC(EUA):
    C00 = chr(0)   # 编号 0
    C01 = chr(1)   # 源数之门 一
    C02 = chr(2)   # 源数之门 二
    C03 = chr(3)   # 源数之门 三
    C04 = chr(4)   # 源数之门 四
    '''
    AND     = '&'
    OR      = '|'
    XOR     = '^'
    RSHIFT  = '>>'
    LSHIFT  = '<<'
    ADD     = '+'
    SUB     = '-'
    MUL     = '*'
    TRUEDIV = '/'
    FLOORDIV= '//'
    MOD     = '%'
    POW     = '**'
    EQ      = '=='
    NE      = '!='
    LT      = '<'
    GT      = '>'
    LE      = '<=' 
    GE      = '>='
    '''
  
  class OAR(TYA._YM):
    #ABS=_op.abs # abs()
    pass


  # 因缩写有重，而魔法须之，故辟此名間
  class OBR(TYA._YM):
    EQ =_op.eq         # ==
    NE =_op.ne         # !=
    GT =_op.gt         # >
    LT =_op.lt         # <
    GE =_op.ge         # >=
    LE =_op.le         # <=
    RSHIFT =_op.rshift # >>
    LSHIFT =_op.lshift # <<
    OR =_op.or_        # |
    AND=_op.and_       # &
    XOR=_op.xor        # ^
    ADD=_op.add        # +
    SUB=_op.sub        # -
    MUL=_op.mul        # *
    POW=_op.pow        # **
    MOD=_op.mod        # %
    TRUEDIV,FLOORDIV=TYB._SM(_op.truediv),TYB._SM(_op.floordiv) #/,//
    _qi= 18
    _ym=lambda jc:'__'+jc.lower()+'__'
    
  
  class SYP(EUA):
    _0B = bool
    _0I = int
    _0F = float
    #_OD= dreal    # num by performence (not embedding) 
    _0K = complex
    _0O = bytes
    _0H = tuple    # 由于不可变，不是组织容器
    _0Q = frozenset
    #_0M= MappingProxy
    ASX = list     # _0X仅由0X元素组成
    TSX = dict
    USX = set
    A0C = str      # code 没有 0C


  class CAR(TYA._UM):
    DDD = ':'
    BBB = '='
  # FIXME CBR to CBR_ALB(+-*/) and CBR_CPR (<>==) 

  #class CBR(TYA._UM):

  # FIXME what's Real
  TYP_=dict(
    B = TYB._0B,
    I = TYB._0I,
    F = TYB._0F,
    D = TYB._0F, # FIXME TYB._0D
    #R= TYB._0R,
    #E= TYB._0E, # 夼:对称闭集
    K = TYB._0K)
  TYP_0N = tuple(TYP_.values())
  TYP_.update(
    H = TYB._0H,
    O = TYB._0O)
  _YP_0X = tuple(TYP_.values())
  #_YP_ITR = list, dict, set
  TYP_.update(
    C = TYB.A0C)
  
  '''
  _   基本型
  abc 组织型(容器)
  w   函数型
  mw  泛型
  '''
  #class TYP(TYA._UM):
  class TYP(TYA._YM):
    _OT = _tp.Type            # 型伪
    ΛOT = _tp._GenericAlias
    NOR = _tp.NoReturn
    NON = None # 不用NoneType
    NST = _tp.TypeVar('NST')
    NSX = _tp.Any
    WSX = _tp.Callable[...,NSX]
    ITR = _tp.Iterable
    ABS = _tp.AbstractSet
    ANT = _tp.Annotated
    A1B = _tp.BinaryIO
    AIO = _tp.ByteString
    Y1X = _tp.ChainMap
    DDD = _tp.ContextManager
    N0B = _tp.Optional[TYB._0B]
    N0I = _tp.Optional[TYB._0I]
    N0d = _tp.Optional[TYB._0F]
    N0K = _tp.Optional[TYB._0K]
    N0H = _tp.Optional[TYB._0H]
    N0C = _tp.Optional[TYB.A0C]
    #_1o= one-hot
    #_JI= IntegralConstant
    A2C = _tp.AnyStr
    _0X = _tp.Union[*_YP_0X]
    N0X = _tp.Union[*(_tp.Optional[_] for _ in _YP_0X)]
    A0I = _tp.List[int]
    A0S = _tp.List[str]
    A0d = _tp.List[float]
    A0K = _tp.List[complex]
    A0H = _tp.List[tuple]
    A0X = _tp.Union[*(_tp.List[_] for _ in _YP_0X)]
    #A0X = _tp.Union[_tp.List[int]]
    ΛUX = _tp.Union[list, tuple]
    AUX = _tp.Union[list, tuple, str, bytearray]
    TUX = _tp.Union[dict, TYA._YM]
    T0I = _tp.Dict[str,int]
    T0d = _tp.Dict[str,float]
    T0K = _tp.Dict[str,complex]
    T0H = _tp.Dict[str,tuple]
    T0X = _tp.Union[*(_tp.Dict[str,_] for _ in _YP_0X)]
    NJC = _tp.Dict[str,str]
    TCX = _tp.Dict[str,NSX]
    _FH = _tp.Tuple[_tp.Callable[[NST],NSX],NST]
    WAR = _tp.Optional[_tp.Type[Warning]]
    #DDD= Sequence Queue
    #_2H = MultiVar
    #L-Tuple
    # TODO Optinal[T]
  for _y in [TYA,TYB,TYC]: updlSaf(TYP,_y, am=(ZTO,SΞ_))
  for _y in [SYA,SYB,SYC]: updlSaf(TAM['C'](),{_j:VAL(_v)for _j,_v in RGT(ZTO(_y)) if not BPC(_j,VAL(SYA.ZRC))})
  reg(TAM['G'](),TAM['C']())
initDep()

# 麻雀初：成役
def initMθd():
  GU_ =lambda a,b: next((x for x in a if b(x)), NON)         # 苛b(
  GUN =lambda a  : next((x for x in a if x is not NON), NON) # 苛有
  G1_ =lambda a,b: sum(1 for _ in filter(b,a)) #不用len防外溢# 计b(
  G1N =lambda a  : sum(1 for x in a if x is not NON)         # 计有
  #多暗刻单骑: um∈{GUN, all, any, sum}
  MUNX=lambda un,um=GUN:lambda ddd:lambda ox,fh,*c,um=um,**g:um(un(ox,fc,*c,**g)for fc in fh)
  #小三元两听: [if-lif-lse] same c 默认不行返回None
  MIFX=lambda   v=Z__,b=Z__,vd=NOM:lambda _am:\
       lambda*c,v= v ,b= b ,vd= vd:v(*c)if b(*c)else vd(*c)
  
  MRI_KEY     = lambda og,pre: dict(filter(lambda item:pre(item[0]), og.items()))
  MRI_KEY_BIN = lambda og,aox: dict(filter(item[0]     in aox, og.items()))
  MRI_KEY_BNI = lambda og,aox: dict(filter(item[0] not in aox, og.items()))
  
  # Triggering, from lazy-r
  def ZTR(rx,t=str):return t(      rx) if t in [list, tuple, dict, set, bytes, bytearray]\
                      else ''.join(rx) if t == str\
                      else         rx

  # filter on basic 
  MRIX=lambda x:lambda _am:lambda rx,*c,pre=x,**g:filter(lambda ri:pre(ri,*c,**g),rx)
  
  @MRIX(list.__contains__)
  def MRA(): pass
  @MRIX(lambda x,y: y.__contains__(x[0]))
  def MRT(): pass
  
  ZTR_DIC=lambda x,c:ZTR(MRT(x.items(),c),dict)

  # TODO 给出函数的对偶函数

  # FIXME
  NXD_EXS  = lambda x: NXD(x) if len(x) else NON
  #NXD_EGO = lambda x: NXD(x) if len(x) else x

  reg(TAM['G'](),TAM['C']())
initMθd()
def initLas():
  #CEG := abC_dEf_Ghi for default
  # TYP LAR = 娄(variable) 
  class LAR(TYA._OT): pass
  # TYP LAM = 函(function)
  class LAM(TYA._OT):
    def __new__(o,j,b,k):
      _F = FЯB
      for _B in b:
        # BΞ_(_B,'_am')
        if BEC(GΞ_(_B,'_am',NON)):
          _F = FRB
          break
      # 查'_am'方法
      if not _F and ('_am' not in k or not BEC(k['_am'])): raise TYC._ET("函宣，必可使'_am'调")
      # 添 __call__ 方法
      k['__call__']=lambda s,*c,**g: s._am(*c,**g)
      # 添 reset 方法
      def resnLAM(s,am):
        if not BEC( am): raise TYC._ET("必可使am调")
        s._am  =    am  
      k['res'] = resnLAM
      # ret-super TYB.SOX()
      return super().__new__(o,j,b,k)
  # Doo
  class Exc(metaclass = LAM):
    def _am(o,c,*d, fb= FRB):
      if fb:return VDO(c,*d)
      else:        ODO(c,*d)

  class AGG():
    @TYB._SM
    def TAZ(): return TZR
    @TYB._SM
    def TAC(): return _in.stack()[1].frame.f_locals
    @TYB._SM
    def TAG(): return _in.stack()[1].frame.f_globals

  # 量局，实时计算 vars() 的引申
  class Xar():
    # Map of abitems
    _JC_DIC = dict(
      Z = 'os.environ'       ,
      B = 'builtins.__dict__',
      G = 'globals()'        ,
      C =  'locals()'        ,
      G1= '_in.stack()[1].frame.f_globals',
      C1= '_in.stack()[1].frame.f_globals',
      Gb= 'OFC().f_back.f_globals',
      Cb= 'OFC().f_back.f_locals' )
    def __init__(o, Z='Z'):
      o._fc = Xar._JC_DIC[Z] if Z in Xar._JC_DIC else Xar._JC_DIC['C']
      o._am = Exc()
    __setstate__=__init__
    def __getstate__(o):  return o._fc
    __repr__=__getstate__
    def __getitem__(o,j:str  )->TYP.NSX: return o._am(f"{o._fc}.get('{j}')")
    def __setitem__(o,j:str,v)->TYP.NON:        o._am(f"{o._fc}")[    j] = v
    get=__getitem__
    def sed(o,j:str,v)->TYP.NON: # 如果有不能更改，更改用 __setitem__
      if BT_(v,str):o._am(f"{o._fc}.setdefault('{j}','{v}')",fb=FЯB)
      else:         o._am(f"{o._fc}.setdefault('{j}', {v} )",fb=FЯB)
    def __call__(o,Z='G'):                return Xar(Z)
  # 量局，维护内部字典
  class Tal():
    def __init__(     o,Z='G')->TYP.NON:o.O=TAM[Z] if Z in TAM else TAM["C"] # 增值するG
    def __getstate__( o      )->TYP.TSX:return o.O()
    def __getitem__(o,c:str  )->TYP.NSX:return o.O()[c] if c in o.O() else NON
    def __setitem__(o,c:str,v)->TYP.NON:o.O()[c]=v
    def __getattr__(o,c:str  )->TYP.NSX:return o.O()[c] if c in o.O() else NON
    #def __setattr__(o,c:str,v)->TYP.NON:o.O()[c]=v
    def rec(o,Z='G'):return Tal(Z)
    #def __call__(     o,Z='G'):         o.O=TAM["G"]()
    def __str__(): return"TAC,TAG,TAZ=TAM['C'](),TAM['G'](),TAM['Z']()"
   
  #reg(TAM["G"](),TAM["C"]())
  TAM['G']()['AGG'] = AGG
  TAM['G']()['TAL'] = Tal()
  TAM['G']()['VAR'] = Xar()
  OUA(__all__,'AGG')
  OUA(__all__,'TAL')
  OUA(__all__,'VAR')
initLas()

if Her():Cal(_me)