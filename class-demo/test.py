import psycopg2

conn = psycopg2.connect('dbname=example user=postgres password=jenifer')

cursor = conn.cursor()

cursor = conn.cursor()

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS todos;")

cur.execute("""
    CREATE TABLE todos (
        id serial PRIMARY KEY,
        description VARCHAR NOT NULL
    );
""")

conn.commit()

cur.close()
conn.close()
