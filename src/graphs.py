from collections import deque
from abc import ABC, abstractmethod
from math import inf
import random
import time
import heapq

""" Exercice 1 : Parcours de graphes """

class BaseGraph(ABC):
    @abstractmethod
    def print(self):
        pass

class MatrixGraph(BaseGraph):
    def __init__(self, vertices, matrix):
        self.vertices = vertices
        self.matrix = matrix
        self.__validate_matrix__()

    def __validate_matrix__(self):
        if not isinstance(self.vertices, list):
            raise Exception("Les sommets doivent être une liste")
        vertices_len = len(self.vertices)
        if vertices_len < 2:
            raise Exception("Les sommets doivent contenir au moins 2 éléments")

        if not isinstance(self.matrix, list):
            raise Exception("La matrice doit être une liste")
        matrix_len = len(self.matrix)
        if matrix_len < 2:
            raise Exception("La matrice doit avoir au moins 2 lignes")

        if vertices_len != matrix_len:
            raise Exception("Les sommets de la matrice doivent correspondre à la liste de sommets")

        for i in range(matrix_len):
            if len(self.matrix[i]) != matrix_len:
                raise Exception(f"L'index de la matrice {i} n'a pas une longueur valide")

    def print(self):
        """affiche le graphe sous forme de matrice d'adjacence de manière lisible"""
        print("\\ | " + " ".join(self.vertices))
        print("--" * (len(self.vertices) + 1) + '-')
        for index, row in enumerate(self.matrix):
            print(self.vertices[index] + " | " + " ".join(map(lambda value : str(value), row)))


class ListGraph(BaseGraph):
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.__validate_list__()

    def __validate_list__(self):
        if not isinstance(self.adjacency_list, dict):
            raise Exception("La liste d'adjacence doit être un dictionnaire")

        if len(self.adjacency_list) < 2:
            raise Exception("La liste d'adjacence doit contenir au moins 2 sommets")

        vertices = set(self.adjacency_list.keys())
        for vertex, neighbors in self.adjacency_list.items():
            if not isinstance(neighbors, list):
                raise Exception(f"Voisins du sommet '{vertex}' doit être une liste")

    def print(self):
        """affiche dans un format lisible le graphe sous forme de liste d'adjacence"""
        for vertex, neighbors in self.adjacency_list.items():
            neighbors_str = ", ".join(str(n) for n in neighbors)
            print(f"{vertex} -> [ {neighbors_str} ]")



class WeightedListGraph(BaseGraph):
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.__validate_list__()

    def __validate_list__(self):
        if not isinstance(self.adjacency_list, dict):
            raise Exception("L'entrée doit être un dictionnaire (dict)")

        if len(self.adjacency_list) < 2:
            raise Exception("Le graphe doit avoir au moins 2 sommets")

        vertices = set(self.adjacency_list.keys())
        for vertex, edges in self.adjacency_list.items():
            if not isinstance(edges, list):
                raise Exception(f"Les arêtes du sommet '{vertex}' doivent être une liste")

            for edge in edges:
                if not isinstance(edge, tuple) or len(edge) != 2:
                    raise Exception(f"L'arête {edge} du sommet '{vertex}' est invalide. Attendu : (voisin, poids)")

                neighbor, weight = edge
                if neighbor not in vertices:
                    raise Exception(f"Le voisin '{neighbor}' du sommet '{vertex}' n'est pas défini comme sommet")

                if not isinstance(weight, (int, float)):
                    raise Exception(f"Le poids de l'arête vers '{neighbor}' doit être un nombre")

    def print(self):
        """Affiche le graphe pondéré de liste d'adjancence de façon lisible humainement"""
        for vertex, edges in self.adjacency_list.items():
            edges_str = ", ".join(f"{neighbor}: {weight}" for neighbor, weight in edges)

            if not edges_str:
                edges_str = "Aucun voisin"

            print(f"{vertex} -> [ {edges_str} ]")

def dfs_recursif(graphe, depart, visites=None, ordre=None):
    """   
    parcours dfs récursif à partir d'un sommet donné  
        graphe -> dict[sommet, list[sommet]]
        depart -> sommet de départ
        visites -> ensemble des sommets deja visités
        ordre -> liste de l'ordre de visite
    
        renvoie une liste avec l ordre de visite des sommets
    """
    if visites is None:
        visites = set()
    if ordre is None:
        ordre = []
    visites.add(depart)
    ordre.append(depart)
    for voisin in graphe.get(depart, []):
        if voisin not in visites:
            dfs_recursif(graphe, voisin, visites, ordre)
    return ordre

def dfs_iteratif(graphe, depart):
    """
    parcours dfs itératif avec une pile
        graphe -> dict[sommet, list[sommet]]
        depart -> sommet de départ
        renvoie une liste avec l'ordre de visite des sommets
    """
    visites = set()
    ordre = []
    pile = [depart]
    
    while pile : 
        sommet = pile.pop()
        if sommet not in visites:
            visites.add(sommet)
            ordre.append(sommet)
            for voisin in reversed(graphe.get(sommet, [])): # on ajoute en ordre inverse pour se rapprocher du dfs récursif
                if voisin not in visites:
                    pile.append(voisin)
    return ordre

def contient_cycle_oriente(graphe):
    """
    détecte si y a un cycle dans un graphe orienté avec dfs
    """
    visites = set()
    en_cours = set()

    def dfs(sommet):
        visites.add(sommet)
        en_cours.add(sommet)
        for voisin in graphe.get(sommet, []):
            if voisin not in visites:
                if dfs(voisin):
                    return True
            elif voisin in en_cours:
                return True
        en_cours.remove(sommet)
        return False

    for sommet in graphe:
        if sommet not in visites:
            if dfs(sommet):
                return True
    return False


def contient_cycle_non_oriente(graphe):
    """
    détecte si y'a un cycle dans un graphe non orienté avec dfs.
    """
    visites = set()

    def dfs(sommet, parent):
        visites.add(sommet)

        for voisin in graphe.get(sommet, []):
            if voisin not in visites:
                if dfs(voisin, sommet):
                    return True
            elif voisin != parent:
                return True
        return False

    for sommet in graphe:
        if sommet not in visites:
            if dfs(sommet, None):
                return True
    return False

def tri_topologique_dfs(graphe):
    """
    tri topologique par dfs uniquement pour un graphe orienté sans cycle
    renvoie une liste avec l ordre topologique
    """
    visites = set()
    en_cours = set()
    ordre = []

    def dfs(sommet):
        if sommet in en_cours:
            raise ValueError("Le graphe contient un cycle impossible de triers")
        if sommet in visites:
            return

        en_cours.add(sommet)

        for voisin in graphe.get(sommet, []):
            dfs(voisin)

        en_cours.remove(sommet)
        visites.add(sommet)
        ordre.append(sommet)

    for sommet in graphe:
        if sommet not in visites:
            dfs(sommet)

    ordre.reverse()
    return ordre

def bfs(graphe, depart):
    """
    parcours bfs itératif avec une file    
    graphe -> dict[sommet, list[sommet]]
    depart -> sommet de départ
    retourne une liste avec l'ordre de visite
    """
    visites = set([depart])
    ordre = []
    file = deque([depart])

    while file:
        sommet = file.popleft()
        ordre.append(sommet)

        for voisin in graphe.get(sommet, []):
            if voisin not in visites:
                visites.add(voisin)
                file.append(voisin)

    return ordre

def plus_court_chemin_bfs(graphe, depart, arrivee):
    """
    retourne une liste avec le plus court chemin entre depart et arrivee dans un graphe non pondéré
    """
    if depart == arrivee:
        return [depart]

    file = deque([depart])
    visites = set([depart])
    parent = {depart: None}

    while file:
        sommet = file.popleft()

        for voisin in graphe.get(sommet, []):
            if voisin not in visites:
                visites.add(voisin)
                parent[voisin] = sommet
                file.append(voisin)

                if voisin == arrivee:
                    chemin = []
                    courant = arrivee
                    while courant is not None:
                        chemin.append(courant)
                        courant = parent[courant]
                    return chemin[::-1]
    return None

""" Exercice 2 : Plus court chemin """

def get_vertices(graph):
    """
    retourne liste des sommets selon le type de graphe
    """
    if isinstance(graph, MatrixGraph):
        return graph.vertices
    elif isinstance(graph, ListGraph):
        return list(graph.adjacency_list.keys())
    else:
        raise TypeError("Type de graphe non supporté")


def get_weighted_edges(graph):
    """
    récupère toutes les aretes pondérées du graphe sous la forme : [(source, destination, poids), ...]
    """
    edges = []

    if isinstance(graph, MatrixGraph):
        vertices = graph.vertices
        matrix = graph.matrix
        n = len(vertices)

        for i in range(n):
            for j in range(n):
                weight = matrix[i][j]

                # pas d'arête si None ou inf
                if weight is None or weight == inf:
                    continue
                edges.append((vertices[i], vertices[j], weight))

    elif isinstance(graph, ListGraph):
        for source, neighbors in graph.adjacency_list.items():
            for edge in neighbors:
                if not isinstance(edge, tuple) or len(edge) != 2:
                    raise ValueError(
                        f"Format invalide pour l'arête depuis '{source}'. "
                        f"Attendu : (voisin, poids)"
                    )
                destination, weight = edge
                edges.append((source, destination, weight))
    else:
        raise TypeError("Type de graphe non supporté")
    return edges


def bellman_ford(graph, source):
    """
    algo de Bellman-Ford, on part d'un sommet source et on cherche le plus court chemin
    retourne un dict de distances avec {sommet: distance minimale depuis source}
    + un autre dict de prédecesseurs avec {sommet: prédécesseur}

    si y'a un cycle négatif alors erreur
    """
    vertices = get_vertices(graph)
    edges = get_weighted_edges(graph)

    if source not in vertices:
        raise ValueError(f"Le sommet source '{source}' n'existe pas dans le graphe")

    distances = {v: inf for v in vertices}
    predecessors = {v: None for v in vertices}
    distances[source] = 0

    # relaxation des arêtes |V| - 1 fois
    for _ in range(len(vertices) - 1):
        updated = False

        for u, v, w in edges:
            if distances[u] != inf and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                predecessors[v] = u
                updated = True

        if not updated:
            break

    # on check si y'a un cycle négatif
    for u, v, w in edges:
        if distances[u] != inf and distances[u] + w < distances[v]:
            raise ValueError("Cycle négatif détecté dans le graphe")

    return distances, predecessors


def reconstruct_path(predecessors, source, target):
    """
    reconstruit le chemin source -> target a partir des prédécesseurs
    retourne une liste de sommets du chemin ou none si inaccesible
    """
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    if not path or path[0] != source:
        return None
    return path


def dijkstra_heap(weighted_graph: WeightedListGraph, start):
    graph = weighted_graph.adjacency_list

    distance = {n: float('inf') for n in graph}
    distance[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        distance_actuelle, sommet_actuel = heapq.heappop(priority_queue)
        # On ignore les anciennes versions d’un sommet dans le tas
        if distance_actuelle > distance[sommet_actuel]:
            continue

        for voisin, poids in graph[sommet_actuel]:
            if distance_actuelle + poids < distance[voisin]:
                distance[voisin] = distance_actuelle + poids
                heapq.heappush(priority_queue, (distance[voisin], voisin))

    return distance

def dijkstra_naif(weighted_graph: WeightedListGraph, start):
    graph = weighted_graph.adjacency_list

    distance = {n: float('inf') for n in graph}
    distance[start] = 0

    non_visites = set(graph.keys())

    while non_visites:
        noeud_actuel = None
        min_dist = float('inf')

        for noeud in non_visites:
            if distance[noeud] < min_dist:
                min_dist = distance[noeud]
                noeud_actuel = noeud

        if noeud_actuel is None:
            break

        non_visites.remove(noeud_actuel)
        for voisin, poids in graph[noeud_actuel]:
            if voisin in non_visites:
                nouvelle_distance = distance[noeud_actuel] + poids

                if nouvelle_distance < distance[voisin]:
                    distance[voisin] = nouvelle_distance

    return distance

def generer_graphe_creux(n_sommets, max_voisins=3):
    """Génère un graphe où chaque sommet n'a que très peu de connexions (sparse)."""
    graph = {i: [] for i in range(n_sommets)}

    # 1. On crée un chemin de base pour s'assurer que tout est connecté
    for i in range(n_sommets - 1):
        poids = random.randint(1, 10)
        graph[i].append((i + 1, poids))
        graph[i + 1].append((i, poids))

    # 2. On ajoute quelques arêtes aléatoires jusqu'à la limite max_voisins
    for i in range(n_sommets):
        while len(graph[i]) < max_voisins:
            voisin = random.randint(0, n_sommets - 1)
            # On évite de se connecter à soi-même ou de créer des doublons
            if voisin != i and not any(v == voisin for v, _ in graph[i]):
                poids = random.randint(1, 10)
                graph[i].append((voisin, poids))
                graph[voisin].append((i, poids))

    return WeightedListGraph(graph)

def generer_graphe_dense(n_sommets, probabilite=0.9):
    """Génère un graphe où presque tous les sommets sont connectés (dense)."""
    graph = {i: [] for i in range(n_sommets)}

    # On teste chaque paire possible
    for i in range(n_sommets):
        for j in range(i + 1, n_sommets):
            # probabilite=0.9 signifie 90% de chances de créer une arête
            if random.random() < probabilite:
                poids = random.randint(1, 10)
                graph[i].append((j, poids))
                graph[j].append((i, poids))

    return WeightedListGraph(graph)



""" Exercice 3 : Flot maximum """

def dfs_chemin_residuel(graphe_residuel, source, puits, visites=None, chemin=None):
    """
    recherche récursive d un chemin augmentant dans le graphe résiduel.
    graphe_residuel -> dict[sommet, dict[voisin, capacité_residuelle]]
    source -> sommet de départ
    puits -> sommet d'arrivée
    visites -> ensemble des sommets déjà visités
    chemin -> liste des arêtes du chemin [(u, v), ...]
    
    renvoie une liste d'arêtes représentant un chemin de source à puits ou none si aucun chemin n'existe
    """
    if visites is None:
        visites = set()
    if chemin is None:
        chemin = []

    if source == puits:
        return chemin

    visites.add(source)
    for voisin, capacite in graphe_residuel.get(source, {}).items():
        if voisin not in visites and capacite > 0:
            resultat = dfs_chemin_residuel(
                graphe_residuel,
                voisin,
                puits,
                visites,
                chemin + [(source, voisin)]
            )
            if resultat is not None:
                return resultat
    return None

def ford_fulkerson(capacites, source, puits):
    """
    algorithme de Ford-Fulkerson avec recherche DFS des chemins augmentants
    capacites -> dict[sommet, dict[voisin, capacité]]
    source -> sommet source
    puits -> sommet puits
    renvoie la valeur du flot maximal (max_flow) et dict[sommet, dict[voisin, flot_envoyé]] (flot)
    """
    # on construit l'ensemble des sommets
    sommets = set(capacites.keys())
    for u in capacites:
        for v in capacites[u]:
            sommets.add(v)

    # création du graphe résiduel
    graphe_residuel = {u: {} for u in sommets}
    for u in sommets:
        for v in sommets:
            graphe_residuel[u][v] = 0

    for u in capacites:
        for v, cap in capacites[u].items():
            graphe_residuel[u][v] = cap
            # l'arête inverse existe aussi dans le résiduel, initialement à 0
            if u not in graphe_residuel[v]:
                graphe_residuel[v][u] = 0

    # création du flot
    flot = {u: {} for u in sommets}
    for u in sommets:
        for v in sommets:
            flot[u][v] = 0
    max_flow = 0

    while True:
        # on cherche un chemin augmentant avec DFS
        chemin = dfs_chemin_residuel(graphe_residuel, source, puits)

        if chemin is None:
            break

        # capacité minimale sur le chemin trouvé
        flot_chemin = min(graphe_residuel[u][v] for u, v in chemin)

        # màj du graphe résiduel et du flot
        for u, v in chemin:
            graphe_residuel[u][v] -= flot_chemin
            graphe_residuel[v][u] += flot_chemin

            # si (u,v) est une arête originale alors on augmente le flot
            if u in capacites and v in capacites[u]:
                flot[u][v] += flot_chemin
            else:
                # sinon c'est une arête retour alors on annule une partie du flot
                flot[v][u] -= flot_chemin
        max_flow += flot_chemin

    # ne garder que les arêtes du graphe initial
    flot_final = {}
    for u in capacites:
        flot_final[u] = {}
        for v in capacites[u]:
            flot_final[u][v] = flot[u][v]
    return max_flow, flot_final


def bfs_chemin_residuel(graphe_residuel, source, puits):
    """
    recherche un chemin augmentant dans le graphe résiduel avec BFS
    graphe_residuel -> dict[sommet, dict[voisin, capacité_residuelle]]
    source -> sommet source
    puits -> sommet puits
    renvoie une liste d'arêtes [(u, v), ...] représentant le chemin ou none s'il n'existe aucun chemin augmentant
    """
    visites = set([source])
    parent = {source: None}
    file = deque([source])

    while file:
        sommet = file.popleft()
        if sommet == puits:
            break
        for voisin, capacite in graphe_residuel.get(sommet, {}).items():
            if voisin not in visites and capacite > 0:
                visites.add(voisin)
                parent[voisin] = sommet
                file.append(voisin)

    if puits not in parent:
        return None

    # on reconstruit du chemin depuis le puits jusqu'à la source
    chemin = []
    courant = puits

    while parent[courant] is not None:
        precedent = parent[courant]
        chemin.append((precedent, courant))
        courant = precedent
    chemin.reverse()
    return chemin


def edmonds_karp(capacites, source, puits):
    """
    algorithme d'Edmonds-Karp (ford-Fulkerson + BFS)
    capacites -> dict[sommet, dict[voisin, capacité]]
    renvoie la valeur du flot maximal (max_flow) et dict[sommet, dict[voisin, flot]] (flot_final)
        max_flow, flot_final
    """
    # on construit l'ensemble des sommets
    sommets = set(capacites.keys())
    for u in capacites:
        for v in capacites[u]:
            sommets.add(v)

    # création du graphe résiduel
    graphe_residuel = {u: {} for u in sommets}
    for u in sommets:
        for v in sommets:
            graphe_residuel[u][v] = 0

    for u in capacites:
        for v, cap in capacites[u].items():
            graphe_residuel[u][v] = cap
            if u not in graphe_residuel[v]:
                graphe_residuel[v][u] = 0

    # création du flot
    flot = {u: {} for u in sommets}
    for u in sommets:
        for v in sommets:
            flot[u][v] = 0
    max_flow = 0

    while True:
        # on cherche d'un plus court chemin augmentant avec BFS
        chemin = bfs_chemin_residuel(graphe_residuel, source, puits)

        if chemin is None:
            break

        # goulot d'étranglement du chemin
        flot_chemin = min(graphe_residuel[u][v] for u, v in chemin)

        # màj du résiduel et du flot
        for u, v in chemin:
            graphe_residuel[u][v] -= flot_chemin
            graphe_residuel[v][u] += flot_chemin

            # arête de base
            if u in capacites and v in capacites[u]:
                flot[u][v] += flot_chemin
            else:
                # arête retour
                flot[v][u] -= flot_chemin

        max_flow += flot_chemin

    # on garde que les arêtes du graphe initial
    flot_final = {}
    for u in capacites:
        flot_final[u] = {}
        for v in capacites[u]:
            flot_final[u][v] = flot[u][v]
    return max_flow, flot_final