from node import CityNode
from queue import LifoQueue

class DepthLimitedSearch:

    def __init__(self, country_map):
        self.frontier = LifoQueue()
        self.reached = []
        self.map = country_map

    def depth(self, node):
        '''
        Returns the depth of a node in a graph
        '''
        depth = 1

        while True:
            if node.get_parent() != None:
                depth += 1
                node = node.get_parent()
            else:
                break

        return depth

    def expand(self, current_node):
        '''
        Used to generate children nodes of a node
        '''
        neighbors = self.map.get_neighbors(current_node.get_state())
        nieghbor_nodes = []
        print(f"Current Node: {current_node.get_state()}\n")
        print(f"Neighbors: {neighbors}\n\n")

        for i in neighbors.keys():
            node = CityNode(state=i,
                            parent=current_node,
                            action=None,
                            path_cost=None)
            
            nieghbor_nodes.append(node)

        return nieghbor_nodes
    
    def pop_node_path(self):
        node = self.frontier.get()
        path = set()
        current = node.get_parent()
        while current != None:
            path.add(current.get_state())
            current = current.get_parent()

        return node, path





    def depth_limited_search(self, initial, goal, max_depth):
        # Add initial node to the frontier using a LIFO queue
        self.frontier.put(CityNode(initial, None, None, 0))
        print(f"Goal: {goal}\n\n")

        # Make result = failure
        print("result = None\n\n")
        result = None

        # while frontier is not empty
        i = 0
        while not self.frontier.empty():
            print(f"i: {i}")
            i += 1
            # Node = frontier.pop()
            node, path = self.pop_node_path()

            print(node.get_state())
            print(f"path: {path}")

            # if node is the goal return the node
            if node.get_state() == goal:
                return node
            
            # if the depth of node is greater than max_depth 
            if self.depth(node) > max_depth:
                # Result = 'cutoff'
                print("result = cutoff\n\n")
                result = "cutoff"
            
            # elif if it is not a cycle
            elif node.get_state() not in path:
                print(f"Node state not in path: {node.get_state()}\n")

                # for each child of the node expand()
                for child in self.expand(node):
                    
                    # Add child to frontier
                    self.frontier.put(child)

        return result


class IterativeDepthLimitedSearch:
    
    def __init__(self, country_map, depth_limited_search=None):
        if depth_limited_search is None:
            self.dls = DepthLimitedSearch(country_map)
        else:
            self.dls = depth_limited_search

    def iterative_depth_limited_search(self, initial, goal, max_depth):
        for depth in range(0, max_depth+1):
            print(f"Depth: {depth}\n\n")
            result = self.dls.depth_limited_search(initial, goal, depth)

            if result != "cutoff" and result != None:
                return result
            
        return None