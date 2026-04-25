class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self.__insert_recursive(self.root, value)

    def __insert_recursive(self, node, value):
        # Si le noeud est vide, on a trouvé l'emplacement : on l'insère ici
        if node is None:
            return Node(value)

        # Navigation à gauche ou à droite selon la valeur insérée
        if value < node.value:
            node.left = self.__insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self.__insert_recursive(node.right, value)

        # Si la valeur existe déjà, on ne l'ajoute pas
        return node

    def search(self, value):
        return self.__search_recursive(self.root, value)

    def __search_recursive(self, node, value):
        # Cas de base : racine nulle ou clé trouvée
        if node is None or node.value == value:
            return node

        # La valeur est plus grande que la valeur du noeud
        if node.value < value:
            return self.__search_recursive(node.right, value)

        # La valeur est plus petite que la valeur du noeud
        return self.__search_recursive(node.left, value)

    def remove(self, value):
        self.root = self.__remove_recursive(self.root, value)

    def __remove_recursive(self, node, value):
        if node is None:
            return None

        # Recherche du noeud à supprimer
        if value < node.value:
            node.left = self.__remove_recursive(node.left, value)
        elif value > node.value:
            node.right = self.__remove_recursive(node.right, value)
        else:
            # Le noeud a soit un seul enfant soit aucun
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Le noeud a deux enfants.
            # On trouve le plus petit élément du sous-arbre droit (le successeur à la valeur a supprimer)
            node.value = self.__min_value(node.right).value
            # On supprime le successeur
            node.right = self.__remove_recursive(node.right, node.value)

        return node

    def __min_value(self, node):
        current_node = node
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def in_order_traversal(self):
        resultat = []
        self.__in_order_traversal_recursive(self.root, resultat)
        return resultat

    def __in_order_traversal_recursive(self, node, result):
        if node is not None:
            self.__in_order_traversal_recursive(node.left, result)
            result.append(node.value)
            self.__in_order_traversal_recursive(node.right, result)

    def print(self):
        self.__print_recursive(self.root, 0)

    def __print_recursive(self, node, level):
        if node is not None:
            # On affiche d'abord la branche droite, puis le noeud, puis la branche gauche
            # Cela donne un arbre lisible de gauche à droite
            self.__print_recursive(node.right, level + 1)
            print('    ' * level + '->', node.value)
            self.__print_recursive(node.left, level + 1)


class AdelsonVelskyLandisNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AdelsonVelskyLandisTree:
    def __init__(self):
        self.root = None
        self.simple_rotations = 0
        self.double_rotations = 0

    def __get_height(self, node):
        if not node:
            return 0
        return node.height

    def __get_balance(self, node):
        if not node:
            return 0

        return self.__get_height(node.left) - self.__get_height(node.right)

    def __min_value(self, node):
        current_node = node
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def __rotation_right(self, y):
        x = y.left
        T2 = x.right
        # Effectuer la rotation
        x.right = y
        y.left = T2
        # Mettre à jour les hauteurs
        y.height = 1 + max(self.__get_height(y.left), self.__get_height(y.right))
        x.height = 1 + max(self.__get_height(x.left), self.__get_height(x.right))

        self.simple_rotations += 1
        return x

    def __rotation_left(self, x):
        y = x.right
        T2 = y.left
        # Effectuer la rotation
        y.left = x
        x.right = T2
        # Mettre à jour les hauteurs
        x.height = 1 + max(self.__get_height(x.left), self.__get_height(x.right))
        y.height = 1 + max(self.__get_height(y.left), self.__get_height(y.right))

        self.simple_rotations += 1
        return y

    # --- INSERTION ---
    def insert(self, value):
        self.root = self.__insert_recursive(self.root, value)

    def __insert_recursive(self, node, value):
        if node is None:
            return AdelsonVelskyLandisNode(value)

        if value < node.value:
            node.left = self.__insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self.__insert_recursive(node.right, value)

        return self.__rebalance(node)

    def __rebalance(self, node):
        # Mise à jour de la hauteur du noeud actuel
        node.height = 1 + max(self.__get_height(node.left), self.__get_height(node.right))

        # Récupération du facteur d'équilibre
        balance = self.__get_balance(node)

        # Vérification des 4 cas de déséquilibre en utilisant l'équilibre des enfants
        if balance > 1:
            # Cas Left-Right : Arbre penché à gauche et l'enfant gauche est penché à droite
            if self.__get_balance(node.left) < 0:
                self.double_rotations += 1
                # Décrémentation car __rotation_left et __rotation_right vont incrémenter simple_rotations
                self.simple_rotations -= 2

                node.left = self.__rotation_left(node.left)
                return self.__rotation_right(node)
            # Cas Left-Left : Arbre penché à gauche et l'enfant gauche est penché à gauche (ou équilibré)
            return self.__rotation_right(node)

        if balance < -1:
            # Cas Right-Left : Arbre penché à droite et l'enfant droit est penché à gauche
            if self.__get_balance(node.right) > 0:
                self.double_rotations += 1
                # Décrémentation car __rotation_left et __rotation_right vont incrémenter simple_rotations
                self.simple_rotations -= 2

                node.right = self.__rotation_right(node.right)
                return self.__rotation_left(node)
            # Cas Right-Right : Arbre penché à droite et l'enfant droit est penché à droite (ou équilibré)
            return self.__rotation_left(node)

        # Si l'arbre est équilibré, on retourne le noeud tel quel
        return node

    def remove(self, value):
        self.root = self.__remove_recursive(self.root, value)

    def __remove_recursive(self, node, value):
        if node is None:
            return None

        # Recherche du noeud à supprimer
        if value < node.value:
            node.left = self.__remove_recursive(node.left, value)
        elif value > node.value:
            node.right = self.__remove_recursive(node.right, value)
        else:
            # Le noeud a soit un seul enfant soit aucun
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Le noeud a deux enfants.
            # On trouve le plus petit élément du sous-arbre droit (le successeur à la valeur a supprimer)
            node.value = self.__min_value(node.right).value
            # On supprime le successeur
            node.right = self.__remove_recursive(node.right, node.value)

        # Si l'arbre n'avait qu'un seul noeud et qu'il vient d'être supprimé, pas besoin de rééquilibrage
        if node is None:
            return None

        # 2. On retourne le noeud après rééquilibrage
        return self.__rebalance(node)

    def get_max_depth(self):
        return self.__get_height(self.root)

    def print(self):
        self.__print_recursive(self.root, 0)

    def __print_recursive(self, node, level):
        if node is not None:
            # On affiche d'abord la branche droite, puis le noeud, puis la branche gauche
            # Cela donne un arbre lisible de gauche à droite
            self.__print_recursive(node.right, level + 1)
            print('    ' * level + '->', node.value)
            self.__print_recursive(node.left, level + 1)