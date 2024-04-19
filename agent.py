class MapAgent:
    '''
    This might be an innapropriate way to handle this. Maybe I need to contain
    the search algorithms within a class for each of them because they don't 
    all have a frontier and reached list.
    '''
    def __init__(self, current_city, frontier) -> None:
        if current_city is None:
            self.current_city = "paris"
        else:
            self.current_city = current_city
        self.frontier = frontier
        self.reached = [self.current_city]


    def move_cities(self, destination_city, map):
        neighbors = map.get_neighbors(self.current_city)
        if destination_city in neighbors:
            self.current_city = destination_city
            '''
            Experimenting with bfs here. I don't think the agent should handle all of this.
            Instead, it should just handle rebuilding the path and moving from a city to the next if needed.
            '''
            self.add_city_to_reached(destination_city)
            new_neighbors = map.get_neighbors(destination_city)

            for i in new_neighbors:
                if i not in self.reached:
                    self.add_city_to_frontier(i)

            return (destination_city, neighbors[destination_city])

    def get_current_city(self):
        return self.current_city
    
    def add_city_to_frontier(self, city):
        self.frontier.put(city)

    def remove_city_from_frontier(self):
        self.frontier.get()

    def add_city_to_reached(self, city):
        self.reached.append(city)
    
    def get_frontier(self):
        return self.frontier
    
    def get_reached(self):
        return self.reached