import requests as r
import json
import pandas as pd

# # Generating data for use in testing portfolio update methods.
# # Data collected on 13/01/2020

# iex_base = 'https://cloud.iexapis.com/v1'
# # Insert production api key below
# api_token = ''

# # Get 2 years benchmark data
# query = f'/stock/voo/chart/2y?token={api_token}'
# url = iex_base + query
# iex_req = r.get(url)
# data = iex_req.json()

# with open('benchmark_data.json', 'w') as outfile:
#     json.dump(data, outfile)

# # Get price charts for stocks
# tickers = 'DIS,TWTR,MTCH'
# stock_query = f'/stock/market/batch?token={api_token}&symbols={tickers}&types=chart&range=5y&chartCloseOnly=true'
# stock_url = iex_base + stock_query
# iex_req_stocks = r.get(stock_url)
# stock_data = iex_req_stocks.json()

# with open('stock_charts.json', 'w') as stock_outfile:
#     json.dump(stock_data, stock_outfile)


# with open('benchmark_data.json') as json_file:
#     data = json.load(json_file)
#     bench_df = pd.DataFrame(data)
#     bench_df.to_csv('benchmark.csv')

# with open('stock_charts.json') as json_file:
#     stock_data = json.load(json_file)
#     for key, value in stock_data.items():
#     	chart = pd.DataFrame(value['chart'])
#     	chart.to_csv(f'{key}_chart.csv')
