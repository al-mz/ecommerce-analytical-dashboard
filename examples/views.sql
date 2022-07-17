DROP VIEW IF EXISTS dbview_schema.cleaned_sales_data CASCADE; -- cleaned sales data
CREATE MATERIALIZED VIEW dbview_schema.cleaned_sales_data AS
    SELECT olist_orders_dataset.order_id, order_purchase_timestamp, payment_value, product_category_name, customer_city
        FROM olist_order_payments_dataset
        JOIN olist_orders_dataset on olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
        JOIN olist_order_items_dataset on olist_order_items_dataset.order_id = olist_order_payments_dataset.order_id
        JOIN olist_products_dataset on olist_products_dataset.product_id = olist_order_items_dataset.product_id
        JOIN olist_customers_dataset on olist_customers_dataset.customer_id = olist_orders_dataset.customer_id
        WHERE order_status = 'delivered'
        ORDER BY order_purchase_timestamp;

DROP VIEW IF EXISTS dbview_schema.geolocation CASCADE; -- geolocation data
CREATE MATERIALIZED VIEW dbview_schema.geolocation AS
    SELECT olist_orders_dataset.order_id, order_purchase_timestamp, customer_city, CAST(geolocation_lat as REAL), CAST(geolocation_lng as REAl)
        FROM olist_orders_dataset
        JOIN olist_customers_dataset on olist_customers_dataset.customer_id = olist_orders_dataset.customer_id
        JOIN olist_geolocation_dataset on olist_customers_dataset.customer_zip_code_prefix = olist_geolocation_dataset.geolocation_zip_code_prefix
        WHERE order_status = 'delivered'
        ORDER BY order_purchase_timestamp;

DROP VIEW IF EXISTS dbview_schema.customer_purchase_trend CASCADE; -- customer purchase trend
CREATE VIEW dbview_schema.customer_purchase_trend AS
select
month,
sum(case when a.year= '2016' then 1 else 0 end) as Year2016,
sum(case when a.year= '2017' then 1 else 0 end) as Year2017,
sum(case when a.year= '2018' then 1 else 0 end) as Year2018
from
(select 
customer_id,
order_id,
order_delivered_customer_date,
order_purchase_year as Year,
order_purchase_month_name as month,
order_purchase_month as month_no
from olist_orders_dataset
where order_status= 'delivered' and order_delivered_customer_date is not null
group by Year, month, month_no, customer_id,order_id,order_delivered_customer_date
order by order_delivered_customer_date asc) a
group by month, month_no
order by month_no asc