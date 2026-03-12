with source as (
    select * from raw_instruments
)

select
    ticker,
    name,
    sector,
    base_price
from source
where ticker is not null