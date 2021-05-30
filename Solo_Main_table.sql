
-- C/S -》 收盘价和短期移动平均线之间的距离， 表达是否有破线
-- EMA（表达了拐头）
-- S/M 短期平均线和中期移动平均线 ， 表达是否有交叉
-- M/L 中期和长期均线

select stock_info_analysis.ts_code, stock_info.name, stock_info.industry,stock_info.market, 
stock_info_analysis.close as "close",  
stock2.close as "LastWeek", 
stock_info_analysis.close / stock_info_analysis."EMA20" as "C-EMA20",
stock2.close / stock2."EMA20" as "C-EMA20(LastWeek)",
stock_info_analysis.close/stock_info_analysis."MA20" as "C/S", 
stock_info_analysis."MA20"/stock_info_analysis."MA60" as "S/M",
stock_info_analysis."MA60"/stock_info_analysis."MA120" as "M/L"
from stock_info_analysis 
inner join  stock_info on stock_info.ts_code=stock_info_analysis.ts_code
inner join ak_industry_details on ak_industry_details.name = stock_info.name 
inner join ak_industry on ak_industry.name = ak_industry_details.board
--inner join index_hs300 on index_hs300.code =stock_info.symbol 

left join stock_info_analysis as stock2 on stock_info_analysis.ts_code = stock2.ts_code and  stock_info_analysis.trade_date - '7 day'::interval = stock2.trade_date
where 1=1 --and stock_info.industry = '小金属'
[[ and {{market}} ]] 
[[and {{trade_date}}]]
[[and {{industry}}]]
order by stock_info_analysis.close/stock_info_analysis."MA20" desc 
