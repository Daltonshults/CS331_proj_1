class MapParser:

    def open_map(self, file_path):  # Add 'self' as the first argument
        strings = []
        try:
            with open(file_path, "r") as file:
                for line in file:
                    # Process each line here
                    strings.append(line.strip())
                    #print(line.strip())  # Example: Print each line

            return strings
                    
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except IOError:
            print(f"Error reading file '{file_path}'.")

    def arrow_split(self, lines):  # Add 'self' as the first argument
        split_lines_vertex = []
        split_lines_edges = []

        for i in lines:
            line = i.split(" --> ")
            split_lines_vertex.append(line[0])
            split_lines_edges.append(line[1])

        return split_lines_vertex, split_lines_edges
    
    def city_from_dms(self, split_lines_vertex):
        
        for vertex in split_lines_vertex:
            city_dms = vertex.split(" ")
            city = city_dms[0]


    
    def driver(self, file_path):
        lines = self.open_map(file_path)
        for line in lines:
            print(line)

        split_lines_vertex, split_lines_edges = self.arrow_split(lines)

        for i, j in zip(split_lines_vertex, split_lines_edges):
            print(f"\nVertex: {i}\nEdges: {j}\n")
            

def main():
    file_path = "./france.txt"
    mp = MapParser()
    mp.driver(file_path)


if __name__ == "__main__":
    main()