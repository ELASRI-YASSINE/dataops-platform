-- fact_orders.sql
-- Table de faits principale : jointure orders + items + payments + reviews

{{ config(materialized='table') }}

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    -- Métriques financières
    SUM(i.price)          AS total_price,
    SUM(i.freight_value)  AS total_freight,
    SUM(i.price + i.freight_value) AS total_revenue,
    COUNT(i.order_item_id) AS total_items,

    -- Paiement
    MAX(p.payment_type)   AS payment_type,
    MAX(p.payment_installments) AS payment_installments,

    -- Satisfaction
    MAX(r.review_score)   AS review_score,

    -- Délai de livraison
    DATE_DIFF(
        DATE(o.order_delivered_customer_date),
        DATE(o.order_purchase_timestamp),
        DAY
    ) AS delivery_days,

    -- Livraison en retard ?
    CASE
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date
        THEN TRUE ELSE FALSE
    END AS is_late_delivery

FROM {{ source('dataops_warehouse', 'bronze_orders') }} o
LEFT JOIN {{ source('dataops_warehouse', 'bronze_order_items') }} i
    ON o.order_id = i.order_id
LEFT JOIN {{ source('dataops_warehouse', 'bronze_payments') }} p
    ON o.order_id = p.order_id
LEFT JOIN {{ source('dataops_warehouse', 'bronze_reviews') }} r
    ON o.order_id = r.order_id

WHERE o.order_status = 'delivered'

GROUP BY
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date
