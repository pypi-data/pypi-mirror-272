from dataclasses import dataclass

@dataclass(frozen=True)
class InToOut:
  input_col: str
  output_col: str
  
def f(x: dict): return InToOut(**x)
def t(): return f({'input_col': 'c', 'output_col': 'output_col'})
