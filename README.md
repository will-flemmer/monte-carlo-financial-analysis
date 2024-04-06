# Monte Carlo Option Prediction
A project which uses monte carlo simulation to predict option pricing.

### Assumptions
- We will only be simulating call options (for now)

### Simulation Design
- We simulate the possible stock price paths using Geometric Brownian Motion.
- We simulate multiple paths from the current date to the expiration date of the option

#### Expected Payoff Calculation
1. Calculate the payoff for a path: payoff = maximum_stock_price_within_time_period - strike_price - ask_price_of_option
2. Calculate the expected_payoff: average the payoffs of each path
3. Calculate the present_value of the of the average payoff: present_value =  expected_payoff / ((1 + risk_free_rate) ** years_to_expiration)


### Visualisation Ideas
- Plot the present_value of an option against time
- For 3 stock options, plot present_value vs time