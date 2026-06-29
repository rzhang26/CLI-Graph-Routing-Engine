from collections import deque
from typing import List, Tuple, Dict, Optional
import heapq
import json

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
    def shortest_path_BFS(self, start_name: str, target_name: str) -> List:
        
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
    def shortest_path_Djikstra(self, start_name: str, target_name: str) -> Tuple[List[str], float]:
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
    
    def save_to_file(self, filename: str) -> None:
        export_data = {}
        
        for source_name, node_obj in self.nodes.items():
            export_data[source_name] = []
            for edge in node_obj.edges:
                export_data[source_name].append({
                    'target': edge.target_name,
                    'distance': edge.distance
                })
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=4)

    def load_from_file(self, filename: str) -> None:
        with open(filename, 'r') as f:
            import_data = json.load(f)

        self.nodes.clear()
        loaded_edges = set()
         
        for source, edges in import_data.items():
            for edge_info in edges:
                target = edge_info['target']
                dist = edge_info['distance']

                edge_signiture = tuple(sorted([source, target]))

                if edge_signiture not in loaded_edges:
                    self.add_edge(source, target, dist, is_bidirectional=True)
                    loaded_edges.add(edge_signiture)

#file saver / parser testing
if __name__ == "__main__":
    # === STEP 1: Build the Original Network ===
    print("Creating original graph network...")
    original_graph = Graph()
    original_graph.add_edge("Downtown", "Midtown", 4.2)
    original_graph.add_edge("Midtown", "Uptown", 5.1)
    original_graph.add_edge("Midtown", "Suburbs", 8.0)
    original_graph.add_edge("Uptown", "Suburbs", 3.3)
    
    # Calculate a baseline path to compare against later
    orig_path, orig_dist = original_graph.shortest_path_Djikstra("Downtown", "Suburbs")
    print(f"Original path calculation: {' -> '.join(orig_path)} ({orig_dist}km)")

    # === STEP 2: Export to JSON ===
    test_filename = "validation_map.json"
    print(f"\nSaving network configuration out to '{test_filename}'...")
    original_graph.save_to_file(test_filename)

    # === STEP 3: Initialize a Fresh, Empty Graph ===
    print("\nInitializing a completely blank second graph workspace...")
    new_graph = Graph()
    print(f"Active nodes in new graph before load: {list(new_graph.nodes.keys())}")

    # === STEP 4: Import the Saved JSON Data ===
    print(f"\nLoading data back from '{test_filename}' into the blank workspace...")
    new_graph.load_from_file(test_filename)
    print(f"Active nodes in new graph after load: {list(new_graph.nodes.keys())}")

    # === STEP 5: Run Comparative Validation ===
    print("\nRunning final routing engine validation checks...")
    new_path, new_dist = new_graph.shortest_path_Djikstra("Downtown", "Suburbs")
    print(f"Post-load path calculation: {' -> '.join(new_path)} ({new_dist}km)")

    print("\n================ VERDICT ================")
    if orig_path == new_path and orig_dist == new_dist:
        print("SUCCESS! The data persistence round-trip is flawless.")
        print("The reconstructed graph yields identical routing results.")
    else:
        print("FAILURE: The loaded map does not match the original layout data.")
    print("=========================================")



#functional testing
# if __name__ == "__main__":
#     router = Graph()
    
#     router.add_edge("Downtown", "Suburbs", 14.5)
#     router.add_edge("Downtown", "Midtown", 4.2)
#     router.add_edge("Midtown", "Uptown", 5.1)
#     router.add_edge("Midtown", "Suburbs", 8.0)
#     router.add_edge("Uptown", "Suburbs", 3.3)
#     router.add_edge("Suburbs", "Airport", 22.1)
    
#     print("--- Current Graph Architecture ---")
#     router.display_graph()
#     print("\n----------------------------------")
    
#     start_loc = "Downtown"
#     end_loc = "Airport"
    
#     shortest_path, total_miles = router.shortest_path_Djikstra(start_loc, end_loc)
    
#     print(f"Calculating optimal path from {start_loc} to {end_loc}...")
#     if shortest_path:
#         path_str = " -> ".join(shortest_path)
#         print(f"Optimal Route Found: {path_str}")
#         print(f"Total Traveled Distance: {total_miles} km")
#     else:
#         print(f"Error: Route from {start_loc} to {end_loc} is disconnected.")


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