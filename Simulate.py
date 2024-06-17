from transport import Transportation, Ferry, Speedboat 
from Functions import truncated_normal_rvs, skewed_data
from Agent import Commuter
from Policy import Policy

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import mesa as ms

class Simulation:
    def __init__(self, num_commuters, num_steps, modes_of_transport, policies):
        '''
        Initialize the simulation.
        args:
            num_commuters: int, number of commuters
            num_steps: int, number of simulation steps
            modes_of_transport: list of transportation modes (Ferry, Speedboat)
            policies: list of policies to apply
        '''
        self.num_commuters = num_commuters
        self.num_steps = num_steps
        self.modes_of_transport = modes_of_transport
        self.policies = policies

        # Initialize commuters
        self.commuters = [Commuter(unique_id=i, modes_of_transport=self.modes_of_transport) for i in range(self.num_commuters)]
        
        # Initialize policies
        self.policy = Policy()
        for policy in policies:
            self.policy.define_policy(*policy)

    def run(self):
        '''
        Run the simulation.
        '''
        for step in range(self.num_steps):
            self.policy.apply_policy(self.modes_of_transport)
            
            for commuter in self.commuters:
                best_mode = commuter.choice_of_transportation(self.modes_of_transport)
                commuter.state = best_mode
                best_mode.update_occupancy(self.get_current_users(best_mode))

            self.update_transport_conditions()

            # Optionally, you can store the results at each step for later analysis
            # self.store_results(step)

    def get_current_users(self, mode):
        '''
        Get the number of commuters currently using a given mode of transport.
        args:
            mode: Transportation mode
        returns:
            int, number of current users
        '''
        return sum(1 for commuter in self.commuters if commuter.state == mode)

    def update_transport_conditions(self):
        '''
        Update the travel conditions for each mode of transport based on current usage.
        '''
        for mode in self.modes_of_transport:
            mode.update_travel_time()
    
    def store_results(self, step):
        '''
        Store the results of the simulation at each step.
        args:
            step: int, current simulation step
        '''
        # This function can be used to save simulation data for analysis
        pass


# Example usage
if __name__ == "__main__":
    # Define transportation modes
    ferry = Ferry(id=1, capacity=100, travel_cost=2.0, travel_time=30)
    speedboat = Speedboat(id=2, capacity=1, travel_cost=5.0, travel_time=10)
    modes_of_transport = [ferry, speedboat]

    # Define policies
    policies = [
        ('ferry', None, None), # Change ferry cost to 1.5
        ('speedboat', None, None) # Change speedboat capacity to 10
    ]

    # Create and run the simulation
    sim = Simulation(num_commuters=50, num_steps=10, modes_of_transport=modes_of_transport, policies=policies)
    sim.run()
    
# Analyzing and reporting data