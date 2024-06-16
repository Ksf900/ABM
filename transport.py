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
    def __init__(self, id, capacity, travel_cost, occupancy, travel_time):
        self.id = id
        self.capacity = capacity
        self.travel_cost = travel_cost
        self.occupancy = occupancy
        self.travel_time = travel_time


class Ferry:
    def __init__(self, id, capacity, travel_cost, occupancy, travel_time):
        super.__init__(id, capacity, travel_cost, occupancy, travel_time)
        self.id = id
        self.capacity = capacity
        self.travel_cost = travel_cost
        self.occupancy = occupancy
        self.travel_time = 5

class Speedboat():
    def __init__(self, id, capacity, travel_cost, occupancy, travel_time):
        super.__init__(id, capacity, travel_cost, occupancy, travel_time)
        self.id = id
        self.capacity = 1
        self.travel_cost = travel_cost
        self.occupancy = occupancy
        self.travel_time = 3
