from abc import ABC, abstractmethod

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

def graphs_main():
    print('Matrix Graph')
    MatrixGraph(['A', 'B', 'C'], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]).print()

    print('List Graph')
    graph_data = {
        'A': ['B', 'C'],
        'B': ['A'],
        'C': ['A', 'B']
    }
    ListGraph(graph_data).print()