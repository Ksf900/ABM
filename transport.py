import numpy as np
from scipy import stats
import mesa as ms 
import matplotlib.pyplot as plt
import argparse


"""
Mode of Transport Class: containt different transportation options available in the
simulation, like ferries and private boats.
– mode type: specifies type of transportation, eg ’ferry’ or ’private boat’.
– travel cost: current cost to use this transport mode.
– occupancy level: how crowded this mode of transport is currently.
– travel time: the current estimated travel time for this mode of transport.
– adjust conditions(new travel cost, new occupancy, new travel time): up-
dates transport cost, crowding, and travel time based on external factors like policy
changes or demand shifts. Accepts new values for cost, crowding, and travel time as
inputs
"""

class Transportation:
    def __init__(self, id, capacity, travel_cost, travel_time):
        self.id = id
        self.capacity = capacity
        self.travel_cost = travel_cost
        self.occupancy = 0 # This updates dynamically so initially set to 0
        self.travel_time = travel_time

    def adjust_conditions(self, new_travel_cost=None, new_occupancy=None, new_travel_time=None):
        if new_travel_cost is not None:
            self.travel_cost = new_travel_cost
        if new_occupancy is not None:
            self.occupancy = new_occupancy
        if new_travel_time is not None:
            self.travel_time = new_travel_time

    def update_occupancy(self, current_users):
        self.occupancy = current_users / self.capacity


class Ferry(Transportation):
    def update_travel_time(self):
        # Travel time increases by 1% for every 5% increase in capacity usage
        usage_percentage = (self.current_users / self.capacity)
        if usage_percentage > 1:
            usage_percentage = 1  # Cap the percentage to 100%
        self.travel_time = self.base_time * (1 + usage_percentage / 5)

class Speedboat(Transportation):
    def update_travel_time(self):
        # Travel time increases with more users
        congestion_effect = max(0, (self.current_users - 1) * 2)
        self.travel_time = self.base_time + congestion_effect
