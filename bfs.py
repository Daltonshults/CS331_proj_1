from node import CityNode
from queue import Queue  as q

class BreadthFirstSearch:
    def __init__(self, country_map) -> None:
        self.frontier = q()
        self.reached = []
        self.map = country_map

    def expand(self, current_node):
        '''
        Used to generate children nodes of a node
        '''
        neighbors = self.map.get_neighbors(current_node.get_state())
        nieghbor_nodes = []

        for i in neighbors.keys():
            node = CityNode(state=i,
                            parent=current_node,
                            action="Explored",
                            path_cost=0)
            
            nieghbor_nodes.append(node)

        return nieghbor_nodes




    def search(self, intitial, goal):
        #print(f"\n------------------------------------------------------------------------------------------------------\n")
        # Initialize first node ROOT
        node = CityNode(state =intitial,
                        parent= None,
                        action="Initial",
                        path_cost=0)

        #If the node is the goal node return node]
        if node.get_state() == goal:
            return node

        # Add node to frontier, FIFO queue
        self.frontier.put(node)

        # Add node to reached set/list
        self.reached.append(node.get_state())

        # While frontier is not empty
        while not self.frontier.empty():
            
            # Node = frontier.pop()
            node = self.frontier.get()

            # For each child of the node    
            for child in self.expand(node):                

                # if node is the goal node return
                if child.get_state() == goal:
                    return child

                # if node not in reached set add node to reached
                if child.get_state() not in self.reached:
                    child.set_action("On Frontier")
                    self.reached.append(child.get_state())
                    self.frontier.put(child)

        return None
