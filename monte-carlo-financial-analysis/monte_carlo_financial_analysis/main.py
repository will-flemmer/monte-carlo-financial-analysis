from datetime import timedelta
from OptionSimulation import OptionSimulation

apple_sim = OptionSimulation("AAPL", timedelta(weeks=100))
apple_sim.simulate_multiple_paths()
apple_sim.plot_price_paths()