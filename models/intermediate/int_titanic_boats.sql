select
    boat,
    capacity,
    side,
    position,
    row_number() over (order by launch_time) as launch_order,
    launch_time
from {{ ref('stg_titanic_boats') }}
order by launch_time asc