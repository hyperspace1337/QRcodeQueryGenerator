from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

db_login = "root"
db_pass = "1337"
db_name = "consumable_query_app"

DATABASE_URL = f"mysql+pymysql://{db_login}:{db_pass}@localhost:3306/{db_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
