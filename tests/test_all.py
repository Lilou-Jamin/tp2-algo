import src.graphs as graphs
import src.np_hard as np_hard
import src.probabilistic as probabilistic
import src.trees as trees

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

graphe_plus_court_chemin = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": ["F"],
    "E": ["F"],
    "F": []
}

print("---- Exercice 1 ----")  
print('\n graphe sous forme de matrice :')
graphs.MatrixGraph(['A', 'B', 'C'], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]).print()
print('\ngraphe sous forme de liste d\'adjacence :')
graphs.ListGraph(graph_data).print()
print("Test parcours dfs récursif :", graphs.dfs_recursif(graphe, "A"))
print("Test parcours dfs itératif :", graphs.dfs_iteratif(graphe, "A"))
print("Test si un graphe est cyclique :", graphs.contient_cycle_oriente(graphe_cycle))
print("Test si un graphe non orienté est cyclique :", graphs.contient_cycle_non_oriente(graphe_cycle))
print("Test tri tipologique :", graphs.tri_topologique_dfs(graphe_tri_tipologique))
print("Test du plus court chemin dans un graphe non pondéré :", graphs.plus_court_chemin_bfs(graphe_plus_court_chemin, "A", "F"))

input("\nAppuyez sur Entrée pour continuer...")

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

print("Test de l'algo de Bellman-Ford :")
print("\nPour un graphe en liste d'adjacence :")
print("Distances :", distances)
print("Prédécesseurs :", predecessors)
print("Chemin A -> E :", graphs.reconstruct_path(predecessors, 'A', 'E'))

print("\nPour un graphe en matrice :")
print("Distances :", distances2)
print("Prédécesseurs :", predecessors2)
print("Chemin A -> E :", graphs.reconstruct_path(predecessors2, 'A', 'E'))

