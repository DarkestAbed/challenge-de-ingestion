# app/backend/assets/config.py

DB_SQLITE_URI_TEMPLATE: str = "sqlite://fileloc"
DB_MYSQL_URI_TEMPLATE: str = "mysql+pymysql://user:passwd@hostname/db?host=hostname?port=servport"
DB_POSTGRES_URI_TEMPLATE: str = "postgresql+psycopg2://user:password@hostname/database_name"
DB_URIS: dict[str, str] = {
    "sqlite": DB_SQLITE_URI_TEMPLATE,
    "mysql": DB_MYSQL_URI_TEMPLATE,
    "postgres": DB_POSTGRES_URI_TEMPLATE,
}
