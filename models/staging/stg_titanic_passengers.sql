select
    class,
    survived,
    sex,
    age,
    sibsp,
    parch,
    CASE
        WHEN embarked = 'Southhampton' THEN 'Southampton'
        ELSE embarked
    END AS embarked_from,
    boat,
    body,
    cabin,
    ticket,
    ROUND(fare::numeric, 2) AS fare,
    destination,
    name,
    split_part(name, ',', 1) AS last_name
from {{ source('raw', 'titanic_passengers') }}
order by class, fare DESC, last_name