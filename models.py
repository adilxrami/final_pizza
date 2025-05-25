from sqlalchemy import Column, Integer, Float,String, create_engine,ForeignKey
from database import Base  # Import the Base object from your database.py file

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(15))
    password = Column(String(255))
class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    pizza_type = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    size = Column(String(20), nullable=False)
    crust = Column(String(20), nullable=False)
    cheese = Column(String(20), nullable=False)
    price = Column(Float)
    email = Column(String(20), nullable=False)
class CustomOrder(Base):
    __tablename__ = 'custom_order'  # Ensure unique table name
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    size = Column(String(20), nullable=False)
    crust = Column(String(20), nullable=False)
    cheese = Column(String(20), nullable=False)
    toppings = Column(String(20), nullable=False)
    price = Column(Float)
    email = Column(String(20), nullable=False)
engine = create_engine('mysql+pymysql://root:@localhost:3306/swizz_pizza')  # Update this to your actual database URI

Base.metadata.create_all(engine)
