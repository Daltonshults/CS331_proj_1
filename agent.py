class MapAgent:

    def __init__(self) -> None:
        ...

    def move_cities(self, current_city, destination_city, map):
        if destination_city in map.get_neighbors(current_city).keys():
            return (destination_city, map.get_neighbors(current_city)[destination_city])
        else:
            return None