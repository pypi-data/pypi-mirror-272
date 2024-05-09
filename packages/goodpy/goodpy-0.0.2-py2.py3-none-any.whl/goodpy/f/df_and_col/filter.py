from goodpy.k.spark_session import SparkSession
from pyspark.sql.types import BooleanType
from pyspark.sql.functions import udf
from pyspark.sql import DataFrame
from pyspark.sql import Column

def f(df: DataFrame, col: Column): return df.filter(col)
def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ]
  )
  func = udf(lambda x: x >= 4, BooleanType())
  out = f(df, func('open'))
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [{'id': 4, 'open': 4}]
  return y == out_dicts
