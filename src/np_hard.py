import src.graphs as graphs
from itertools import permutations
from itertools import combinations
import math
import time

def tsp_force_brute(graphe, depart=0):
    """
    TSP en force brute
    graphe -> WeightedListGraph
    depart -> sommet de départ
    renvoit un dictionnaire avec :
        - coût optimal
        - chemin optimal
        - temps d'exécution
        - ratio = 1.0 car force brute est optimale
    """

    debut = time.perf_counter()

    adjacency_list = graphe.adjacency_list

    if depart not in adjacency_list:
        raise Exception(f"Le sommet de départ {depart} n'existe pas dans le graphe")

    # on convertit la liste d'adjacence en dictionnaire de poids pour accès rapide
    poids = {}
    for sommet, aretes in adjacency_list.items():
        poids[sommet] = {}
        for voisin, cout in aretes:
            poids[sommet][voisin] = cout

    sommets = list(adjacency_list.keys())
    sommets.remove(depart)

    meilleur_cout = math.inf
    meilleur_chemin = None
    permutations_testees = 0
    chemins_valides = 0

    for permutation in permutations(sommets):
        permutations_testees += 1

        chemin = [depart] + list(permutation) + [depart]
        cout_total = 0
        chemin_valide = True

        for i in range(len(chemin) - 1):
            u = chemin[i]
            v = chemin[i + 1]

            if v not in poids[u]:
                chemin_valide = False
                break

            cout_total += poids[u][v]

        if chemin_valide:
            chemins_valides += 1

            if cout_total < meilleur_cout:
                meilleur_cout = cout_total
                meilleur_chemin = chemin

    fin = time.perf_counter()

    temps_execution = fin - debut

    if meilleur_chemin is None:
        return {
            "cout": None,
            "chemin": None,
            "temps": temps_execution,
            "qualite": 0,
            "ratio": None
        }

    return {
        "cout": meilleur_cout,
        "chemin": meilleur_chemin,
        "temps": temps_execution,
        "qualite": 1.0,
        "ratio": 1.0
    } 

def tsp_nearest_neighbor(graphe, depart=0):
    """
    TSP par Nearest Neighbor
    graphe -> WeightedListGraph
    depart -> sommet de départ
    renvoit un dictionnaire avec :
        - coût du chemin trouvé
        - chemin trouvé
        - temps d'exécution
    """

    debut = time.perf_counter()

    adjacency_list = graphe.adjacency_list

    if depart not in adjacency_list:
        raise Exception(f"Le sommet de départ {depart} n'existe pas dans le graphe")

    # on convertit la liste d'adjacence en dictionnaire de poids pour accès rapide
    poids = {}
    for sommet, aretes in adjacency_list.items():
        poids[sommet] = {}
        for voisin, cout in aretes:
            poids[sommet][voisin] = cout

    sommets = list(adjacency_list.keys())
    non_visites = set(sommets)
    non_visites.remove(depart)

    chemin = [depart]
    cout_total = 0
    actuel = depart

    while non_visites:
        prochain = min(non_visites, key=lambda x: poids[actuel].get(x, math.inf))
        if poids[actuel].get(prochain, math.inf) == math.inf:
            break

        chemin.append(prochain)
        cout_total += poids[actuel][prochain]
        actuel = prochain
        non_visites.remove(prochain)

    if len(chemin) == len(sommets):
        chemin.append(depart)
        cout_total += poids[actuel].get(depart, math.inf)

    fin = time.perf_counter()
    temps_execution = fin - debut

    return {
        "cout": cout_total,
        "chemin": chemin,
        "temps": temps_execution,
    }

def tsp_programmation_dynamique_mesure(graphe, depart=0, cout_optimal=None):
    """
    TSP avec programmation dynamique
    graphe -> WeightedListGraph
    depart -> sommet de départ
    cout_optimal -> optionnel, utile pour calculer ratio/qualité
                   si on veut comparer avec la force brute
    renvoit un dictionnaire avec :
        - coût
        - chemin
        - temps
        - qualité
        - ratio
    """

    debut = time.perf_counter()

    adjacency_list = graphe.adjacency_list

    if depart not in adjacency_list:
        raise Exception(f"Le sommet de départ {depart} n'existe pas dans le graphe")

    # on convertit la liste d'adjacence en dictionnaire de poids pour accès rapide
    poids = {}
    for sommet, aretes in adjacency_list.items():
        poids[sommet] = {}
        for voisin, cout in aretes:
            poids[sommet][voisin] = cout

    sommets = list(adjacency_list.keys())
    sommets_sans_depart = [s for s in sommets if s != depart]

    # dp[(ensemble_visite, dernier)] = coût minimal pour atteindre "dernier"
    # ensemble_visite est un frozenset contenant les sommets visités hors départ
    dp = {}
    parent = {}

    # initialisation des cas de base : visiter un seul sommet depuis le départ
    for sommet in sommets_sans_depart:
        if sommet in poids[depart]:
            etat = frozenset([sommet])
            dp[(etat, sommet)] = poids[depart][sommet]
            parent[(etat, sommet)] = depart

    for taille in range(2, len(sommets_sans_depart) + 1):
        nouveaux_dp = {}

        for ensemble_tuple in combinations(sommets_sans_depart, taille):
            ensemble = frozenset(ensemble_tuple)

            for dernier in ensemble:
                meilleur_cout = math.inf
                meilleur_precedent = None

                ensemble_precedent = ensemble - {dernier}

                for precedent in ensemble_precedent:
                    etat_precedent = (ensemble_precedent, precedent)

                    if etat_precedent in dp and dernier in poids[precedent]:
                        cout = dp[etat_precedent] + poids[precedent][dernier]

                        if cout < meilleur_cout:
                            meilleur_cout = cout
                            meilleur_precedent = precedent

                if meilleur_precedent is not None:
                    nouveaux_dp[(ensemble, dernier)] = meilleur_cout
                    parent[(ensemble, dernier)] = meilleur_precedent

        dp.update(nouveaux_dp)

    # on ferme le circuit dernier sommet -> depart
    ensemble_total = frozenset(sommets_sans_depart)
    meilleur_cout = math.inf
    meilleur_dernier = None

    for dernier in sommets_sans_depart:
        etat = (ensemble_total, dernier)

        if etat in dp and depart in poids[dernier]:
            cout = dp[etat] + poids[dernier][depart]

            if cout < meilleur_cout:
                meilleur_cout = cout
                meilleur_dernier = dernier

    if meilleur_dernier is None:
        fin = time.perf_counter()
        return {
            "cout": None,
            "chemin": None,
            "temps": fin - debut,
            "qualite": 0,
            "ratio": None
        }

    # on reconstruit le chemin optimal
    chemin_inverse = [meilleur_dernier]
    ensemble_courant = ensemble_total
    courant = meilleur_dernier

    while courant != depart:
        precedent = parent[(ensemble_courant, courant)]
        if precedent == depart:
            break
        chemin_inverse.append(precedent)
        ensemble_courant = ensemble_courant - {courant}
        courant = precedent

    chemin = [depart] + list(reversed(chemin_inverse)) + [depart]

    fin = time.perf_counter()

    if cout_optimal is not None and cout_optimal > 0:
        ratio = meilleur_cout / cout_optimal
        qualite = cout_optimal / meilleur_cout
    else:
        ratio = 1.0
        qualite = 1.0

    return {
        "algorithme": "TSP programmation dynamique",
        "cout": meilleur_cout,
        "chemin": chemin,
        "temps": fin - debut,
        "etats_dp": len(dp),
        "qualite": qualite,
        "ratio": ratio
    }

def est_valide(graphe, sommet, couleur, coloration):
    """
    check si on peut donner couleur à sommet sans conflit avec ses voisins
    """
    for voisin in graphe.get(sommet, []):
        if coloration.get(voisin) == couleur:
            return False
    return True


def coloration_k_couleurs(graphe, k):
    """
    colorie le graphe avec k couleurs si possible
    graphe -> dict[sommet, list[sommet]]
    k -> nombre de couleurs disponibles
    renvoie coloration du graphe ou none si impossible
    """
    sommets = list(graphe.keys())
    couleurs = list(range(k))
    coloration = {}

    def backtrack(index):
        if index == len(sommets):
            return True
        sommet = sommets[index]

        for couleur in couleurs:
            if est_valide(graphe, sommet, couleur, coloration):
                coloration[sommet] = couleur

                if backtrack(index + 1):
                    return True
                del coloration[sommet]
        return False
    if backtrack(0):
        return coloration
    return None

def coloration_minimale(graphe):
    """
    trouve le nombre minimal de couleurs nécessaires
    """
    n = len(graphe)
    for k in range(1, n + 1):
        coloration = coloration_k_couleurs(graphe, k)
        if coloration is not None:
            return k, coloration
    return None, None