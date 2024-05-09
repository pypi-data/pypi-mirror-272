from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class InsToOut:
  input_cols: List[str]
  output_col: str
  
def f(x: dict): return InsToOut(**x)
def t(): return f({'input_cols': ['c'], 'output_col': 'output_col'})
