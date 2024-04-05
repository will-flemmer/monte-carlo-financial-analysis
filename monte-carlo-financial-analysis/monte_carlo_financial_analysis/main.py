from datetime import datetime, timedelta
from OptionSimulation import OptionSimulation

apple_sim = OptionSimulation("AAPL", timedelta(weeks=1))
apple_sim.simulate_multiple_paths()
apple_sim.plot_price_paths()