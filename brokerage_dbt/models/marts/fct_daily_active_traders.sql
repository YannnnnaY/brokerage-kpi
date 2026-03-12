with trades as (
    select * from {{ ref('stg_trades') }}
),

daily as (
    select
        trade_date,
        count(distinct user_id)     as daily_active_traders,
        count(trade_id)             as total_trades,
        sum(total_value)            as total_volume,
        count(distinct ticker)      as unique_tickers
    from trades
    group by 1
)

select * from daily
order by trade_date