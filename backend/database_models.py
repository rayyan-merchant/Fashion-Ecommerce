from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


# ---------- ARTICLES ----------
class Articles(Base):
    __tablename__ = "articles"

    article_id = Column(Integer, primary_key=True, index=True)
    product_code = Column(Integer)
    prod_name = Column(String(255))
    product_type_name = Column(String(255))
    product_group_name = Column(String(255))
    graphical_appearance_name = Column(String(255))
    colour_group_name = Column(String(255))
    department_no = Column(String(50))
    department_name = Column(String(255))
    index_name = Column(String(255))
    index_group_name = Column(String(255))
    section_name = Column(String(255))
    garment_group_name = Column(String(255))
    detail_desc = Column(String(255))
    price = Column(Float)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.category_id"))


# ---------- CATEGORIES ----------
class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    parent_category_id = Column(Integer, ForeignKey("categories.category_id"))


# ---------- CUSTOMERS ----------
class Customers(Base):
    __tablename__ = "customers"

    customer_id = Column(String(255), primary_key=True, index=True)
    age = Column(Integer)
    postal_code = Column(String(20))
    club_member_status = Column(String(100))
    fashion_news_frequency = Column(String(100))
    active = Column(Boolean)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    signup_date = Column(DateTime, default=datetime.utcnow)


# ---------- EVENTS ----------
class Events(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255))
    customer_id = Column(String(255), ForeignKey("customers.customer_id"))
    article_id = Column(String(255), ForeignKey("articles.article_id"))
    event_type = Column(String(100))
    campaign_id = Column(Integer, ForeignKey("campaigns.campaign_id"))
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------- ORDER ITEMS ----------
class OrderItems(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    article_id = Column(String(255), ForeignKey("articles.article_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    line_total = Column(Float)


# ---------- ORDERS ----------
class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(255), ForeignKey("customers.customer_id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    payment_status = Column(String(100))
    shipping_address = Column(String(255))


# ---------- REVIEWS ----------
class Reviews(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(255), ForeignKey("customers.customer_id"))
    article_id = Column(String(255), ForeignKey("articles.article_id"))
    rating = Column(Integer)
    review_text = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------- TRANSACTIONS ----------
class Transactions(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    t_dat = Column(Date)
    customer_id = Column(String(255), ForeignKey("customers.customer_id"))
    article_id = Column(String(255), ForeignKey("articles.article_id"))
    price = Column(Float)
    sales_channel_id = Column(Integer)
