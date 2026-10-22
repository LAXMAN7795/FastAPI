from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
from sqlalchemy.engine import URL


SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=int(settings.database_port),
    database=settings.database_name
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
def get_db():
    db = SessionLocal() # everytime we run we get session after that closed
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Laxman@7795',
#                                 cursor_factory=RealDictCursor)
#         # cursor_factory tells the Python PostgreSQL driver (psycopg2) to return database query results as a list of 
#         # Python dictionaries instead of standard tuples
#         cursor = conn.cursor()
#         print("DataBase connection was successfull!")
#         break
#     except Exception as error:
#         print("DataBase connection failed")
#         print("Error was:",error)