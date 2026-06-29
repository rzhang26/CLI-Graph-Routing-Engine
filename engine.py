from graph import Graph
from typing import Optional

class RoutingEngineCLI:
    
    def __init__(self, graph: Graph):
        self.graph = graph

    def display_availible_nodes(self) -> None:
        locations = sorted(list(self.graph.nodes.keys()))
        print(f'\nAvailible nodes: {locations}')

    def prompt_valid_node(self, prompt_text: str) -> Optional[str]:
        while True:
            input_text = input(prompt_text).strip()

            if input_text.lower() == 'exit':
                return None
            if input_text in self.graph.nodes:
                return input_text
        
            print(f'Error: {input_text} is not a recognized location or is mispelled. Please try again.')

    def run(self) -> None:
        print('=======================================')
        print('    Initiating CLI Routing Engine     ')
        print('=======================================')

        while True:
            print('[ Main Menu Options ]')
            print('1. Find shortest path')
            print('2. Show current map topology')
            print('3. Exit system')

            choice = input('\nPlease select an option (1-3): ').strip()

            if choice == '1':
                if not self.graph.nodes:
                    print('\nError: The network is currently empty')
                    continue
                    
                self.display_availible_nodes()
                print('(Type "Exit" at any prompt to cancel)')

                start = self.prompt_valid_node('\nEnter starting location: ')
                if not start:
                    continue

                target = self.prompt_valid_node('\nEnter end location: ')
                if not target:
                    continue

                print(f'Calculating the shortest_path from "{start}" to "{target}"... ')
                path, total_dist = self.graph.shortest_path_Djikstra(start, target)

                print('------------------------------------')
                if path:
                    path_route = ' -> '.join(path)
                    print(f'Route Found: {path_route}')
                    print(f'Total Distance: {total_dist}')
                else:
                    print(f'No path can be constructed between {start} and {target}. ')
                print('------------------------------------')
            
            elif choice == '2':
                print('\n---Current Map Topology Structure---')
                self.display_availible_nodes()
                print('------------------------------------')
            
            elif choice == '3':
                print('\nShutting down engine routing system.')
                break
            else:
                print('Invalid command. Please select a valid option (1-3): ')
                continue

if __name__ == "__main__":
    # Pre-populate map infrastructure data
    network = Graph()
    network.add_edge("Downtown", "Suburbs", 14.5)
    network.add_edge("Downtown", "Midtown", 4.2)
    network.add_edge("Midtown", "Uptown", 5.1)
    network.add_edge("Midtown", "Suburbs", 8.0)
    network.add_edge("Uptown", "Suburbs", 3.3)
    network.add_edge("Suburbs", "Airport", 22.1)

    cli_app = RoutingEngineCLI(network)
    cli_app.run()
                