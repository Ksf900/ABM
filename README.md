# ABM

# Transportation Mode Choice Simulation

## Project Overview

This project focuses on simulating commuter behavior in choosing transportation modes between islands using agent-based modeling (ABM). The primary goal is to understand the impact of various policies, such as reducing ferry prices and increasing ferry capacities, on the usage of public transportation (ferry) versus private transportation (speedboat). The simulation uses a utility-based decision-making process influenced by factors such as travel time, density, and cost.

## Project Structure

The project is organized into several files, each handling different aspects of the simulation and analysis:

### 1. Agent Class
The `agent.py` file defines the `Commuter` class, representing individual agents (commuters) in the simulation. Each commuter has:
- Attributes: location, travel preferences (sensitivity to price, density, and time), and memory of past experiences.
- Methods: 
  - `choose_transportation`: Chooses the transportation mode based on utility maximization.
  - `update_memory`: Updates the commuter's memory with new experiences.
  - `utility`: Calculates the utility for a given mode based on historical data and a stochastic term.

### 2. Transportation Class
The `transportation.py` file defines the `Transportation` class and its subclasses (`Ferry` and `Speedboat`). Each transportation mode has:
- Attributes: start and end locations, capacity, base price, and base travel time.
- Methods:
  - `update_density`: Updates the density based on the number of users.
  - `update_time`: Updates the travel time based on the current density.
  - `update_price`: Updates the price dynamically.

### 3. Simulation Class
The `simulation.py` file defines the `Simulation` class, which orchestrates the entire simulation process. It includes:
- Attributes: number of commuters, number of days, number of islands, and transportation modes.
- Methods:
  - `run`: Executes the simulation over the specified number of days.
  - `create_transport_modes`: Initializes the transportation modes.
  - `collect_specific_results`: Collects results for specific attributes such as density, travel time, and price.
  - `return_percentage_ferry_users`: Returns the percentage of commuters using the ferry.

### 4. Analysis Jupyter Notebook
The `analysis.ipynb` file contains the actual experiments and plots. It includes:
- Initialization of the simulation environment with various parameters.
- Running the simulation for different scenarios (varying ferry capacities and prices).
- Collecting and analyzing the results.
- Generating plots to visualize the impact of policy changes on transportation mode usage.

## How to Run the Project

1. **Clone the Repository**: Clone this repository to your local machine.
   ```sh
   git clone <repository-url>
   cd <repository-directory>