select
    tp.boat,
    tb.launch_order,
    sum(tp.fare) as total_fare
from {{ ref('stg_titanic_passengers') }} tp
left join {{ ref('int_titanic_boats')}} tb on tp.boat = tb.boat
group by tp.boat, tb.launch_order
order by tb.launch_order
