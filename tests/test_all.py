import src.graphs as graphs
import src.np_hard as np_hard
import src.probabilistic as probabilistic
import src.trees as trees
from graphs import MatrixGraph, ListGraph

graph_data = {
    'A': ['B', 'C'],
    'B': ['A'],
    'C': ['A', 'B']
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
print('Matrix Graph')
MatrixGraph(['A', 'B', 'C'], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]).print()
print('List Graph')
ListGraph(graph_data).print()
print("Test parcours dfs récursif :", graphs.dfs_recursif(graphe, "A"))
print("Test parcours dfs itératif :", graphs.dfs_iteratif(graphe, "A"))
print("Test si un graphe est cyclique :", graphs.contient_cycle_oriente(graphe_cycle))
print("Test si un graphe non orienté est cyclique :", graphs.contient_cycle_non_oriente(graphe_cycle))
print("Test tri tipologique :", graphs.tri_topologique_dfs(graphe_tri_tipologique))
input("Appuyez sur Entrée pour continuer...")
from graphs import MatrixGraph, ListGraph

print('Matrix Graph')
MatrixGraph(['A', 'B', 'C'], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]).print()

print('List Graph')
graph_data = {
    'A': ['B', 'C'],
    'B': ['A'],
    'C': ['A', 'B']
}
ListGraph(graph_data).print()