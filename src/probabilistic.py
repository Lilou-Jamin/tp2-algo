import random

def partition(arr, low, high):
    # Fonction de partitionnement classique (Lomuto).
    # Le pivot est supposé être le dernier élément du sous-tableau.
    pivot = arr[high]
    i = low - 1  # Indice du plus petit élément

    for j in range(low, high):
        # Si l'élément actuel est plus petit ou égal au pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # On place le pivot à sa position triée dans le sous tableau.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def randomized_partition(arr, low, high):
    rand_index = random.randint(low, high)

    # On échange le pivot aléatoire avec le dernier élément. (c'est l'indice choisi par la fonction partition classique)
    arr[rand_index], arr[high] = arr[high], arr[rand_index]

    # On appelle la fonction partition classique maintenant que notre pivot randomisé est mis en place.
    return partition(arr, low, high)


def quicksort_inplace(arr, low, high, randomized = False):
    # On trie les données en entrée qui sont passées par référence.
    # Cela signifie que l'on a pas besoin de retourner la nouvelle liste triée.
    if low < high:
        if randomized:
            pivot = randomized_partition(arr, low, high)
        else:
            pivot = partition(arr, low, high)

        quicksort_inplace(arr, low, pivot - 1, randomized)
        quicksort_inplace(arr, pivot + 1, high, randomized)


def randomized_quicksort(arr):
    quicksort_inplace(arr, 0, len(arr) - 1, True)

def deterministic_quicksort(arr):
    quicksort_inplace(arr, 0, len(arr) - 1)


def quickselect_inplace(arr, low, high, k, randomized = False):
    # Trouve le k-ième plus petit élément (k est l'index, de 0 à n-1).
    # Si le sous-tableau ne contient qu'un seul élément, c'est forcément le bon
    if low == high:
        return arr[low]

    if randomized:
        pivot = randomized_partition(arr, low, high)
    else:
        pivot = partition(arr, low, high)

    # 3 scénarios possibles :
    if k == pivot:
        # Le pivot est tombé exactement sur l'index qu'on cherche.
        return arr[pivot]
    elif k < pivot:
        # L'index qu'on cherche est à gauche du pivot.
        return quickselect_inplace(arr, low, pivot - 1, k, randomized)
    else:
        # L'index qu'on cherche est à droite du pivot.
        return quickselect_inplace(arr, pivot + 1, high, k, randomized)


def randomized_quickselect(arr, k):
    # Pour le 1er plus petit élément : k = 0.
    # Pour la médiane : k = len(arr) // 2.
    return quickselect_inplace(arr, 0, len(arr) - 1, k, True)

def deterministic_quickselect(arr, k):
    # Pour le 1er plus petit élément : k = 0.
    # Pour la médiane : k = len(arr) // 2.
    return quickselect_inplace(arr, 0, len(arr) - 1, k)

def estimate_pi(samples):
    inside_circle = 0
    for _ in range(samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x * x + y * y <= 1:
            inside_circle += 1

    return 4 * inside_circle / samples
