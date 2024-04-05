import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

def calculate_change_in_stock_price(price_df, params):
  drift = params['expected_return'] * price_df.tail(1)['price'] * params['dt']
  shock = params['volatility'] * price_df.tail(1)['price'] * np.sqrt(params['dt']) * params['z']
  return drift + shock



class OptionSimulation():
  def __init__(self, stock, timedelta):
    self.start_date = datetime.now()
    self.timedelta = timedelta
    self.expiration_date = self.start_date + self.timedelta

    self.stock = yf.Ticker("AAPL")
    self.s0 = self.stock.info['currentPrice']  # Initial stock price

    self.number_of_time_steps = 100
    self.dt_days = timedelta.days / self.number_of_time_steps  # time delta
    self.price_path_dataframes = []

    self.calculate_expected_return_per_day()
    self.calculate_volatility_per_day()
    print(f"init simulation for {stock}, expiring on {self.expiration_date}")
  
  def simulate_multiple_paths(self):
    for i in range(2):
      expected_return = self.return_over_time_period * (i + 1)
      volatility = self.volatility_over_time_period * (i + 1)
      result_df = self.simulate_price_path(expected_return, volatility)
      self.price_path_dataframes.append(result_df)
    concat_df = pd.concat(self.price_path_dataframes)
    self.mean_df = concat_df.groupby('date').mean().reset_index()


  def simulate_price_path(self, expected_return, volatility):
    np.random.seed(42)  # For reproducibility

    price_df = pd.DataFrame({'price': [self.s0], 'date': self.start_date})
    for i in range(self.number_of_time_steps):
        change_in_stock_price = self.calculate_change_in_stock_price(
          price_df, { 'expected_return': expected_return, 'volatility': volatility }
        )
        new_price_df = pd.DataFrame({
          'price': price_df.tail(1)['price'] + change_in_stock_price,
          'date': self.start_date + timedelta(days=1) * (i + 1)
        })
        price_df = pd.concat([price_df, new_price_df])
    
    return price_df
  
  def calculate_change_in_stock_price(self, price_df, params):
    drift = params['expected_return'] * price_df.tail(1)['price'] * self.dt_days
    shock = params['volatility'] * price_df.tail(1)['price'] * np.sqrt(self.dt_days) * np.random.normal()
    return drift + shock

  def calculate_volatility_per_day(self):
    # calculate from historical data.
    # 1. time period = datetime.now() - self.timedelta()
    # 2. get historical data
    # 3. calculate volatility_over_time_period
    self.volatility_over_time_period = 0.2


  def calculate_expected_return_per_day(self):
    # calculate from historical data.
    # 1. time period = datetime.now() - self.timedelta()
    # 2. get historical data
    # 3. calculate return_over_time_period
    annual_return = 0.05
    self.return_over_time_period = annual_return / 252

  def plot_price_paths(self):
    assert(len(self.price_path_dataframes) > 0)
    for df in self.price_path_dataframes:
      plt.plot(df['date'], df['price'])
    plt.plot(self.mean_df['date'], self.mean_df['price'], label='Mean')
    plt.legend()
    plt.show()


  
