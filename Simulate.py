from transport import Ferry, Speedboat
from Functions import truncated_normal_rvs
from Agent import Commuter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector

class Simulation:
    def __init__(self, num_commuters, num_days, islands, capacity, ferry_base_price, ferry_base_time,
                 speedboat_base_price, speedboat_base_time, transport_restrictions=None):
        self.num_commuters = num_commuters
        self.num_days = num_days
        self.islands = islands
        self.transport_modes = []  # Initialize transport_modes as an empty list
        self.transport_restrictions = transport_restrictions if transport_restrictions else {}

        self.create_transport_modes(islands, capacity, ferry_base_price, ferry_base_time, speedboat_base_price, speedboat_base_time)
        self.commuters = [Commuter(i, np.random.choice(islands), self.transport_modes) for i in range(num_commuters)]

        self.datacollector = DataCollector(
            model_reporters=self.create_data_collectors()
        )

        self.initial_ferry_score = (ferry_base_time - speedboat_base_time)/ (ferry_base_time + speedboat_base_time)
        
    def create_transport_modes(self, islands, capacity, ferry_base_price, ferry_base_time, speedboat_base_price, speedboat_base_time):
        for i, island_start in enumerate(islands):
            for island_end in islands[i+1:]:
                allowed_modes = self.transport_restrictions.get((island_start, island_end), {'Ferry', 'Speedboat'})
                if 'Ferry' in allowed_modes:
                    self.transport_modes.append(Ferry(island_start, island_end, capacity, ferry_base_price, ferry_base_time))
                    self.transport_modes.append(Ferry(island_end, island_start, capacity, ferry_base_price, ferry_base_time))
                if 'Speedboat' in allowed_modes:
                    self.transport_modes.append(Speedboat(island_start, island_end, capacity, speedboat_base_price, speedboat_base_time))
                    self.transport_modes.append(Speedboat(island_end, island_start, capacity, speedboat_base_price, speedboat_base_time))

    def create_data_collectors(self):
        data_collectors = {}
        for mode in self.transport_modes:
            mode_key = f'{type(mode).__name__}_{mode.start_location}_{mode.end_location}'
            data_collectors[f'{mode_key}_users'] = (lambda m, mode=mode: mode.number_of_mode_users)
            data_collectors[f'{mode_key}_time'] = (lambda m, mode=mode: mode.time)
            data_collectors[f'{mode_key}_density'] = (lambda m, mode=mode: mode.density)
            data_collectors[f'{mode_key}_price'] = (lambda m, mode=mode: mode.price)
        return data_collectors

    def run(self):
        for day in range(self.num_days):
            daily_choices = {mode: 0 for mode in self.transport_modes}
            commuter_choices = {}

            for commuter in self.commuters:
                chosen_mode = commuter.choose_transportation()
                daily_choices[chosen_mode] += 1
                commuter_choices[commuter] = chosen_mode

            for mode, num_users in daily_choices.items():
                mode.update_conditions(num_users, self.num_commuters, self.initial_ferry_score)
                # print(num_users)

            for commuter, chosen_mode in commuter_choices.items():
                commuter.update_memory(chosen_mode)

            self.datacollector.collect(self)

    def plot_specific_results(self, metrics):
        data = self.datacollector.get_model_vars_dataframe()

        plt.figure(figsize=(15, 8))
        
        for metric in metrics:
            plt.plot(data.index, data[metric], label=metric.replace('_', ' ').title())
        
        plt.xlabel('Day')
        plt.ylabel('Number of Commuters')
        plt.legend()
        plt.title('Users per Transportation Mode')
        plt.tight_layout()
        plt.xticks(np.arange(min(data.index), max(data.index)+1, 1))
        plt.grid(True)
        plt.show()
        
    def plot_percentage_ferry_users(self, metrics):
        data = self.datacollector.get_model_vars_dataframe()
        num_Ferry_users = 0
        for metric in metrics:
            if metric[0] == 'F':
                num_Ferry_users += data[metric]

        percentage_Ferry_users = num_Ferry_users / self.num_commuters
        
        plt.figure(figsize=(20, 8))
        plt.plot(data.index, percentage_Ferry_users)
        plt.xlabel('Day')
        plt.ylabel('Percentage of commuters using the Ferry')
        plt.legend()
        plt.title('Percentage Ferry users')
        plt.tight_layout()
        plt.xticks(np.arange(min(data.index), max(data.index)+1, 1))
        plt.grid(True)
        plt.show()


islands = ["Island_A", "Island_B", "Island_C"]

# Example usage with transport restrictions (restrictions are which mode to use)
# transport_restrictions = {
#     ("Island_C", "Island_D"): {"Speedboat"},
#     ("Island_D", "Island_C"): {"Speedboat"}
# }

simulation = Simulation(
    num_commuters=200,
    num_days=60,
    islands=islands,
    capacity=200,
    ferry_base_price=1,
    ferry_base_time=40,
    speedboat_base_price=6,
    speedboat_base_time=10,
)

simulation.run()

# Plot specific results
metrics_to_plot = [
    'Ferry_Island_A_Island_B_users', 'Ferry_Island_A_Island_C_users', 'Ferry_Island_B_Island_C_users',
    'Ferry_Island_B_Island_A_users', 'Ferry_Island_C_Island_A_users', 'Ferry_Island_C_Island_B_users',
    'Speedboat_Island_A_Island_B_users', 'Speedboat_Island_A_Island_C_users', 'Speedboat_Island_B_Island_C_users',
    'Speedboat_Island_B_Island_A_users', 'Speedboat_Island_A_Island_C_users', 'Speedboat_Island_C_Island_B_users'
]

simulation.plot_specific_results(metrics_to_plot)

###########################################

islands = ["Island_A", "Island_B"]

# # Example usage with transport restrictions (restrictions are which mode to use)
# # transport_restrictions = {
# #     ("Island_C", "Island_D"): {"Speedboat"},
# #     ("Island_D", "Island_C"): {"Speedboat"}
# # }

simulation = Simulation(
    num_commuters=1000,
    num_days=100,
    islands=islands,
    capacity=1000,
    ferry_base_price=1,
    ferry_base_time=40,
    speedboat_base_price=6,
    speedboat_base_time=20,
)

simulation.run()

# Plot specific results
metrics_to_plot = [
    'Ferry_Island_A_Island_B_users',
    'Ferry_Island_B_Island_A_users', 
    'Speedboat_Island_A_Island_B_users', 
    'Speedboat_Island_B_Island_A_users'
]

simulation.plot_percentage_ferry_users(metrics_to_plot)