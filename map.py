class CountryMap:
    def __init__(self, city_nodes):
        self.graph = {}
        self.city_nodes = city_nodes

    def create_graph(self):
        for city in self.city_nodes:
            self.graph[city.city_name] = {}

            for go_city in city.go_cities_with_weights:
                self.graph[city.city_name][go_city[0]] = go_city[1]

    def get_graph(self):
        return self.graph
    
    def get_city_node(self, city_name):
        if city_name in self.graph.keys():
            return self.graph[city_name]
        
    def get_neighbors(self, city_name):
        return self.graph[city_name]