select
	tp.boat,
    tb.position,
    tb.side,
	count(tp.boat) as people_on_board,
	tb.capacity,
	tb.launch_order,
    tb.launch_time
from {{ ref('stg_titanic_passengers') }} tp 
left join {{ ref('int_titanic_boats') }} tb on tp.boat = tb.boat 
group by tp.boat, tb.position, tb.side, tb.capacity, tb.launch_order, tb.launch_time
order by tb.launch_order 