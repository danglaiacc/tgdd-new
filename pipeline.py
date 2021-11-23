# -*- coding: utf-8 -*-
'''
spark-submit --conf spark.ui.port=5051 pipeline.py
'''
from pyspark.sql import SparkSession, functions as f
from pyspark.sql.types import DateType, IntegerType, StringType, TimestampType
import random
from datetime import datetime


spark = SparkSession.builder\
    .appName('ETL Pipeline')\
    .master('local[2]')\
    .getOrCreate()

phone_path = './getphone/phones.csv'
color_path = './getphone/colors.csv'
comment_path = './getphone/comments.csv'

driver = 'org.postgresql.Driver'
url = "jdbc:postgresql://localhost/tgdd?user=postgres&password=12345"

''' done add phone and series '''
# EXTRACT
'''
phone_df = spark.read\
    .option('header', 'true')\
    .option('inferSchema', 'true')\
    .option("quote", "\"")\
    .option("escape", "\"")\
    .format('csv')\
    .load(phone_path)

manu_dic = {'iphone': 1, 'samsung': 2, 'oppo': 3, 'vivo': 4, 'xiaomi': 5, 'realme': 6,
            'oneplus': 7, 'nokia': 8, 'mobell': 9, 'itel': 10, 'masstel': 11, 'energizer': 12, 'vsmart': 13}
get_manu_id_udf = f.udf(
    lambda manu_name: manu_dic[manu_name.lower()],
    IntegerType()
)

# transform series table
series_df = phone_df.select('manu_name', 'series_name')\
    .distinct()\
    .withColumnRenamed('series_name', 'name')\
    .withColumn('manu_id', get_manu_id_udf(f.col('manu_name')))\
    .drop('manu_name')

series_df\
    .write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='series'
    )\
    .mode('append')\
    .save()

# extract series table
series_df_read = spark.read\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='series'
    ).load()

get_manu_series_udf = f.udf(
    lambda manu_id, series_name: str(manu_id)+'-'+series_name,
    StringType()
)

series_dic = series_df_read\
    .select('manu_id', 'name', 'id')\
    .withColumn(
        'manu_series',
        get_manu_series_udf(f.col('manu_id'), f.col('name')))\
    .toPandas()\
    .set_index("manu_series")["id"]\
    .to_dict()

# TRANSFORM phone df

get_series_id_udf = f.udf(
    lambda manu_name, series_name:
    series_dic[str(manu_dic[manu_name.lower()])+'-'+series_name],
    IntegerType()
)


phone_df_write = phone_df\
    .withColumn(
        'series_id',
        get_series_id_udf(f.col('manu_name'), f.col('series_name')))\
    .drop('manu_name', 'series_name')


# LOAD phone to product table
phone_df_write.write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='product'
    )\
    .mode('append')\
    .save()

color_df = spark.read\
    .option('header', 'true')\
    .option('inferSchema', 'true')\
    .option("quote", "\"")\
    .option("escape", "\"")\
    .format('csv')\
    .load(color_path)


color_df.write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='color'
    )\
    .mode('append')\
    .save()
'''

comment_df = spark.read\
    .option('header', 'true')\
    .option('inferSchema', 'true')\
    .option("quote", "\"")\
    .option("escape", "\"")\
    .format('csv')\
    .load(comment_path)

'''
customer_df = comment_df.selectExpr(
    'customer_id as id',
    'customer_fullname as fullname')


customer_df.write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='customer'
    )\
    .mode('append')\
    .save()

# comment_imgs,content,date_buy,product_id,rate_star,time_up,customer_id,customer_fullname
'''


def random_date(time_up):
    if time_up != None:
        return time_up+' 0:0:0'
    first_timestamp = 1546324200
    second_timestamp = 1642197000
    random_timestamp = random.randint(first_timestamp, second_timestamp)
    return datetime\
        .fromtimestamp(random_timestamp)\
        .strftime('%d/%m/%Y %H:%M:%S')


timeup_udf = f.udf(
    lambda time_up: random_date(time_up),
    StringType()
)

comment_df.select(
    'customer_id',
    'product_id',
    'time_up',
    'content',
    'rate_star'
)\
    .withColumn(
    'time_up',
    f.to_timestamp(
        timeup_udf(f.col('time_up')),
        'd/M/y H:m:s'))\
    .write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='comment')\
    .mode('append')\
    .save()
