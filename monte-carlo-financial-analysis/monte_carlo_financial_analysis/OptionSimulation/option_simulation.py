import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

class OptionSimulation():
  def __init__(self, stock, timedelta):
    self.start_date = datetime.now()
    self.timedelta = timedelta
    self.expiration_date = self.start_date + self.timedelta

    self.number_of_time_steps = 100
    self.dt_days = timedelta.days / self.number_of_time_steps  # time delta
    self.price_path_dataframes = []

    self.store_stock_data(stock)
    self.calculate_expected_return_per_day()
    self.calculate_volatility_per_day()
    print(f"init simulation for {stock}, expiring on {self.expiration_date}")
  
  def simulate_multiple_paths(self):
    for _ in range(20):
      result_df = self.simulate_price_path()
      self.price_path_dataframes.append(result_df)
    concat_df = pd.concat(self.price_path_dataframes)
    self.mean_df = concat_df.groupby('date').mean().reset_index()


  def simulate_price_path(self):
    price_df = pd.DataFrame({'price': [self.s0], 'date': self.start_date})
    for i in range(self.number_of_time_steps):
        change_in_stock_price = self.calculate_change_in_stock_price(
          price_df
        )
        new_price_df = pd.DataFrame({
          'price': price_df.tail(1)['price'] + change_in_stock_price,
          'date': self.start_date + timedelta(days=1) * (i + 1)
        })
        price_df = pd.concat([price_df, new_price_df])
    
    return price_df
  
  def calculate_change_in_stock_price(self, price_df):
    drift = self.expected_return_over_time_period * price_df.tail(1)['price'] * self.dt_days
    shock = self.volatility_over_time_period * price_df.tail(1)['price'] * np.sqrt(self.dt_days) * np.random.normal()
    return drift + shock

  def calculate_volatility_per_day(self):
    self.volatility_over_time_period = self.daily_returns().std()

  def calculate_expected_return_per_day(self):
    self.expected_return_over_time_period = self.daily_returns().mean()

  def store_stock_data(self, stock):
    self.stock = yf.Ticker(stock)
    self.s0 = self.stock.info['currentPrice']
    expiration_date = (self.start_date + self.timedelta).strftime('%Y-%m-%d')
    option_df = self.stock.option_chain(expiration_date).calls
    self.option = self.choose_option(option_df)

  def choose_option(self, option_df):
    # this method can be improved later, for now we just take the median option
    sorted_df = option_df.sort_values('strike')
    midpoint = round(len(sorted_df) / 2)
    return sorted_df.iloc[midpoint]
  

  def daily_returns(self):
    period = f'{self.timedelta.days}d'
    hist = self.stock.history(period=period)
    return hist['Close'].pct_change().dropna()

  def plot_price_paths(self, show_all_paths=False):
    assert(len(self.price_path_dataframes) > 0)
    if show_all_paths:
      for df in self.price_path_dataframes:
        plt.plot(df['date'], df['price'])
    plt.plot(self.mean_df['date'], self.mean_df['price'], label='Mean')
    plt.title("Expected Stock Price Vs Time")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.show()


  
