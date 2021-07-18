import backtrader as bt


class EmaCross7And21(bt.SignalStrategy):

    params = dict(ema1=7, ema2=21)

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
            print('Trade {}-{}: profit {}'.format(trade.dtopen, trade.dtclose, trade.pnlcomm))

    def __init__(self):
        ema1 = bt.ind.EMA(period=self.params.ema1)
        ema2 = bt.ind.EMA(period=self.params.ema2)
        crossover = bt.ind.CrossOver(ema1, ema2)

        self.signal_add(bt.SIGNAL_LONG, crossover)


class EmaCross10And20(bt.SignalStrategy):

    params = dict(ema1=10, ema2=20)

    def notify_order(self, order):
        pass
        # if not order.alive():
        #     print('{} {} {}@{}'.format(
        #         bt.num2date(order.executed.dt),
        #         'buy' if order.isbuy() else 'sell',
        #         order.executed.size,
        #         order.executed.price)
        #     )

    def notify_trade(self, trade):
        if trade.isclosed:
            print('Trade {}~{}:  profit {}'.format(bt.num2date(trade.dtopen).strftime('%Y-%m-%d'),
                                                  bt.num2date(trade.dtclose).strftime('%Y-%m-%d'),
                                                  trade.pnlcomm))

    def __init__(self):
        ema1 = bt.ind.EMA(period=self.params.ema1)
        ema2 = bt.ind.EMA(period=self.params.ema2)
        crossover = bt.ind.CrossOver(ema1, ema2)

        self.signal_add(bt.SIGNAL_LONG, crossover)


class EmaCross12And50(bt.SignalStrategy):

    params = dict(ema1=5, ema2=10)

    def notify_order(self, order):
        pass
        # if not order.alive():
        #     print('{} {} {}@{}'.format(
        #         bt.num2date(order.executed.dt),
        #         'buy' if order.isbuy() else 'sell',
        #         order.executed.size,
        #         order.executed.price)
        #     )

    def notify_trade(self, trade):
        if trade.isclosed:
            print('profit {}'.format(trade.pnlcomm))

    def __init__(self):
        ema1 = bt.ind.EMA(period=self.params.ema1)
        ema2 = bt.ind.EMA(period=self.params.ema2)
        crossover = bt.ind.CrossOver(ema1, ema2)

        self.signal_add(bt.SIGNAL_LONG, crossover)