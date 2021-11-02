"""
name: Antonio Vinicius de Moura Rodrigues

sources:
- https://iq.opengenus.org/bron-kerbosch-algorithm/
- https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm

"""

import os
import random

class dolphinConnections():

    def average_agglomeration_coefficient(all_graph): #average Agglomeration Coefficient
        agglomeration_coefficient_list = []
        for key, value in sorted(all_graph.items()):
            possible_triangles = len(value)*(len(value)-1)/2 #calculates the possible triangles for each key
            
            if possible_triangles != 0: #if there are possible triangles, calculate how many there really are
                qty_triangles_list = []; aux_value = value.copy()

                for neighbor in value: #for each neighbor within value
                    existing_triangles_num = len(set(all_graph.get(neighbor)).intersection(aux_value))
                    aux_value.remove(neighbor) #remove the value of aux_value to not repeat triangles
                    qty_triangles_list.append(existing_triangles_num) #keep the number of triangles in a list

                agglomeration_coefficient_list.append(sum(qty_triangles_list)/possible_triangles)

            else: agglomeration_coefficient_list.append(0)

        return (sum(agglomeration_coefficient_list)/len(agglomeration_coefficient_list)) #returns the sum of the agglomeration coefficient divided by the number of nodes

    def bron_kerbosch_whitout_pivoting(all_graph, potential_clique=[], remaining_nodes=[], skip_nodes=[], depth=0): #bron kerbosch algorithm without pivoting #potential_click == R, remaining_nodes == P, skip_nodes == X

        if len(remaining_nodes) == 0 and len(skip_nodes) == 0:
            print(f'{sorted(potential_clique)}')
            return 1 #returns 1 to add to the amount of clicks found

        found_cliques = 0
        for node in remaining_nodes[:]: #for each node in the list of remaining nodes
            new_potential_clique = potential_clique + [node]
            new_remaining_nodes = [n for n in remaining_nodes if n in all_graph.get(node)]
            new_skip_list = [n for n in skip_nodes if n in all_graph.get(node)]
            
            found_cliques += dolphinConnections.bron_kerbosch_whitout_pivoting(all_graph, new_potential_clique, new_remaining_nodes, new_skip_list, depth + 1)

            remaining_nodes.remove(node)
            skip_nodes.append(node)

        return found_cliques

    def bron_kerbosch_with_pivoting(all_graph, potential_clique=[], remaining_nodes=[], skip_nodes=[], depth=0): ##bron kerbosch algorithm with pivoting #potential_click == R, remaining_nodes == P, skip_nodes == X

        if len(remaining_nodes) == 0 and len(skip_nodes) == 0:
            print(f'{sorted(potential_clique)}')
            return 1 #Returns 1 to add to the amount of clicks found

        found_cliques = 0

        pivot = random.choice(list(set(remaining_nodes).union(set(skip_nodes)))) #Choose a random pivot
        difference = list(set(remaining_nodes).difference(set(all_graph.get(pivot)))) 

        for node in difference:
            new_potential_clique = potential_clique + [node]
            new_remaining_nodes = [n for n in remaining_nodes if n in all_graph.get(node)]
            new_skip_list = [n for n in skip_nodes if n in all_graph.get(node)] 

            found_cliques += dolphinConnections.bron_kerbosch_with_pivoting(all_graph, new_potential_clique, new_remaining_nodes, new_skip_list, depth + 1)

            remaining_nodes.remove(node)
            skip_nodes.append(node)

        return found_cliques

    def main():
        adjacency_list = {}

        with open(f"{os.getcwd()}/data_input.txt") as file:
            dolphins_community = [line.rstrip('\n') for line in file] #saving each line to a list element
            dolphins_community.pop(0) #excluding the first line that brings info about the size of the matrix and the amount of inputs

        for network in dolphins_community:
            network_adjacency = [int(value) for value in network.split()] #separating the adjacencies of the network and keeping it in a list of numbers
            
            for element in network_adjacency:

                leftover = network_adjacency.copy() #making a copy of the adjacency
                leftover.remove(element) #leaving only the list with the elements without the element

                if adjacency_list.get(int(element)): #checks if there is already a key in adjacency_list with the same value as value
                    element_content = adjacency_list.get(int(element))
                    element_content.extend(leftover)
                    adjacency_list[int(element)] = element_content
                else:
                    adjacency_list[int(element)] = leftover #create the list if it doesn't already exist

        all_nodes = list(adjacency_list.keys()) #putting only the adjacency list keys into a separate list

        print(f"- Adjacency List:\n")
        for key, value in sorted(adjacency_list.items()): #printing the adjacency list
            print(f"{key} : {value}")

        print(f"\n\n- Clicks (Bron-Kerbosch without pivoting):\n")
        total_cliques_whitout_pivoting = dolphinConnections.bron_kerbosch_whitout_pivoting(all_graph=adjacency_list, remaining_nodes=all_nodes.copy())
        print(f"\nTotal clicks found with bron_kerbosch_whitout_pivoting: {total_cliques_whitout_pivoting}")

        print(f"\n\n- Clicks (Bron-Kerbosch with pivoting):\n")
        total_cliques_with_pivoting = dolphinConnections.bron_kerbosch_with_pivoting(all_graph=adjacency_list, remaining_nodes=all_nodes.copy())
        print(f"\nTotal clicks found with bron_kerbosch_with_pivoting: {total_cliques_with_pivoting}")

        average_agglomeration_coefficient_result = dolphinConnections.average_agglomeration_coefficient(all_graph=adjacency_list)
        print(f"\n\n- Average Graph Agglomeration Coefficient: {average_agglomeration_coefficient_result}")

if __name__ == "__main__":
    dolphinConnections.main()
