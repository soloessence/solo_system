
--Solo industry heatmap

select stock_info_analysis.trade_date,
avg(case when ak_industry_details.board = '基础化学' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "基础化学",
avg(case when ak_industry_details.board = '中药' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "中药",
avg(case when ak_industry_details.board = '传媒' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "传媒",
avg(case when ak_industry_details.board = '化学制药' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "化学制药",
avg(case when ak_industry_details.board = '半导体及元件' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "半导体及元件",
avg(case when ak_industry_details.board = '建筑装饰' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "建筑装饰",
avg(case when ak_industry_details.board = '有色冶炼加工' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "有色冶炼加工",
avg(case when ak_industry_details.board in( '汽车整车','汽车零部件') then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "汽车整车",
avg(case when ak_industry_details.board = '电力' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "电力",
avg(case when ak_industry_details.board = '白色家电' then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "白色家电",
avg(case when ak_industry_details.board in( '种植业与林业','养殖业','农产品加工','农业服务') then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "农业",
avg(case when ak_industry_details.board in( '证券','银行') then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "银行证券",
avg(case when ak_industry_details.board in( '饮料制造') then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "饮料制造",
avg(case when ak_industry_details.board in( '计算机应用','计算机设备') then stock_info_analysis.close/stock_info_analysis."MA20" else null end) as "基础化学"
from stock_info 
inner join ak_industry_details on stock_info.name = ak_industry_details.name 
inner join ak_industry on ak_industry.name = ak_industry_details.board
left join stock_info_analysis on stock_info_analysis.ts_code = stock_info.ts_code

where stock_info_analysis.trade_date > '2021-01-01' and stock_info.name not like '%ST%' and stock_info.market = '主板'
[[ and {{industry}}]]
group by stock_info_analysis.trade_date 
order by stock_info_analysis.trade_date  desc 
