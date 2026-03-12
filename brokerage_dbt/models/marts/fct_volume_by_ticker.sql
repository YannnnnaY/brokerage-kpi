with trades as (
    select * from {{ ref('stg_trades') }}
),

instruments as (
    select * from {{ ref('stg_instruments') }}
),

volume as (
    select
        t.ticker,
        i.sector,
        date_trunc('month', t.trade_date)   as month,
        count(t.trade_id)                   as total_trades,
        sum(t.total_value)                  as total_volume,
        avg(t.price)                        as avg_price,
        sum(case when t.trade_type = 'buy' 
            then t.total_value else 0 end)  as buy_volume,
        sum(case when t.trade_type = 'sell' 
            then t.total_value else 0 end)  as sell_volume
    from trades t
    left join instruments i on t.ticker = i.ticker
    group by 1, 2, 3
)

select * from volume
order by month, ticker