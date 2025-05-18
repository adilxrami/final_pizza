from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

adil_db = create_engine("mysql+pymysql://root:@localhost:3306", echo=True) 
with adil_db.connect() as conn: 
    conn.execute(text("CREATE DATABASE IF NOT EXISTS swizz_pizza"))
    print("Database 'swizz_pizza' checked/created.")
    
connection = "mysql+pymysql://root:@localhost:3306/swizz_pizza"

engine = create_engine(connection, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1")) 
        print("Database connected successfully!")
        print("Connection test successful!")
except Exception as e:
    print("Error connecting to the database:", e)
    print("Connection test failed.")
