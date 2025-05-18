from models import Order, CustomOrder
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class OrderService:
    def __init__(self):
        engine = create_engine('mysql+pymysql://root:@localhost:3306/swizz_pizza')
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def get_regular_orders(self):
        session = self.Session()
        try:
            return session.query(Order).all()
        finally:
            session.close()

    def get_custom_orders(self):
        session = self.Session()
        try:
            return session.query(CustomOrder).all()
        finally:
            session.close()

    def delete_order(self, order_id):
        session = self.Session()
        try:
            order = session.query(Order).get(order_id)
            if order:
                session.delete(order)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def delete_custom_order(self, order_id):
        session = self.Session()
        try:
            order = session.query(CustomOrder).get(order_id)
            if order:
                session.delete(order)
                session.commit()
                return True
            return False
        finally:
            session.close()
