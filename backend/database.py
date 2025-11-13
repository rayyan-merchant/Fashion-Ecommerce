from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Example: update with your own credentials
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/FashionDb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
