select
    boat,
    {{ sum_fare_per_class('class', 'fare') }}
from {{ ref('stg_titanic_passengers') }}
group by boat