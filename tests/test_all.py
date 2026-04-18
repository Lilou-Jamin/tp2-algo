import time
from datetime import timedelta

import src.graphs as graphs
import src.np_hard as np_hard
import src.probabilistic as probabilistic
import src.trees as trees

graph_data = {
    'A': ['B', 'C'],
    'B': ['A'],
    'C': ['A', 'B']
}

weighted_graph_data = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 1), ('D', 5)],
    'C': [('A', 2), ('B', 1), ('D', 8)],
    'D': [('B', 5), ('C', 8)]
}

graphe = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": [],
    "F": []
}

graphe_cycle = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A"]
}

graphe_tri_tipologique = {
    "A": ["C"],
    "B": ["C", "D"],
    "C": ["E"],
    "D": ["F"],
    "E": ["F"],
    "F": []
}

graphe_plus_court_chemin = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": ["F"],
    "E": ["F"],
    "F": []
}

print("---- Exercice 1 ----")  
print("Graphe à matrice d'adjacence")
graphs.MatrixGraph(['A', 'B', 'C'], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]).print()
print("Graphe à liste d'adjacence")
graphs.ListGraph(graph_data).print()
print("Graphe à liste d'adjacence pondéré")
weighted_list_graph = graphs.WeightedListGraph(weighted_graph_data)
weighted_list_graph.print()
print('\n graphe sous forme de matrice :')
graphs.MatrixGraph(['A', 'B', 'C'], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]).print()
print('\ngraphe sous forme de liste d\'adjacence :')
graphs.ListGraph(graph_data).print()
print("Test parcours dfs récursif :", graphs.dfs_recursif(graphe, "A"))
print("Test parcours dfs itératif :", graphs.dfs_iteratif(graphe, "A"))
print("Test si un graphe est cyclique :", graphs.contient_cycle_oriente(graphe_cycle))
print("Test si un graphe non orienté est cyclique :", graphs.contient_cycle_non_oriente(graphe_cycle))
print("Test tri tipologique :", graphs.tri_topologique_dfs(graphe_tri_tipologique))

input("\nAppuyez sur Entrée pour continuer vers l'exo 2")

print("\n---- Exercice 2 ----")  

graph_liste = graphs.ListGraph({
    'A': [('B', 4), ('C', 2)],
    'B': [('C', 3), ('D', 2), ('E', 3)],
    'C': [('B', 1), ('D', 4), ('E', 5)],
    'D': [('E', -5)],
    'E': []
})
distances, predecessors = graphs.bellman_ford(graph_liste, 'A')

graph_matrice = graphs.MatrixGraph(
    vertices = ['A', 'B', 'C', 'D', 'E'],
    matrix = [
        [0,    4,    2,    None, None],
        [None, 0,    3,    2,    3],
        [None, 1,    0,    4,    5],
        [None, None, None, 0,   -5],
        [None, None, None, None, 0]
    ]
)
distances2, predecessors2 = graphs.bellman_ford(graph_matrice, 'A')

print('\nTest Djikstra Heap avec graphe simple')
print(graphs.dijkstra_heap(weighted_list_graph, 'A'))
print('Test Djikstra Naïf avec graphe simple')
print(graphs.dijkstra_naif(weighted_list_graph, 'A'))

creux_sommets = 15000
creux_max_voisins = 3
print(f"Génération graphe creux... (V = {creux_sommets}, max {creux_max_voisins} voisins)")
start = time.time()
graphe_creux = graphs.generer_graphe_creux(creux_sommets, creux_max_voisins)
end = time.time()
print(f'Génération terminée en {timedelta(seconds=end - start)}')

# Note: la génération de graphe dense a plus de 3000 sommets peut prendre un temps
# significatif selon la machine, lancer ce test que lorsque nécessaire
#dense_sommets = 15000
# dense_sommets = 2000
# dense_prob_connecte = 0.90
# print(f"Génération graphe dense... (V = {dense_sommets}, {int(dense_prob_connecte * 100)}% connectés)")
# start = time.time()
# graphe_dense = graphs.generer_graphe_dense(2000, 0.90)
# graphe_dense = graphs.generer_graphe_dense(dense_sommets, dense_prob_connecte)
# end = time.time()
# print(f'Génération terminée en {timedelta(seconds=end - start)}')
# print("Test du plus court chemin dans un graphe non pondéré :", graphs.plus_court_chemin_bfs(graphe_plus_court_chemin, "A", "F"))

print('Test Djikstra Heap avec un graphe creux')
start = time.time()
result = graphs.dijkstra_heap(graphe_creux, 0)
end = time.time()
print(f'Djikstra Heap graphe creux terminé en {timedelta(seconds=end - start)}')
# print(f'Résultat: {result}')

print('Test Djikstra Naïf avec un graphe creux')
start = time.time()
result = graphs.dijkstra_naif(graphe_creux, 0)
end = time.time()
print(f'Djikstra Naïf graphe creux terminé en {timedelta(seconds=end - start)}')
# print(f'Résultat: {result}')

# A PARTIR DE LA CA NE MARCHE PAS
# print('Test Djikstra Heap avec un graphe dense')
# start = time.time()
# result = graphs.dijkstra_heap(graphs.generer_graphe_dense, 0)
# end = time.time()
# print(f'Djikstra Heap graphe dense terminé en {timedelta(seconds=end - start)}')
# # print(f'Résultat: {result}')

# print('Test Djikstra Naïf avec un graphe dense')
# start = time.time()
# result = graphs.dijkstra_naif(graphs.generer_graphe_dense, 0)
# end = time.time()
# print(f'Djikstra Naïf graphe dense terminé en {timedelta(seconds=end - start)}')
# print(f'Résultat: {result}')

print("\nTest de l'algo de Bellman-Ford :")
print("\nPour un graphe en liste d'adjacence :")
print("Distances :", distances)
print("Prédécesseurs :", predecessors)
print("Chemin A -> E :", graphs.reconstruct_path(predecessors, 'A', 'E'))

print("\nPour un graphe en matrice :")
print("Distances :", distances2)
print("Prédécesseurs :", predecessors2)
print("Chemin A -> E :", graphs.reconstruct_path(predecessors2, 'A', 'E'))
