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


    def update_conditions(self, number_of_mode_users, total_number_of_commuters, initial_ferry_score):
        """Update the transport conditions based on the number of current users."""
        self.number_of_mode_users = number_of_mode_users
        self.total_number_of_commuters = total_number_of_commuters
        self.initial_ferry_score = initial_ferry_score
        self.update_percentage_users()
        
        self.update_density()
        self.update_time()
        self.update_price()
        

    def update_percentage_users(self):
        """Calculate the percentage of commuters for a certain mode of transport."""
        self.percentage_users = self.number_of_mode_users / self.total_number_of_commuters
        # print(self.number_of_mode_users, self.capacity, self.percentage_users)


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
        """Update the density based on the number of commuters that used the ferry, using
        a sigmoid function.
    
        """
        self.density = 1 + (9/(1+np.exp(-10*((self.number_of_mode_users/self.capacity)-0.5))))
        print(f'Ferry: density={self.density}')

    def update_time(self):
        
        # The ferry experiences small delay until capacity, then steeper increase
        normalizing_factor = 10 - self.initial_ferry_score
        self.time = self.initial_ferry_score + (normalizing_factor/(1+np.exp(-2*((self.number_of_mode_users/self.capacity)-1)))) # Only increase significantly after capacity is reached
        print(f'Ferry: time={self.time}')

    
        
        
class Speedboat(Transportation):
    def update_density(self):
        """Update density of speedboats based on nr of mode users. Comfort may decrease because of time increase when there are loads of people."""
        self.density = 1 + (9/(1+np.exp(-10*((self.number_of_mode_users/self.total_number_of_commuters)-0.7))))
        print(f'Speedboat: density={self.density}')

    def update_time(self):
        """Update travel time based on congestion levels."""
        self.time = 1 + (9/(1+np.exp(-20*((self.number_of_mode_users/self.total_number_of_commuters)-0.3)))) # Research showed that traffic increases at 30% of car use
        print(f'Speedboat: time={self.time}')
        


        