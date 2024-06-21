import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from Functions import truncated_normal_rvs


class Commuter():
    '''
    Represents a commuter in a transportation simulation.
    
    Attributes:
        commuter_id (int): A unique identifier for the commuter.
        location (str): Current location of the commuter.
        modes_of_transportation (list): Available transportation modes.
        preferences (dict): Commuter's preferences for price, density, and time.
        memory (dict): Historical data of experiences with each transportation mode.
    '''
    def __init__(self, commuter_id, start_location, modes_of_transport):
        self.commuter_id = commuter_id
        self.location = start_location
        self.modes_of_transportation = modes_of_transport

        # Initialise preferences for price, density, and time
        self.pref_price, self.pref_density, self.pref_time = truncated_normal_rvs(0.0, 1.0, 0.5, 0.5/3, 3)
    
        # Agent memory concerning price, density, time for each transportation mode
        self.memory = {}
        for mode in self.modes_of_transportation:
            # Initialise a memory for each mode 
            self.memory[mode] = {'Price': [], 'Density': [], 'Time': []}
 
    
    def get_available_modes(self):
        """Returns a list of available transportation modes from the current location."""
        available_modes = []
        for mode in self.modes_of_transportation:
            if mode.start_location == self.location:
                available_modes.append(mode)
        return available_modes


    def update_location(self, chosen_mode):
        """Updates the commuter's chosen_modelocation based on the end location of the chosen transportation mode."""
        self.location = chosen_mode.end_location

    def update_memory(self, chosen_mode):
        """Updates memory for the chosen transportation mode with the latest trip data."""
        self.memory[chosen_mode]['Price'].append(chosen_mode.price)
        self.memory[chosen_mode]['Density'].append(chosen_mode.density)
        self.memory[chosen_mode]['Time'].append(chosen_mode.time)


    def choose_transportation(self):
        ''' Choose the best transportation mode based on utility, and only on available modes. '''
        
        # First, define the available modes
        available_modes = self.get_available_modes()

        mode_utility = {}
        
        # For each mode of transportation calculate the utility
        for mode in available_modes:
            mode_utility[mode] = self.utility(mode)

        # Define best mode of transport based on highest utility score
        best_option = max(mode_utility, key=mode_utility.get)
        
        # Update location of the commuter (this info is stored in the transport mode)
        self.update_location(best_option)

        return best_option

        
    def utility(self, mode, noise_std=0.01):
        ''' Calculate utility for a given mode based on historical data. '''
        if len(self.memory[mode]['Price']) > 0:
            average_price_memory = np.mean(self.memory[mode]['Price'][-5:])
            average_density_memory = np.mean(self.memory[mode]['Density'][-5:])
            average_time_memory = np.mean(self.memory[mode]['Time'][-5:])
        else:
            average_density_memory = average_price_memory = average_time_memory = 1

        stochastic_term = np.random.normal(0, noise_std)
        # stochastic_term = 0

        return (- self.pref_price * average_price_memory 
                - self.pref_density * average_density_memory 
                - self.pref_time * average_time_memory
                + stochastic_term)



