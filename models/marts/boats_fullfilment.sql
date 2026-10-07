select
	tp.boat,
	count(tp.boat) as people_on_board,
	tb.capacity,
	tb.launch_order 
from {{ source('raw', 'titanic_passengers') }} tp 
left join {{ source('raw', 'titanic_boats') }} tb on tp.boat = tb.boat 
group by tp.boat, tb.capacity, tb.launch_order 
order by tb.launch_order 