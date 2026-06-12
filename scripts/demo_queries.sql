SHOW CATALOGS;

SHOW SCHEMAS FROM iceberg;

SHOW TABLES FROM iceberg.lakehouse;

SELECT count(*) AS total_sales_rows
FROM iceberg.lakehouse.sales_partitioned;

SELECT
    city,
    channel,
    total_events,
    total_returns,
    total_delivery_charges
FROM iceberg.lakehouse.sales_city_summary
ORDER BY total_events DESC
LIMIT 20;

SELECT *
FROM "iceberg"."lakehouse"."sales_partitioned$partitions";

SELECT count(*) AS total_products
FROM clickhouse.analytics.products;

SELECT *
FROM clickhouse.analytics.powerbi_product_kpi_overview;

SELECT
    category,
    subcategory,
    total_products,
    avg_price,
    avg_rating,
    inventory_value
FROM clickhouse.analytics.powerbi_product_category_summary
ORDER BY total_products DESC
LIMIT 20;
