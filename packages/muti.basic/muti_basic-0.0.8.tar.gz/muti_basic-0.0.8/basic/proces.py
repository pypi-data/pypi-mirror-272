from .__deps__ import *


class 


def TRY(s, s_e=NON):
    try: exec(s) if s is str else 
    except: exec('pass') if s_e is NON else exec(s_e)

# 辶：迹所程式 (Process)
class   EXE(Namespace):
  #FIXME
  DOO = lambda s: exec(s)     # 道
  
  TRY = lambda s: TRY        # 迫