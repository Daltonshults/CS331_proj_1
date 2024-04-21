from node import CityNodeAStar
from queue import PriorityQueue
from distance_checker import EuclideanDistance, HaversineDistance

class AStarSearch:
    def __init__(self, country_map):
        self.frontier = PriorityQueue()
        self.reached = {}
        self.map = country_map

    def expand(self, current_node, city_to_weight_map, city_to_cords, goal, heuristic):
        nodes = []

        state = current_node.get_state()
        neighbors = city_to_weight_map[state]

        for neighbor in neighbors:
            s_prime = neighbor[0]
            
            cost = int(neighbor[1]) + current_node.get_path_cost()
            # Wrong should be between s_prime and goal
            h_score = heuristic(point_1 = city_to_cords[s_prime],
                                  point_2 = city_to_cords[goal])
            f_score = cost + h_score
            
            new_node = CityNodeAStar(state = s_prime,
                                     parent= current_node,
                                     action="Explored",
                                     path_cost = cost,
                                     h_score=h_score,
                                     f_score=f_score)
            nodes.append(new_node)

        return nodes

    def astar_search(self, initial, goal, city_to_weight_map, city_to_coords, heuristic):
        initial_h_score = heuristic(point_1 = city_to_coords[initial],
                                    point_2 = city_to_coords[goal])

        node = CityNodeAStar(state = initial,
                            parent=None,
                            action="Initial Node",
                            path_cost= 0,
                            h_score = initial_h_score,
                            f_score=initial_h_score)

        self.frontier.put(node)

        self.reached[initial] = node

        while not self.frontier.empty():

            node = self.frontier.get()

            if node.get_state() == goal:
                return node

            for child in self.expand(node, city_to_weight_map, city_to_coords, goal, heuristic):
                s = child.get_state()

                if s not in self.reached or child.get_path_cost() < self.reached[s].get_path_cost():
                    child.set_action("On Frontier")
                    self.reached[s] = child
                    self.frontier.put(child)

        return None
    
    def astar_search_haversine(self, initial, goal, city_to_weight_map, city_to_coords):
        return self.astar_search(initial, goal, city_to_weight_map, city_to_coords, HaversineDistance().distance)
    
    def astar_search_euclidean(self, initial, goal, city_to_weight_map, city_to_coords):
        return self.astar_search(initial, goal, city_to_weight_map, city_to_coords, EuclideanDistance().distance)