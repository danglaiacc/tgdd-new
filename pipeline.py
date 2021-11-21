# -*- coding: utf-8 -*-
'''
spark-submit --conf spark.ui.port=5051 pipeline.py
'''
from pyspark.sql import SparkSession, functions as f
from pyspark.sql.types import IntegerType, StringType
spark = SparkSession.builder\
    .appName('ETL Pipeline')\
    .master('local[2]')\
    .getOrCreate()

phone_path = './getphone/phones.csv'
driver = 'org.postgresql.Driver'
url = "jdbc:postgresql://localhost/tgdd?user=postgres&password=12345"

# EXTRACT
phone_df = spark.read\
    .option('header', 'true')\
    .option('inferSchema', 'true')\
    .option("quote", "\"")\
    .option("escape", "\"")\
    .format('csv')\
    .load(phone_path)

manufacturers = {'iphone': 1, 'samsung': 2, 'oppo': 3, 'vivo': 4, 'xiaomi': 5, 'realme': 6,
                 'oneplus': 7, 'nokia': 8, 'mobell': 9, 'itel': 10, 'masstel': 11, 'energizer': 12, 'vsmart': 13}
get_manu_id_udf = f.udf(
    lambda manu_name: manufacturers[manu_name.lower()],
    IntegerType()
)

get_series_id_udf = f.udf(
    lambda series_name: series_name.lower().replace(' ', '-'),
    StringType()
)
# transform series table
series_df = phone_df.select('manu_name', 'series_name')\
    .distinct()\
    .withColumn('id', get_series_id_udf(f.col('series_name')))\
    .withColumnRenamed('series_name', 'name')\
    .withColumn('manu_id', get_manu_id_udf(f.col('manu_name')))

# load to series table
series_df.write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='series'
    )\
    .mode('ignore')\
    .save()


# extract series table
series_df = spark.read\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='series'
    ).load()

series_dic = series_df\
    .select('name', 'id')\
    .distinct()\
    .toPandas()\
    .set_index("name")["id"]\
    .to_dict()

# transform product table
phone_df = phone_df\
    .withColumn('series_id', get_series_id_udf(f.col('series_name')))\
    .drop('manu_name', 'series_name')

phone_df.printSchema()
phone_df.show(5)

phone_df.write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='product'
    )\
    .mode('ignore')\
    .save()

# print(series_dic)
