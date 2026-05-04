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

    def traversal(self, type = 'inordre'):
        """
        Traverse l'arbre binaire et retourne un tableau de la traversée.
        :param type: Le type de traversée : "inordre", "preordre" ou "postordre".
        :return: Le tableau résultant de la traversée.
        """
        if type != 'inordre' and type != 'preordre' and type != 'postordre':
            raise ValueError('Type de traversée invalide.')

        resultat = []
        self.__traversal_recursive(self.root, resultat, type)
        return resultat

    def __traversal_recursive(self, node, result, type):
        if node is not None:
            if type == 'preordre':
                result.append(node.value)

            self.__traversal_recursive(node.left, result, type)

            if type == 'inordre':
                result.append(node.value)

            self.__traversal_recursive(node.right, result, type)

            if type == 'postordre':
                result.append(node.value)

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


class RedBlackNode:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  # 1 = RED, 0 = BLACK. Un nouveau nœud est toujours RED.


class RedBlackTree:
    def __init__(self):
        # 1. Création de la sentinelle TNULL (remplace les 'None')
        self.TNULL = RedBlackNode(0)
        self.TNULL.color = 0  # Les feuilles TNULL sont toujours noires
        self.root = self.TNULL

    # --- RECHERCHE ET PARCOURS ---
    def search(self, value):
        return self.__search_recursive(self.root, value)

    def __search_recursive(self, node, value):
        if node == self.TNULL or value == node.value:
            return node
        if value < node.value:
            return self.__search_recursive(node.left, value)
        return self.__search_recursive(node.right, value)

    def in_order(self):
        result = []
        self.__in_order_recursive(self.root, result)
        return result

    def __in_order_recursive(self, node, result):
        if node != self.TNULL:
            self.__in_order_recursive(node.left, result)
            result.append(node.value)
            self.__in_order_recursive(node.right, result)

    # --- ROTATIONS (Nécessitent la gestion du 'parent') ---
    def __left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def __right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, value):
        new_node = RedBlackNode(value)
        new_node.left = self.TNULL
        new_node.right = self.TNULL

        parent = None
        current = self.root

        # Descente classique de BST pour trouver où insérer la valeur
        while current != self.TNULL:
            parent = current
            if new_node.value < current.value:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        # Attachement du nouveau noeud
        if parent is None:
            self.root = new_node
        elif new_node.value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        # Si c'est la racine, on la met en noir et on s'arrête
        if new_node.parent is None:
            new_node.color = 0
            return

        # Si le grand-parent n'existe pas, pas besoin de réparer l'arbre
        if new_node.parent.parent is None:
            return

        # 3. Réparation des règles Rouge-Noir
        self.__fix_insert(new_node)

    def __fix_insert(self, k):
        # On répare tant que le parent de k est RED (Violation de la règle 4)
        while k.parent.color == 1:
            # Le parent est l'enfant gauche du grand-parent
            if k.parent == k.parent.parent.left:
                uncle = k.parent.parent.right

                # CAS 1 : L'oncle est RED (ON effectue seulement une recoloration)
                if uncle.color == 1:
                    uncle.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    # CAS 2 : L'oncle est BLACK et on est un enfant droit -> Rotation Gauche
                    if k == k.parent.right:
                        k = k.parent
                        self.__left_rotate(k)

                    # CAS 3 : L'oncle est BLACK et on est un enfant gauche -> Rotation Droite + recoloration
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.__right_rotate(k.parent.parent)

            # Le parent est l'enfant droit du grand-parent (Symétrie)
            else:
                uncle = k.parent.parent.left

                # CAS 1
                if uncle.color == 1:
                    uncle.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    # CAS 2
                    if k == k.parent.left:
                        k = k.parent
                        self.__right_rotate(k)

                    # CAS 3
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.__left_rotate(k.parent.parent)

            if k == self.root:
                break

        # La racine reste toujours noire
        self.root.color = 0

    def print(self):
        self.__print_recursive(None, 0)

    # --- AFFICHAGE ---
    def __print_recursive(self, node, level):
        if node is None:
            node = self.root

        if node != self.TNULL:
            self.__print_recursive(node.right, level + 1)
            print('    ' * level + f'-> {node.value} ({"R" if node.color == 1 else "B"})')
            self.__print_recursive(node.left, level + 1)

