with source as (
    select * from raw_trades
)

select
    trade_id,
    user_id,
    ticker,
    cast(trade_date as date) as trade_date,
    trade_type,
    quantity,
    price,
    total_value
from source
where trade_id is not null
  and total_value > 0