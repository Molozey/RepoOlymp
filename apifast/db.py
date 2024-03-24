import psycopg2 as pg
import os
import pandas as pd


HOST = os.getenv("NET_NAME", "localhost")
DBNAME = os.getenv("DB_NAME", "task1")
DBUSER = os.getenv("DB_USER", "root")
DBPWD = os.getenv("DB_PWD", "password")

ENGINE = lambda : pg.connect(f"dbname='{DBNAME}' user='{DBUSER}' host='{HOST}' port='5432' password='{DBPWD}'")

print(pd.read_sql(f"""SELECT * FROM platform.user_with_roles WHERE login='login' AND password='password'""", con=ENGINE()))