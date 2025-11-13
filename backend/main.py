from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Session, engine
import database_models
import models

app = FastAPI()



# Allow React frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create tables
# database_models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        
from sqlalchemy import text

@app.get("/testdb")
def test_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT COUNT(*) FROM articles;")).scalar()
        return {"status": "ok", "articles_count": result}
    except Exception as e:
        return {"error": str(e)}



@app.get("/")
def greet():
    return "Welcome to ML-DB FastAPI backend!"


# ======================================================
# --------------------- ARTICLES -----------------------
# ======================================================
@app.get("/articles", response_model=list[models.Articles])
def get_all_articles(db: Session = Depends(get_db)):
    return db.query(database_models.Articles).all()

# @app.get("/articles")
# def get_all_articles(db: Session = Depends(get_db)):
#     try:
#         # limit for testing
#         articles = db.query(database_models.Articles).limit(5).all()
#         print("✅ Successfully fetched:", len(articles), "articles")
#         return articles
#     except Exception as e:
#         print("❌ ERROR in /articles:", e)
#         return {"error": str(e)}


@app.get("/articles/{id}",response_model=list[models.Articles])
def get_article(id: int, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if db_article:
        return db_article
    return "Article not found."


@app.post("/articles")
def add_article(article: models.Articles, db: Session = Depends(get_db)):
    db.add(database_models.Articles(**article.model_dump()))
    db.commit()
    return "Article added successfully."


@app.put("/articles/{id}")
def update_article(id: int, article: models.Articles, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if db_article:
        for key, value in article.model_dump().items():
            setattr(db_article, key, value)
        db.commit()
        return "Article updated successfully."
    return "Article not found."


@app.delete("/articles/{id}")
def delete_article(id: int, db: Session = Depends(get_db)):
    db_article = db.query(database_models.Articles).filter(database_models.Articles.article_id == id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
        return "Article deleted successfully."
    return "Article not found."


# ======================================================
# -------------------- CATEGORIES ----------------------
# ======================================================
@app.get("/test_categories")
def test_categories(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT COUNT(*) FROM categories;")).scalar()
    return {"category_count": result}

@app.get("/categories", response_model=list[models.Categories])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(database_models.Categories).all()


@app.post("/categories")
def add_category(category: models.Categories, db: Session = Depends(get_db)):
    db.add(database_models.Categories(**category.model_dump()))
    db.commit()
    return "Category added successfully."


@app.put("/categories/{id}")
def update_category(id: int, category: models.Categories, db: Session = Depends(get_db)):
    db_category = db.query(database_models.Categories).filter(database_models.Categories.category_id == id).first()
    if db_category:
        for key, value in category.model_dump().items():
            setattr(db_category, key, value)
        db.commit()
        return "Category updated successfully."
    return "Category not found."


@app.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):
    db_category = db.query(database_models.Categories).filter(database_models.Categories.category_id == id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return "Category deleted successfully."
    return "Category not found."


# ======================================================
# -------------------- CUSTOMERS -----------------------
# ======================================================
@app.get("/customers", response_model=list[models.Customers])
def get_all_customers(db: Session = Depends(get_db)):
    return db.query(database_models.Customers).all()


@app.get("/customers/{id}", response_model=list[models.Customers])
def get_customer(id: str, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if db_customer:
        return db_customer
    return "Customer not found."


@app.post("/customers")
def add_customer(customer: models.Customers, db: Session = Depends(get_db)):
    db.add(database_models.Customers(**customer.model_dump()))
    db.commit()
    return "Customer added successfully."


@app.put("/customers/{id}")
def update_customer(id: str, customer: models.Customers, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if db_customer:
        for key, value in customer.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        return "Customer updated successfully."
    return "Customer not found."


@app.delete("/customers/{id}")
def delete_customer(id: str, db: Session = Depends(get_db)):
    db_customer = db.query(database_models.Customers).filter(database_models.Customers.customer_id == id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return "Customer deleted successfully."
    return "Customer not found."


# ======================================================
# ---------------------- EVENTS ------------------------
# ======================================================
@app.get("/events", response_model=list[models.Events])
def get_all_events(db: Session = Depends(get_db)):
    return db.query(database_models.Events).all()


@app.post("/events")
def add_event(event: models.Events, db: Session = Depends(get_db)):
    db.add(database_models.Events(**event.model_dump()))
    db.commit()
    return "Event added successfully."


@app.put("/events/{id}")
def update_event(id: int, event: models.Events, db: Session = Depends(get_db)):
    db_event = db.query(database_models.Events).filter(database_models.Events.event_id == id).first()
    if db_event:
        for key, value in event.model_dump().items():
            setattr(db_event, key, value)
        db.commit()
        return "Event updated successfully."
    return "Event not found."


@app.delete("/events/{id}")
def delete_event(id: int, db: Session = Depends(get_db)):
    db_event = db.query(database_models.Events).filter(database_models.Events.event_id == id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return "Event deleted successfully."
    return "Event not found."


# ======================================================
# ---------------------- ORDERS ------------------------
# ======================================================
@app.get("/orders", response_model=list[models.Orders])
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(database_models.Orders).all()


@app.post("/orders")
def add_order(order: models.Orders, db: Session = Depends(get_db)):
    db.add(database_models.Orders(**order.model_dump()))
    db.commit()
    return "Order added successfully."


@app.put("/orders/{id}")
def update_order(id: int, order: models.Orders, db: Session = Depends(get_db)):
    db_order = db.query(database_models.Orders).filter(database_models.Orders.order_id == id).first()
    if db_order:
        for key, value in order.model_dump().items():
            setattr(db_order, key, value)
        db.commit()
        return "Order updated successfully."
    return "Order not found."


@app.delete("/orders/{id}")
def delete_order(id: int, db: Session = Depends(get_db)):
    db_order = db.query(database_models.Orders).filter(database_models.Orders.order_id == id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
        return "Order deleted successfully."
    return "Order not found."


# ======================================================
# ------------------- ORDER ITEMS ----------------------
# ======================================================
@app.get("/order_items", response_model=list[models.OrderItems])
def get_all_order_items(db: Session = Depends(get_db)):
    return db.query(database_models.OrderItems).all()


@app.post("/order_items")
def add_order_item(order_item: models.OrderItems, db: Session = Depends(get_db)):
    db.add(database_models.OrderItems(**order_item.model_dump()))
    db.commit()
    return "Order item added successfully."


@app.put("/order_items/{id}")
def update_order_item(id: int, order_item: models.OrderItems, db: Session = Depends(get_db)):
    db_item = db.query(database_models.OrderItems).filter(database_models.OrderItems.order_item_id == id).first()
    if db_item:
        for key, value in order_item.model_dump().items():
            setattr(db_item, key, value)
        db.commit()
        return "Order item updated successfully."
    return "Order item not found."


@app.delete("/order_items/{id}")
def delete_order_item(id: int, db: Session = Depends(get_db)):
    db_item = db.query(database_models.OrderItems).filter(database_models.OrderItems.order_item_id == id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return "Order item deleted successfully."
    return "Order item not found."


# ======================================================
# ---------------------- REVIEWS -----------------------
# ======================================================
@app.get("/reviews", response_model=list[models.Reviews])
def get_all_reviews(db: Session = Depends(get_db)):
    return db.query(database_models.Reviews).all()


@app.post("/reviews")
def add_review(review: models.Reviews, db: Session = Depends(get_db)):
    db.add(database_models.Reviews(**review.model_dump()))
    db.commit()
    return "Review added successfully."


@app.put("/reviews/{id}")
def update_review(id: int, review: models.Reviews, db: Session = Depends(get_db)):
    db_review = db.query(database_models.Reviews).filter(database_models.Reviews.review_id == id).first()
    if db_review:
        for key, value in review.model_dump().items():
            setattr(db_review, key, value)
        db.commit()
        return "Review updated successfully."
    return "Review not found."


@app.delete("/reviews/{id}")
def delete_review(id: int, db: Session = Depends(get_db)):
    db_review = db.query(database_models.Reviews).filter(database_models.Reviews.review_id == id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return "Review deleted successfully."
    return "Review not found."


# ======================================================
# ------------------- TRANSACTIONS ---------------------
# ======================================================
@app.get("/transactions", response_model=list[models.Transactions])
def get_all_transactions(db: Session = Depends(get_db)):
    return db.query(database_models.Transactions).all()


@app.post("/transactions")
def add_transaction(transaction: models.Transactions, db: Session = Depends(get_db)):
    db.add(database_models.Transactions(**transaction.model_dump()))
    db.commit()
    return "Transaction added successfully."


@app.put("/transactions/{id}")
def update_transaction(id: int, transaction: models.Transactions, db: Session = Depends(get_db)):
    db_transaction = db.query(database_models.Transactions).filter(database_models.Transactions.transaction_id == id).first()
    if db_transaction:
        for key, value in transaction.model_dump().items():
            setattr(db_transaction, key, value)
        db.commit()
        return "Transaction updated successfully."
    return "Transaction not found."


@app.delete("/transactions/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(database_models.Transactions).filter(database_models.Transactions.transaction_id == id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return "Transaction deleted successfully."
    return "Transaction not found."

