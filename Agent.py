import numpy as np
from scipy import stats
import mesa as ms 
import matplotlib.pyplot as plt
from Functions import truncated_normal_rvs

#TODO:
# Utility function
# Choice function
# 




class Commuter():
    '''
    Agent class for commuters
    '''
    def __init__(self, unique_id):
        '''
        Initialize the agent
        args: 
            unique_id: int, unique identifier for the agent
        '''
        self.unique_id = unique_id
        self.state = np.random.choice(['Ferry', 'Speedboat'])
        self.pref_price, self.pref_crowd, self.pref_time = truncated_normal_rvs(0.0, 1.0, 0.5, 0.5/3, 3)
        self.choice([0,1])


    def choice(self, mode_of_transport):
        x = {}

        for mode in mode_of_transport:
            x[mode] = self.utility(mode)

        best_option = max(x, key=x.get)

        return best_option


    def utility(self, mode):
        

   

agent = Commuter(0)

# agent.choice([0,1])
# agent.run()


# print()
# data = Commuter(0)
# data = data.skewed_data(20.0, 0.1, 0.3, 10000)

# if data.any() < 0 or data.any() > 1:
#     raise ValueError("Data is not between 0 and 1")

# bins = np.linspace(-1, 2, 100)
# plt.hist(data, bins, alpha=1, label='histogram')
# plt.legend(loc='upper right')
# plt.show()


# print(data)


        




