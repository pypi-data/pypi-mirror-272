from pyspark.sql.dataframe import DataFrame as PySparkDataFrame
from goodpy.f.iterable_and_seperator.concat import f as concat
from pyspark.sql.functions import collect_list as collect
from pyspark.ml.feature import VectorAssembler as V
from pyspark.testing import assertDataFrameEqual
from goodpy.k.spark_session import SparkSession
from pyspark.sql.types import BooleanType
from pyspark.sql.functions import explode
from pyspark.ml.linalg import DenseVector
from pyspark.sql.functions import struct
from pyspark.sql.functions import array
from pyspark.sql.types import ArrayType
from pyspark.sql.types import LongType
from pyspark.sql.functions import udf
from pyspark.sql.functions import lit
from pyspark.sql.functions import col
from typing_extensions import Self
from pyspark.sql import Column
from functools import partial
from pyspark.sql import Row
from typing import Union
from typing import List

shift = udf(lambda x, n: x + n, LongType())
gen_window = udf(lambda x, n: [x + i for i in range(n)], ArrayType(LongType()))
check_len  = udf(lambda x, n: len(x) == n, BooleanType())
c = partial(concat, seperator='-')

class DataFrame(PySparkDataFrame):
  def __init__(
    self,
    data: Union[list, tuple, dict, PySparkDataFrame, 'DataFrame'],
    spark_session: SparkSession):
    if type(data) in [PySparkDataFrame, DataFrame]: df = data
    else: df = spark_session.createDataFrame(data)
    super().__init__(df._jdf, df.sparkSession)
    
  def add_vector_col(
    s: Self,
    in_cols: List[Union[Column, str]],
    out_col_name: str
  ) -> 'DataFrame':
    return V(inputCols=in_cols, outputCol=out_col_name).transform(s)
  
  def add_col(s: Self, col_name: str, col: Column ) -> 'DataFrame':
    return super().withColumn(col_name, col)

  def add_array_col(
    s: Self,
    in_cols: List[Union[Column, str]],
    out_col_name: str
  ) -> 'DataFrame':
    return DataFrame(s.add_col(out_col_name, array(*in_cols)), s.sparkSession)
  
  def add_struct_col(
    s: Self,
    in_cols: List[Union[Column, str]],
    out_col_name: str
  ) -> 'DataFrame':
    return DataFrame(s.add_col(out_col_name, struct(*in_cols)), s.sparkSession)
  
  def add_shifted_col(
    s: Self,
    in_col: List[Union[Column, str]],
    shift_size: int,
    out_col_name: str
  ) -> 'DataFrame':
    shifted_df = s.add_col('id', shift('id', lit(shift_size)))
    shifted_df = shifted_df.select('id', col(in_col).alias(out_col_name))
    return DataFrame(s.join(shifted_df, on='id', how='inner'), s.sparkSession)
  
  def add_sliding_col(
    s: Self,
    in_col: Union[str, Column],
    window_size: int,
    out_col_name: str
  ) -> 'DataFrame':
    df_flatmap = s.add_col('id', explode(gen_window('id', lit(window_size))))
    df_sliding = df_flatmap.groupBy('id').agg(collect(in_col).alias(out_col_name))
    df_sliding = df_sliding.filter(check_len(out_col_name, lit(window_size)))
    return DataFrame(s.join(df_sliding, on='id', how='inner'), s.sparkSession)
  
  def add_shifted_cols(
    s: Self,
    in_cols: list[Union[str, Column]],
    shift_size: int,
    out_col_names: list[str]
  ) -> 'DataFrame':
    
    cols = s.columns
    array_col_name = c(in_cols)
    s = s.add_array_col(in_cols, array_col_name)
    shifted_array_col_name = c([array_col_name] + ['shift', str(shift_size)])
    s = s.add_shifted_col(array_col_name, shift_size, shifted_array_col_name)
    shifted_col = col(shifted_array_col_name)
    cols += [shifted_col[i].alias(out_col_names[i]) for i in range(len(in_cols))]
    return DataFrame(s.select(cols), s.sparkSession)
  
  def add_sliding_cols(
    s: Self,
    in_cols: list[Union[str, Column]],
    shift_size: int,
    out_col_names: list[str]
  ) -> 'DataFrame':
    cols = s.columns
    array_col_name = c(in_cols)
    s = s.add_array_col(in_cols, array_col_name)
    sliding_array_col_name = c([array_col_name] + ['sliding', str(shift_size)])
    s = s.add_sliding_col(array_col_name, shift_size, sliding_array_col_name)
    sliding_col = col(sliding_array_col_name)
    cols += [sliding_col[i].alias(out_col_names[i]) for i in range(len(in_cols))]
    return DataFrame(s.select(cols), s.sparkSession)
  
def f(x: dict): return DataFrame(**x)

def t_add_vector_col(x: DataFrame) -> bool:
  z = x.add_vector_col(['id', 'open'], 'vector')
  y = DataFrame(
    data=[
      {'id': 1, 'open': 1, 'vector': DenseVector([1.0, 1.0])},                       
      {'id': 2, 'open': 2, 'vector': DenseVector([2.0, 2.0])},
      {'id': 3, 'open': 3, 'vector': DenseVector([3.0, 3.0])},
      {'id': 4, 'open': 4, 'vector': DenseVector([4.0, 4.0])}
    ],
    spark_session=x.sparkSession
  )
  return True

def t_add_array_col(x: DataFrame) -> bool:
  z = x.add_array_col(['id', 'open'], 'array')
  y = DataFrame(
    [
      Row(id=1, open=1, array=[1, 1]),
      Row(id=2, open=2, array=[2, 2]),
      Row(id=4, open=4, array=[4, 4]),
      Row(id=3, open=3, array=[3, 3])
    ],
    x.sparkSession
  )
  assertDataFrameEqual(z, y)
  return True

def t_add_struct_col(x: DataFrame) -> bool:
  z = x.add_struct_col(['id', 'open'], 'struct')
  y = DataFrame(
    [
      Row(id=1, open=1, struct=Row(id=1, open=1)),                                   
      Row(id=2, open=2, struct=Row(id=2, open=2)),
      Row(id=3, open=3, struct=Row(id=3, open=3)),
      Row(id=4, open=4, struct=Row(id=4, open=4))
    ],
    x.sparkSession
  )
  assertDataFrameEqual(z, y)
  return True

def t_add_shifted_col(x: DataFrame) -> bool:
  
  def t_add_shifted_col_shift_up(x: DataFrame) -> bool:
    z = x.add_shifted_col('open', 2, 'shifted_open').sort('id')
    y = DataFrame(
      [
        {'id': 3, 'open': 3, 'shifted_open': 1},                                       
        {'id': 4, 'open': 4, 'shifted_open': 2}
      ],
      x.sparkSession
    )
    assertDataFrameEqual(z, y)
    return True
  
  def t_add_shifted_col_shift_down(x: DataFrame) -> bool:
    z = x.add_shifted_col('open', -2, 'shifted_open').sort('id')
    y = DataFrame(
      [
        {'id': 1, 'open': 1, 'shifted_open': 3},
        {'id': 2, 'open': 2, 'shifted_open': 4}
      ],
      x.sparkSession
    )
    assertDataFrameEqual(z, y)
    return True
  
  return all([t_add_shifted_col_shift_up(x), t_add_shifted_col_shift_down(x)])

def t_add_sliding_col(x: DataFrame) -> bool:
  y = DataFrame(
    [
      Row(id=2, open=2, sliding_open=[1, 2]),                                        
      Row(id=3, open=3, sliding_open=[2, 3]),
      Row(id=4, open=4, sliding_open=[3, 4])
    ],
    x.sparkSession
  )
  z = x.add_sliding_col('open', 2, 'sliding_open')
  assertDataFrameEqual(z, y)
  return True

def t_single_column_tests():
  x = DataFrame(
    data=[
      {'id': 1, 'open': 1},
      {'id': 2, 'open': 2},
      {'id': 3, 'open': 3},
      {'id': 4, 'open': 4}
    ],
    spark_session=SparkSession()
  )

  return all(
    [
      t_add_vector_col(x),
      t_add_array_col(x),
      t_add_struct_col(x),
      t_add_shifted_col(x),
      t_add_sliding_col(x)
    ]
  )
  
def t_add_shifted_cols(x: DataFrame):
  z = x.add_shifted_cols(['open', 'close'], 2, ['shifted_open', 'shifted_close'])
  y = DataFrame(
    data=[
      Row(id=3, open=3, close=4, shifted_open=1, shifted_close=2),
      Row(id=4, open=4, close=5, shifted_open=2, shifted_close=3)
    ],
    spark_session=SparkSession()
  )
  assertDataFrameEqual(z, y)
  return True

def t_add_sliding_cols(x: DataFrame):
  z = x.add_sliding_cols(['open', 'close'], 2, ['sliding_open', 'sliding_close'])
  y = DataFrame(
    data=[
      Row(id=2, open=2, close=3, sliding_open=[1, 2], sliding_close=[2, 3]),
      Row(id=3, open=3, close=4, sliding_open=[2, 3], sliding_close=[3, 4]),
      Row(id=4, open=4, close=5, sliding_open=[3, 4], sliding_close=[4, 5])
    ],
    spark_session=SparkSession()
  )
  assertDataFrameEqual(z, y)
  return True
  
def t_multi_columns_tests():
  x = DataFrame(
    data=[
      Row(id=1, open=1, close=2),
      Row(id=2, open=2, close=3),
      Row(id=3, open=3, close=4),
      Row(id=4, open=4, close=5)
    ],
    spark_session=SparkSession()
  )
  return all(
    [
      t_add_shifted_cols(x),
      t_add_sliding_cols(x)
    ]
  )
  
def t(): return all([t_single_column_tests(), t_multi_columns_tests()])
