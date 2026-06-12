CREATE SCHEMA IF NOT EXISTS hive.raw
WITH (location = 's3a://warehouse/raw/');

DROP TABLE IF EXISTS hive.raw.people_csv;

CREATE TABLE hive.raw.people_csv
(
    id varchar,
    name varchar,
    age varchar
)
WITH (
    external_location = 's3a://warehouse/raw/people/',
    format = 'CSV',
    csv_separator = ',',
    csv_quote = '"',
    csv_escape = '"',
    skip_header_line_count = 1
);

DROP TABLE IF EXISTS hive.raw.sales_csv;

CREATE TABLE hive.raw.sales_csv
(
    sale_date varchar,
    sku varchar,
    channel varchar,
    city varchar,
    payment_method varchar,
    return_flag varchar,
    event_flag varchar,
    delivery_charges varchar
)
WITH (
    external_location = 's3a://warehouse/raw/sales/',
    format = 'CSV',
    csv_separator = ',',
    csv_quote = '"',
    csv_escape = '"',
    skip_header_line_count = 1
);

CREATE SCHEMA IF NOT EXISTS iceberg.lakehouse
WITH (location = 's3a://warehouse/iceberg/lakehouse/');

DROP TABLE IF EXISTS iceberg.lakehouse.people;

CREATE TABLE iceberg.lakehouse.people
WITH (format = 'PARQUET') AS
SELECT
    CAST(id AS integer) AS id,
    name,
    CAST(age AS integer) AS age
FROM hive.raw.people_csv;

DROP TABLE IF EXISTS iceberg.lakehouse.sales;

CREATE TABLE iceberg.lakehouse.sales
WITH (format = 'PARQUET') AS
SELECT
    CAST(sale_date AS date) AS sale_date,
    sku,
    channel,
    city,
    payment_method,
    CAST(return_flag AS integer) AS return_flag,
    CAST(event_flag AS integer) AS event_flag,
    CAST(delivery_charges AS integer) AS delivery_charges
FROM hive.raw.sales_csv;

DROP TABLE IF EXISTS iceberg.lakehouse.sales_partitioned;

CREATE TABLE iceberg.lakehouse.sales_partitioned
WITH (
    format = 'PARQUET',
    partitioning = ARRAY['city', 'channel']
) AS
SELECT
    CAST(sale_date AS date) AS sale_date,
    sku,
    channel,
    city,
    payment_method,
    CAST(return_flag AS integer) AS return_flag,
    CAST(event_flag AS integer) AS event_flag,
    CAST(delivery_charges AS integer) AS delivery_charges
FROM hive.raw.sales_csv;

DROP TABLE IF EXISTS iceberg.lakehouse.sales_city_summary;

CREATE TABLE iceberg.lakehouse.sales_city_summary
WITH (format = 'PARQUET') AS
SELECT
    city,
    channel,
    count(*) AS total_events,
    sum(return_flag) AS total_returns,
    sum(event_flag) AS total_flagged_events,
    sum(delivery_charges) AS total_delivery_charges
FROM iceberg.lakehouse.sales_partitioned
GROUP BY
    city,
    channel;
