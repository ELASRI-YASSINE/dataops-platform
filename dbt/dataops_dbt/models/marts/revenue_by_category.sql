{{ config(materialized='table') }}

SELECT
    p.product_category_name,
    COUNT(DISTINCT o.order_id)                           AS total_orders,
    COUNT(DISTINCT i.seller_id)                          AS total_sellers,
    ROUND(SUM(SAFE_CAST(i.price AS FLOAT64)), 2)         AS total_revenue,
    ROUND(AVG(SAFE_CAST(i.price AS FLOAT64)), 2)         AS avg_price,
    ROUND(SUM(SAFE_CAST(i.freight_value AS FLOAT64)), 2) AS total_freight,
    ROUND(AVG(SAFE_CAST(r.review_score AS FLOAT64)), 2)  AS avg_satisfaction,
    ROUND(SUM(SAFE_CAST(i.price AS FLOAT64)) * 100.0 /
        SUM(SUM(SAFE_CAST(i.price AS FLOAT64))) OVER(), 2) AS revenue_share_pct

FROM {{ source('bronze', 'bronze_order_items') }} i
LEFT JOIN {{ source('bronze', 'bronze_products') }} p ON i.product_id = p.product_id
LEFT JOIN {{ source('bronze', 'bronze_orders') }}   o ON i.order_id   = o.order_id
LEFT JOIN {{ source('bronze', 'bronze_reviews') }}  r ON o.order_id   = r.order_id

WHERE o.order_status = 'delivered'

GROUP BY p.product_category_name
ORDER BY total_revenue DESC
