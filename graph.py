from collections import deque
from typing import List, Tuple, Dict, Optional
import heapq

class Node:
    def __init__(self, name: str):
        self.name = name
        self.edges = []

    def add_edges(self, target_name:str, distance: float) -> None:
        edge = Edge(target_name, distance)
        self.edges.append(edge) 

class Edge:
    def __init__(self, target_name: str, distance: float):
        self.distance = distance
        self.target_name = target_name
        
    def __repr__(self) -> str:
        return f'Edge(to_node={self.target_name}, dist={self.distance}km)'

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name: str) -> Node:
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def add_edge(self, from_node: str, to_node: str, distance: float, is_bidirectional: bool=True) -> None:
        from_node_obj = self.add_node(from_node)
        to_node_obj = self.add_node(to_node)

        from_node_obj.add_edges(to_node, distance)
        if is_bidirectional:
            to_node_obj.add_edges(from_node, distance)

    def display_graph(self):
        for name, node in self.nodes.items():
            connections = [f'{edge.target_name} ({edge.distance})' for edge in node.edges]
            print(f'{name} -> {",".join(connections) if connections else "No connections"}')


    #alg for unweighted graph (dist=0 for all city connections)
    def find_path_BFS(self, start_name: str, target_name: str) -> List:
        
        #edge case
        if start_name not in self.nodes or target_name not in self.nodes:
            return None
        
        queue = deque([start_name])
        parent_map = {start_name: None}
        visited = set()
        visited.add(start_name)

        path_found = False

        while queue:
            curr_city = queue.popleft()

            #base case
            if curr_city == target_name:
                path_found = True
                break

            #layer traversal BFS
            for edge in self.nodes[curr_city].edges:
                neighbor_name = edge.target_node.name 

                if neighbor_name not in visited:
                    visited.add(neighbor_name)
                    parent_map[neighbor_name] = curr_city
                    queue.append(neighbor_name)
        
        if not path_found:
            return None

        reconstructed_path = []
        step = target_name
        while step:
            reconstructed_path.append(step)
            step = parent_map[step]

        return reconstructed_path[::-1]

    #alg for weighted graph (varying connection dists)
    def shortest_path(self, start_name: str, target_name: str) -> Tuple[List[str], float]:
        #edge case for invalid start/target lcoations 
        if start_name not in self.nodes or target_name not in self.nodes:
            return [], float('inf')
        
        distances = {node_name: float('inf') for node_name in self.nodes}
        distances[start_name] = 0

        previous = {node_name: None for node_name in self.nodes}

        priority_queue = [(0, start_name)]

        while priority_queue:
            curr_dist, curr_name = heapq.heappop(priority_queue)

            if curr_name == target_name:
                break
            if curr_dist > distances[curr_name]:
                continue

            curr_node = self.nodes[curr_name]
            for edge in curr_node.edges:
                neighbor = edge.target_name
                temp_dist = curr_dist + edge.distance

                if temp_dist < distances[neighbor]:
                    distances[neighbor] = temp_dist
                    previous[neighbor] = curr_name
                    heapq.heappush(priority_queue, (temp_dist, neighbor))

        if distances[target_name] == float('inf'):
            return [], float('inf')
        
        path = []
        curr_city = target_name
        while curr_city:
            path.append(curr_city)
            curr_city = previous[curr_city]
        
        return path[::1], distances[target_name]


#functional testing
if __name__ == "__main__":
    router = Graph()
    
    router.add_edge("Downtown", "Suburbs", 14.5)
    router.add_edge("Downtown", "Midtown", 4.2)
    router.add_edge("Midtown", "Uptown", 5.1)
    router.add_edge("Midtown", "Suburbs", 8.0)
    router.add_edge("Uptown", "Suburbs", 3.3)
    router.add_edge("Suburbs", "Airport", 22.1)
    
    print("--- Current Graph Architecture ---")
    router.display_graph()
    print("\n----------------------------------")
    
    start_loc = "Downtown"
    end_loc = "Airport"
    
    shortest_path, total_miles = router.shortest_path(start_loc, end_loc)
    
    print(f"Calculating optimal path from {start_loc} to {end_loc}...")
    if shortest_path:
        path_str = " -> ".join(shortest_path)
        print(f"Optimal Route Found: {path_str}")
        print(f"Total Traveled Distance: {total_miles} km")
    else:
        print(f"Error: Route from {start_loc} to {end_loc} is disconnected.")


# if __name__ == "__main__":
#     router = Graph()
    
#     cities = ["New York", "Boston", "Chicago", "Denver"]
#     for city in cities:
#         router.add_node(city)
        
#     router.add_edge("New York", "Boston", 0)
#     router.add_edge("Boston", "Chicago", 0)
#     router.add_edge("Chicago", "Denver", 0)
#     router.add_edge("New York", "Chicago", 0) # A direct route bypassing Boston!
    
#     start = "New York"
#     destination = "Denver"
#     route = router.find_path_BFS(start, destination)
    
#     print("--- CLI Routing Engine (BFS) Test ---")
#     if route:
#         print(f"Success! Shortest route from {start} to {destination}:")
#         print(" -> ".join(route))
#     else:
#         print(f"No route could be calculated between {start} and {destination}.")