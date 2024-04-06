import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

ANNUAL_RISK_FREE_RATE = 0.03

def find_closest_expiration_date(expiration_date, option_dates):
  date_format = "%Y-%m-%d"

  current_closest_date = None
  for date_string in option_dates:
    datetime_obj = datetime.strptime(date_string, date_format)
    if current_closest_date == None:
      current_closest_date = datetime_obj
      continue
    if abs(current_closest_date - expiration_date) > abs(datetime_obj - expiration_date):
      current_closest_date = datetime_obj
  
  if abs(current_closest_date - expiration_date).days > 365:
    raise Exception('The closest option date is not in the same year as the provided date. Please choose a different time period')
  return current_closest_date


class OptionSimulation():
  def __init__(self, stock, timedelta):
    self.store_stock_data(stock)
    self.expiration_date = find_closest_expiration_date(datetime.now() + timedelta, self.stock.options)

    self.start_date = datetime.now()
    self.timedelta = self.expiration_date - self.start_date
    self.expiration_date = self.start_date + self.timedelta

    self.number_of_time_steps = 100
    self.dt_days = timedelta.days / self.number_of_time_steps  # time delta
    self.price_path_dataframes = []
    self.discounted_payoffs = []

    self.set_option()
    self.calculate_expected_return_per_day()
    self.calculate_volatility_per_day()
    print(f"init simulation for {stock}, expiring on {self.expiration_date}")
  
  def simulate_multiple_paths(self):
    for _ in range(200):
      result_df = self.simulate_price_path()
      self.calculate_discounted_payoff(result_df)
      self.price_path_dataframes.append(result_df)
    concat_df = pd.concat(self.price_path_dataframes)
    self.mean_df = concat_df.groupby('date').mean().reset_index()
    expected_present_value = np.mean(self.discounted_payoffs)
    print(f"Expected present value of option: {expected_present_value}")


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
  
  def calculate_discounted_payoff(self, price_path_df):
    payoff = price_path_df['price'].max() - self.option['strike'] - self.option['ask']
    discounted_payoff = payoff / (1 + ANNUAL_RISK_FREE_RATE) ** (self.timedelta.days / 365)
    self.discounted_payoffs.append(discounted_payoff)

  def calculate_volatility_per_day(self):
    self.volatility_over_time_period = self.daily_returns().std()

  def calculate_expected_return_per_day(self):
    self.expected_return_over_time_period = self.daily_returns().mean()  

  def daily_returns(self):
    period = f'{self.timedelta.days}d'
    hist = self.stock.history(period=period)
    return hist['Close'].pct_change().dropna()
  
  def store_stock_data(self, stock):
    self.stock = yf.Ticker(stock)
    self.s0 = self.stock.info['currentPrice']

  def set_option(self):
    # this method can be improved later, for now we just take the median option.
    # We could loop through each option and find the present value of each
    expiration_date = (self.start_date + self.timedelta).strftime('%Y-%m-%d')
    option_df = self.stock.option_chain(expiration_date).calls
    sorted_df = option_df.sort_values('strike')
    midpoint = round(len(sorted_df) / 2)
    self.option = sorted_df.iloc[midpoint]

  def plot_price_paths(self, show_all_paths=False):
    assert(len(self.price_path_dataframes) > 0)
    if show_all_paths:
      for df in self.price_path_dataframes:
        plt.plot(df['date'], df['price'])
    
    strike_line = np.full((self.number_of_time_steps + 1,), self.option['strike'] + self.option['ask'])
    plt.plot(self.mean_df['date'], strike_line, label='Strike Price + Ask Price')
    plt.plot(self.mean_df['date'], self.mean_df['price'], label='Expected Stock Price')
    
    plt.title("Expected Stock Price Vs Time")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.show()


  
