from map_parser import MapParser
from city_node import CityNode  
from city_node_factory import CityNodeFactory

def main():
    file_path = "./france.txt"
    mp = MapParser()

    cities, go_cities_with_weights, coordinates = mp.driver(file_path)

    for i in range(len(cities)):
        print(f"cities[i]: {cities[i]}\ngo_cities_with_weights[i]: {go_cities_with_weights[i]}\ncoordinates[i]: {coordinates[i]}\n\n-----------------------------------\n")
    cnf = CityNodeFactory()
    node_list = cnf.create_city_nodes_from_lists(cities, go_cities_with_weights, coordinates)

    for i in node_list:
        print(i.city_name)
        print(i.go_cities_with_weights)
        print(i.coordinates)
        print("\n\n\n")

if __name__ == "__main__":
    main()