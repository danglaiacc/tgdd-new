

## Query for data from postgreSQL
- invoice: `select id, customer_id, time_invoice, branch_id from invoice`
- invoice_detail: `select invoice_id, product_id, quantity, product_price from invoice_detail`
- product:
```
select p.id product_id, p."name" product_name, s."name" series_name, m."name" manu_name
from product p join series s on p.series_id = s.id
join manufacturer m on s.manu_id = m.id
```

