SELECT *
FROM analytics.powerbi_product_kpi_overview;

SELECT
    category,
    subcategory,
    total_products,
    total_brands,
    avg_price,
    avg_rating,
    total_reviews,
    total_stock,
    inventory_value
FROM analytics.powerbi_product_category_summary
ORDER BY total_products DESC;

SELECT
    brand,
    category,
    total_products,
    avg_price,
    avg_rating,
    total_reviews,
    total_stock,
    inventory_value
FROM analytics.powerbi_product_brand_summary
ORDER BY total_products DESC;

SELECT
    stock_status,
    category,
    total_products,
    avg_price,
    total_stock,
    inventory_value
FROM analytics.powerbi_product_stock_summary
ORDER BY stock_status, total_products DESC;

SELECT
    added_month,
    category,
    products_added,
    avg_price,
    total_stock
FROM analytics.powerbi_product_timeline
ORDER BY added_month, category;
