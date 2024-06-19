from transport import Ferry, Speedboat
from Functions import truncated_normal_rvs
from Agent import Commuter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector

# Steps for simulation should be something like this:
# 1. initialise commuters

# 2. choose location for a commuter

# 3. collect amount of commuters taking a certain mode of transport

# 4. update the conditions of the transportation modes (after each iteration/day)

# 5. per commuter that used e.g. Ferry_AB it should update the memory of that specific ferry 
# after each iteration and after updating the conditions of the transport because the transport class 
# contains functions for calculating price, density, and time etc(this is quite difficult i think)

# 6. start at 2.


# It works mostly but I think the transportation class with the time implementation can be improved still.


class Simulation:
    def __init__(self, num_commuters, num_days, ferry_capacity, ferry_base_price, ferry_base_time,
                 speedboat_base_price, speedboat_base_time):
        self.num_commuters = num_commuters
        self.num_days = num_days
        self.ferry_AB = Ferry("Island_A", "Island_B", ferry_capacity, ferry_base_price, ferry_base_time)
        self.speedboat_AB = Speedboat("Island_A", "Island_B", 200, speedboat_base_price, speedboat_base_time)  # Assume a smaller fixed capacity for speedboats
        self.ferry_BA = Ferry("Island_B", "Island_A", ferry_capacity, ferry_base_price, ferry_base_time)
        self.speedboat_BA = Speedboat("Island_B", "Island_A", 200, speedboat_base_price, speedboat_base_time)
        self.commuters = [Commuter(i, "Island_A", [self.ferry_AB, self.speedboat_AB, self.speedboat_BA, self.ferry_BA]) for i in range(num_commuters)]
        self.results = []

    def run(self):
        for day in range(self.num_days):
            # Collect choices for the day
            daily_choices = {mode: 0 for mode in [self.ferry_AB, self.speedboat_AB, self.ferry_BA, self.speedboat_BA]}
            commuter_choices = {}

            for commuter in self.commuters:
                chosen_mode = commuter.choose_transportation()
                daily_choices[chosen_mode] += 1
                commuter_choices[commuter] = chosen_mode
            
            # Update conditions based on the collected choices
            for mode, num_users in daily_choices.items():
                mode.update_conditions(num_users)

            # Update memory of each commuter after conditions have been updated
            for commuter, chosen_mode in commuter_choices.items():
                commuter.update_memory(chosen_mode)

            # Record the day's results
            self.record_day(day)

    def record_day(self, day):
        self.results.append({
            'day': day,
            'ferry_AB_users': self.ferry_AB.number_of_mode_users,
            'speedboat_AB_users': self.speedboat_AB.number_of_mode_users,
            'ferry_BA_users': self.ferry_BA.number_of_mode_users,
            'speedboat_BA_users': self.speedboat_BA.number_of_mode_users,
            'ferry_AB_density': self.ferry_AB.density,
            'speedboat_AB_density': self.speedboat_AB.density,
            'ferry_BA_density': self.ferry_BA.density,
            'speedboat_BA_density': self.speedboat_BA.density,
            'ferry_AB_time': self.ferry_AB.time,
            'speedboat_AB_time': self.speedboat_AB.time,
            'ferry_BA_time': self.ferry_BA.time,
            'speedboat_BA_time': self.speedboat_BA.time
        })

    def plot_results(self):
        days = [result['day'] for result in self.results]
        
        ferry_AB_users = [result['ferry_AB_users'] for result in self.results]
        speedboat_AB_users = [result['speedboat_AB_users'] for result in self.results]
        ferry_BA_users = [result['ferry_BA_users'] for result in self.results]
        speedboat_BA_users = [result['speedboat_BA_users'] for result in self.results]

        ferry_AB_times = [result['ferry_AB_time'] for result in self.results]
        speedboat_AB_times = [result['speedboat_AB_time'] for result in self.results]
        ferry_BA_times = [result['ferry_BA_time'] for result in self.results]
        speedboat_BA_times = [result['speedboat_BA_time'] for result in self.results]

        plt.figure(figsize=(12, 10))
        
        plt.subplot(2, 1, 1)
        plt.plot(days, ferry_AB_users, label='Ferry AB Users')
        plt.plot(days, speedboat_AB_users, label='Speedboat AB Users')
        plt.plot(days, ferry_BA_users, label='Ferry BA Users')
        plt.plot(days, speedboat_BA_users, label='Speedboat BA Users')
        plt.xlabel('Day')
        plt.ylabel('Number of Users')
        plt.legend()
        plt.title('Number of Users per Transportation Mode')

        plt.subplot(2, 1, 2)
        plt.plot(days, ferry_AB_times, label='Ferry AB Time')
        plt.plot(days, speedboat_AB_times, label='Speedboat AB Time')
        plt.plot(days, ferry_BA_times, label='Ferry BA Time')
        plt.plot(days, speedboat_BA_times, label='Speedboat BA Time')
        plt.xlabel('Day')
        plt.ylabel('Travel Time')
        plt.legend()
        plt.title('Travel Time per Transportation Mode')

        plt.tight_layout()
        plt.show()

# Example usage
simulation = Simulation(
    num_commuters=200, 
    num_days=30, 
    ferry_capacity=200, 
    ferry_base_price=5, 
    ferry_base_time=40, 
    speedboat_base_price=5, 
    speedboat_base_time=20
)

simulation.run()
simulation.plot_results()




################################################################################
class Simulation:
    def __init__(self, num_commuters, num_days, ferry_capacity, ferry_base_price, ferry_base_time,
                 speedboat_base_price, speedboat_base_time):
        self.num_commuters = num_commuters
        self.num_days = num_days
        self.ferry_AB = Ferry("Island_A", "Island_B", ferry_capacity, ferry_base_price, ferry_base_time)
        self.speedboat_AB = Speedboat("Island_A", "Island_B", 200, speedboat_base_price, speedboat_base_time)
        self.ferry_BA = Ferry("Island_B", "Island_A", ferry_capacity, ferry_base_price, ferry_base_time)
        self.speedboat_BA = Speedboat("Island_B", "Island_A", 200, speedboat_base_price, speedboat_base_time)
        self.commuters = [Commuter(i, "Island_A", [self.ferry_AB, self.speedboat_AB, self.ferry_BA, self.speedboat_BA]) for i in range(num_commuters)]

        self.datacollector = DataCollector(
            model_reporters={
                'day': lambda m: m.current_day,
                'ferry_AB_users': lambda m: m.ferry_AB.number_of_mode_users,
                'speedboat_AB_users': lambda m: m.speedboat_AB.number_of_mode_users,
                'ferry_BA_users': lambda m: m.ferry_BA.number_of_mode_users,
                'speedboat_BA_users': lambda m: m.speedboat_BA.number_of_mode_users,
                'ferry_AB_density': lambda m: m.ferry_AB.density,
                'speedboat_AB_density': lambda m: m.speedboat_AB.density,
                'ferry_BA_density': lambda m: m.ferry_BA.density,
                'speedboat_BA_density': lambda m: m.speedboat_BA.density,
                'ferry_AB_time': lambda m: m.ferry_AB.time,
                'speedboat_AB_time': lambda m: m.speedboat_AB.time,
                'ferry_BA_time': lambda m: m.ferry_BA.time,
                'speedboat_BA_time': lambda m: m.speedboat_BA.time
            }
        )
        self.current_day = 0

    def step(self):
        daily_choices = {mode: 0 for mode in [self.ferry_AB, self.speedboat_AB, self.ferry_BA, self.speedboat_BA]}
        commuter_choices = {}

        for commuter in self.commuters:
            chosen_mode = commuter.choose_transportation()
            daily_choices[chosen_mode] += 1
            commuter_choices[commuter] = chosen_mode

        for mode, num_users in daily_choices.items():
            mode.update_conditions(num_users)

        for commuter, chosen_mode in commuter_choices.items():
            commuter.update_memory(chosen_mode)

        self.datacollector.collect(self)
        self.current_day += 1

    def run(self):
        for _ in range(self.num_days):
            self.step()
        self.export_data()

    def export_data(self, filename='simulation_data.csv'):
        df = self.datacollector.get_model_vars_dataframe()
        df.to_csv(filename)
        print(f"Data exported to {filename}")

    def plot_results(self):
        df = self.datacollector.get_model_vars_dataframe()

        plt.figure(figsize=(12, 10))

        plt.subplot(2, 1, 1)
        plt.plot(df.index, df['ferry_AB_users'], label='Ferry AB Users')
        plt.plot(df.index, df['speedboat_AB_users'], label='Speedboat AB Users')
        plt.plot(df.index, df['ferry_BA_users'], label='Ferry BA Users')
        plt.plot(df.index, df['speedboat_BA_users'], label='Speedboat BA Users')
        plt.xlabel('Day')
        plt.ylabel('Number of Users')
        plt.legend()
        plt.title('Number of Users per Transportation Mode')

        plt.subplot(2, 1, 2)
        plt.plot(df.index, df['ferry_AB_time'], label='Ferry AB Time')
        plt.plot(df.index, df['speedboat_AB_time'], label='Speedboat AB Time')
        plt.plot(df.index, df['ferry_BA_time'], label='Ferry BA Time')
        plt.plot(df.index, df['speedboat_BA_time'], label='Speedboat BA Time')
        plt.xlabel('Day')
        plt.ylabel('Travel Time')
        plt.legend()
        plt.title('Travel Time per Transportation Mode')

        plt.tight_layout()
        plt.show()
        
    def plot_specific_results(self, metrics):
        data = self.datacollector.get_model_vars_dataframe()

        plt.figure(figsize=(12, 10))
        
        for metric in metrics:
            plt.plot(data.index, data[metric], label=metric.replace('_', ' ').title())
        
        plt.xlabel('Day')
        plt.ylabel('Value')
        plt.legend()
        plt.title('Specific Metrics over Time')
        plt.tight_layout()
        plt.show()

# Example usage
simulation = Simulation(
    num_commuters=200,
    num_days=30,
    ferry_capacity=200,
    ferry_base_price=5,
    ferry_base_time=40,
    speedboat_base_price=5,
    speedboat_base_time=20
)

simulation.run()
simulation.plot_results()

data = pd.read_csv("simulation_data.csv")
data.plot()

# Plot specific results, type in name of speicific result using ''
metrics_to_plot = [
    'ferry_BA_density', 'speedboat_BA_density'
]

simulation.plot_specific_results(metrics_to_plot)