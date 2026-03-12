with trades as (
    select * from {{ ref('stg_trades') }}
),

monthly_activity as (
    select
        user_id,
        date_trunc('month', trade_date) as activity_month
    from trades
    group by 1, 2
),

retention as (
    select
        curr.user_id,
        curr.activity_month,
        case when prev.user_id is not null 
            then true else false 
        end as is_retained
    from monthly_activity curr
    left join monthly_activity prev
        on curr.user_id = prev.user_id
        and prev.activity_month = curr.activity_month - interval '1 month'
)

select * from retention