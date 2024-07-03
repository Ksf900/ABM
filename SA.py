from IPython.display import clear_output
import SALib
clear_output()
print("Everything imported!")

#%matplotlib inline
from SALib.sample import saltelli
from mesa import batch_run
from SALib.analyze import sobol
#from mesa.batchrunner import BatchRunner
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

from BatchRunner import *
from Simulate import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import pandas as pd

plt.style.use('default')

# We define our variables and bounds
problem = {
    'num_vars': 2,
    'names': ['ferry_price', 'ferry_capacity'],
    'bounds': [[1, 10], [200, 2000]]
}

# Generate samples
distinct_samples = 512
param_values = saltelli.sample(problem, distinct_samples, calc_second_order=False)

# Define the model reporters
model_reporters = {
    "Ferry_Users": lambda m: sum([mode.number_of_mode_users for mode in m.transport_modes if isinstance(mode, Ferry)])
}

# Prepare the BatchRunner
replicates = 10
max_steps = 100
batch = BatchRunner(Simulation, 
                    max_steps=max_steps,
                    variable_parameters={name: [] for name in problem['names']},
                    model_reporters=model_reporters)

# Prepare DataFrame to collect the results
data = pd.DataFrame(index=range(replicates * len(param_values)), 
                    columns=['ferry_base_price', 'ferry_base_time', 'speedboat_base_price', 'Run', 'Ferry_Users', 'Speedboat_Users'])

count = 0
for i in range(replicates):
    for vals in param_values:
        variable_parameters = {name: val for name, val in zip(problem['names'], vals)}
        batch.run_iteration(variable_parameters, tuple(vals), count)
        iteration_data = batch.get_model_vars_dataframe().iloc[count]
        iteration_data['Run'] = count
        data.iloc[count, :3] = vals
        data.iloc[count, 3:] = iteration_data
        count += 1
        print(f'{count / (len(param_values) * replicates) * 100:.2f}% done')

# Save the results
data.to_csv('simulation_results.csv', index=False)

# Perform sensitivity analysis
Y_ferry = data['Ferry_Users'].values
Y_speedboat = data['Speedboat_Users'].values

Si_ferry = sobol.analyze(problem, Y_ferry, print_to_console=True)
Si_speedboat = sobol.analyze(problem, Y_speedboat, print_to_console=True)

### Function to plot ###

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')
    
    
### Plotting ###

for Si in (Si_ferry, Si_speedboat):
    # First order
    plot_index(Si, problem['names'], '1', 'First order sensitivity')
    plt.show()

    # Total order
    plot_index(Si, problem['names'], 'T', 'Total order sensitivity')
    plt.show()    
    
###### Test ######
import scipy as sp 
from Simulate import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import pandas as pd
import numpy as np
from scipy.stats import sobol_indices, uniform

problem = {
    'num_vars': 2,
    'names': ['ferry_prices', 'ferry_capacitie'],
    'bounds': [np.arange(1, 11, 1), np.arange(200, 2200, 200)]
}

indices = sobol_indices(func=Simulation, n=512, dists=[
        uniform(loc=-np.pi, scale=2*np.pi),
        uniform(loc=-np.pi, scale=2*np.pi)], method='saltelli_2010')