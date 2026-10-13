select *
from {{ ref('fct_total_fare_per_boat') }} 
where total_fare < 0