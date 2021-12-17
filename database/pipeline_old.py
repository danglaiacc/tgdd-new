# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, col
import psycopg2

conn = psycopg2.connect(
    database="tgdd",
    host="localhost",
    user="postgres",
    password="12345")

with conn:
    with conn.cursor() as cur:
        with open('.initdb', 'r', encoding='utf8') as f:
            cur.execute(f.read())

conn.close()

# nếu muốn tạo bảng thì phải dùng psycopg2, phải kết nối 2 lần.
spark = SparkSession.builder\
    .appName('ETL Pipeline')\
    .master('local[2]')\
    .getOrCreate()

driver = 'org.postgresql.Driver'
url = "jdbc:postgresql://localhost/tgdd?user=postgres&password=12345"

def read_from_csv(file_path):
    return spark.read\
        .option('header', 'true')\
        .option('inferSchema', 'true')\
        .option("quote", '\"')\
        .option("escape", '\"')\
        .format('csv')\
        .load(file_path)


def write_to_postgresql(df, table, mode='append'):
    df.write\
        .format('jdbc')\
        .options(
            url=url,
            driver=driver,
            dbtable=table
        )\
        .mode(mode)\
        .save()

files = ['manufacturer.csv', 'branch.csv', 'series.csv', 'product.csv',
        'color.csv', 'customer.csv']

for file in files:
    file_df = read_from_csv(file)
    write_to_postgresql(file_df, file[:-4])

comment_df = read_from_csv('comment.csv')
comment_df_write = comment_df.select('customer_id', 'product_id', 'time_up', 'content', 'rate_star')\
    .withColumn('time_up', to_timestamp(col('time_up'), 'd/M/y H:m:s'))

write_to_postgresql(comment_df_write, 'comment')
