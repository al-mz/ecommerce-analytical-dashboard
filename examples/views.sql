DROP VIEW IF EXISTS dbview_schema.cleaned_sales_data CASCADE; -- cleaned sales data
CREATE MATERIALIZED VIEW dbview_schema.cleaned_sales_data AS
    SELECT olist_orders_dataset.order_id, 
    order_purchase_timestamp, 
    payment_value, 
    product_category_name, 
    customer_city, 
    EXTRACT(YEAR from order_purchase_timestamp) as year
    FROM olist_order_payments_dataset
    JOIN olist_orders_dataset ON olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
    JOIN olist_order_items_dataset ON olist_order_items_dataset.order_id = olist_order_payments_dataset.order_id
    JOIN olist_products_dataset ON olist_products_dataset.product_id = olist_order_items_dataset.product_id
    JOIN olist_customers_dataset ON olist_customers_dataset.customer_id = olist_orders_dataset.customer_id
    WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL
    ORDER BY order_purchase_timestamp;

DROP VIEW IF EXISTS dbview_schema.customer_purchase_trend CASCADE; -- customer purchase trend
CREATE VIEW dbview_schema.customer_purchase_trend AS
select 
count(payment_value) as total_purchases,
sum(payment_value) as total_revenue,
year,
to_char(order_purchase_timestamp, 'Month') as month,
CAST(to_char(order_purchase_timestamp, 'MM') as INT) as month_no
from dbview_schema.cleaned_sales_data
group by year, month, month_no;


DROP VIEW IF EXISTS dbview_schema.geolocation CASCADE; -- geolocation data
CREATE MATERIALIZED VIEW dbview_schema.geolocation AS
    SELECT
    SUM(payment_value) as total_payment, 
    ROUND(CAST(geolocation_lat as NUMERIC), 2) geolocation_lat, 
    ROUND(CAST(geolocation_lng as NUMERIC), 2) as geolocation_lng,
    AVG(review_score) review_score,
    customer_city
    FROM olist_order_payments_dataset
    JOIN olist_orders_dataset ON olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
    JOIN olist_customers_dataset ON olist_customers_dataset.customer_id = olist_orders_dataset.customer_id
    JOIN olist_geolocation_dataset on olist_customers_dataset.customer_zip_code_prefix = olist_geolocation_dataset.geolocation_zip_code_prefix
    JOIN olist_order_reviews_dataset ON olist_orders_dataset.order_id = olist_order_reviews_dataset.order_id
    WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL
    GROUP BY geolocation_lat, geolocation_lng, customer_city