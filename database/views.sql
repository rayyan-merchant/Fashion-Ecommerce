-- customer features
CREATE OR REPLACE VIEW niche_data.customer_features AS
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.gender,
    c.age,
    c.active,
    COUNT(DISTINCT e.article_id) AS unique_products_interacted,
    COUNT(*) FILTER (WHERE e.event_type = 'view') AS total_views,
    COUNT(*) FILTER (WHERE e.event_type = 'click') AS total_clicks,
    COUNT(*) FILTER (WHERE e.event_type = 'wishlist') AS total_wishlist,
    COUNT(*) FILTER (WHERE e.event_type = 'add_to_cart') AS total_cart_adds,
    COUNT(*) FILTER (WHERE e.event_type = 'purchase') AS total_purchases,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    MAX(o.order_date) AS last_purchase_date,
    COUNT(DISTINCT r.review_id) AS total_reviews,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM niche_data.customers c
LEFT JOIN niche_data.events e USING(customer_id)
LEFT JOIN niche_data.orders o USING(customer_id)
LEFT JOIN niche_data.reviews r USING(customer_id)
GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.gender, c.age, c.active;



-- product performance
CREATE OR REPLACE VIEW niche_data.product_performance AS
SELECT 
    a.article_id,
    a.prod_name,
    a.product_type_name,
    a.product_group_name,
    a.section_name,
    a.colour_group_name,
    ROUND(a.price, 2) AS price,
    SUM(CASE WHEN e.event_type = 'view' THEN 1 ELSE 0 END) AS total_views,
    SUM(CASE WHEN e.event_type = 'click' THEN 1 ELSE 0 END) AS total_clicks,
    SUM(CASE WHEN e.event_type = 'wishlist' THEN 1 ELSE 0 END) AS total_wishlist,
    SUM(CASE WHEN e.event_type = 'add_to_cart' THEN 1 ELSE 0 END) AS total_cart_adds,
    SUM(CASE WHEN e.event_type = 'purchase' THEN 1 ELSE 0 END) AS total_purchases,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.review_id) AS total_reviews,
    COALESCE(SUM(o_i.line_total), 0) AS total_revenue
FROM niche_data.articles a
LEFT JOIN niche_data.events e USING(article_id)
LEFT JOIN niche_data.reviews r USING(article_id)
LEFT JOIN niche_data.order_items o_i USING(article_id)
GROUP BY a.article_id, a.prod_name, a.product_type_name, a.product_group_name, a.section_name, a.colour_group_name, a.price;



-- Category Sales Summary View
CREATE OR REPLACE VIEW niche_data.category_sales_summary AS
SELECT 
    c.category_id,
    c.name AS category_name,
    COUNT(DISTINCT a.article_id) AS total_articles,
    COUNT(DISTINCT oi.order_item_id) AS total_items_sold,
    ROUND(SUM(oi.line_total), 2) AS total_revenue,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM niche_data.categories c
LEFT JOIN niche_data.articles a USING(category_id)
LEFT JOIN niche_data.order_items oi USING(article_id)
LEFT JOIN niche_data.reviews r USING(article_id)
GROUP BY c.category_id, c.name;


-- Monthly Sales Summary View
CREATE OR REPLACE VIEW niche_data.monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', o.order_date) AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(SUM(o.total_amount), 2) AS total_revenue,
    ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM niche_data.orders o
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;


-- Funnel Metrics View
CREATE OR REPLACE VIEW niche_data.funnel_metrics AS
WITH stage_counts AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_type = 'view' THEN customer_id || '-' || article_id END) AS views,
        COUNT(DISTINCT CASE WHEN event_type = 'click' THEN customer_id || '-' || article_id END) AS clicks,
        COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN customer_id || '-' || article_id END) AS cart_adds,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN customer_id || '-' || article_id END) AS purchases
    FROM niche_data.events
)
SELECT 
    views,
    clicks,
    cart_adds,
    purchases,
    ROUND(100.0 * clicks / views, 2) AS view_to_click_rate,
    ROUND(100.0 * cart_adds / clicks, 2) AS click_to_cart_rate,
    ROUND(100.0 * purchases / cart_adds, 2) AS cart_to_purchase_rate
FROM stage_counts;



SELECT * FROM niche_data.customer_features LIMIT 5;
SELECT * FROM niche_data.product_performance ORDER BY total_purchases DESC LIMIT 5;
SELECT * FROM niche_data.category_sales_summary ORDER BY total_revenue DESC LIMIT 5;
SELECT * FROM niche_data.monthly_sales_summary;
SELECT * FROM niche_data.funnel_metrics;



SELECT pg_size_pretty(pg_total_relation_size('niche_data.product_performance'));
SELECT pg_size_pretty(pg_total_relation_size('niche_data.category_sales_summary'));

SET work_mem = '256MB';


-- Customer Lifetime Value: CLV View

CREATE MATERIALIZED VIEW niche_data.mv_customer_clv AS
SELECT 
    c.customer_id,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    AVG(o.total_amount) AS avg_order_value,
    MAX(o.order_date) AS last_order_date,
    MIN(o.order_date) AS first_order_date,
    (DATE(MAX(o.order_date)) - DATE(MIN(o.order_date))) AS customer_lifespan_days,
    c.loyalty_score
FROM niche_data.customers c
LEFT JOIN niche_data.orders o USING(customer_id)
GROUP BY c.customer_id;


CREATE INDEX idx_mv_customer_clv_customer_id
ON niche_data.mv_customer_clv(customer_id);



-- Customer Purchase Frequency View: This shows purchases per month per customer.

CREATE OR REPLACE VIEW niche_data.v_customer_purchase_frequency AS
SELECT 
    customer_id,
    COUNT(order_id) AS total_orders,
    DATE_TRUNC('month', MIN(order_date)) AS first_month,
    DATE_TRUNC('month', MAX(order_date)) AS last_month,
    COUNT(order_id) / 
        NULLIF(EXTRACT(MONTH FROM AGE(MAX(order_date), MIN(order_date))) + 1, 0)
        AS avg_orders_per_month
FROM niche_data.orders
GROUP BY customer_id;



-- RFM Segmentation View (R = Recency, F = Frequency, M = Monetary)

CREATE MATERIALIZED VIEW niche_data.mv_rfm AS
WITH base AS (
    SELECT 
        o.customer_id,
        MAX(o.order_date) AS last_purchase_date,
        COUNT(o.order_id) AS frequency,
        SUM(o.total_amount) AS monetary
    FROM niche_data.orders o
    GROUP BY o.customer_id
)
SELECT 
    customer_id,
    (CURRENT_DATE - DATE(last_purchase_date)) AS recency_days,
    frequency,
    monetary,
    NTILE(4) OVER (ORDER BY (CURRENT_DATE - DATE(last_purchase_date))) AS r_score,
    NTILE(4) OVER (ORDER BY frequency) AS f_score,
    NTILE(4) OVER (ORDER BY monetary) AS m_score
FROM base;



-- Product Demand Trend View: Shows weekly/monthly demand from orders.

CREATE MATERIALIZED VIEW niche_data.mv_product_demand AS
SELECT 
    oi.article_id,
    DATE_TRUNC('month', o.order_date) AS month,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.line_total) AS total_revenue
FROM niche_data.order_items oi
JOIN niche_data.orders o ON oi.order_id = o.order_id
GROUP BY 1, 2
ORDER BY 1, 2;

CREATE INDEX idx_mv_product_demand_article_month
ON niche_data.mv_product_demand(article_id, month);



-- Article Inventory Status View: Shows availability, stock levels, restock flags.
CREATE OR REPLACE VIEW niche_data.v_article_inventory AS
SELECT 
    article_id,
    prod_name,
    stock,
    CASE 
        WHEN stock = 0 THEN 'Out of Stock'
        WHEN stock < 5 THEN 'Low Stock'
        ELSE 'In Stock'
    END AS stock_status
FROM niche_data.articles;




-- Daily Sales View

CREATE MATERIALIZED VIEW niche_data.mv_daily_sales AS
SELECT 
    DATE(order_date) AS day,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM niche_data.orders
GROUP BY 1;

CREATE INDEX idx_mv_daily_sales_day ON niche_data.mv_daily_sales(day);


--Monthly Sales View

CREATE MATERIALIZED VIEW niche_data.mv_monthly_sales AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM niche_data.orders
GROUP BY 1;

CREATE INDEX idx_mv_monthly_sales_month ON niche_data.mv_monthly_sales(month);

DROP MATERIALIZED VIEW IF EXISTS niche_data.mv_monthly_sales;
DROP INDEX IF EXISTS niche_data.mv_monthly_sales;


-- Funnel Conversion Metric: Shows product funnel performance: views → cart → wishlist → purchase.

CREATE MATERIALIZED VIEW niche_data.mv_funnel AS
SELECT 
    a.article_id,
    COUNT(*) FILTER (WHERE e.event_type='view') AS views,
    COUNT(*) FILTER (WHERE e.event_type='add_to_cart') AS add_to_cart,
    COUNT(*) FILTER (WHERE e.event_type='wishlist') AS wishlist,
    COUNT(oi.order_item_id) AS purchases
FROM niche_data.articles a
LEFT JOIN niche_data.events e ON a.article_id = e.article_id
LEFT JOIN niche_data.order_items oi ON a.article_id = oi.article_id
GROUP BY a.article_id;

