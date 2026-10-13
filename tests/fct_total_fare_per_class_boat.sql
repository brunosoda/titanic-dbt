select *
from {{ ref('fct_total_fare_per_class_boat') }} 
where first_total_fare < 0
or second_total_fare < 0
or steerage_total_fare < 0
