from Transportation import Ferry, Speedboat
from Functions import truncated_normal_rvs
from Agent import Commuter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector

class Simulation:
    """
    Class representing the simulation of commuters choosing transportation modes over a number of days.

    Attributes:
        num_commuters (int): Number of commuters in the simulation.
        num_days (int): Number of days the simulation will run.
        islands (list): List of island names.
        transport_modes (list): List of available transport modes.
        transport_restrictions (dict): Restrictions on transportation between islands.
        commuters (list): List of commuter agents.
        datacollector (DataCollector): Object to collect data during the simulation.
        initial_ferry_score (float): Initial score representing ferry conditions.
    """
    
    def __init__(self, num_commuters=1000, num_days=80, islands=['A', 'B'], capacity=1000, ferry_base_price=6, ferry_base_time=40,
                 speedboat_base_price=6, speedboat_base_time=10, transport_restrictions=None):
        """
        Initialises the Simulation instance with the given parameters.

        Args:
            num_commuters (int): Number of commuters in the simulation.
            num_days (int): Number of days the simulation will run.
            islands (list): List of island names.
            capacity (int): Capacity of the transportation modes.
            ferry_base_price (float): Base price for ferry transportation.
            ferry_base_time (float): Base time for ferry transportation.
            speedboat_base_price (float): Base price for speedboat transportation.
            speedboat_base_time (float): Base time for speedboat transportation.
            transport_restrictions (dict, optional): Restrictions on transportation between islands.
        """
        self.num_commuters = num_commuters
        self.num_days = num_days
        self.islands = islands
        self.transport_modes = []  # Initialise transport_modes as an empty list
        self.transport_restrictions = transport_restrictions if transport_restrictions else {}

        # Create transportation modes based on provided parameters
        self.create_transport_modes(capacity, ferry_base_price, ferry_base_time, speedboat_base_price, speedboat_base_time)

        # Initialise commuters with random start locations
        self.commuters = [Commuter(i, np.random.choice(self.islands), self.transport_modes) for i in range(num_commuters)]

        # Initialise DataCollector to gather data during the simulation
        self.datacollector = DataCollector(
            model_reporters=self.create_data_collectors()
        )

        # Calculate the initial ferry score that is used to normalise the time points in Transportation
        self.initial_ferry_score = (ferry_base_time - speedboat_base_time) / (ferry_base_time + speedboat_base_time)
        
    def create_transport_modes(self, capacity, ferry_base_price, ferry_base_time, speedboat_base_price, speedboat_base_time):
        """
        Create transportation modes (ferry and speedboat) between islands.

        Args:
            islands (list): List of island names.
            capacity (int): Capacity of the transportation modes.
            ferry_base_price (float): Base price for ferry transportation.
            ferry_base_time (float): Base time for ferry transportation.
            speedboat_base_price (float): Base price for speedboat transportation.
            speedboat_base_time (float): Base time for speedboat transportation.
        """
        for i, island_start in enumerate(self.islands):
            for island_end in self.islands[i+1:]:
                # Get allowed modes between the pair of islands
                allowed_modes = self.transport_restrictions.get((island_start, island_end), {'Ferry', 'Speedboat'})
                
                # Create ferry transport modes if allowed
                if 'Ferry' in allowed_modes:
                    self.transport_modes.append(Ferry(island_start, island_end, capacity, ferry_base_price, ferry_base_time))
                    self.transport_modes.append(Ferry(island_end, island_start, capacity, ferry_base_price, ferry_base_time))
                
                # Create speedboat transport modes if allowed
                if 'Speedboat' in allowed_modes:
                    self.transport_modes.append(Speedboat(island_start, island_end, capacity, speedboat_base_price, speedboat_base_time))
                    self.transport_modes.append(Speedboat(island_end, island_start, capacity, speedboat_base_price, speedboat_base_time))

    def create_data_collectors(self):
        """
        Create a dictionary of data collectors for each transport mode.

        Returns:
            dict: A dictionary with data collectors for number of users, time, density, and price for each transport mode.
        """
        data_collectors = {}
        for mode in self.transport_modes:
            # Create a unique key for each mode based on its type and route
            mode_key = f'{type(mode).__name__}_{mode.start_location}{mode.end_location}'
            
            # Define data collection functions for users, time, density, and price
            data_collectors[f'{mode_key}_users'] = (lambda m, mode=mode: mode.number_of_mode_users)
            data_collectors[f'{mode_key}_time'] = (lambda m, mode=mode: mode.time)
            data_collectors[f'{mode_key}_density'] = (lambda m, mode=mode: mode.density)
            data_collectors[f'{mode_key}_price'] = (lambda m, mode=mode: mode.price)
        return data_collectors

    def run(self):
        """
        Run the simulation for the specified number of days.
        """
        for day in range(self.num_days):
            daily_choices = {mode: 0 for mode in self.transport_modes}
            commuter_choices = {}

            # Each commuter chooses a transportation mode
            for commuter in self.commuters:
                chosen_mode = commuter.choose_transportation()
                daily_choices[chosen_mode] += 1
                commuter_choices[commuter] = chosen_mode

            # Update the conditions for each mode based on the number of users
            for mode, num_users in daily_choices.items():
                mode.update_conditions(num_users, self.num_commuters, self.initial_ferry_score)

            # Update the memory of each commuter with the chosen mode
            for commuter, chosen_mode in commuter_choices.items():
                commuter.update_memory(chosen_mode)

            # Collect data at the end of each day
            self.datacollector.collect(self)

    def return_percentage_ferry_users(self):
        """
        Return the percentage of commuters using the ferry.
        """
        data = self.datacollector.get_model_vars_dataframe()
        num_Ferry_users = 0
        
        # Calculate the total number of ferry users
        for metric in data:
            if metric.startswith('Ferry'):
                num_Ferry_users += data[metric]

        # Calculate the percentage of ferry users
        percentage_Ferry_users = num_Ferry_users / self.num_commuters
        return percentage_Ferry_users
    
    
    def return_equilibrium_value(self):
        results = self.return_percentage_ferry_users()
        equilibrium_value = np.mean(results[-10:])

        return equilibrium_value
    

    def plot_specific_results(self, attribute='users', metrics=None):
        """
        Plot the results for specific attributes and metrics.

        Args:
            metrics (list): List of metrics to plot (e.g. Ferry_AB).
            attributes (str): Attributes to plot (e.g. density, time, price, users)
        """
    
        data = self.datacollector.get_model_vars_dataframe()

        plt.figure(figsize=(15, 8))
        
        # Plot each metric over the simulation days
        if metrics:
            for metric in metrics:
                    plt.plot(data.index, data[f'{metric}_{attribute}'], label=metric.replace('_', ' '))
        else:
            for metric in data:
                if metric.endswith(attribute):
                    plt.plot(data.index, data[metric], label=metric.replace('_', ' ').replace('users', ''))
        
        plt.xlabel('Time [a.u.]')
        plt.ylabel(f'{attribute}'.title())
        plt.legend()
        plt.title(f'{attribute} per Transportation Mode'.title())
        plt.tight_layout()
        plt.xticks(np.arange(min(data.index), max(data.index) + 1, 5))
        plt.grid(True)
        plt.show()
        
    def plot_percentage_ferry_users(self):
        """
        Plot the percentage of commuters using the ferry.
        """
        data = self.datacollector.get_model_vars_dataframe()
        num_Ferry_users = 0
        
        # Calculate the total number of ferry users
        for metric in data:
            if metric.startswith('Ferry'):
                num_Ferry_users += data[metric]

        # Calculate the percentage of ferry users
        percentage_Ferry_users = num_Ferry_users / self.num_commuters
    
        plt.figure(figsize=(20, 8))
        plt.plot(data.index, percentage_Ferry_users)
        plt.xlabel('Day')
        plt.ylabel('Percentage of Commuters Using the Ferry')
        plt.legend()
        plt.title('Percentage of Ferry Users')
        plt.tight_layout()
        plt.xticks(np.arange(min(data.index), max(data.index) + 1, 5))
        plt.grid(True)
        plt.show()

    