import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from Functions import truncated_normal_rvs

class Commuter:
    """
    Represents a commuter in a transportation simulation.
    
    Attributes:
        commuter_id (int): A unique identifier for the commuter.
        location (str): Current location of the commuter.
        modes_of_transportation (list): Available transportation modes.
        preferences (dict): Commuter's preferences for price, density, and time.
        memory (dict): Historical data of experiences with each transportation mode.
    """
    
    def __init__(self, commuter_id, start_location, modes_of_transportation):
        """
        Initialises a new Commuter instance.
        
        Args:
            commuter_id (int): The unique ID for the commuter.
            start_location (str): The initial location of the commuter.
            modes_of_transportation (list): The available transportation modes for the commuter.
        """
        self.commuter_id = commuter_id
        self.location = start_location
        self.modes_of_transportation = modes_of_transportation

        # Initialise preferences for price, density, and time using truncated normal distribution 
        self.pref_price, self.pref_density, self.pref_time = truncated_normal_rvs(0.0, 1.0, 0.5, 0.5/3, 3)
    
        # Initialise memory for each mode of transportation
        self.memory = {}
        for mode in self.modes_of_transportation:
            self.memory[mode] = {'Price': [], 'Density': [], 'Time': []}
    
    def get_available_modes(self):
        """
        Returns a list of available transportation modes from the current location.
        
        Returns:
            list: Available modes of transportation.
        """
        available_modes = []
        for mode in self.modes_of_transportation:
            if mode.start_location == self.location:
                available_modes.append(mode)
        return available_modes


    def update_location(self, chosen_mode):
        """
        Updates the commuter location based on the chosen transportation mode.
        
        Args:
            chosen_mode: The chosen transportation mode.
        """
        self.location = chosen_mode.end_location


    def update_memory(self, chosen_mode):
        """
        Updates memory for the chosen transportation mode with the latest trip data.
        
        Args:
            chosen_mode: The chosen transportation mode.
        """
        self.memory[chosen_mode]['Price'].append(chosen_mode.price)
        self.memory[chosen_mode]['Density'].append(chosen_mode.density)
        self.memory[chosen_mode]['Time'].append(chosen_mode.time)


    def choose_transportation(self):
        """
        Chooses the best transportation mode based on utility from available modes.
        
        Returns:
            The best transportation mode based on utility.
        """
        # Get the available modes
        available_modes = self.get_available_modes()

        mode_utility = {}
        
        # Calculate the utility for each available mode
        for mode in available_modes:
            mode_utility[mode] = self.utility(mode)

        # Select the best mode based on the highest utility score
        best_option = max(mode_utility, key=mode_utility.get)
        
        # Update the location of the commuter
        self.update_location(best_option)

        return best_option
        
    def utility(self, mode, noise_std=1):
        """
        Calculates utility for a given mode based on historical data.
        
        Args:
            mode: The transportation mode to calculate utility for.
            noise_std (float): The standard deviation of the noise term (default is 1).
        
        Returns:
            float: The calculated utility for the mode.
        """
        # Use last 5 days of historical data for calculation, if available
        if len(self.memory[mode]['Price']) > 0:
            average_price_memory = np.mean(self.memory[mode]['Price'][-5:])
            average_density_memory = np.mean(self.memory[mode]['Density'][-5:])
            average_time_memory = np.mean(self.memory[mode]['Time'][-5:])
        else:
            # Default values if no historical data is available
            average_density_memory = average_price_memory = average_time_memory = 1

        # Add a stochastic term to the utility
        stochastic_term = np.random.normal(0, noise_std)

        # Calculate utility based on preferences and historical data
        utility = (- self.pref_price * average_price_memory 
                   - self.pref_density * average_density_memory 
                   - self.pref_time * average_time_memory
                   + stochastic_term)

        return utility