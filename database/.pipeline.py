import psycopg2

conn = psycopg2.connect(
    database="tgdd",
    host="localhost",
    user="postgres",
    password="12345")

def copy_data(file_path, table):
    with open('.csv', 'r') as f:
        next(f) # Skip the header row.
        cur.copy_from(f, 'users', sep=',')
     
with conn:
    with conn.cursor() as cur:
        with open('.initdb', 'r', encoding='utf8') as f:
            cur.execute(f.read())

        files = ['manufacturer.csv', 'branch.csv', 'series.csv', 'product.csv',
                'color.csv', 'customer.csv', 'comment.csv' ]

        for file in files:
            with open(file, 'r', encoding='utf8') as f:
                next(f) # Skip the header row.
                cur.copy_from(f, file[:-4], sep=',') # file[:-4] = table name
 
conn.close()
