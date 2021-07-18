import backtrader as bt


class EmaCross(bt.Strategy):
    #lines = ('crossover',)

    params = (('ema1', 7),
              ('ema2', 21),
              )

    def __init__(self):
        self.order = None

        self.ema1 = bt.ind.EMA(period=self.params.ema1)
        self.ema2 = bt.ind.EMA(period=self.params.ema2)
        self.crossover = bt.ind.CrossOver(self.ema1, self.ema2)

        self.crossover.plotinfo.plot = False

#        self.signal_add(bt.SIGNAL_LONG, crossover)

    def next(self):

        # 检查是否持仓
        if self.position.size == 0:  # 没有持仓
            if self.crossover[0] > 0:
                self.buy()
        else:
            if self.crossover[0] < 0:
                self.sell()
        # print(self.order)
        # if self.order:  # 检查是否有指令等待执行,
        #     return
        # # 检查是否持仓
        # if not self.position:  # 没有持仓
        #     # 执行买入条件判断：收盘价格上涨突破15日均线
        #     if self.crossover[0] > 0:
        #         print("BUY CREATE, %.2f" % self.data_close[0])
        #         # 执行买入
        #         self.order = self.buy()
        # else:
        #     # 执行卖出条件判断：收盘价格跌破15日均线
        #     if self.crossover[0]<0:
        #         print("SELL CREATE, %.2f" % self.data_close[0])
        #         # 执行卖出
        #         self.order = self.sell()

    def notify_order(self, order):
        if not order.alive():
            print('{} {} {}@{}'.format(
                bt.num2date(order.executed.dt),
                'buy' if order.isbuy() else 'sell',
                order.executed.size,
                order.executed.price)
            )

    def notify_trade(self, trade):
        if trade.isclosed:
            print('profit {}'.format(trade.pnlcomm))