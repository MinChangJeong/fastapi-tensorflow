# config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL 컨테이너 정보에 맞게 수정
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "watersaver"
MYSQL_HOST = "mysqldb"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "watersaver"

# SQLALCHEMY_DATABASE_URL 설정
SQLALCHEMY_DATABASE_URL = f"mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# SQLAlchemy 설정
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
