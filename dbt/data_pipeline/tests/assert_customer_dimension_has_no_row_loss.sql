-- dim_customers must have the same number of rows as its staging counterpart
-- therefore return records where this isn't true to make the test fail

select *
from (
    select dim_customers.customer_id
    from {{ ref('dim_customers')}} dim_customers
    left join {{ref('stg_eltool__customers')}} stg_customers 
    on dim_customers.customer_id = stg_customers.customer_id
    where stg_customers.customer_id is NULL
    UNION ALL
    select stg_customers.customer_id
    from {{ ref('stg_eltool__customers')}} stg_customers
    left join {{ref('dim_customers')}} dim_customers 
    on stg_customers.customer_id = dim_customers.customer_id
    where dim_customers.customer_id is NULL
) temp