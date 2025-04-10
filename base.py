from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://user:password123!@localhost:5432/database')
Session = sessionmaker(bind=engine)

Base = declarative_base()