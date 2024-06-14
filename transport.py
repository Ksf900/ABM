import numpy as np
from scipy import stats
import mesa as ms 
import matplotlib.pyplot as plt
import argparse

class Ferry:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

    def transport(self, agents):
        transported_agents = agents[:self.capacity] # Dit moet nog aangepast worden
        # return transported_agents


class Speedboat():
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = 1

    def transport(self, agents):
        transported_agents = agents[:self.capacity] # Dit moet nog aangepast worden
