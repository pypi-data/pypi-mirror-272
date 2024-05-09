from goodpy.f.df_col_name_and_col.add_col import f as add_col
from goodpy.f.df_and_col import get_filtered_df
from goodpy.k.spark_session import SparkSession
from pyspark.sql.functions import collect_list
from pyspark.sql.functions import explode
from pyspark.ml.linalg import DenseVector
from pyspark.sql.types import BooleanType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import ArrayType
from goodpy.k.in_to_out import InToOut
from pyspark.sql.functions import udf
from pyspark.sql.functions import col
from pyspark.sql import DataFrame

window_type = ArrayType(IntegerType())
def f(df: DataFrame, in_to_out: InToOut,  window_size: int):
  in_col = in_to_out.input_col
  out_col = in_to_out.output_col
  gen_window = udf(lambda x: [x + i for i in range(window_size)], window_type)
  flatmap_df = add_col(df, 'id', gen_window('id'))
  flatmap_df = add_col(flatmap_df, 'id', explode('id'))
  sliding_df = flatmap_df.groupBy('id').agg(collect_list(in_col).alias(out_col))
  check_len = udf(lambda x: len(x) == window_size, BooleanType())
  sliding_df = get_filtered_df(sliding_df, check_len(col(out_col)))
  out_df =  df.join(sliding_df, on='id', how='inner')
  return out_df

def t():
  df = SparkSession().createDataFrame(
    [
      {'id': 1, 'vector': DenseVector([1.0, 2.0])},                       
      {'id': 2, 'vector': DenseVector([2.0, 3.0])},
      {'id': 3, 'vector': DenseVector([3.0, 4.0])},
      {'id': 4, 'vector': DenseVector([4.0, 5.0])}
    ]
  )
  out = f(df, InToOut('vector', 'sliding_vector'), 2)
  out = out.sort('id')
  out_dicts = list(map(lambda x: x.asDict(), out.collect()))
  y = [
    {
      'id': 2,
      'sliding_vector': [DenseVector([1.0, 2.0]), DenseVector([2.0, 3.0])],
      'vector': DenseVector([2.0, 3.0])
    },
    {
      'id': 3,
      'sliding_vector': [DenseVector([2.0, 3.0]), DenseVector([3.0, 4.0])],
      'vector': DenseVector([3.0, 4.0])},
    {
      'id': 4,
      'sliding_vector': [DenseVector([3.0, 4.0]), DenseVector([4.0, 5.0])],
      'vector': DenseVector([4.0, 5.0])
    }
  ]
  return out_dicts == y
