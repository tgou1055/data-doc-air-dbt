{% snapshot customers_snapshot  %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',

        strategy='timestamp',
        updated_at='datetime_updated',
    )
}}

SELECT * FROM {{ source('raw_layer', 'customers') }}

{% endsnapshot  %}