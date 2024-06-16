import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from Functions import truncated_normal_rvs


class Commuter():
    '''
    Agent class for commuters
    '''
    def __init__(self, unique_id, modes_of_transport):
        '''
        Initialize the agent
        args: 
            unique_id: int, unique identifier for the agent
        '''
        self.unique_id = unique_id

        # Initial state for transportation
        self.state = np.random.choice(modes_of_transport)

        # Initialise preferences for price, density, and time
        self.pref_price, self.pref_density, self.pref_time = truncated_normal_rvs(0.0, 1.0, 0.5, 0.5/3, 3)
    
        # Agent memory concerning price, density, time for each transportation mode
        self.memory = {}
        for mode in modes_of_transport:
            self.memory[mode] = {'Price': [], 'Density': [], 'Time': []}


    def update_memory(self, mode):
        self.memory[mode]['Price'].append(mode.price)
        self.memory[mode]['Density'].append(mode.density)
        self.memory[mode]['Time'].append(mode.time)


    def choice_of_transportation(self, mode_of_transport):
        ''' Choose the best transportation mode based on utility. '''
    
        mode_utility = {}

        # For each mode of transportation calculate the utility
        for mode in mode_of_transport:
            self.update_memory(mode) # Update memory before making choice
            mode_utility[mode] = self.utility(mode)

        # Define best mode of transport based on highest utility score
        best_option = max(mode_utility, key=mode_utility.get)

        return best_option

        
    def utility(self, mode):
        ''' Calculate utility for a given mode based on historical data. '''
        if len(self.memory[mode]['Price']) > 0:
            average_price_memory = np.mean(self.memory[mode]['Price'][-5:])
            average_density_memory = np.mean(self.memory[mode]['Density'][-5:])
            average_time_memory = np.mean(self.memory[mode]['Time'][-5:])
        else:
            average_density_memory = average_density_memory = average_time_memory = 0

        return (- self.pref_price * average_price_memory 
                - self.pref_density * average_density_memory 
                - self.pref_time * average_time_memory)







"""
This part is for running the model. The argparse part asks the user to give a command-line argument for the number of agents.
"""
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run an agent-based model simulation.")
#     parser.add_argument('--num_agents', type=int, default=1000, help='Number of agents in the simulation')
    
#     args = parser.parse_args()
    
#     main(args.num_agents)
        




