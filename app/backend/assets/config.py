# app/backend/assets/config.py

from os import getcwd
from os.path import join


DB_LOCATION: str = join(getcwd(), "app", "backend", "db")
DB_MYSQL_URI_TEMPLATE: str = "mysql+pymysql://user:passwd@hostname/db?host=hostname?port=servport"
DB_POSTGRES_URI_TEMPLATE: str = "postgresql+psycopg2://user:password@hostname/database_name"
