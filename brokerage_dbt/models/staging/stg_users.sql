with source as (
    select * from raw_users
)

select
    user_id,
    name,
    email,
    cast(signup_date as date) as signup_date,
    country,
    account_type
from source
where user_id is not null