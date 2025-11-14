from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date


# ----------- ARTICLES -----------
class Articles(BaseModel):
    article_id: str
    product_code: Optional[int] = None
    prod_name: Optional[str] = None
    product_type_name: Optional[str] = None
    product_group_name: Optional[str] = None
    graphical_appearance_name: Optional[str] = None
    colour_group_name: Optional[str] = None
    department_no: Optional[str] = None
    department_name: Optional[str] = None
    index_name: Optional[str] = None
    index_group_name: Optional[str] = None
    section_name: Optional[str] = None
    garment_group_name: Optional[str] = None
    detail_desc: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- CATEGORIES -----------
class Categories(BaseModel):
    category_id: int
    name: Optional[str] = None
    parent_category_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- CUSTOMERS -----------
class Customers(BaseModel):
    customer_id: str
    age: Optional[int] = None
    postal_code: Optional[str] = None
    club_member_status: Optional[str] = None
    fashion_news_frequency: Optional[str] = None
    active: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    signup_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- EVENTS -----------
class Events(BaseModel):
    event_id: Optional[int] = None
    session_id: Optional[str] = None
    customer_id: Optional[str] = None
    article_id: Optional[str] = None
    event_type: Optional[str] = None
    campaign_id: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- ORDER ITEMS -----------
class OrderItems(BaseModel):
    order_item_id: Optional[int] = None
    order_id: Optional[int] = None
    article_id: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    line_total: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- ORDERS -----------
class Orders(BaseModel):
    order_id: Optional[int] = None
    customer_id: Optional[str] = None
    order_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    payment_status: Optional[str] = None
    shipping_address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- REVIEWS -----------
class Reviews(BaseModel):
    review_id: Optional[int] = None
    customer_id: Optional[str] = None
    article_id: Optional[str] = None
    rating: Optional[int] = None
    review_text: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ----------- TRANSACTIONS -----------
class Transactions(BaseModel):
    transaction_id: Optional[int] = None
    t_dat: Optional[date] = None
    customer_id: Optional[str] = None
    article_id: Optional[str] = None
    price: Optional[float] = None
    sales_channel_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
