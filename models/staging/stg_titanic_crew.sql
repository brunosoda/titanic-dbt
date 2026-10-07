select
    *,
    split_part(name, ',', 1) as last_name
from {{ source('raw', 'titanic_crew') }}
