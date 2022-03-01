"""
Fonction utilisees dans le plateau
"""

from src.logger.Logger import logger


def trouver_element_avec_nom(nom_element: str, liste: list):
	"""
	Trouver un element (carte, merveille, jeton progres) avec son nom dans une liste.

	:param nom_element: nom de l element a chercher.
	:param liste: liste des objets ou chercher l element.
	:return: l element si trouvee, None sinon.
	"""
	
	logger.debug(f"trouver_element_avec_nom(\'{nom_element}\'\n{afficher(liste)})")
	
	for element in liste:
		if element.nom == nom_element:
			logger.debug(f"\t\'{nom_element}\' est dans la liste")
			return element
	
	logger.debug(f"\t\'{nom_element}\' n'est pas dans la liste")
	return None


def demander_element_dans_une_liste(nom_joueur: str, type_element: str, liste_element: list):
	"""
	Renvoie l element contenu dans liste_element correspondant au nom donne par le nom_joueur.

	:param nom_joueur: le nom du nom_joueur a qui on demande l element.
	:param type_element: le type d element de que l on cherche (uniquement pour l'affichage)
		(carte, merveille, jeton progres).
	:param liste_element: la liste ou l on cherche l element.
	:return: l element choisi.
	"""
	
	logger.debug(f"[{nom_joueur}] demander_element_dans_une_liste(\'{type_element}\'\n{afficher(liste_element)})")
	
	while True:
		print(f"* liste choix possibles *\n{afficher(liste_element)}")
		nom_element = input(f"[{nom_joueur}] Choix {type_element} ?\n > ")
		element_choisi = trouver_element_avec_nom(nom_element, liste_element)
		
		if element_choisi is None:
			print(f" * ERREUR * Aucun element ne repond au nom \'{nom_element}\', veuillez recommencer")
			continue
		else:
			break
	
	logger.debug(f"[{nom_joueur}] a choisit \'{element_choisi.nom}\'")
	return element_choisi


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


def demander_ressource_dans_une_liste(nom_joueur: str, liste_element: list):
	"""
	Renvoie l element contenu dans liste_element correspondant au nom donne par le nom_joueur.

	:param nom_joueur: le nom du nom_joueur a qui on demande l element.
	:param liste_element: la liste ou l on cherche la ressource.
	:return: la ressource choisie.
	"""
	
	logger.debug(f"[{nom_joueur}] demander_ressource_dans_une_liste(\n{afficher(liste_element)})")
	
	while True:
		print(f"* liste choix possibles *\n{liste_element}")
		nom_ressource = input(f"[{nom_joueur}] Choix ressource ?\n > ")
		ressource_choisie = trouver_ressource_avec_nom(nom_ressource, liste_element)
		
		if ressource_choisie is None:
			print(f" * ERREUR * Aucune ressource ne repond au nom \'{nom_ressource}\', veuillez recommencer")
			continue
		else:
			break
	
	logger.debug(f"[{nom_joueur}] a choisit \'{ressource_choisie}\'")
	return nom_ressource, ressource_choisie


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
