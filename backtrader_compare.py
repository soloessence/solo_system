import datetime
import backtrader as bt
import pandas as pd
from strategy import EMAStrategy,SMAStrategy,ParamEMAStrategy
from pprint import pprint as print

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://solo:solo@localhost:5432/metabase')

def get_my_analyzer(result):

    analyzer = {}
    # 返回参数
    analyzer['ema1'] = result.params.ema1
    analyzer['ema2'] = result.params.ema2
    # 提取年化收益
    # analyzer['年化收益率'] = result.analyzers._Returns.get_analysis()['rnorm']
    analyzer['年化收益率（%）'] = result.analyzers._Returns.get_analysis()['rnorm100']

    # 提取最大回撤(习惯用负的做大回撤，所以加了负号)
    analyzer['最大回撤（%）'] = result.analyzers._DrawDown.get_analysis()['max']['drawdown'] * (-1)
    # 提取夏普比率
    analyzer['年化夏普比率'] = result.analyzers._SharpeRatio_A.get_analysis()['sharperatio']

    #analyzer['收益率时序'] = result.analyzers._TimeReturn.get_analysis()

    return analyzer


# Prepare Data feed
start_cash = 100000
stock = 'sh601888'
#stock = 'sz002241'

# df = pd.read_sql('''select trade_date as datetime, open, close, high, low, vol
# from stock_info_analysis where ts_code = '{}' order by trade_date asc '''.format(stock), engine)


cerebro = bt.Cerebro(optdatas=True, optreturn=True)
cerebro.broker.set_cash(start_cash)
cerebro.broker.set_coc(True)

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
start_date = datetime.datetime.strptime('2016-05-24', '%Y-%m-%d')
end_date = datetime.datetime.strptime('2021-07-09', '%Y-%m-%d')
data0 = bt.feeds.PandasData(dataname=df, fromdate=start_date, todate=end_date)

cerebro.adddata(data0)

cerebro.addstrategy(ParamEMAStrategy.EmaCross)
#cerebro.optstrategy(ParamEMAStrategy.EmaCross, ema1=range(5, 10), ema2=range(15, 30, 5))

cerebro.addsizer(bt.sizers.AllInSizerInt)  ## all in
#cerebro.broker.setcommission(0.0001)
#cerebro.broker.set_slippage_perc(perc=0.2)


# 添加分析指标
# 返回年初至年末的年度收益率
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
# 计算最大回撤相关指标
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
# 计算年化收益
cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns', tann=252)
# 计算年化夏普比率
cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='_SharpeRatio_A')
# 返回收益率时序
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')

result = cerebro.run()


port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
pnl = port_value - start_cash  # 盈亏统计

print(f"回测标的: {stock}")
print(f"初始资金: {start_cash} \n 回测期间：{start_date.strftime('%Y-%m-%d')}:{end_date.strftime('%Y-%m-%d')}")
print(f"总资金: {round(port_value, 2)}")
print(f"净收益: {round(pnl, 2)}")

print(get_my_analyzer(result[0]))

cerebro.plot()






