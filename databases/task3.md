1. Каждый месяц компания выдает премию в размере 5% от суммы продаж менеджеру, который за предыдущие 3 месяца продал товаров на самую большую сумму
   Выведите месяц, manager_id, manager_first_name, manager_last_name, премию за период с января по декабрь 2014 года

```sql
WITH month_sales AS
 (SELECT manager_id,
         manager_first_name,
         manager_last_name,
         DATE_TRUNC('month', sale_date) AS MONTH,
         SUM(sale_amount) AS total_sales
  FROM public.v_fact_sale
  WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
  GROUP BY manager_id,
           manager_first_name,
           manager_last_name,
           DATE_TRUNC('month', sale_date)),
     prev_3_months_sales AS
 (SELECT manager_id,
         manager_first_name,
         manager_last_name,
         MONTH,
         SUM(total_sales) OVER (PARTITION BY manager_id
                                ORDER BY MONTH ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS total_sales_3_months
  FROM month_sales),
     top_manager AS
 (SELECT MONTH,
         manager_id,
         manager_first_name,
         manager_last_name,
         total_sales_3_months,
         ROW_NUMBER() OVER (PARTITION BY MONTH
                            ORDER BY total_sales_3_months DESC) AS rn
  FROM prev_3_months_sales)
SELECT MONTH,
      manager_id,
      manager_first_name,
      manager_last_name,
      total_sales_3_months * 0.05 AS manager_bonus
FROM top_manager
WHERE rn = 1
ORDER BY MONTH;
```

2. Компания хочет оптимизировать количество офисов, проанализировав относительные объемы продаж по офисам в течение периода с 2013-2014 гг.
   Выведите год, office_id, city_name, country, относительный объем продаж за текущий год
   Офисы, которые демонстрируют наименьший относительной объем в течение двух лет скорее всего будут закрыты.

```sql
WITH year_sales AS
 (SELECT office_id,
         city_name,
         country,
         EXTRACT(YEAR
                 FROM sale_date) AS YEAR,
         SUM(sale_amount) AS total_sales
  FROM public.v_fact_sale
  WHERE sale_date BETWEEN TO_DATE('01-01-2013', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
  GROUP BY office_id,
           city_name,
           country,
           EXTRACT(YEAR
                   FROM sale_date)),
     total_sales_per_year AS
 (SELECT YEAR,
         SUM(total_sales) AS total_sales_year
  FROM year_sales
  GROUP BY YEAR)
SELECT ys.YEAR,
         ys.office_id,
         ys.city_name,
         ys.country,
         ys.total_sales / tspy.total_sales_year AS relative_sales
FROM year_sales ys
JOIN total_sales_per_year tspy ON ys.YEAR = tspy.YEAR
ORDER BY ys.YEAR,
           ys.office_id;
```

3. Для планирования закупок, компанию оценивает динамику роста продаж по товарам.
   Динамика оценивается как отношение объема продаж в текущем месяце к предыдущему.
   Выведите товары, которые демонстрировали наиболее высокие темпы роста продаж в течение первого полугодия 2014 года.

```sql
WITH month_sales AS
 (SELECT product_id,
         product_name,
         DATE_TRUNC('month', sale_date) AS MONTH,
         SUM(sale_amount) AS total_sales
  FROM public.v_fact_sale
  WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('30-06-2014', 'DD-MM-YYYY')
  GROUP BY product_id,
           product_name,
           DATE_TRUNC('month', sale_date)),
     sales_growth AS
 (SELECT product_id,
         product_name,
         MONTH,
         total_sales,
         LAG(total_sales) OVER (PARTITION BY product_id
                                ORDER BY MONTH) AS prev_total_sales
  FROM month_sales)
SELECT product_id,
      product_name,
      MONTH,
      total_sales / prev_total_sales AS growth_rate
FROM sales_growth
WHERE prev_total_sales IS NOT NULL
ORDER BY growth_rate DESC;
```

4. Напишите запрос, который выводит отчет о прибыли компании за 2014 год: помесячно и поквартально.
   Отчет включает сумму прибыли за период и накопительную сумму прибыли с начала года по текущий период.

```sql
WITH month_sales AS
 (SELECT DATE_TRUNC('month', sale_date) AS MONTH,
         SUM(sale_amount) AS total_sales
  FROM public.v_fact_sale
  WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
  GROUP BY DATE_TRUNC('month', sale_date)),
     quarter_sales AS
 (SELECT DATE_TRUNC('quarter', sale_date) AS quarter,
         SUM(sale_amount) AS total_sales
  FROM public.v_fact_sale
  WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
  GROUP BY DATE_TRUNC('quarter', sale_date)),
     cumulative_sales AS
 (SELECT MONTH,
         total_sales,
         SUM(total_sales) OVER (ORDER BY MONTH) AS cumulative_sales
  FROM month_sales)
SELECT MONTH,
      total_sales,
      cumulative_sales
FROM cumulative_sales
UNION ALL
SELECT quarter AS MONTH,
      total_sales,
      SUM(total_sales) OVER (
                             ORDER BY quarter) AS cumulative_sales
FROM quarter_sales
ORDER BY MONTH;
```

5. Найдите вклад в общую прибыль за 2014 год 10% наиболее дорогих товаров и 10% наиболее дешевых товаров.
   Выведите product_id, product_name, total_sale_amount, percent

```sql
WITH total_sales AS
  ( SELECT product_id,
           product_name,
           SUM(sale_amount) AS total_sale_amount
   FROM public.v_fact_sale
   WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
   GROUP BY product_id,
            product_name),
     ranked_products AS
  ( SELECT product_id,
           product_name,
           total_sale_amount,
           NTILE(10) OVER (
                           ORDER BY total_sale_amount DESC) AS decile
   FROM total_sales),
     top_10_percent AS
  ( SELECT product_id,
           product_name,
           total_sale_amount,
           'Top 10%' AS category
   FROM ranked_products
   WHERE decile = 1),
     bottom_10_percent AS
  ( SELECT product_id,
           product_name,
           total_sale_amount,
           'Bottom 10%' AS category
   FROM ranked_products
   WHERE decile = 10),
     combined_products AS
  ( SELECT *
   FROM top_10_percent
   UNION ALL SELECT *
   FROM bottom_10_percent)
SELECT product_id,
       product_name,
       total_sale_amount,
       (total_sale_amount / SUM(total_sale_amount) OVER ()) * 100 AS percent
FROM combined_products
ORDER BY category,
         total_sale_amount DESC;
```

6. Компания хочет премировать трех наиболее продуктивных (по объему продаж, конечно) менеджеров в каждой стране в 2014 году.
   Выведите country, <список manager_last_name manager_first_name, разделенный запятыми> которым будет выплачена премия

```sql
WITH manager_sales AS (
    SELECT
        manager_id,
        manager_first_name,
        manager_last_name,
        country,
        SUM(sale_amount) AS total_sales
    FROM public.v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
    GROUP BY manager_id, manager_first_name, manager_last_name, country
),
top_managers AS (
    SELECT
        country,
        STRING_AGG(manager_last_name || ' ' || manager_first_name, ', ') AS top_managers
    FROM (
        SELECT
            country,
            manager_last_name,
            manager_first_name,
            ROW_NUMBER() OVER (PARTITION BY country ORDER BY total_sales DESC) AS rn
        FROM manager_sales
    ) sub
    WHERE rn <= 3
    GROUP BY country
)
SELECT
    country,
    top_managers
FROM top_managers
ORDER BY country;
```

7. Выведите самый дешевый и самый дорогой товар, проданный за каждый месяц в течение 2014 года.
   cheapest_product_id, cheapest_product_name, expensive_product_id, expensive_product_name, month, cheapest_price, expensive_price

```sql
WITH month_prices AS (
    SELECT
        DATE_TRUNC('month', sale_date) AS month,
        MIN(sale_price) AS cheapest_price,
        MAX(sale_price) AS expensive_price
    FROM public.v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
    GROUP BY DATE_TRUNC('month', sale_date)
),
cheapest_products AS (
    SELECT
        month,
        product_id AS cheapest_product_id,
        product_name AS cheapest_product_name,
        sale_price AS cheapest_price
    FROM public.v_fact_sale
    JOIN month_prices ON DATE_TRUNC('month', sale_date) = month AND sale_price = cheapest_price
),
expensive_products AS (
    SELECT
        month,
        product_id AS expensive_product_id,
        product_name AS expensive_product_name,
        sale_price AS expensive_price
    FROM public.v_fact_sale
    JOIN month_prices ON DATE_TRUNC('month', sale_date) = month AND sale_price = expensive_price
)
SELECT
    c.month,
    c.cheapest_product_id,
    c.cheapest_product_name,
    e.expensive_product_id,
    e.expensive_product_name,
    c.cheapest_price,
    e.expensive_price
FROM cheapest_products c
JOIN expensive_products e ON c.month = e.month
ORDER BY c.month;
```

8. Менеджер получает оклад в 30 000 + 5% от суммы своих продаж в месяц. Средняя наценка стоимости товара - 10%
   Посчитайте прибыль предприятия за 2014 год по месяцам (сумма продаж - (исходная стоимость товаров + зарплата))
   month, sales_amount, salary_amount, profit_amount

```sql
WITH month_sales AS
( SELECT DATE_TRUNC('month', sale_date) AS MONTH,
         SUM(sale_amount) AS total_sales
 FROM public.v_fact_sale
 WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
 GROUP BY DATE_TRUNC('month', sale_date)),
                   manager_salaries AS
( SELECT manager_id,
         DATE_TRUNC('month', sale_date) AS MONTH,
         SUM(sale_amount) * 0.05 AS bonus,
         30000 AS base_salary
 FROM public.v_fact_sale
 WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
 GROUP BY manager_id,
          DATE_TRUNC('month', sale_date)),
                   total_salaries AS
( SELECT MONTH,
         SUM(bonus + base_salary) AS total_salary
 FROM manager_salaries
 GROUP BY MONTH),
                   product_costs AS
( SELECT DATE_TRUNC('month', sale_date) AS MONTH,
         SUM(sale_qty * sale_price * 0.9) AS total_cost
 FROM public.v_fact_sale
 WHERE sale_date BETWEEN TO_DATE('01-01-2014', 'DD-MM-YYYY') AND TO_DATE('31-12-2014', 'DD-MM-YYYY')
 GROUP BY DATE_TRUNC('month', sale_date))
SELECT ms.MONTH,
          ms.total_sales,
          ts.total_salary,
          ms.total_sales - (pc.total_cost + ts.total_salary) AS profit_amount
FROM month_sales ms
JOIN total_salaries ts ON ms.MONTH = ts.MONTH
JOIN product_costs pc ON ms.MONTH = pc.MONTH
ORDER BY ms.MONTH;
```
