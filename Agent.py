import numpy as np
from scipy import stats
import mesa as ms 
import matplotlib.pyplot as plt
import argparse

#To do:
# - Travel time (per tijdstap/gebeurtenis definieren)
# - States ( A of B, en mogelijk tussenin)



class Commuter():
    '''
    Agent class for commuters
    '''
    def __init__(self, unique_id, n_agents = 1000): # n_agents moet gekoppeld worden aan de command-line arg
        '''
        Initialize the agent
        args: 
            unique_id: int, unique identifier for the agent
        '''
        self.unique_id = unique_id
        self.init_population(n_agents)


    def truncated_normal_rvs(self, x_min = 0.0, x_max= 1.0, loc = 0.5, scale= 0.5/3, size = 2): 
        '''
        Create truncated normal random variables for preferences
        arg:
            x_min:  float, minimum value
            x_max:  float, maximum value
            loc:    float, mean of the normal distribution
            scale:  float, standard deviation of the normal distribution
            size:   int, number of random variables
        '''

        # Define upper and lower quantiles
        quantile1 = stats.norm.cdf(x_min, loc=loc, scale=scale)
        quantile2 = stats.norm.cdf(x_max, loc=loc, scale=scale)

        # return the truncated normal variable from the distribution
        return stats.norm.ppf(
            np.random.uniform(quantile1, quantile2, size=size),
            loc=loc,
            scale=scale)
    
    def skewed_data(self, skew_parameter=0, loc= 1.0, scale=1.0, size= 1): \
        # skew_parameter=0, want er is geen skew! Kan ook verwijderd worden; ik heb het voor nu op 0 gezet.
        '''
        Create truncated skewed random variables
        agrs: 
            skew_parameter: float, skew parameter 
            loc:            float, mean of the normal distribution
            scale:          float, standard deviation of the normal distribution
            size:           int, number of random variables
        '''

        data = stats.skewnorm.rvs(skew_parameter, loc=loc, scale=scale, size=size)
        data = np.round(data,2).astype(float) # Round to 2 decimals

        # Fixing Limitation for truncation
        for d_ix, d_value in enumerate(data):
            print(d_ix, d_value)
            if d_value < 0:
                print(d_ix, d_value, data[d_ix])
                data[d_ix] = 0
                print(d_ix, d_value, data[d_ix])
            elif d_value > 1:
                print(d_ix, d_value, data[d_ix])
                data[d_ix] = 1
                print(d_ix, d_value, data[d_ix])

        # Check if it worked
        
        assert data.any() < 0 or data.any() > 1, "Not All Data is between 0 and 1"

        return data
   
    def Preferences(self):
        '''
        Set the Preferences using the random variables function:
            pref_price: The degree to which an agent prefers lower prices.
            pref_crowd: The degree to which an agent (dis)likes crowdedness.
            pref_time: The degree to which an agent dislikes time spent in transportation.
        '''

        preferences = self.truncated_normal_rvs(0.0, 1.0, 0.5, 0.5/3, 3)
        self.pref_price = preferences[0]
        self.pref_crowd = preferences[1]
        self.pref_time = preferences[2]

    def init_population(self, n_agent=1000): #num_agent van command-line arg
        '''
        Define the two states of the agents:
            0: Island A
            1: Island B

        args:
            n_agent: int, number of agents
        '''

        for i in range(n_agent):
            state = np.random.choice([0,1])

        self.new_agent(state)

    def new_agent(self, state):
        '''
        Make a new agent
        '''
        self.state = state
    
    def price_sensitivity(self):
        # Price sensitivity
        self.price_sensitivity = self.skewed_data(20.0, 0.1, 0.3, 10000)

    def run(self):
        self.Preferences()
        self.init_population()
        self.price_sensitivity()


agent = Commuter(0)

agent.run()


print()
# data = Commuter(0)
# data = data.skewed_data(20.0, 0.1, 0.3, 10000)

# if data.any() < 0 or data.any() > 1:
#     raise ValueError("Data is not between 0 and 1")

# bins = np.linspace(-1, 2, 100)
# plt.hist(data, bins, alpha=1, label='histogram')
# plt.legend(loc='upper right')
# plt.show()


# print(data)

"""
This part is for running the model. The argparse part asks the user to give a command-line argument for the number of agents.
"""
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run an agent-based model simulation.")
#     parser.add_argument('--num_agents', type=int, default=1000, help='Number of agents in the simulation')
    
#     args = parser.parse_args()
    
#     main(args.num_agents)
        




