import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import argparse

class Transportation:
    """Base class for different modes of transportation.

        Attributes:
            start_location (str): Starting point of the transportation mode.
            end_location (str): Destination point of the transportation mode.
            capacity (int): Maximum number of users the transport can handle at once.
            base_price (float): Initial price without any dynamic pricing considerations.
            base_time (float): Base travel time without any delays.
            current_price (float): Updated price considering current conditions.
            time (float): Current travel time considering the latest updates.
            density (float): Current density of usage.
        """
    def __init__(self, start_location, end_location, capacity, base_price, base_time):
        
        self.capacity = capacity # Include possibility of max capacity for ferry
        self.current_price = base_price
        self.price = base_price
        self.base_time = base_time
        self.time = base_time
        self.density = 0

        self.number_of_mode_users = 0
        self.percentage_users = 0
        

        self.start_location = start_location # Start location as characteristic of mode
        self.end_location = end_location # Destination as characteristic of mode


    def update_conditions(self, number_of_mode_users):
        """Update the transport conditions based on the number of current users."""
        self.number_of_mode_users = number_of_mode_users
        self.update_percentage_users()
        self.update_density()
        self.update_time()
        self.update_price()

    def update_percentage_users(self):
        """Calculate the percentage of capacity currently used."""
        self.percentage_users = self.number_of_mode_users / self.capacity if self.capacity > 0 else 0

    def scale_time(self, time_value):
        # Normalize time to [1,10], using the following formula: 1+9*((value-min_value)/(max_value-min_value))
        normalized_time = int(1 + 9 * ((time_value - self.base_time)/((64 + self.base_time) - self.base_time)))
        self.time = normalized_time

    def update_density(self):
        """Placeholder for subclasses to implement specific density calculations."""
        pass

    def update_time(self):
        """Placeholder for subclasses to implement specific time updates."""
        pass


    def update_price(self):
        """Placeholder for future dynamic pricing implementations."""
        pass



class Ferry(Transportation):
    def update_density(self):  
        """Update the density based on the percentage of capacity used."""
        self.density = self.percentage_users * 10 # Scale the density to range [1,10]

    def update_time(self):
        """Update travel time based on current usage, with delays at high capacity."""
        # The ferry experiences delay if there are a lot of commuters e.g. 90% of total commuters
        if self.percentage_users > 0.9:
            self.time = self.base_time * 1.1 # 10% time increase at >90% capacity
        else:
            self.time = self.base_time

        self.scale_time(self.time)



class Speedboat(Transportation):
    def update_density(self):
        """Set density to 1 as speedboats are less likely to be affected by user density."""
        self.density = 1 

    def update_time(self):
        """Update travel time based on congestion levels."""
        # Speedboats experience "traffic jam" when more than 30% of total commuters are taking the speedboat
        if self.percentage_users >= 0.3:
            # Traffic congestion increases the travel time exponentially
            # Travel time increase per increase in percentage user: 
            # {0.3: +1min, 0.4: +4min, 0.5: +9 min, 0.6: +16min, 0.7: +25min, 0.8: +36min, 0.9: +49min, 1.0: +64min}
            congestion = ((self.percentage_users - 0.2) * 10)**2 
            self.time = self.base_time + congestion
    
        else:
            self.time = self.base_time

        self.scale_time(self.time)
        