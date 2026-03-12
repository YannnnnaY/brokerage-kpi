with trades as (
    select * from {{ ref('stg_trades') }}
),

users as (
    select * from {{ ref('stg_users') }}
),

summary as (
    select
        t.user_id,
        u.account_type,
        u.country,
        u.signup_date,
        count(t.trade_id)                           as total_trades,
        sum(t.total_value)                          as total_volume,
        sum(case when t.trade_type = 'buy' 
            then t.total_value else 0 end)          as buy_volume,
        sum(case when t.trade_type = 'sell' 
            then t.total_value else 0 end)          as sell_volume,
        min(t.trade_date)                           as first_trade_date,
        max(t.trade_date)                           as last_trade_date,
        count(distinct t.ticker)                    as unique_tickers_traded
    from trades t
    left join users u on t.user_id = u.user_id
    group by 1, 2, 3, 4
)

select * from summary