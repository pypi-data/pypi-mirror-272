"""
 #  bas-muti :: tye-las 懒类集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Las of lazy builtin basic-python
"""


from .__deps__ import *
from .depLam import *
from .decLam import *

#def betrOng( c): return len(ox) >0 容 TODO PALL

# lazyUP function tuple
class Fup(tuple):
    def __new__(ido, am,*c ,**g):
        if  not bet( am,'C'    ):     raise TYC.EOT("e_1._fB-lEt-Cal:FRB")
        #用tuple，因TypeError: unhashable type: 'dict','mappingproxy'
        ego = super().__new__(ido,(am,c,tuple(g.items())))
        ego.initLam()
        return  ego
    def initLam(ego):
        @TYB._HM(maxsize=1) # only once 理论上tuple自身只有一种情况，除非元素是一个结构对象
        def val():return ego[0](*ego[1],**dict(ego[2])) # 闭包
        ego.val = val
    @TYB._HM(maxsize=256)   # FIXME 对整个Fup设置合适缓存对付计算密集型 
    def __call__(ego): return ego.val()

# 示例类，使用装饰器
@MAXXCBL()
class Laz:
    @TYB._CM
    @TYB._HM(maxsize=OBR._qi) # 保证运算的唯一性
    def aop(ido, op):
        return (lambda x,y: op(x.val, y.val)), (lambda x,y: op(x.val, y))
    def __new__(ido, am,*c ,**g):
        ego=super().__new__(ido)
        if      bet( am,Fup) :  ego._up=     am          # __call__ cache
        elif    bet( am,'C') :  ego._up=Fup( am, *c,**g) # need calculate
        else: raise TYC.EOT("e_1._fB-lEt-Fup or._fB-lEt-Cal:FRB")
        ego.__call__=ego.__cal__
        ego.__repr__=ego.__str__
        return  ego
    # 去魅：被调用或符化时
    def __cal__(ego):return     ego._up()
    def __str__(ego):return str(ego._up())
    @property #去魅端：取其值
    def   val  (ego):return     ego._up()
    # 二元操作泛型
    def __cbl__( o , d , op=OBR.ADD):
        _1p,_2p=Laz.aop( op)
        return  Laz(_1p,o,d)if BT_(d,Laz)\
           else Laz(_2p,o,d)
        #return  Laz(lambda x,y:op(x.val,y.val),o,d)if BT_(d,Laz)\
        #   else Laz(lambda x,y:op(x.val,y    ),o,d)

if  Her(__name__):
    print(__name__)
    def SUM(*c): return sum(c)
    q0= Fup(range, 10000000)
    q1= Fup(range, 10000001)
    print('enp')
    a0= Fup(SUM,*list(q0()))
    a1= Fup(SUM,*list(q1()))
    u = Fup(SUM,*list(q0()))
    print('range转list再解包需要时间')
    x = Laz(a0) +1
    y = Laz(a1)
    z = Laz(u)
    print(1)
    print(x.val)
    print('第一次计算x需要时间')
    print(x.val)
    print(z.val)
    z = x+y
    print(z.val)
    print(1)
    y = x+1
    z = x+y
    print(z.val)
    g = x+y+1
    t = x+y+2
    print(t.val)
    print(g.val)
    print('end')