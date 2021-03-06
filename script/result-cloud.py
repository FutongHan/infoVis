from script.Processor.DataProcessor import DataProcessor as Dp
from pyspark.sql.functions import col, lit, udf
from pyspark.sql.types import IntegerType
from SYS import FILE, COL, MODE


def update_year(in_year):
    return int(int((int(in_year)) / 20.1) * 20.1)


dp = Dp()
clean_udf = udf(update_year, IntegerType())

df = dp.read_parquet(FILE.word_cloud_data2_uri)
df = df.filter(col(COL.year) >= 0)
df = df.withColumn(COL.year, clean_udf(col(COL.year)))
if MODE.debug:
    df.show()
    print(df.select(COL.year).drop_duplicates([COL.year]).count())
else:
    dp.save_parquet(df, FILE.result_word_cloud_uri)
