SELECT ROUND(cast(AVG(sales) as numeric), 2)
FROM sales_data
GROUP BY order_id;

SELECT ROUND(cast(AVG(sales) as numeric), 2)
FROM sales_data
GROUP BY EXTRACT(month FROM order_date);