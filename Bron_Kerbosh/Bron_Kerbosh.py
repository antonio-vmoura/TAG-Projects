#Nome: Antonio Vinicius de Moura Rodrigues
#Fontes: https://iq.opengenus.org/bron-kerbosch-algorithm/ , https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm , 

import os #Importando o biblioteca "os" para ler o arquivo .txt
import random #Importando a biblioteca "random" para escolher um pivo aleatorio

def average_agglomeration_coefficient(all_graph): #Coeficiente médio de Aglomeração
    agglomeration_coefficient_list = []
    for key, value in sorted(all_graph.items()):
        possible_triangles = len(value)*(len(value)-1)/2 #Calcula os possiveis triangulos de cada key
        
        if possible_triangles != 0: #Caso exista possiveis triangulos calcula quantos realemte existem
            qty_triangles_list = []; aux_value = value.copy()

            for neighbor in value: #Para cada vizinho dentro de value
                existing_triangles_num = len(set(all_graph.get(neighbor)).intersection(aux_value)) #retorna o numero de trinagulos existentes relacionado com neighbor  # all_graph.get(neighbor) Pega os vizinhos dos vizinhos (vizinhos distantes)
                aux_value.remove(neighbor) #Remove o valor de aux_value para nao repetir triangulos
                qty_triangles_list.append(existing_triangles_num) #Guarda em uma lista a quantidade de triangulos

            agglomeration_coefficient_list.append(sum(qty_triangles_list)/possible_triangles) #Guarda o coeficiente de aglomeracao em uma lista # sum(qty_triangles_list)/possible_triangles Faz o calculo do coeficiente de aglomeracao

        else: agglomeration_coefficient_list.append(0)

    return (sum(agglomeration_coefficient_list)/len(agglomeration_coefficient_list)) #Retorna a soma do oeficiente de aglomeracao dividido pela quantidade de "nos" # 0.258958

def bron_kerbosch_whitout_pivoting(all_graph, potential_clique=[], remaining_nodes=[], skip_nodes=[], depth=0): #Algoritimo de Bron Kerbosch sem o pivoteamento #potential_clique == R, remaining_nodes == P, skip_nodes == X 

    if len(remaining_nodes) == 0 and len(skip_nodes) == 0:
        print(f'{sorted(potential_clique)}')
        return 1 #Retorna 1 para somar na quantidade de cliques encontrados

    found_cliques = 0
    for node in remaining_nodes[:]: #Para cada no na lista de nos restantes
        new_potential_clique = potential_clique + [node]
        new_remaining_nodes = [n for n in remaining_nodes if n in all_graph.get(node)] #Pega a lista de vizinhos do "node"  #Verifica se n esta presente na lista de vizinhos do "node" #Adiciona na lista de "nos" restantes 
        new_skip_list = [n for n in skip_nodes if n in all_graph.get(node)] #Pega a lista de vizinhos do node #Verifica se n esta presente na lista de vizinhos do node #Adiciona na lista de "nos" já processados
        
        found_cliques += bron_kerbosch_whitout_pivoting(all_graph, new_potential_clique, new_remaining_nodes, new_skip_list, depth + 1)

        remaining_nodes.remove(node) #Removendo o no da lista de nos restantes
        skip_nodes.append(node) #Adicionando o no a lista de nos já visualizados

    return found_cliques

def bron_kerbosch_with_pivoting(all_graph, potential_clique=[], remaining_nodes=[], skip_nodes=[], depth=0): #Algoritimo de Bron Kerbosch com o pivoteamento #potential_clique == R, remaining_nodes == P, skip_nodes == X 

    if len(remaining_nodes) == 0 and len(skip_nodes) == 0:
        print(f'{sorted(potential_clique)}')
        return 1 #Retorna 1 para somar na quantidade de cliques encontrados

    found_cliques = 0

    pivot = random.choice(list(set(remaining_nodes).union(set(skip_nodes)))) #Escolhe um pivo aleatorio
    difference = list(set(remaining_nodes).difference(set(all_graph.get(pivot)))) 

    for node in difference:
        new_potential_clique = potential_clique + [node]
        new_remaining_nodes = [n for n in remaining_nodes if n in all_graph.get(node)] #Pega a lista de vizinhos do "node"  #Verifica se n esta presente na lista de vizinhos do "node" #Adiciona na lista de "nos" restantes 
        new_skip_list = [n for n in skip_nodes if n in all_graph.get(node)] #Pega a lista de vizinhos do node #Verifica se n esta presente na lista de vizinhos do node #Adiciona na lista de "nos" já processados
        
        found_cliques += bron_kerbosch_with_pivoting(all_graph, new_potential_clique, new_remaining_nodes, new_skip_list, depth + 1)

        remaining_nodes.remove(node) #Removendo o no da lista de nos restantes
        skip_nodes.append(node) #Adicionando o no a lista de nos já visualizados

    return found_cliques

def main():

    adjacency_list = {}

    with open(f"{os.getcwd()}/soc-dolphins.txt") as file:
        dolphins_community = [line.rstrip('\n') for line in file] #Guardando cada linha em um elemento da lista
        dolphins_community.pop(0) #Excluindo a primeira linha que traz infos sobre a o tamanho da matriz e a quantidade de inputs

    for network in dolphins_community:
        network_adjacency = [int(value) for value in network.split()] #Separando as adjacencias da rede e guarda em uma lista de numero
        
        for element in network_adjacency:

            leftover = network_adjacency.copy() #fazendo uma copia da adjacencia
            leftover.remove(element) #deixando apenas a lista com os elementos sem o element

            if adjacency_list.get(int(element)): #Verifica se ja existe uma chave em adjacency_list com o mesmo valor de value
                element_content = adjacency_list.get(int(element))
                element_content.extend(leftover)
                adjacency_list[int(element)] = element_content
            else:
                adjacency_list[int(element)] = leftover #Cria a lista caso ainda nao exista

    all_nodes = list(adjacency_list.keys()) #colocando apenas as chaves da lista de adjacencia dentro de uma lista separada

    print(f"Lista de adjacência:\n")
    for key, value in sorted(adjacency_list.items()): #Printando a lista de adjacencia
        print(f"{key} : {value}")

    print(f"\n\nCliques (Bron-Kerbosch sem pivoteamento):\n")
    total_cliques_whitout_pivoting = bron_kerbosch_whitout_pivoting(all_graph=adjacency_list, remaining_nodes=all_nodes.copy())
    print(f"\nTotal de cliques encontrados com bron_kerbosch_whitout_pivoting: {total_cliques_whitout_pivoting}")

    print(f"\n\nCliques (Bron-Kerbosch com pivoteamento):\n")
    total_cliques_with_pivoting = bron_kerbosch_with_pivoting(all_graph=adjacency_list, remaining_nodes=all_nodes.copy())
    print(f"\nTotal de cliques encontrados com bron_kerbosch_with_pivoting: {total_cliques_with_pivoting}")

    average_agglomeration_coefficient_result = average_agglomeration_coefficient(all_graph=adjacency_list)
    print(f"\n\nCoeficiente médio de Aglomeração do Grafo: {average_agglomeration_coefficient_result}")

if __name__ == "__main__":
    main()
