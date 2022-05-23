from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from application.config import Config
import os

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

session = sessionmaker(bind=engine)
Base = declarative_base()

Session = session()


# print(engine.url.database)
# for tbl in reversed(Base.metadata.sorted_tables):
#     engine.execute(tbl.delete())

def get_db():
    db = Session()
    try:
        yield db
    except:
        db.close()
