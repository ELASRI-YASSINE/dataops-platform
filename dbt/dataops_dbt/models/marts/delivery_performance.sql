{{ config(materialized='table') }}

SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id)   AS total_orders,

    ROUND(AVG(DATE_DIFF(
        DATE(o.order_delivered_customer_date),
        DATE(o.order_purchase_timestamp),
        DAY
    )), 1) AS avg_delivery_days,

    COUNTIF(
        o.order_delivered_customer_date > o.order_estimated_delivery_date
    ) AS late_deliveries,

    ROUND(COUNTIF(
        o.order_delivered_customer_date > o.order_estimated_delivery_date
    ) * 100.0 / COUNT(o.order_id), 1) AS late_rate_pct,

    ROUND(AVG(SAFE_CAST(r.review_score AS FLOAT64)), 2) AS avg_satisfaction

FROM {{ source('bronze', 'bronze_orders') }} o
LEFT JOIN {{ source('bronze', 'bronze_customers') }} c
    ON o.customer_id = c.customer_id
LEFT JOIN {{ source('bronze', 'bronze_reviews') }} r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL

GROUP BY c.customer_state
ORDER BY total_orders DESC
