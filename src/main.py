import src.graphs as graphs
import src.np_hard as np_hard
import probabilistic as probabilistic
import trees as trees

# On a choisit de représenter les graphes sous forme de dictionnaire
# où les clés sont les sommets et les valeurs sont des listes de sommets adjacents
graphe = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": [],
    "F": []
}

print(dfs_recursif(graphe, "A"))
