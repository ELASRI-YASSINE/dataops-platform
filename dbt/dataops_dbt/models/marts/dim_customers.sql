{{ config(materialized='table') }}

SELECT
    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    c.customer_zip_code_prefix,
    COUNT(DISTINCT o.order_id)                        AS total_orders,
    SUM(SAFE_CAST(i.price AS FLOAT64))                AS total_spent,
    ROUND(AVG(SAFE_CAST(r.review_score AS FLOAT64)), 2) AS avg_review_score,
    MAX(o.order_purchase_timestamp)                   AS last_order_date,
    MIN(o.order_purchase_timestamp)                   AS first_order_date

FROM {{ source('bronze', 'bronze_customers') }} c
LEFT JOIN {{ source('bronze', 'bronze_orders') }}      o ON c.customer_id = o.customer_id
LEFT JOIN {{ source('bronze', 'bronze_order_items') }} i ON o.order_id    = i.order_id
LEFT JOIN {{ source('bronze', 'bronze_reviews') }}     r ON o.order_id    = r.order_id

GROUP BY
    c.customer_id, c.customer_unique_id,
    c.customer_city, c.customer_state,
    c.customer_zip_code_prefix
