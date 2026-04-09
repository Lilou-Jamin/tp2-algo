import time
from datetime import timedelta

import src.graphs as graphs
import src.np_hard as np_hard
import src.probabilistic as probabilistic
import src.trees as trees
from graphs import MatrixGraph, ListGraph, dijkstra_heap, WeightedListGraph, dijkstra_naif

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

print("---- Exercice 1 ----")  
print("Graphe à matrice d'adjacence")
MatrixGraph(['A', 'B', 'C'], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]).print()
print("Graphe à liste d'adjacence")
ListGraph(graph_data).print()
print("Graphe à liste d'adjacence pondéré")
weighted_list_graph = WeightedListGraph(weighted_graph_data)
weighted_list_graph.print()
print("Test parcours dfs récursif :", graphs.dfs_recursif(graphe, "A"))
print("Test parcours dfs itératif :", graphs.dfs_iteratif(graphe, "A"))
print("Test si un graphe est cyclique :", graphs.contient_cycle_oriente(graphe_cycle))
print("Test si un graphe non orienté est cyclique :", graphs.contient_cycle_non_oriente(graphe_cycle))
print("Test tri tipologique :", graphs.tri_topologique_dfs(graphe_tri_tipologique))
#input("Appuyez sur Entrée pour continuer...")
from graphs import MatrixGraph, ListGraph

print('Test Djikstra Heap avec graphe simple')
print(dijkstra_heap(weighted_list_graph, 'A'))

print('Test Djikstra Naïf avec graphe simple')
print(dijkstra_naif(weighted_list_graph, 'A'))

print("Génération graphe creux... (V = 15 000, max 3 voisins)")
start = time.time()
graphe_creux = graphs.generer_graphe_creux(15000)
end = time.time()
print(f'Génération terminée en {timedelta(seconds=end - start)}')

print("Génération graphe dense... (V = 7 000, 90% connectés)")
start = time.time()
# Note: la génération de graphe dense a plus de 3000 sommets prend un temps significatif,
# lancer ce test que lorsque nécessaire
# graphe_dense = graphs.generer_graphe_dense(7000, 0.90)
graphe_dense = graphs.generer_graphe_dense(2000, 0.90)
end = time.time()
print(f'Génération terminée en {timedelta(seconds=end - start)}')

print('Test Djikstra Heap avec un graphe creux')
start = time.time()
result = dijkstra_heap(graphe_creux, 0)
end = time.time()
print(f'Djikstra Heap graphe creux terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')

print('Test Djikstra Naïf avec un graphe creux')
start = time.time()
result = dijkstra_naif(graphe_creux, 0)
end = time.time()
print(f'Djikstra Naïf graphe creux terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')

print('Test Djikstra Heap avec un graphe dense')
start = time.time()
result = dijkstra_heap(graphe_dense, 0)
end = time.time()
print(f'Djikstra Heap graphe dense terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')

print('Test Djikstra Naïf avec un graphe dense')
start = time.time()
result = dijkstra_naif(graphe_dense, 0)
end = time.time()
print(f'Djikstra Naïf graphe dense terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')