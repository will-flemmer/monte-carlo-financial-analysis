# Monte Carlo Option Prediction
A project which uses monte carlo simulation to predict option pricing for European options.

### Assumptions
- We will only be simulating call options (for now)

### Simulation Design
- We simulate the possible stock price paths using Geometric Brownian Motion.
- We simulate multiple paths from the current date to the expiration date of the option to find stock_price_at_expiration

#### Expected Payoff Calculation
1. Calculate the payoff for a path: payoff = stock_price_at_expiration - strike_price
2. Calculate the expected_payoff we average the payoffs of each of the paths
3. Calculate the present_value of the of the average payoff: present_value =  expected_payoff / ((1 + risk_free_rate) ** years_to_expiration)


### Visualisation Ideas
- Plot the present_value of an option against time
- For 3 stock options, plot present_value vs time