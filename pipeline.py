from pyspark.sql import SparkSession, functions as f
spark = SparkSession.builder\
        .appName('ETL Pipeline')\
        .master('local[2]')\
        .getOrCreate()

phone_path = '/FileStore/tables/phones.csv'
phone_df = spark.read\
        .option('header','true')\
        .option('inferSchema', 'true')\
        .format('csv')\
        .load(phone_path)





