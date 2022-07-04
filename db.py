from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base, sessionmaker
engine = create_engine('mariadb+pymysql://root:@localhost/LPR-db?charset=utf8mb4' )
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
# create Database
def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)

        
    

