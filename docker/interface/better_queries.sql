SELECT order_id, ROUND(cast(AVG(sales) as numeric), 2)
FROM orders
GROUP BY order_id;

SELECT ROUND(CAST(AVG(sales) as numeric), 2)
FROM orders
GROUP BY EXTRACT(month from order_date);