import numpy as np
from scipy import stats
import mesa as ms 
import matplotlib.pyplot as plt
from Functions import truncated_normal_rvs


#TODO:
# Update
# Memory

class Commuter():
    '''
    Agent class for commuters
    '''
    def __init__(self, unique_id, modes_of_transport = ['Ferry', 'Speedboat']):
        '''
        Initialize the agent
        args: 
            unique_id: int, unique identifier for the agent
        '''
        self.unique_id = unique_id
        self.state = np.random.choice(modes_of_transport)
        self.pref_price, self.pref_crowd, self.pref_time = truncated_normal_rvs(0.0, 1.0, 0.5, 0.5/3, 3)
        self.choice([0,1])

        self.memory = {}
        for mode in modes_of_transport:
            print(mode)
            self.memory[mode] = {'Price': 0, 'Density': 0, 'Time': 0}
        print(self.memory)


    def choice(self, mode_of_transport):
        mode_utility = {}

        for mode in mode_of_transport:
            mode_utility[mode] = self.utility(mode)

        best_option = max(mode_utility, key=mode_utility.get)

        return best_option


    def utility(self, mode):
        self.memory[mode]['Price'].append(mode.price)
        self.memory[mode]['Density'].append(mode.density)
        self.memory[mode]['Time'].append(mode.time)
        
        if len(self.memory[mode]['Price']) > 5:
            average_price_memory = np.mean(self.memory['Price'][-5:])
            average_density_memory = np.mean(self.memory['Density'][-5:])
            average_time_memory = np.mean(self.memory['Time'][-5:])
        else:
            average_price_memory = np.mean(self.memory['Price'])
            average_density_memory = np.mean(self.memory['Density'])
            average_time_memory = np.mean(self.memory['Time'])

        return self.pref_price*average_price_memory +self.pref_crowd*average_density_memory + self.pref_time*average_time_memory



agent = Commuter(0)





"""
This part is for running the model. The argparse part asks the user to give a command-line argument for the number of agents.
"""
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run an agent-based model simulation.")
#     parser.add_argument('--num_agents', type=int, default=1000, help='Number of agents in the simulation')
    
#     args = parser.parse_args()
    
#     main(args.num_agents)
        




