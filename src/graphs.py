from collections import deque
from abc import ABC, abstractmethod
from math import inf

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
