with summary as (
    select * from {{ ref('int_user_trade_summary') }}
),

retention as (
    select
        user_id,
        round(avg(case when is_retained then 1.0 else 0.0 end) * 100, 2) as retention_rate
    from {{ ref('int_monthly_retention') }}
    group by 1
)

select
    s.user_id,
    s.account_type,
    s.country,
    s.signup_date,
    s.total_trades,
    s.total_volume,
    s.buy_volume,
    s.sell_volume,
    s.unique_tickers_traded,
    s.first_trade_date,
    s.last_trade_date,
    r.retention_rate,
    datediff('day', s.signup_date, s.last_trade_date) as days_active
from summary s
left join retention r on s.user_id = r.user_id