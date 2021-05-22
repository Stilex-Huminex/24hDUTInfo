class Node:
    # Initialize the class
    def __init__(self, position: (), parent: ()):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.position == other.position

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    # Print node
    def __repr__(self):
        return '({0},{1})'.format(self.position, self.f)


class MapManager:

    open_nodes = None
    closed_nodes = None
    plateau: [] = None

    def __init__(self, plat: str):
        self.open_nodes = []
        self.closed_nodes = []
        self.plat_str = plat

    def unwrap_plateau(self):
        def insert_newline(source_str, pos):
            return source_str[:pos] + "\n" + source_str[pos:]

        for i in range(31):
            self.plat_str = insert_newline(self.plat_str, (32 * i) + 31)

        self.plateau = self.plat_str.split('\n')

    def astar_search(self, start, end):

        # Create a start node and an goal node
        start_node = Node(start, None)
        goal_node = Node(end, None)

        # Add the start node
        self.open_nodes.append(start_node)

        # Loop until the open list is empty
        while len(self.open_nodes) > 0:
            # Sort the open list to get the node with the lowest cost first
            self.open_nodes.sort()
            # Get the node with the lowest cost
            current_node = self.open_nodes.pop(0)
            # Add the current node to the closed list
            self.closed_nodes.append(current_node)

            # Check if we have reached the goal, return the path
            if current_node == goal_node:
                path = []
                while current_node != start_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                # Return reversed path
                return path[::-1]
            # Unzip the current node position
            (x, y) = current_node.position
            # Get neighbors
            neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            # Loop neighbors
            for next_node in neighbors:
                # Get value from plat
                map_value = self.plateau.get(next_node)
                # Check if the node is a wall
                if map_value == '#':
                    continue
                # Create a neighbor node
                neighbor = Node(next_node, current_node)
                # Check if the neighbor is in the closed list
                if neighbor in self.closed_nodes:
                    continue
                # Generate heuristics (Manhattan distance)
                neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                    neighbor.position[1] - start_node.position[1])
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                    neighbor.position[1] - goal_node.position[1])
                neighbor.f = neighbor.g + neighbor.h
                # Check if neighbor is in open list and if it has a lower f value
                if self.add_to_open(neighbor):
                    # Everything is green, add neighbor to open list
                    self.open_nodes.append(neighbor)
        # Return None, no path is found
        return None

    # Check if a neighbor should be added to open list
    def add_to_open(self, neighbor):
        for node in self.open_nodes:
            if neighbor == node and neighbor.f >= node.f:
                return False
        return True


plateau = "RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRREEEREREEERERSREREREEEREREEHHERRRRERRRERRRRRHRRRRRHRRRERRRRRERRERERHEEREREHERHRERERHRERSRHHHRRRRRRERERRRRRERRRRRRRERERRRRRHRRSRHREREEHEEREHERERERHREESRSRERRRRERSRRRERRRRRERERHRERRRERERRRRERHREREREEERHRHREREREREREEERERRERRRRREREEERERRRERERRRRRRRERERRHREREREREEESHEHREEEEERERERERERRRRRRERRREEERRRRRRRHEERRRRRRRRRRHRERHRHRHEEEEREEEEEEHREREHESERRRRHRERHREEERRRRRRRERHRRRSRRRERRESERHEEREEHEEEERERERERHRHRSHERRRREREEERRRRRRRERERRRRRERERERRRREREEEEHREREHERERHEEREREEEREHERRRRRRERRRRRERERRRHRRRERRRRRRRERREEHEEESRHREREREEEREHHRERESERERRERSEERRRRRRRERRRRRHRRRERRRERSRREREEERERERHRERHSERERHEEREHERERRRRHRERERRRRRRRRRERERERRRRRRRERRERERERHESREEEEERERERHREEEREHERRRRRRERRRRRERRRRRRRRRRRERRRRRRRREHEEEREEEREREHEREHHRSREREREEERREEEEERRRRRERRREREEERERERRRERRRRESSEERERHREEEEERHEERHREHEEEEERRRRRRRRRRERRRRRERHEERRRERERERRRRHRERSHHRERERERHEEEEHESSRERERERRERERRRRRHRRRRRRRRRHRRRRRRRERRRREEERERERHEESESHREEEEEHERERERERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR"
