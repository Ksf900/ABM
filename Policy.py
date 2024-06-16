class Policy:
    def __init__(self):
        """
        Initialises the Policy class with an empty list to store changes (policies).
        Each policy can affect the cost and capacity or both of a specific transportation mode (ferry or private boat).
        """
        self.changes = []

    
    def define_policy(self, mode_type, cost=None, capacity=None):
        """
        Defines a new policy that will affect a specified mode. 
        The policy can modify either the cost, the capacity, or both.

        Parameters:
            mode_type (str): The type of transportation mode to which the policy will apply (e.g., ferry or private boat).
            cost (float, optional): The new cost to apply to the transport mode. If None, cost is not changed.
            capacity (int, optional): The new capacity to set for the transport mode. If None, capacity is not changed.
        """
        # Include all changes in the list if there are any, the changes are tuples 
        # so we can make a "waiting list" for policies
        self.changes.append((mode_type, cost, capacity))

    def apply_policy(self, transport_modes):
        """
        Applies defined policies to the respective transportation modes. This method iterates over all registered
        policies and modifies the cost and/or capacity of the transport modes that match the policy mode type.

        Parameters:
            transport_modes (list): A list of all transport modes available in the simulation.
        """
    
        for mode in transport_modes:
            for change in self.changes:
                if mode.mode_type == change[0]:
                    if change[1] is not None:
                        mode.cost = change[1] # Apply cost policy
                    if change[2] is not None:
                        mode.capacity = change[2] # Apply capacity policy

