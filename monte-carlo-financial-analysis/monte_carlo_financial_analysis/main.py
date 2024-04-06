from datetime import datetime, timedelta
from OptionSimulation import OptionSimulation

weeks = 31
days = 6
total_days = weeks * 7 + days
apple_sim = OptionSimulation("AAPL", timedelta(days=total_days))
# apple_sim.simulate_multiple_paths()
# apple_sim.plot_price_paths()