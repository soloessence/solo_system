import backtrader as bt

class Sma13(bt.Strategy):
    params = (
        ('period', 13),
    )

    def __init__(self):
        sma = bt.indicators.SMA(self.data, period=self.p.period)
        self.crossover = bt.indicators.CrossOver(self.data, sma)

    def next(self):

        if self.position:
            if self.crossover < 0.0:
                self.sell()

        else:
            if self.crossover > 0.0:
                self.buy()