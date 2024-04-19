from node import Node
from queue import Queue  as q

class BreadthFirstSearch:
    def __init__(self, country_map) -> None:
        self.frontier = q()
        self.reached = []
        self.map = country_map

    def search(self, intitial, goal):
        ...
        # Initialize first node ROOT

        #If the node is the goal node return node

            # Add node to frontier, FIFO queue

            # Add node to reached set/list

            # While frontier is not empty

                # Node = frontier.pop()

                # For each child of the node

                    # if node iw the goal node return

                    # if node not in reached set add node to reached
