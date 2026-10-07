select *
from {{ source('raw', 'titanic_boats') }}