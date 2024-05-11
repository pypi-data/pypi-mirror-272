"""
 #  bas-muti :: dec-lam 使函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of deco builtin basic-python
    欺世盗名
"""
from   .__deps__  import *

#MAX_CAL
# 类饰, 基于__cbl__(若有)自动扩充二元运算符
def MAXsCBL(las, am = NON):
    # 创建模板函数 _am
    _am=GΞ_(las,'__cbl__',am) # FIXME first am
    if _am is NON:_am=lambda o,d,op=OBR.ADD:las(op(o.val, d.val))if BT_(d, las)\
                                       else las(op(o.val, d    ))
    # _fm.partial(_am, op=_op)
    max_opr = lambda _op: lambda e,d:_am(e,d,op=_op)
    # 为每个运算符添加相应的方法
    for _jc,_op in OBR.__dict__.items():
        if not BPC(_jc,'_'):SΞ_(las,OBR._ym(_jc),max_opr(_op))
    return las
# 時計之MAX
def MAX_CST( am):
    def     wam( *c,**g):
      _li = GST(       )
      res =  am( *c,**g)
      print(f"[{am.__name__}]時耗{time.time()-_li}秒")
      return res
    return wam

MAXXCBL = lambda _am=NON: lambda _as: MAXsCBL(_as, am=_am)