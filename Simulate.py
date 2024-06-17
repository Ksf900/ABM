from Transport import 
from Functions import
from Agent import
from Policy import

# Steps for simulation should be:
# 1. initialise commuters

# 2. choose location for a commuter

# 3. collect amount of commuters taking a certain mode of transport

# 4. update the conditions of the transportation modes (after each iteration/day)

# 5. per commuter that used e.g. Ferry_AB it should update the memory of that specific ferry 
# after each iteration and after updating the conditions of the transport because the transport class 
# contains functions for calculating price, density, and time etc(this is quite difficult i think)

# 6. start at 2.



class Simulation:
    '''
    Transport modes should include a list (btw you should initialise ferry outside of simulation class before running:
      ferry_AB = Ferry(A, B, amount_of_commuters, price, time)
    such as transport_modes = [ferry_AB, ferry_BA, speedboat_AB, speedboat_BA]
    And commuters is the amount of commuters e.g. 100 or something
    '''
    def __init__(self, commuters, transport_modes):
        self.commuters = commuters
        self.transport_modes = transport_modes

    def run_simulation(self, num_days):
        for day in range(num_days):
            self.simulate_day()

    def simulate_day(self):
        # Simulate a day of commuting
        for commuter in self.commuters:
            
            # Choose best mode
            best_mode = commuter.choose_transportation()

            # 
        

            
        
        