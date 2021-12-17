

## Query for data from postgreSQL
- invoice: `select id, customer_id, time_invoice, branch_id, pay from invoice`
- invoice_detail: `select invoice_id, product_id, quantity, product_price from invoice_detail`
- product: `select p.id, s.manu_id, m."name" from product p join series s on p.series_id=s."id" join manufacturer m on m.id = s.manu_id`

