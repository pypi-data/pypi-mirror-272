from goodpy.k.spark_session import SparkSession
from pyspark.sql.types import BooleanType
from pyspark.sql.functions import udf
from pyspark.sql import DataFrame
from pyspark.sql import Column

def f(df: DataFrame, col_name: str, col: Column)->DataFrame:
  return df.withColumn(col_name, col)

def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ]
  )
  
  def compare(x, y): return x > y
  compare_udf = udf(compare, BooleanType())
  out = f(df, 'compare_result', compare_udf('id', 'open'))
  return True