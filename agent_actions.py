class AgentActions:

    def move_city_a_to_city_b(self, city_a, city_b, node):

        action = f"Moved from {city_a} to {city_b}"
        node.set_action(action)

