"""
Fonction utilisees dans le plateau
"""

from src.logger.Logger import logger


def trouver_element_avec_nom(nom: str, liste: list):
	"""
	Trouver un element (carte_a_enlever, merveille) avec son nom dans une liste.

	:param nom: nom de l element a chercher.
	:param liste: liste des objets ou chercher l element.
	:return: l element si trouvee, None sinon.
	"""
	
	logger.debug(f"trouver_element_avec_nom avec le nom \'{nom}\' dans la liste : \n {afficher(liste)}")
	
	for element in liste:
		if element.nom == nom:
			logger.debug(f"\t\'{nom}\' est dans la liste")
			return element
	
	logger.debug(f"\t\'{nom}\' n'est pas dans la liste")
	return None


def demander_element_dans_une_liste(nom_joueur: str, type_element: str, liste_element: list):
	"""
	Renvoie l element contenu dans liste_element correspondant au nom renseigne par le nom_joueur.

	:param nom_joueur: le nom du nom_joueur a qui on demande l element.
	:param type_element: le type d element de que l on cherche (uniquement pour l'affichage)
		(carte_a_enlever, merveille, ..).
	:param liste_element: la liste ou l on cherche l element.
	:return: l element choisi.
	"""
	
	logger.debug(f"[{nom_joueur}] demander_element_dans_une_liste choisit \'{type_element}\' "
		f"dans la liste : \n{afficher(liste_element)}")
	
	while True:
		print(f"* liste choix possibles *\n{afficher(liste_element)}")
		nom_element = input(f"[{nom_joueur}] Choix {type_element} ?\n > ")
		element_choisi = trouver_element_avec_nom(nom_element, liste_element)
		if element_choisi is None:
			print(f" * ERREUR * Aucun element ne repond au nom \'{nom_element}\', veuillez recommencer * ERREUR * ")
			continue
		else:
			break
	
	logger.debug(f"[{nom_joueur}] a choisit \'{element_choisi.nom}\'")
	return element_choisi


def afficher(liste: list) -> str:
	"""
	Affiche une liste de Carte, CarteFille, ...

	:param liste: la liste a afficher.
	:return: return l'affichage de la liste.
	"""
	if liste is None:
		return "None"
	if len(liste) == 0:
		return "vide"
	
	affichage = ""
	for elem in liste:
		affichage += str(elem) + "\n"
	return affichage
