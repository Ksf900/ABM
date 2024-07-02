from IPython.display import clear_output
import SALib
clear_output()
print("Everything imported!")

#%matplotlib inline
from SALib.sample import saltelli
#from mesa.batchrunner import FixedBatchRunner
from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

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

# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 30
max_steps = 100
distinct_samples = 30 

# Set the outputs
model_reporters = {"Ferry users": lambda m: m.percentage_ferry_users}

# We get all our samples here
param_values = saltelli.sample(problem, distinct_samples, calc_second_order=False)

# READ NOTE BELOW CODE
batch = BatchRunner(Simulation, 
                    max_steps=max_steps,
                    variable_parameters={name:[] for name in problem['names']},
                    model_reporters=model_reporters)

count = 0
data = pd.DataFrame(index=range(replicates*len(param_values)), 
                                columns=['ferry_price', 'ferry_capacity'])
data['Run'], data['Pruces'], data['Capacities'] = None, None, None

for i in range(replicates):
    for vals in param_values: 
        # Change parameters that should be integers
        vals = list(vals)
        vals[2] = int(vals[2])
        # Transform to dict with parameter names and their values
        variable_parameters = {}
        for name, val in zip(problem['names'], vals):
            variable_parameters[name] = val

        batch.run_iteration(variable_parameters, tuple(vals), count)
        iteration_data = batch.get_model_vars_dataframe().iloc[count]
        iteration_data['Run'] = count # Don't know what causes this, but iteration number is not correctly filled
        data.iloc[count, 0:3] = vals
        data.iloc[count, 3:6] = iteration_data
        count += 1

        clear_output()
        print(f'{count / (len(param_values) * (replicates)) * 100:.2f}% done')

print(data)

Si_prices = sobol.analyze(problem, data['Prices'].values, print_to_console=True) # Using the `analyze()` method provided by SALib that performs Sobol analysis.
Si_capacities = sobol.analyze(problem, data['Capacities'].values, print_to_console=True)

# Function for plotting
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
    
for Si in (Si_prices, Si_capacities):
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
        uniform(loc=-np.pi, scale=2*np.pi),
        uniform(loc=-np.pi, scale=2*np.pi)], method='saltelli_2010')