"""
Fonction utilisees dans le plateau
"""


def trouver_ressource_avec_nom(nom_ressource: str, liste: list):
    """
    Trouver une ressource avec son nom dans une liste.

    :param nom_ressource: le nom de la ressource.
    :param liste: une liste de ressource.
    :return: la ressource correspondant au nom.
    """

    for ressource in liste:

        # decoupage
        ressource_split = ressource.split(" ")

        if ressource_split[0] == "ressource" and ressource_split[1] == nom_ressource:
            return ressource

    return None


def mon_str_liste(liste: list) -> str:
    """
    Affiche une liste de Carte, CarteFille, ...

    :param liste: la liste a afficher.
    :return: l'affichage de la liste.
    """
    if liste is None:
        return "None\n"
    if len(liste) == 0:
        return "vide\n"

    affichage = ""
    for elem in liste:
        affichage += str(elem) + "\n"
    return affichage


def mon_str_liste2D(liste: list) -> str:
    if liste is None:
        return "None\n"
    if len(liste) == 0:
        return "vide\n"

    affichage = ""
    for elem in liste:
        affichage += mon_str_liste(elem) + "\n"
    return affichage
