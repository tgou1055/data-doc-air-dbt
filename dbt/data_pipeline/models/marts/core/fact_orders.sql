/*
Create fact table
*/

{{
    config(
        schema='core_layer'
    )
}}

with orders as (
    select * from {{ ref('stg_eltool__orders') }}
)

select * from orders