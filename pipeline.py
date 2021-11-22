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

#print('series df from csv file')
# series_df.show(2)
#print('series df count:',series_df.count())

series_df_origin = spark.read\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='series'
    ).load()

#series_df_origin = series_df_origin.select('name', 'id', 'manu_id')
#print('series df from database origin')
# series_df_origin.show(2)
#print('series_df_origin count: ',series_df_origin.count())
# print((series_df.count(), len(series_df.columns)))
# load to series table

write_df = series_df.join(
    series_df_origin,
    (series_df.name == series_df_origin.name) &
    (series_df.manu_id == series_df_origin.manu_id),
    how='left_anti')

# write_df.show(200)
#
#print('write df count: ',write_df.count())
write_df\
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

#print('total series in database', len(series_dic))
# print(series_dic)
# transform product table
'''
phone_df.printSchema()
get_orig_price_udf = f.udf(
    lambda sale_price, orig_price: sale_price if orig_price == 'null' else orig_price,
    IntegerType()
)

    .withColumn('orig_price', get_orig_price_udf(
        f.col('sale_price'),
        f.col('orig_price')))\
 
'''


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

#phone_df = phone_df.limit(5)

# phone_df.select('id', 'orig_price').show(10)
phone_df_write.write\
    .format('jdbc')\
    .options(
        url=url,
        driver=driver,
        dbtable='product'
    )\
    .mode('append')\
    .save()

# print(series_dic)
