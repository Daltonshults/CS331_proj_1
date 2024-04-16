from map_parser import MapParser
from city_node import CityNode
from city_node_factory import CityNodeFactory
from map import CountryMap
from agent import MapAgent
import argparse

def arg_parsing():
    parser = argparse.ArgumentParser(description="Process a map file.")

    parser.add_argument('-algorithm',
                        type=str,
                        help="The algorithm to use.",
                        default="bsf",
                        nargs="?")
    
    parser.add_argument('-A',
                        type=str,
                        help="The A argument.",
                        nargs="?")
    
    parser.add_argument('-B',
                        type=str,
                        help="The B argument.",
                        nargs="?")
    
    parser.add_argument('-file',
                        type=str,
                        help="The file to process.",
                        default="./france.txt",
                        nargs="?")

    args = parser.parse_args()

    return args

def main():
    # parser = argparse.ArgumentParser(description="Process a map file.")

    # parser.add_argument('-algorithm',
    #                     type=str,
    #                     help="The algorithm to use.",
    #                     default="bsf",
    #                     nargs="?")
    
    # parser.add_argument('-A',
    #                     type=str,
    #                     help="The A argument.",
    #                     nargs="?")
    
    # parser.add_argument('-B',
    #                     type=str,
    #                     help="The B argument.",
    #                     nargs="?")
    
    # parser.add_argument('-file',
    #                     type=str,
    #                     help="The file to process.",
    #                     default="./france.txt",
    #                     nargs="?")

    # args = parser.parse_args()
    args = arg_parsing()

    if args.A == None or args.B == None:
        visiting = [
            ("brest", "nice"),
            ("montpellier", "calais"),
            ("stratsbourg", "bordeaux"),
            ("paris", "grenoble"),
            ("grenoble", "paris"),
            ("brest", "grenoble"),
            ("grenoble", "brest"),
            ("nice", "nantes"),
            ("caen", "strasbourg")            
            ]
    else:
        visiting = [(args.A, args.B)]

    print(visiting)
    print(args.algorithm)
    # print(args.A)
    # print(f"type A: {type(args.A)}\n\n")
    # print(args.B)
    # print(f"type B: {type(args.B)}\n\n")  
    mp = MapParser()

    cities, go_cities_with_weights, coordinates = mp.driver(args.file)

    # for i in range(len(cities)):
    #     print(f"cities[i]: {cities[i]}\ngo_cities_with_weights[i]: {go_cities_with_weights[i]}\ncoordinates[i]: {coordinates[i]}\n\n-----------------------------------\n")
    cnf = CityNodeFactory()
    node_list = cnf.create_city_nodes_from_lists(cities, go_cities_with_weights, coordinates)
    cm = CountryMap(node_list)
    cm.create_graph()
    # for i in node_list:
    #     print(i.city_name)
    #     print(i.go_cities_with_weights)
    #     print(i.coordinates)
    #     print("\n\n\n")

    graph = cm.get_graph()

    # for key in graph.keys():
    #     print(f"key: {key}\nvalue: {graph[key]}\n\n\n")

    # print(cm.get_city_node("paris"))
    # print(cm.get_city_node("dijon"))
    neighbors = cm.get_neighbors("paris")
    # print(neighbors)

    agent = MapAgent()

    grenoble = agent.move_cities("paris", "va-caen", cm)

    print(grenoble)

    print(graph)

    va = "va-paris"

    print(cm.strip_va(va))

    # for n in neighbors:
    #     print(f"n: {n}\nneighbors[n]: {neighbors[n]}\n\n\n")

if __name__ == "__main__":
    main()