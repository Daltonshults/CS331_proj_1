from queue import PriorityQueue
from node import CityNode
class UniformCostSearch:

    def __init__(self, country_map):
        self.frontier = PriorityQueue()
        self.reached = {}
        self.map = country_map

    def expand(self, current_node, city_to_weight_map):

        nodes = []
        print(f"Current Node: {current_node.get_state()}")
        print(f"Neighbors: {city_to_weight_map[current_node.get_state()]}")
        state = current_node.get_state()
        neighbors = city_to_weight_map[state]

        for neighbor in neighbors:
            print(f"Neighbor: {neighbor}")
            print(f"Neighbor[0]: {neighbor[0]}")
            print(f"Neighbor[1]: {neighbor[1]}")
            s_prime = neighbor[0]

            cost = int(neighbor[1]) + current_node.get_path_cost()

            new_node = CityNode(s_prime, current_node, None, cost)
            nodes.append(new_node)

        return nodes


    def uniform_cost_search(self, initial, goal, city_to_weight_map):
        # Set initial node
        node = CityNode(initial, None, None, 0)

        # Put node in priority queue
        self.frontier.put(node)

        # Put node into reached with a value of 0
        self.reached[initial] = node
        
        # While frontier is not empty do
        while not self.frontier.empty():

            # node = frontier.pop()
            node = self.frontier.get()
            print(f"Node: {node}")
            # If problem is goal state then return node
            if node.get_state() == goal:
                return node
            
            # for each child of the current node EXPAND do
            for child in self.expand(node, city_to_weight_map):

                # s = child.state
                s = child.get_state()

                # if s is not in reached or child.PATH-COST < reached[s].PATH-COST then
                if s not in self.reached or child.get_path_cost() < self.reached[s].get_path_cost():
                    # reached[s] = child
                    self.reached[s] = child
                    # add child to frontier
                    self.frontier.put(child)
                    
        # return failure
        return None