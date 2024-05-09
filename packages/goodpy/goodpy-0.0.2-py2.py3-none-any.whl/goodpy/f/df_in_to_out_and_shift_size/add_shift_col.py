from goodpy.f.df_col_name_and_col.add_col import f as add_col

from goodpy.k.spark_session import SparkSession
from pyspark.sql.types import IntegerType
from goodpy.k.in_to_out import InToOut
from pyspark.sql.functions import udf
from pyspark.sql.functions import col
from pyspark.sql import DataFrame

def f(df: DataFrame, in_to_out: InToOut, shift_size: int):
  col_name = in_to_out.input_col
  shift_col_name = in_to_out.output_col
  shift = udf(lambda x: x + shift_size, IntegerType())
  shifted_df = add_col(df, 'id', shift(col('id')))
  shifted_df = shifted_df.select('id', col(col_name).alias(shift_col_name))
  out = shifted_df.join(df, on='id')
  return out
  
def t1(df):
  out = f(df, InToOut('open', 'shifted_open'), 2)
  out = out.sort('id')
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [
    {'id': 3, 'open': 3, 'shifted_open': 1},                                       
    {'id': 4, 'open': 4, 'shifted_open': 2}
  ]
  return y == out_dicts

def t2(df):
  out = f(df, InToOut('open', 'shifted_open'), -2)
  out = out.sort('id')
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [
    {'id': 1, 'open': 1, 'shifted_open': 3},                                       
    {'id': 2, 'open': 2, 'shifted_open': 4}
  ]
  return y == out_dicts
  
def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ]
  )
  return all(
    [
      t1(df),
      t2(df)
    ]
  )
