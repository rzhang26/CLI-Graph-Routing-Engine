class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edges(self, target_node, distance):
        edge = Edge(target_node, distance)
        self.edges.append(edge) 

class Edge:
    def __init__(self, target_node, distance):
        self.distance = distance
        self.target_node = target_node
        
    def repr(self):
        return f'Edge(to_node={self.target_node}, dist={self.distance}km)'

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes[name] = Node(name)
        return self.nodes[name]

    def add_edge(self, from_node, to_node, distance, is_bidirectional: bool=True):
        from_node = self.add_node(from_node)
        to_node = self.add_node(to_node)

        from_node.add_edges(to_node, distance)
        if is_bidirectional:
            to_node.add_edges(from_node, distance)
        

    def display_graph(self):
        for name, node in self.nodes.items():
            connections = [f'{edge.target_node.name} ({edge.distance})' for edge in node.edges]
            print(f'{name} -> {','.join(connections) if connections else 'No connections'}')

#test script
# if __name__ == '__main__':
#     geo_map = Graph()
    
#     geo_map.add_edge('A', 'B', 5.2)
#     geo_map.add_edge('B', 'C', 10.5)
#     geo_map.add_edge('C', 'A', 12.1)

#     print("---Graph Repr Test ---")
#     geo_map.display_graph()