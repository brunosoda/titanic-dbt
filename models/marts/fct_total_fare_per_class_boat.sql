select
    tp.boat,
    {{ sum_fare_per_class('class', 'fare') }},
    tb.launch_order
from {{ ref('stg_titanic_passengers') }} tp
left join {{ ref('int_titanic_boats') }} tb on tp.boat = tb.boat
group by tp.boat, tb.launch_order
order by tb.launch_order