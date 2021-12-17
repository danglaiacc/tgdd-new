from pyspark.sql import SparkSession

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
        'color.csv', 'customer.csv', 'comment.csv' ]

for file in files:
    file_df = read_from_csv(file)
    write_to_postgresql(file_df, file[:-4])
