import psycopg2
import uuid

con = psycopg2.connect(dbname='aqi_index', user='user', password='password', host='localhost')
cursor = con.cursor()

