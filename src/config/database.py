from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import *

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(bind=engine)