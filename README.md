# Monte Carlo Option Prediction
A project which uses monte carlo simulation to predict option pricing. For documentation see [this section](#documentation)

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

# Documentation
This project uses [poetry](https://python-poetry.org/docs/) for dependency management and to run the project. Please install it before running the simulation.

### Getting Started
1. Clone this repo
2. Install [poetry](https://python-poetry.org/docs/)
3. `poetry install`
4. In the top level directory: `./run`
5. Change the parameters in `monte_carlo_financial_analysis/main.py`

### Running tests
Unit tests can be run using poetry: `poetry run pytest`