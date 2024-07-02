import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import argparse

class Transportation:
    """
    Base class for different modes of transportation.

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
        """
        Initialises a new Transportation instance.

        Args:
            start_location (str): Starting point of the transportation mode.
            end_location (str): Destination point of the transportation mode.
            capacity (int): Maximum number of users the transport can handle at once.
            base_price (float): Initial price without any dynamic pricing considerations.
            base_time (float): Base travel time without any delays.
        """
        self.capacity = capacity # Include possibility of max capacity for ferry
        self.current_price = base_price
        self.price = base_price
        self.base_time = base_time
        self.time = base_time
        self.density = 0

        self.number_of_mode_users = 0
        self.percentage_users = 0

        self.start_location = start_location 
        self.end_location = end_location 


    def update_conditions(self, number_of_mode_users, total_number_of_commuters, initial_ferry_score):
        """
        Update the transport conditions based on the number of current users.

        Args:
            number_of_mode_users (int): Number of users currently using this mode of transport.
            total_number_of_commuters (int): Total number of commuters.
            initial_ferry_score (float): Initial score representing ferry conditions.
        """
        # Update state variables of class
        self.number_of_mode_users = number_of_mode_users
        self.total_number_of_commuters = total_number_of_commuters
        self.initial_ferry_score = initial_ferry_score
        self.update_percentage_users()
        
        # Update density, time, price
        self.update_density()
        self.update_time()
        self.update_price()
        

    def update_percentage_users(self):
        """Calculate the percentage of commuters for a certain mode of transport."""
        self.percentage_users = self.number_of_mode_users / self.total_number_of_commuters

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
    """
    Represents a ferry mode of transportation.
    """
    
    def update_density(self):  
        """
        Update the density based on the number of commuters using the ferry.
        If capacity is not reached, there is a linear increase in density until 5.
        If capacity is exceeded, there is an exponential increase from 5 to 10.
        """
        # Linear increase until 5 points
        if self.number_of_mode_users <= self.capacity:
            self.density = 1 + 4 * (self.number_of_mode_users / self.capacity)
        else:
            # Exponential increase until 10 points
            excess_users = self.number_of_mode_users - self.capacity
            excess_max = self.total_number_of_commuters - self.capacity
            self.density = 5 + (5/(1+np.exp(-15*((excess_users/excess_max)-0.2))))

    def update_time(self):
        """
        Update the travel time based on the number of commuters and initial ferry score.
        The ferry experiences small delays until capacity is reached, then steeper increases.
        """
        # The ferry experiences small delay until capacity then steep increase when capacity is reached (sigmoid)
        normalizing_factor = 10 - self.initial_ferry_score
        self.time = self.initial_ferry_score + (normalizing_factor/(1+np.exp(-2*((self.number_of_mode_users/self.capacity)-1)))) 

        

class Speedboat(Transportation):
    """
    Represents a speedboat mode of transportation.
    """

    def update_density(self):
        """
        Update density of speedboats based on nr of mode users, with a sigmoid. 
        Midpoint is 60% of commuters, indicating a steep increase only after 60% of commuters use the speedboat. 
        """
        self.density = 1 + (9/(1+np.exp(-10*((self.number_of_mode_users/self.total_number_of_commuters)-0.6))))

    def update_time(self):
        """
        Update travel time based on congestion levels, with a sigmoid.
        Midpoint is 35% since research has shown that traffic jam establishes, when 30-40% of commuters take the car.
        """
        self.time = 1 + (9/(1+np.exp(-20*((self.number_of_mode_users/self.total_number_of_commuters)-0.35)))) 


        