from city_node import CityNode

class CityNodeFactory:

    def create_city_nodes_from_lists(self, cities, go_cities_with_weights, coordinates):
        node_list = []
        for i in range(len(cities)):
            node_list.append(CityNode(cities[i], coordinates[i], go_cities_with_weights[i]))

        return node_list