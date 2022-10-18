WITH aggregation_ca as (
SELECT
  client_id,
  b.product_type,
  SUM(prod_price*prod_qty) AS ventes
FROM
  `transaction_table` as a 
LEFT JOIN 
 `products_table` as b
ON 
a.prod_id = b.product_id
WHERE
  date BETWEEN "2019-01-01"
  AND "2019-12-31"
GROUP BY
  client_id,
  product_type
)
SELECT * FROM
aggregation_ca
PIVOT(
  SUM(ventes) as ventes
  for product_type in ("MEUBLE", "DECO")
)