""" Service class used in portfolio updates """
import pandas as pd

class StockUpdate():
    """ Class updates a stock gain/loss given historical prices and trades """
    def __init__(self, benchmark, prices, trades):
        self.benchmark_df = pd.DataFrame(benchmark)
        self.benchmark_df['date'] = pd.to_datetime(self.benchmark_df['date'])
        self.price_chart = pd.read_json(prices)
        self.price_chart['date'] = pd.to_datetime(self.price_chart['date'])
        self.trades = trades

    def get_update(self):
        """ Call update methods """
        print(f"updating stock...")
        trades_chart = self.trade_charts()
        print(f"formatted trades...")
        return self.apply_price_chart(trades_chart)

    def trade_charts(self):
        """ Loop through trades and collate prices and amounts incrementing buys then detracting
        sells need trades to be ordered by date """
        stock_df = pd.DataFrame()
        for index, trade in enumerate(self.trades):
            date = pd.to_datetime(trade.date)
            chart = self.trade_amount(date, trade)
            if index == 0:
                stock_df = chart
            else:
                current_buys = [trade.avg_price for trade in self.trades[0:index+1] if trade.trade_type == 'b']
                pre_trade_df = stock_df.loc[stock_df['date'] < date]
                pre_trade_amounts = pre_trade_df.loc[pre_trade_df['date'] == pre_trade_df['date'].max()]
                stock_df.loc[stock_df['date'] > date, ['fees_usd']] = pre_trade_amounts['fees_usd'].array[0] + chart['fees_usd'].array[0]
                stock_df.loc[stock_df['date'] > date, ['amount']] = pre_trade_amounts['amount'].array[0] + chart['amount'].array[0]
                stock_df.loc[stock_df['date'] > date, ['bench_amount']] = pre_trade_amounts['bench_amount'].array[0] + chart['bench_amount'].array[0]
                if trade.trade_type == 'b':
                    stock_df.loc[stock_df['date'] > date, ['invested']] = pre_trade_amounts['invested'].array[0] + chart['invested'].array[0]
                    stock_df.loc[stock_df['date'] > date, ['avg_price']] = sum(current_buys)/len(current_buys)
                else:
                    stock_df.loc[stock_df['date'] > date, ['invested']] = pre_trade_amounts['invested'].array[0] - (trade.amount*pre_trade_amounts['avg_price'].array[0])
        return stock_df

    def trade_amount(self, date, trade):
        """ Function calculates trade amounts given prices on day """
        if trade.trade_type == 'b':
            trade_df = self.price_chart[self.price_chart['date'] >= date][['date', 'close', 'volume']]
            trade_df['amount'] = trade.amount
            trade_df['stock_id'] = trade.stock.id
            trade_df['ticker'] = trade.stock.ticker
            trade_df['avg_price'] = trade.avg_price
            trade_df['fees_usd'] = trade.fees_usd
            trade_df['amount'] = trade.amount
            trade_df['invested'] = trade.amount * trade.avg_price
            trade_df['bench_amount'] = self.benchmark_amount(trade.amount*trade.avg_price, date)
        else:
            data = {'amount': -(trade.amount), 'fees_usd': trade.fees_usd, 'bench_amount': -(self.benchmark_amount(trade.amount*trade.avg_price, date))}
            trade_df = pd.DataFrame(data, index=[0])
        return trade_df

    def benchmark_amount(self, to_invest, date):
        """ Calculate amount of benchmark trade value could purchase averaging open, close ,high and low """
        day = self.benchmark_df[self.benchmark_df['date'] == date]
        bench_avg = (day['high'] + day['low'] + day['open'] + day['close'])/4
        bench_amount = to_invest/bench_avg
        return bench_amount.array[0]

    def apply_price_chart(self, trades_chart):
        """ Combine trade with historical prices """
        trades_chart['date'] = pd.to_datetime(trades_chart['date'])
        min_date = min(trades_chart['date'])
        max_date = max(trades_chart['date'])
        mask = (self.benchmark_df['date'] >= min_date) & (self.benchmark_df['date'] <= max_date)
        benchmark_prices = self.benchmark_df.loc[mask]['close']
        trades_chart = trades_chart.assign(bench_close=benchmark_prices.array)
        print(f"assigned benchmark column...")
        trades_chart['bench_value'] = trades_chart['bench_amount'] * trades_chart['bench_close']
        trades_chart['value'] = trades_chart['amount'] * trades_chart['close']
        trades_chart['gain'] = trades_chart['value'] - trades_chart['invested']
        trades_chart['gain_pct'] = (trades_chart['gain']/trades_chart['invested'])*100
        trades_chart['bench_gain'] = trades_chart['bench_value'] - trades_chart['invested']
        trades_chart['bench_gain_pct'] = (trades_chart['bench_gain']/trades_chart['invested'])*100
        return trades_chart
