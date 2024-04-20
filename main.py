from map_parser import MapParser
from city_factory import CityFactory
from map import CountryMap
import argparse
from bfs import BreadthFirstSearch
from dls import IterativeDepthLimitedSearch
from ucs import UniformCostSearch

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

def get_city_to_weights_map(node_list):
    city_to_weights_map = {}

    for i in node_list:
        city_to_weights_map[i.get_city_name()] = i.get_go_cities_with_weights()

    return city_to_weights_map

def main():
    args = arg_parsing()

    if args.A == None or args.B == None:
        visiting = [
            ("brest", "nice"),
            ("montpellier", "calais"),
            ("strasbourg", "bordeaux"),
            ("paris", "grenoble"),
            ("grenoble", "paris"),
            ("brest", "grenoble"),
            ("grenoble", "brest"),
            ("nice", "nantes"),
            ("caen", "strasbourg")            
            ]
    else:
        visiting = [(args.A, args.B)]

    print(f"Visiting: {visiting}")
    print(f"Args Algo: {args.algorithm}")
    mp = MapParser()

    cities, go_cities_with_weights, coordinates = mp.driver(args.file)

    cnf = CityFactory()
    node_list = cnf.create_city_nodes_from_lists(cities, go_cities_with_weights, coordinates)
    cm = CountryMap(node_list)
    cm.create_graph()

    # city_to_weights_map = {}

    # for i in node_list:
    #     print(f"Node list: {i.get_city_name()}\nNeighbors: {i.get_go_cities_with_weights()}")
    #     city_to_weights_map[i.get_city_name()] = i.get_go_cities_with_weights()
    city_to_weights_map = get_city_to_weights_map(node_list)

    print(f"City to Weights Map: {city_to_weights_map}")


    # for i in range(len(cities)):
    #     print(f"City: {cities[i]}\nGo Cities With Weights: {go_cities_with_weights[i]}")

    print(type(node_list))

    bfs = UniformCostSearch(cm)

    expanded = bfs.best_first_search("paris", "nice", city_to_weights_map)

    current_node = expanded
    print(f"\n------------------------------------------------------------------------------------------------------------------\n")
    while current_node != None:
        print(f"Current Node State: {current_node.get_state()}")
        if current_node.get_parent() == None:
            print("Current Node Parent: None")
            break
        else:
            current_node = current_node.get_parent()

    
    # for i in visiting:
    #     bfs = BreadthFirstSearch(cm)

    #     final_node = bfs.search(i[0], i[1])

    #     current_node = final_node

    #     while True:
    #         print(f"Current Node State: {current_node.get_state()}")
    #         if current_node.get_parent() == None:
    #             print("Current Node Parent: None")
    #             break
    #         #print(f"Current Node Parent: {current_node.get_parent().get_state()}")
    #         if current_node.get_parent() == None:
    #             break
    #         current_node = current_node.get_parent()

    # for i in visiting:
    #     dls = IterativeDepthLimitedSearch(cm)
    #     print(f"\n------------------------------------------------------------------------------------------------------------------\n")
    #     print(f"\nStarting: {i[0]}\nEnding: {i[1]}\n")
    #     final_node = dls.iterative_depth_limited_search(i[0], i[1], 10)
    #     current_node = final_node

    #     while True:
    #         print(f"Current Node State: {current_node.get_state()}")
    #         if current_node.get_parent() == None:
    #             print("Current Node Parent: None")
    #             break
    #         #print(f"Current Node Parent: {current_node.get_parent().get_state()}")
    #         if current_node.get_parent() == None:
    #             break
    #         current_node = current_node.get_parent()

    

            

    # bfs = BreadthFirstSearch(cm)

    # final_node = bfs.search("nice", "brest")

    # current_node = final_node

    # # while current_node.get_parent() != None:
    # #     print(current_node.get_city_name())
    # #     current_node = current_node.get_parent()

    # while True:
    #     print(f"Current Node State: {current_node.get_state()}")
    #     if current_node.get_parent() == None:
    #         print("Current Node Parent: None")
    #         break
    #     print(f"Current Node Parent: {current_node.get_parent().get_state()}")
    #     if current_node.get_parent() == None:
    #         break
    #     current_node = current_node.get_parent()

    # print(f"\n\n------------------------------------------------------------------------------------------------------------------\n\n")

    # dls = DepthLimitedSearch(cm)

    # final_node = dls.depth_limited_search("strasbourg", "toulouse", 4)
    # current_node = final_node

    
    # # graph = cm.get_graph()
    # print(f"Final Node: {final_node.get_state()}")

    # while True:
    #     print(f"Current Node State: {current_node.get_state()}")
    #     if current_node.get_parent() == None:
    #         print("Current Node Parent: None")
    #         break
    #     print(f"Current Node Parent: {current_node.get_parent().get_state()}")
    #     if current_node.get_parent() == None:
    #         break
    #     current_node = current_node.get_parent()
    # print(f"\n\n------------------------------------------------------------------------------------------------------------------\n\n")
    # idls = IterativeDepthLimitedSearch(cm)
    # final_node = idls.iterative_depth_limited_search("dijon", "rennes", 50)
    # current_node = final_node

    # while True:
    #     print(f"Current Node State: {current_node.get_state()}")
    #     if current_node.get_parent() == None:
    #         print("Current Node Parent: None")
    #         break
    #     print(f"Current Node Parent: {current_node.get_parent().get_state()}")
    #     if current_node.get_parent() == None:
    #         break
    #     current_node = current_node.get_parent()
    # # agent = MapAgent("caen", SimpleQueue())

    # # print(f"Agent's Current City: {agent.get_current_city()}")

    # # grenoble = agent.move_cities("paris", cm)

    # # print(f"Print agent.get_current_city() :{agent.get_current_city()}")

    # # print(f"agent get reached: {agent.get_reached()}")
    # # front = agent.get_frontier()
    # # print(f"Get Frontier: {front}")

    # # temp = []

    # # while not front.empty():
    # #     temp.append(front.get())
    # # print(f"we here-----------------------------------\n\n")
    # # for i in temp:
    # #     print(i)

if __name__ == "__main__":
    main()