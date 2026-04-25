import time
from datetime import timedelta

import src.graphs as graphs
import src.np_hard as np_hard
import src.probabilistic as probabilistic
import src.trees as trees

def generer_listes_pour_arbre(taille):
    """Génère trois listes de test : séquentielle, décroissante et aléatoire."""
    sequentiel = list(range(1, taille + 1))
    decroissant = list(range(taille, 0, -1))

    # Aléatoire : on utilise les mêmes nombres, mais on les mélange
    # random.sample garantit qu'il n'y a pas de doublons
    import random
    aleatoire = random.sample(range(1, taille + 1), taille)

    return [[f'séquentielle ({1}..{taille})', sequentiel], [f'décroissante ({taille}..{1})', decroissant], ['aléatoire', aleatoire]]

def avl_benchmark(taille):
    listes = generer_listes_pour_arbre(taille)
    arbre = trees.AdelsonVelskyLandisTree()
    for liste in listes:
        print(f"\n\nListe {liste[0]} :")
        arbre = trees.AdelsonVelskyLandisTree()
        print("\nInsertion...")
        start = time.time()
        for i in liste[1]:
            arbre.insert(i)
        end = time.time()
        print(f'Insertion terminée en {timedelta(seconds=end - start)}')
        print(f"\nProfondeur maximale : {arbre.get_max_depth()}")
        print(f"Rotations simples effectuées : {arbre.simple_rotations}")
        print(f"Rotations doubles effectuées : {arbre.double_rotations}")

    print('Dernier arbre traité :')
    arbre.print()


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
print("Test du plus court chemin dans un graphe non pondéré :", graphs.plus_court_chemin_bfs(graphe_plus_court_chemin, "A", "F"))

input("\nAppuyez sur Entrée pour continuer vers l'exo 2")

print("\n---- Exercice 2 ----")

print("\n2.1 : ")

print('\nTest Djikstra Heap avec graphe simple')
start = time.time()
print(graphs.dijkstra_heap(weighted_list_graph, 'A'))
end = time.time()
print(f'Test terminé en {timedelta(seconds=end - start)}')

print('\nTest Djikstra Naïf avec graphe simple')
start = time.time()
print(graphs.dijkstra_naif(weighted_list_graph, 'A'))
end = time.time()
print(f'Test terminé en {timedelta(seconds=end - start)}')

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
dense_sommets = 2000
dense_prob_connecte = 0.90
print(f"Génération graphe dense... (V = {dense_sommets}, {int(dense_prob_connecte * 100)}% connectés)")
start = time.time()
graphe_dense = graphs.generer_graphe_dense(dense_sommets, dense_prob_connecte)
end = time.time()
print(f'Génération terminée en {timedelta(seconds=end - start)}')

print('Test Djikstra Heap avec un graphe creux')
start = time.time()
result = graphs.dijkstra_heap(graphe_creux, 0)
end = time.time()
print(f'Djikstra Heap graphe creux terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')

print('Test Djikstra Naïf avec un graphe creux')
start = time.time()
result = graphs.dijkstra_naif(graphe_creux, 0)
end = time.time()
print(f'Djikstra Naïf graphe creux terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')

print('\nTest Djikstra Heap avec un graphe dense')
start = time.time()
result = graphs.dijkstra_heap(graphe_dense, 0)
end = time.time()
print(f'Djikstra Heap graphe dense terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')

print('Test Djikstra Naïf avec un graphe dense')
start = time.time()
result = graphs.dijkstra_naif(graphe_dense, 0)
end = time.time()
print(f'Djikstra Naïf graphe dense terminé en {timedelta(seconds=end - start)}')
print(f'Résultat: {result}')

print("\n2.2 : ")

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

print("\nTest de l'algo de Bellman-Ford :")
print("\nPour un graphe en liste d'adjacence :")
print("Distances :", distances)
print("Prédécesseurs :", predecessors)
print("Chemin A -> E :", graphs.reconstruct_path(predecessors, 'A', 'E'))

print("\nPour un graphe en matrice :")
print("Distances :", distances2)
print("Prédécesseurs :", predecessors2)
print("Chemin A -> E :", graphs.reconstruct_path(predecessors2, 'A', 'E'))

print("\n2.3 - Algorithme de Floyd-Warshall :")
print("- Graphes sans cycles négatifs :")
print("V = 10")
graphe = graphs.generer_graphe_matrice(10)
graphe.print_spaced()
print("Plus court chemins : ")
graphs.floyd_warshall(graphe).print()

print("\nV = 50")
graphe = graphs.generer_graphe_matrice(50)
graphe.print_spaced()
print("Plus court chemins : ")
graphs.floyd_warshall(graphe).print()

print("\nV = 100")
graphe = graphs.generer_graphe_matrice(100)
graphe.print_spaced()
print("Plus court chemins : ")
graphs.floyd_warshall(graphe).print()

print("\n\n- Graphes avec cycles négatifs :")
print("V = 10")
graphe = graphs.generer_graphe_matrice(10, True)
graphe.print_spaced()
print("Plus court chemins : ")
graphs.floyd_warshall(graphe)

print("\nV = 50")
graphe = graphs.generer_graphe_matrice(50, True)
graphe.print_spaced()
print("Plus court chemins : ")
graphs.floyd_warshall(graphe)

print("\nV = 100")
graphe = graphs.generer_graphe_matrice(100, True)
graphe.print_spaced()
print("Plus court chemins : ")
graphs.floyd_warshall(graphe)

input("\nAppuyez sur Entrée pour continuer vers l'exo 3")

print("\n---- Exercice 3 ----")

capacites = {
    's': {'a': 10, 'b': 5},
    'a': {'b': 15, 't': 10},
    'b': {'t': 10},
    't': {}
}

print("\nTest de l'algo de Ford-Fulkerson :")
max_flow, flot = graphs.ford_fulkerson(capacites, 's', 't')
print("Flot maximal =", max_flow)
print("Répartition du flot :")
for u in flot:
    for v in flot[u]:
        print(f"{u} -> {v} : {flot[u][v]}")

print("\nTest de l'algo de Edmonds-Karp :")
max_flow, flot = graphs.edmonds_karp(capacites, 's', 't')
print("Flot maximal :", max_flow)
print("Flots sur les arêtes :")
for u in flot:
    for v in flot[u]:
        print(f"{u} -> {v} : {flot[u][v]}")

input("\nAppuyez sur Entrée pour continuer vers l'exo 4")

print("\n---- Exercice 4 ----")

print("4.1 - BST - Binary Search Tree")
arbre = trees.BinarySearchTree()

print("\nInsertion")
valeurs = [50, 30, 20, 40, 70, 60, 80]
print(f"Valeurs à ajouter: {valeurs}")
for v in valeurs:
    arbre.insert(v)

print(f'Arbre après ajout :\n')
arbre.print()

print("\nParcours infixe (trié) :", arbre.in_order_traversal())

print("\nRecherche")
print("\nRecherche 40 : ", "Trouvé" if arbre.search(40) else "Non trouvé")
print("Recherche 90 : ", "Trouvé" if arbre.search(90) else "Non trouvé")

print("\nSuppression")
print("\nSuppression de 20 (feuille)...")
arbre.remove(20)
arbre.print()

print("\nSuppression de 50 (racine avec deux enfants)...")
arbre.remove(50)
arbre.print()

print("\nBST avec valeurs séquentielles :")
arbre = trees.BinarySearchTree()

valeurs = [10, 20, 30, 40, 50, 60, 70, 80]
print(f"Valeurs à ajouter: {valeurs}")
for v in valeurs:
    arbre.insert(v)

arbre.print()

print("\n4.2 - AVL - Adelson-Velsky & Landis Tree")

print("Arbre de 100 éléments :")
avl_benchmark(100)

