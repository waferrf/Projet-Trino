CREATE DATABASE IF NOT EXISTS analytics;

DROP TABLE IF EXISTS analytics.people;
DROP TABLE IF EXISTS analytics.sales_interactions;
DROP TABLE IF EXISTS analytics.sales_kpi_by_city;

CREATE TABLE IF NOT EXISTS analytics.products
(
    product_id String,
    product_name String,
    product_description String,
    category String,
    subcategory String,
    brand String,
    price Float64,
    rating_avg Nullable(Float32),
    review_count UInt32,
    stock_quantity UInt32,
    date_added Date
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(date_added)
ORDER BY (category, subcategory, brand, product_id);

TRUNCATE TABLE analytics.products;

INSERT INTO analytics.products
SELECT
    product_id,
    product_name,
    product_description,
    category,
    subcategory,
    brand,
    toFloat64(price) AS price,
    toFloat32OrNull(nullIf(rating_avg, '')) AS rating_avg,
    toUInt32(review_count) AS review_count,
    toUInt32(stock_quantity) AS stock_quantity,
    toDate(date_added) AS date_added
FROM file(
    'products.csv',
    'CSVWithNames',
    'product_id String, product_name String, product_description String, category String, subcategory String, brand String, price String, rating_avg String, review_count String, stock_quantity String, date_added String'
);

DROP TABLE IF EXISTS analytics.powerbi_product_kpi_overview;

CREATE TABLE analytics.powerbi_product_kpi_overview
ENGINE = TinyLog
AS
SELECT
    count() AS total_products,
    uniqExact(category) AS total_categories,
    uniqExact(brand) AS total_brands,
    round(avg(price), 2) AS avg_price,
    round(avgIf(rating_avg, isNotNull(rating_avg)), 2) AS avg_rating,
    sum(review_count) AS total_reviews,
    sum(stock_quantity) AS total_stock,
    sum(price * stock_quantity) AS inventory_value
FROM analytics.products;

DROP TABLE IF EXISTS analytics.powerbi_product_category_summary;

CREATE TABLE analytics.powerbi_product_category_summary
ENGINE = MergeTree
ORDER BY (category, subcategory)
AS
SELECT
    category,
    subcategory,
    count() AS total_products,
    uniqExact(brand) AS total_brands,
    round(avg(price), 2) AS avg_price,
    round(avgIf(rating_avg, isNotNull(rating_avg)), 2) AS avg_rating,
    sum(review_count) AS total_reviews,
    sum(stock_quantity) AS total_stock,
    round(sum(price * stock_quantity), 2) AS inventory_value
FROM analytics.products
GROUP BY
    category,
    subcategory;

DROP TABLE IF EXISTS analytics.powerbi_product_brand_summary;

CREATE TABLE analytics.powerbi_product_brand_summary
ENGINE = MergeTree
ORDER BY (brand, category)
AS
SELECT
    brand,
    category,
    count() AS total_products,
    round(avg(price), 2) AS avg_price,
    round(avgIf(rating_avg, isNotNull(rating_avg)), 2) AS avg_rating,
    sum(review_count) AS total_reviews,
    sum(stock_quantity) AS total_stock,
    round(sum(price * stock_quantity), 2) AS inventory_value
FROM analytics.products
GROUP BY
    brand,
    category;

DROP TABLE IF EXISTS analytics.powerbi_product_stock_summary;

CREATE TABLE analytics.powerbi_product_stock_summary
ENGINE = MergeTree
ORDER BY (stock_status, category)
AS
SELECT
    multiIf(
        stock_quantity = 0, 'Out of stock',
        stock_quantity < 10, 'Low stock',
        stock_quantity < 50, 'Medium stock',
        'High stock'
    ) AS stock_status,
    category,
    count() AS total_products,
    round(avg(price), 2) AS avg_price,
    sum(stock_quantity) AS total_stock,
    round(sum(price * stock_quantity), 2) AS inventory_value
FROM analytics.products
GROUP BY
    stock_status,
    category;

DROP TABLE IF EXISTS analytics.powerbi_product_timeline;

CREATE TABLE analytics.powerbi_product_timeline
ENGINE = MergeTree
ORDER BY (added_month, category)
AS
SELECT
    toStartOfMonth(date_added) AS added_month,
    category,
    count() AS products_added,
    round(avg(price), 2) AS avg_price,
    sum(stock_quantity) AS total_stock
FROM analytics.products
GROUP BY
    added_month,
    category;
