# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import Session, engine
import database_models
import models

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# If you want to create tables from SQLAlchemy models (careful in production)
# database_models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/testdb")
def test_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM articles;")).scalar()
        return {"status": "ok", "articles_count": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def greet():
    return {"message": "Welcome to ML-DB FastAPI backend!"}

# ---------------- ARTICLES ----------------
@app.get("/articles", response_model=list[models.Articles])
def get_all_articles(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    # pagination to avoid returning all 100k rows
    rows = db.query(database_models.Articles).limit(limit).offset(offset).all()
    return rows

@app.get("/articles/{id}", response_model=models.Articles)
def get_article(id: str, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if db_article:
        return db_article
    raise HTTPException(status_code=404, detail="Article not found.")

@app.post("/articles", status_code=201)
def add_article(article: models.Articles, db: Session = Depends(get_db)):
    db_obj = database_models.Articles(**article.model_dump())
    db.add(db_obj)
    db.commit()
    return {"detail": "Article added successfully."}

@app.put("/articles/{id}")
def update_article(id: str, article: models.Articles, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found.")
    for key, value in article.model_dump().items():
        setattr(db_article, key, value)
    db.commit()
    return {"detail": "Article updated successfully."}

@app.delete("/articles/{id}")
def delete_article(id: str, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found.")
    db.delete(db_article)
    db.commit()
    return {"detail": "Article deleted successfully."}

# ---------------- CATEGORIES ----------------
@app.get("/categories", response_model=list[models.Categories])
def get_all_categories(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(database_models.Categories).limit(limit).offset(offset).all()

@app.post("/categories", status_code=201)
def add_category(category: models.Categories, db: Session = Depends(get_db)):
    db.add(database_models.Categories(**category.model_dump()))
    db.commit()
    return {"detail": "Category added successfully."}

@app.put("/categories/{id}")
def update_category(id: int, category: models.Categories, db: Session = Depends(get_db)):
    db_category = db.query(database_models.Categories).filter(database_models.Categories.category_id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found.")
    for key, value in category.model_dump().items():
        setattr(db_category, key, value)
    db.commit()
    return {"detail": "Category updated successfully."}

@app.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    db_category = db.query(database_models.Categories).filter(database_models.Categories.category_id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found.")
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted successfully."}

# ---------------- CUSTOMERS ----------------
@app.get("/customers", response_model=list[models.Customers])
def get_all_customers(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(database_models.Customers).limit(limit).offset(offset).all()


@app.get("/customers/{id}", response_model=models.Customers)
def get_customer(id: str, db: Session = Depends(get_db)):
    customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer

@app.post("/customers", status_code=201)
def add_customer(customer: models.Customers, db: Session = Depends(get_db)):
    db.add(database_models.Customers(**customer.model_dump()))
    db.commit()
    return {"detail": "Customer added successfully."}

@app.put("/customers/{id}")
def update_customer(id: str, customer: models.Customers, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    for key, value in customer.model_dump().items():
        setattr(db_customer, key, value)
    db.commit()
    return {"detail": "Customer updated successfully."}

@app.delete("/customers/{id}")
def delete_customer(id: str, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    db.delete(db_customer)
    db.commit()
    return {"detail": "Customer deleted successfully."}

# ---------------- EVENTS ----------------
@app.get("/events", response_model=list[models.Events])
def get_all_events(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(database_models.Events).limit(limit).offset(offset).all()

@app.post("/events", status_code=201)
def add_event(event: models.Events, db: Session = Depends(get_db)):
    db.add(database_models.Events(**event.model_dump()))
    db.commit()
    return {"detail": "Event added successfully."}

@app.put("/events/{id}")
def update_event(id: int, event: models.Events, db: Session = Depends(get_db)):
    db_event = db.query(database_models.Events).filter(database_models.Events.event_id == id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found.")
    for key, value in event.model_dump().items():
        setattr(db_event, key, value)
    db.commit()
    return {"detail": "Event updated successfully."}

@app.delete("/events/{id}")
def delete_event(id: int, db: Session = Depends(get_db)):
    db_event = db.query(database_models.Events).filter(database_models.Events.event_id == id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found.")
    db.delete(db_event)
    db.commit()
    return {"detail": "Event deleted successfully."}

# ---------------- ORDERS ----------------
@app.get("/orders", response_model=list[models.Orders])
def get_all_orders(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(database_models.Orders).limit(limit).offset(offset).all()

@app.post("/orders", status_code=201)
def add_order(order: models.Orders, db: Session = Depends(get_db)):
    db.add(database_models.Orders(**order.model_dump()))
    db.commit()
    return {"detail": "Order added successfully."}

@app.put("/orders/{id}")
def update_order(id: int, order: models.Orders, db: Session = Depends(get_db)):
    db_order = db.query(database_models.Orders).filter(database_models.Orders.order_id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found.")
    for key, value in order.model_dump().items():
        setattr(db_order, key, value)
    db.commit()
    return {"detail": "Order updated successfully."}

@app.delete("/orders/{id}")
def delete_order(id: int, db: Session = Depends(get_db)):
    db_order = db.query(database_models.Orders).filter(database_models.Orders.order_id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found.")
    db.delete(db_order)
    db.commit()
    return {"detail": "Order deleted successfully."}

# ---------------- ORDER ITEMS ----------------
@app.get("/order_items", response_model=list[models.OrderItems])
def get_all_order_items(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(database_models.OrderItems).limit(limit).offset(offset).all()

@app.post("/order_items", status_code=201)
def add_order_item(order_item: models.OrderItems, db: Session = Depends(get_db)):
    db.add(database_models.OrderItems(**order_item.model_dump()))
    db.commit()
    return {"detail": "Order item added successfully."}

@app.put("/order_items/{id}")
def update_order_item(id: int, order_item: models.OrderItems, db: Session = Depends(get_db)):
    db_item = db.query(database_models.OrderItems).filter(database_models.OrderItems.order_item_id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found.")
    for key, value in order_item.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    return {"detail": "Order item updated successfully."}

@app.delete("/order_items/{id}")
def delete_order_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(database_models.OrderItems).filter(database_models.OrderItems.order_item_id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found.")
    db.delete(db_item)
    db.commit()
    return {"detail": "Order item deleted successfully."}

# ---------------- REVIEWS ----------------
@app.get("/reviews", response_model=list[models.Reviews])
def get_all_reviews(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(database_models.Reviews).limit(limit).offset(offset).all()

@app.post("/reviews", status_code=201)
def add_review(review: models.Reviews, db: Session = Depends(get_db)):
    db.add(database_models.Reviews(**review.model_dump()))
    db.commit()
    return {"detail": "Review added successfully."}

@app.put("/reviews/{id}")
def update_review(id: int, review: models.Reviews, db: Session = Depends(get_db)):
    db_review = db.query(database_models.Reviews).filter(database_models.Reviews.review_id == id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found.")
    for key, value in review.model_dump().items():
        setattr(db_review, key, value)
    db.commit()
    return {"detail": "Review updated successfully."}

@app.delete("/reviews/{id}")
def delete_review(id: int, db: Session = Depends(get_db)):
    db_review = db.query(database_models.Reviews).filter(database_models.Reviews.review_id == id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found.")
    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted successfully."}

# ---------------- TRANSACTIONS ----------------
@app.get("/transactions", response_model=list[models.Transactions])
def get_all_transactions(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    return db.query(database_models.Transactions).limit(limit).offset(offset).all()

@app.post("/transactions", status_code=201)
def add_transaction(transaction: models.Transactions, db: Session = Depends(get_db)):
    db.add(database_models.Transactions(**transaction.model_dump()))
    db.commit()
    return {"detail": "Transaction added successfully."}

@app.put("/transactions/{id}")
def update_transaction(id: int, transaction: models.Transactions, db: Session = Depends(get_db)):
    db_transaction = db.query(database_models.Transactions).filter(database_models.Transactions.transaction_id == id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    for key, value in transaction.model_dump().items():
        setattr(db_transaction, key, value)
    db.commit()
    return {"detail": "Transaction updated successfully."}

@app.delete("/transactions/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(database_models.Transactions).filter(database_models.Transactions.transaction_id == id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")
    db.delete(db_transaction)
    db.commit()
    return {"detail": "Transaction deleted successfully."}
