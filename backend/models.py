from pydantic import BaseModel
from datetime import datetime, date

# ----------- ARTICLES -----------
class Articles(BaseModel):
    article_id: str
    product_code: int
    prod_name: str
    product_type_name: str
    product_group_name: str
    graphical_appearance_name: str
    colour_group_name: str
    department_no: str
    department_name: str
    index_name: str
    index_group_name: str
    section_name: str
    garment_group_name: str
    detail_desc: str
    price: float
    stock: int
    category_id: int | None= None
    
    class Config:
        orm_mode = True


# ----------- CATEGORIES -----------
class Categories(BaseModel):
    category_id: int
    name: str
    parent_category_id: int


# ----------- CUSTOMERS -----------
class Customers(BaseModel):
    customer_id: str
    age: int
    postal_code: str
    club_member_status: str
    fashion_news_frequency: str
    active: bool
    first_name: str
    last_name: str
    email: str
    signup_date: datetime


# ----------- EVENTS -----------
class Events(BaseModel):
    event_id: int
    session_id: str
    customer_id: str
    article_id: str
    event_type: str
    campaign_id: int
    created_at: datetime


# ----------- ORDER ITEMS -----------
class OrderItems(BaseModel):
    order_item_id: int
    order_id: int
    article_id: str
    quantity: int
    unit_price: float
    line_total: float


# ----------- ORDERS -----------
class Orders(BaseModel):
    order_id: int
    customer_id: str
    order_date: datetime
    total_amount: float
    payment_status: str
    shipping_address: str


# ----------- REVIEWS -----------
class Reviews(BaseModel):
    review_id: int
    customer_id: str
    article_id: str
    rating: int
    review_text: str
    created_at: datetime


# ----------- TRANSACTIONS -----------
class Transactions(BaseModel):
    transaction_id: int
    t_dat: date
    customer_id: str
    article_id: str
    price: float
    sales_channel_id: int
