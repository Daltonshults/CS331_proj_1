from map_parser import MapParser
from city_factory import CityFactory
from map import CountryMap
import argparse
from bfs import BreadthFirstSearch
from dls import IterativeDepthLimitedSearch
from ucs import UniformCostSearch
from astar import AStarEuclideanSearch, AStarHaversineSearch
from distance_checker import EuclideanDistance, HaversineDistance
from agent import Agent
from agent_actions import AgentActions

class ArgParser:        
    def arg_parsing():
        parser = argparse.ArgumentParser(description="Process a map file.")

        parser.add_argument('algorithm',
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
        
        parser.add_argument('file',
                            type=str,
                            help="The file to process.",
                            default="./france.txt",
                            nargs="?")

        args = parser.parse_args()

        return args

class MapGenerator:
    def get_city_to_weights_map(self, node_list):
        city_to_weights_map = {}

        for i in node_list:
            city_to_weights_map[i.get_city_name()] = i.get_go_cities_with_weights()

        return city_to_weights_map

    def get_city_to_coordinates_map(self, node_list):
        city_to_coordinates_map = {}

        for i in node_list:
            city_to_coordinates_map[i.get_city_name()] = i.get_coordinates()

        return city_to_coordinates_map

def main():
    args = ArgParser.arg_parsing()

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
        
        mp = MapParser()
        cnf = CityFactory()
        mg = MapGenerator()
        
        

        cities, go_cities_with_weights, coordinates = mp.driver(args.file)
        node_list = cnf.create_city_nodes_from_lists(cities,
                                                     go_cities_with_weights,
                                                     coordinates)
        
        city_to_weights_map = mg.get_city_to_weights_map(node_list)
        city_to_coordinates_map = mg.get_city_to_coordinates_map(node_list)
        
        cm = CountryMap(node_list)
        agent = Agent(None, None, None, cm, AgentActions)

        # Breadth-First Search ---------------------------------------------------------------------
        bfs_final_nodes = []
        for cities in visiting:
            bfs = BreadthFirstSearch(cm)

            agent.set_algorithm(bfs)
            agent.set_goal_city(cities[1])
            agent.set_start_city(cities[0])


            bfs_final_node = agent.search()
            bfs_final_nodes.append(bfs_final_node)


        # Iterative Deepening Depth-Limited Search -----------------------------------------------
        idls_final_nodes = []
        for cities in visiting:
            idls = IterativeDepthLimitedSearch(cm)
            
            agent.set_algorithm(idls)
            agent.set_goal_city(cities[1])
            agent.set_start_city(cities[0])

            idls_final_node = agent.search()
            idls_final_nodes.append(idls_final_node)


        # Uniform-Cost Search ---------------------------------------------------------------------
        ucs_final_nodes = []
        for cities in visiting:
            ucs = UniformCostSearch(country_map=cm,
                                    city_to_weight_map=city_to_weights_map)
            
            agent.set_algorithm(ucs)
            agent.set_goal_city(cities[1])
            agent.set_start_city(cities[0])
            
            ucs_final_node = ucs.uniform_cost_search(cities[0], cities[1])
            ucs_final_nodes.append(ucs_final_node)

        # A-Star Euclidean Search ---------------------------------------------------------------------------
        astar_e_final_nodes = []
        for cities in visiting:
            astar_e = AStarEuclideanSearch(country_map=cm,
                                  city_to_weight_map=city_to_weights_map,
                                  city_to_coords=city_to_coordinates_map)
            
            agent.set_algorithm(astar_e)
            agent.set_goal_city(cities[1])
            agent.set_start_city(cities[0])
            
            
            astar_e_final_node = agent.search()
            astar_e_final_nodes.append(astar_e_final_node)

        # A-Star Haversine Search ---------------------------------------------------------------------------
        astar_h_final_nodes = []
        for cities in visiting:
            astar_h = AStarHaversineSearch(country_map=cm,
                                  city_to_weight_map=city_to_weights_map,
                                  city_to_coords=city_to_coordinates_map)
            
            agent.set_algorithm(astar_h)
            agent.set_goal_city(cities[1])
            agent.set_start_city(cities[0])
            
            astar_h_final_node = agent.search()#astar_h.astar_search_haversine(cities[0], cities[1])
            astar_h_final_nodes.append(astar_h_final_node)

        print(f"Length of astar_h_final_nodes: {len(astar_h_final_nodes)}")
        list_of_paths = [[] for _ in range(len(visiting))]
        for search in range(len(astar_h_final_nodes)):
            
            current_node = astar_h_final_nodes[search]

            while current_node != None:
                list_of_paths[search].append(current_node)
                current_node = current_node.get_parent()

        copy_list_of_paths = list_of_paths[0].copy()

        copy_list_of_paths.reverse()        
        for i in copy_list_of_paths:
            print(i.get_state())





    else:
        visiting = [(args.A, args.B)]

    

    print(f"Visiting: {visiting}")
    print(f"Args Algo: {args.algorithm}")
    '''
    mp = MapParser()

    cities, go_cities_with_weights, coordinates = mp.driver(args.file)

    cnf = CityFactory()
    node_list = cnf.create_city_nodes_from_lists(cities, go_cities_with_weights, coordinates)
    cm = CountryMap(node_list)
    mg = MapGenerator()
    city_to_weights_map = mg.get_city_to_weights_map(node_list)

    print(f"City to Weights Map: {city_to_weights_map}")

    city_to_coordinates_map = mg.get_city_to_coordinates_map(node_list)

    print(f"City to Coordinates Map: {city_to_coordinates_map}")
    for i in visiting:

        astar = AStarSearch(cm)
        hd = HaversineDistance()
        print(f"\nStarting: {i[0]}\nEnding: {i[1]}")
        last_node = astar.astar_search_euclidean(i[0], i[1], city_to_weights_map, city_to_coordinates_map)

        current_node = last_node
        path = []
        while current_node !=None:
        
            path.append(current_node.get_state())


            current_node = current_node.get_parent()

        print(f"Path: {path[::-1]}")
    
    
    
    
    
    # for i in range(len(cities)):
    #     print(f"City: {cities[i]}\nGo Cities With Weights: {go_cities_with_weights[i]}")

    # print(type(node_list))

    # bfs = UniformCostSearch(cm)

    # expanded = bfs.best_first_search("paris", "nice", city_to_weights_map)

    # current_node = expanded
    # print(f"\n------------------------------------------------------------------------------------------------------------------\n")
    # while current_node != None:
    #     print(f"Current Node State: {current_node.get_state()}")
    #     if current_node.get_parent() == None:
    #         print("Current Node Parent: None")
    #         break
    #     else:
    #         current_node = current_node.get_parent()

    
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
    '''

if __name__ == "__main__":
    main()