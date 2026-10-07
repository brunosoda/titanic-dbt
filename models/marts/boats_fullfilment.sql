select
	tp.boat,
    tb.position,
    tb.side,
	count(tp.boat) as people_on_board,
	tb.capacity,
	tb.launch_order,
    tb.launch_time
from {{ source('raw', 'titanic_passengers') }} tp 
left join {{ source('raw', 'titanic_boats') }} tb on tp.boat = tb.boat 
group by tp.boat, tb.position, tb.side, tb.capacity, tb.launch_order, tb.launch_time
order by tb.launch_order 