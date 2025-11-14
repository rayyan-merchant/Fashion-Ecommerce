# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update these credentials if needed
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/FashionDb"

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
