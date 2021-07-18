import datetime
import backtrader as bt
import pandas as pd
from strategy import EMAStrategy,SMAStrategy,SingleSMAStrategy


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://solo:solo@localhost:5432/metabase')


# Prepare Data feed
start_cash = 100000
#stock = '002241.SZ'
stock = 'sz002241'

# df = pd.read_sql('''select trade_date as datetime, open, close, high, low, vol
# from stock_info_analysis where ts_code = '{}' order by trade_date asc '''.format(stock), engine)

sql = '''
select date as datetime, open, close, high, low, volume 
            from ak_stock_daily where code = '{}' order by date asc 
'''.format(stock)
df = pd.read_sql(sql, engine)


df.columns = [
    'datetime',
    'open',
    'close',
    'high',
    'low',
    'volume',
]
df.index = pd.to_datetime(df['datetime'])


cerebro = bt.Cerebro()
cerebro.broker.set_cash(start_cash)
#cerebro.broker.set_coc(True)

start_date = datetime.datetime.strptime('2016-05-24', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2021-07-14', '%Y-%m-%d')
data0 = bt.feeds.PandasData(dataname=df, fromdate=start_date, todate=end_date)

cerebro.adddata(data0)

#cerebro.addstrategy(SingleSMAStrategy.Sma13)

#cerebro.addstrategy(EMAStrategy.EmaCross7And21)
cerebro.addstrategy(EMAStrategy.EmaCross10And20)
#cerebro.addstrategy(EMAStrategy.EmaCross12And50)

#cerebro.addstrategy(EMAStrategy.EmaCross12And50)v

#cerebro.addstrategy(SMAStrategy.SmaCross7And21)
#cerebro.addstrategy(SMAStrategy.SmaCross20And60)

cerebro.addsizer(bt.sizers.AllInSizerInt)  ## all in
#cerebro.addsizer(bt.sizers.FixedSize, stake=1000) ## fixSize

cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Months)
cerebro.addanalyzer(bt.analyzers.TimeReturn, timeframe=bt.TimeFrame.Years)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)

cerebro.addwriter(bt.WriterFile, csv=True, out="./solo.csv")
cerebro.run()

# for o in cerebro.broker.orders:
#     print()




port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
pnl = port_value - start_cash  # 盈亏统计

print(f"回测标的: {stock}")
print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y-%m-%d')}:{end_date.strftime('%Y-%m-%d')}")
print(f"总资金: {round(port_value, 2)}")
print(f"净收益: {round(pnl, 2)}")

cerebro.plot()
