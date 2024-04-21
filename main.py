from map_parser import MapParser
from city_factory import CityFactory
from map import CountryMap
import argparse
from bfs import BreadthFirstSearch
from dls import IterativeDepthLimitedSearch
from ucs import UniformCostSearch
from astar import AStarEuclideanSearch, AStarHaversineSearch
from agent import Agent
from agent_actions import AgentActions

class LinePrinter:
    def print_line():
        print("------------------------------------------------------------------------------------------------------------------")

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

        # Beginning of results
        
        # BFS
        LinePrinter.print_line()
        print("bfs")
        agent.get_results(bfs_final_nodes, "bfs")

        # IDLS
        LinePrinter.print_line()
        print("idls")
        agent.get_results(idls_final_nodes, "idls")

        # UCS
        LinePrinter.print_line()
        print("ucs")
        agent.get_results(ucs_final_nodes, "ucs")

        # A* Euclidean
        LinePrinter.print_line()
        print("astar_e")
        agent.get_results(astar_e_final_nodes, "astar_e")

        # A* Haversine
        LinePrinter.print_line()
        print("astar_h")
        agent.get_results(astar_h_final_nodes, "astar_h")
    
    else:
        visiting = [(args.A, args.B)]
        algo = args.algorithm
        mp = MapParser()
        cnf = CityFactory()
        mg = MapGenerator()
        initial = args.A.lower()
        goal = args.B.lower()

        cities, go_cities_with_weights, coordinates = mp.driver(args.file)

        if initial not in cities or goal not in cities:
            print("One or both of the cities are not in the map.")
            return
        

        node_list = cnf.create_city_nodes_from_lists(cities,
                                                     go_cities_with_weights,
                                                     coordinates)
        
        city_to_weights_map = mg.get_city_to_weights_map(node_list)
        city_to_coordinates_map = mg.get_city_to_coordinates_map(node_list)
        
        cm = CountryMap(node_list)
        agent = Agent(None, None, None, cm, AgentActions)    

        if algo == "bfs":
            bfs = BreadthFirstSearch(cm)

            agent.set_algorithm(bfs)
            agent.set_goal_city(goal)
            agent.set_start_city(initial)

            bfs_final_node = agent.search()

            agent.get_results([bfs_final_node], "bfs")

        elif algo == "idls":
            idls = IterativeDepthLimitedSearch(cm)

            agent.set_algorithm(idls)
            agent.set_goal_city(goal)
            agent.set_start_city(initial)

            idls_final_node = agent.search()

            agent.get_results([idls_final_node], "idls")

        elif algo == "ucs":
            ucs = UniformCostSearch(country_map=cm,
                                    city_to_weight_map=city_to_weights_map)

            agent.set_algorithm(ucs)
            agent.set_goal_city(goal)
            agent.set_start_city(initial)

            ucs_final_node = ucs.uniform_cost_search(initial, goal)

            agent.get_results([ucs_final_node], "ucs")

        elif algo == "astar":
            astar_e = AStarEuclideanSearch(country_map=cm,
                                  city_to_weight_map=city_to_weights_map,
                                  city_to_coords=city_to_coordinates_map)
            
            agent.set_algorithm(astar_e)
            agent.set_goal_city(goal)
            agent.set_start_city(initial)
            
            astar_e_final_node = agent.search()

            agent.get_results([astar_e_final_node], "astar_e")

            astar_h = AStarHaversineSearch(country_map=cm,
                                           city_to_weight_map=city_to_weights_map,
                                           city_to_coords=city_to_coordinates_map)
            
            agent.set_algorithm(astar_h)
            agent.set_goal_city(goal)
            agent.set_start_city(initial)

            astar_e_final_node = agent.search()

            agent.get_results([astar_e_final_node], "astar_h")

        else:
            print("Invalid algorithm.")
            return

if __name__ == "__main__":
    main()