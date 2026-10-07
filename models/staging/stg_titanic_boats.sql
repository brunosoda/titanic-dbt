select
    boat,
    capacity,
    side,
    position,
    launch_order,
    case
        when launch_time in (
            '2012-04-15 12:40:00',
            '2012-04-15 12:43:00'
        )
            then launch_time - interval '12 hours'
        else launch_time
    end - interval '100 years' as launch_time
from {{ source('raw', 'titanic_boats') }}