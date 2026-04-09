from collections import deque
from abc import ABC, abstractmethod

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
            raise Exception("Vertices must be a list")
        vertices_len = len(self.vertices)
        if vertices_len < 2:
            raise Exception("Vertices must have at least 2 elements")

        if not isinstance(self.matrix, list):
            raise Exception("Matrix must be a list")
        matrix_len = len(self.matrix)
        if matrix_len < 2:
            raise Exception("Matrix must have at least 2 vertices")

        if vertices_len != matrix_len:
            raise Exception("Matrix vertices must have the same number of vertices")

        for i in range(matrix_len):
            if len(self.matrix[i]) != matrix_len:
                raise Exception(f"Matrix index {i} has an invalid length")

    def print(self):
        """Display the Matrix Graph in a human-readable way"""
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
            raise Exception("Adjacency list must be a dict")

        if len(self.adjacency_list) < 2:
            raise Exception("Adjacency list must have at least 2 vertices")

        vertices = set(self.adjacency_list.keys())
        for vertex, neighbors in self.adjacency_list.items():
            if not isinstance(neighbors, list):
                raise Exception(f"Neighbors of vertex '{vertex}' must be supplied as a list")

    def print(self):
        """Display the List Graph in a human-readable way."""
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
    Args:
        graphe: dict[sommet, list[sommet]]
        depart: sommet de départ
    
    Returns:
        list: ordre de visite
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