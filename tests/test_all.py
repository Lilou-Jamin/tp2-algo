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