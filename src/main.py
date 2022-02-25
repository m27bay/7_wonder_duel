"""
fichier principale
"""
import logging
import random

logging.basicConfig(filename="../logger.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Generique:
	"""
	Classe generique permettant de stocker le nom et le chemin des objects du jeu
	Nom a changer par la suite.
	"""
	
	def __init__(self, nom, chemin_image):
		self.nom = nom
		self.chemin_image = chemin_image


class Carte(Generique):
	"""
	Classe representant une carte.
	"""
	
	def __init__(self, nom, chemin_image, effets, couts, nom_carte_chainage, couleur, age):
		"""
		Constructeur de la classe Carte.

		:param nom: nom de la carte.
		:param chemin_image: chemin pour afficher la carte.
		:param effets: liste d effets que donne la carte respectant un pattern precis.
		:param couts: liste de couts pour construire la carte respactant un pattern precis.
		:param nom_carte_chainage: nom de la carte permettant de construire gratuitement la carte.
		:param couleur: couleur de la carte.
		:param age: age de la carte (entre 1 et 3).
		"""
		super().__init__(nom, chemin_image)
		self.effets = effets
		self.couts = couts
		self.nom_carte_chainage = nom_carte_chainage
		self.couleur = couleur
		self.age = age
		self.est_face_cachee = False
	
	def devoiler(self):
		"""
		Devoile la carte, indique que la carte n est plus face cachee.
		"""
		logger.debug(f"devoilement carte {self.nom}")
		self.est_face_cachee = False
	
	def cacher(self):
		"""
		Cacher la carte, indique que la carte est face cachee.
		"""
		logger.debug(f"cachement carte {self.nom}")
		self.est_face_cachee = True
	
	def __eq__(self, other):
		"""
		Redefinition de l operateur == pour une Carte.
		Deux cartes sont identiques si elles ont le meme nom.

		:param other: une autre carte a comparer.
		:return: vrai/ faux
		"""
		if isinstance(other, Carte):
			return self.nom == other.nom
		else:
			return False
	
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
		       f"image : {self.chemin_image}, " \
		       f"effets : {str(self.effets)}, " \
		       f"couts : {str(self.couts)}, " \
		       f"cout chainage : {self.nom_carte_chainage}, " \
		       f"couleur : {self.couleur}, " \
		       f"age : {self.age}, " \
		       f"face cachee : {self.est_face_cachee}"


class Merveille(Carte):
	"""
	Classe representant une merveille, une classe fille de la classe Carte.
	"""
	
	def __init__(self, nom, chemin_image, effets, couts):
		"""
		Constructeur de la classe Merveille.

		:param nom: nom de la merveille.
		:param chemin_image: chemin pour afficher la merveille.
		:param effets: liste d effets que donne la merveille respectant un pattern precis.
		:param couts: liste de couts pour construire la merveille respactant un pattern precis.
		"""
		super().__init__(nom, chemin_image, effets, couts, None, None, None)


class JetonProgres(Generique):
	"""
	Classe representant un jeton progres
	"""
	
	def __init__(self, nom, chemin_image, effets):
		"""
		Constructeur de la classe JetonProgres.

		:param nom: nom du jeton.
		:param effets: liste des effets du jeton.
		"""
		super().__init__(nom, chemin_image)
		self.effets = effets
	
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
		       f"chemin_image : {self.chemin_image}, " \
		       f"effets : {str(self.effets)}"


class JetonMilitaire(Generique):
	"""
	Classe representant un jeton militaire
	"""
	
	def __init__(self, nom, chemin_image, pieces, points_victoire):
		super().__init__(nom, chemin_image)
		self.est_utilise = False
		self.pieces = pieces
		self.points_victoire = points_victoire


class Joueur:
	"""
	Classe representant un joueur.
	"""
	
	def __init__(self, nom):
		"""
		Constructeur de la classe Joueur.

		:param nom: nom du joueur.
		"""
		self.nom = nom
		
		#
		self.cartes = []
		self.merveilles = []
		self.monnaie = 0
		self.points_victoire = 0
		self.jetons = []
	
	def couts_manquants(self, carte: Carte):
		"""
		Renvoie une liste des ressources_manquantes (monnaie ou matiere premiere/ produit manufacture)
		que le joueur ne possede pas pour construire une carte.

		:param carte: carte a construire.
		:return: une liste avec les ressources_manquantes manquantes.
		"""
		
		logger.debug(f"[{self.nom}] couts_manquants avec la carte [{carte}]")
		
		# Cout ou Effet
		# "monnaie prix"
		# "ressource type quantite"
		couts_manquants_carte = carte.couts.copy()
		for cout_manquant in carte.couts:
			
			# decoupage couts de la carte
			cout_manquant_split = cout_manquant.split(" ")
			
			# cout monnetaire
			if cout_manquant_split[0] == "monnaie":
				
				if self.monnaie < int(cout_manquant_split[1]):
					# changement du cout avec le cout manquant
					prix_manquant = str(int(cout_manquant_split[1]) - self.monnaie)
					monnaie_manquante = "monnaie " + prix_manquant
					couts_manquants_carte[couts_manquants_carte.index(cout_manquant)] = monnaie_manquante
					
					logger.debug(f"\t[{self.nom}] manque {monnaie_manquante}")
				
				else:
					# ce n'est pas un cout manquant
					couts_manquants_carte.remove(cout_manquant)
					logger.debug(f"\t[{self.nom}] possede argent necessaire")
			
			# cout ressource
			else:
				for ma_carte in self.cartes:
					for effet in ma_carte.effets:
						
						# decoupage effets
						effet_split = effet.split(" ")
						
						# si c'est la même ressource
						if cout_manquant_split[1] == effet_split[1]:
							
							if int(effet_split[2]) < int(cout_manquant_split[2]):
								# changement du cout avec le cout manquant
								quantite_manquante = str(int(cout_manquant_split[2]) - int(effet_split[2]))
								ressource_manquante = effet_split[0] + " " + effet_split[1] + " " + quantite_manquante
								couts_manquants_carte[couts_manquants_carte.index(cout_manquant)] = ressource_manquante
								
								logger.debug(f"\t[{self.nom}] manque {ressource_manquante}")
							
							else:
								# ce n'est pas un cout manquant
								couts_manquants_carte.remove(cout_manquant)
								logger.debug(f"\t[{self.nom}] possede {cout_manquant_split[1]}")
		
		return couts_manquants_carte
	
	def possede_carte_chainage(self, carte: Carte):
		"""
		Indique si le joueur possede la carte de chainage de la carte en parametre.

		:param carte: la carte dont on cherche la carte de chainage.
		:return: vrai/ faux.
		"""
		
		logger.debug(f"[{self.nom}] possede_carte_chainage avec la carte \'{carte}\'")
		
		# si la carte ne possede pas de carte de chainage
		if carte.nom_carte_chainage is None:
			logger.debug(f"\t[{self.nom}] la carte n a pas de carte de chainage")
			return False
		
		#
		for ma_carte in self.cartes:
			if ma_carte.nom == carte.nom_carte_chainage:
				logger.debug(f"\t[{self.nom}] possede la carte chainage")
				return True
		
		logger.debug(f"\t[{self.nom}] ne possede pas carte chainage")
		return False
	
	def production_type_ressources(self, ressource: str):
		"""
		Retourne la carte produisant la ressource.

		:param ressource: la ressource dont on veut la carte.
		:return: une carte si elle existe, None sinon.
		"""
		
		logger.debug(f"[{self.nom}] production_type_ressources avec la ressource \'{ressource}\'")
		
		ressource_split = ressource.split(" ")
		for carte in self.cartes:
			for effet in carte.effets:
				effet_split = effet.split(" ")
				
				# ressource type quantite
				if effet_split[0] == "ressource" and effet_split[1] == ressource_split[1]:
					logger.debug(f"\t[{self.nom}] possede une carte qui produit la ressource")
					return carte
		
		logger.debug(f"\t[{self.nom}] ne possede pas de carte qui produit la ressource")
		return None
	
	def possede_carte_reduction(self, ressource: str):
		"""
		Renvoie le prix de la reduction de la ressource.

		:param ressource: la ressource dont on cherche la reduction.
		:return: le prix reduit si le joueur possede une carte reduction de la ressource, 0 sinon.
		"""
		
		logger.debug(f"[{self.nom}] possede_carte_reduction avec la ressource \'{ressource}\'")
		
		for carte in self.cartes:
			for effet in carte.effets:
				effet_split = effet.split(" ")
				
				# reduc_ressource type prixReduc
				if effet_split[0] == "reduc_ressource" and effet_split[1] == ressource:
					logger.debug(f"\t[{self.nom}] possede une carte donnant une reduction")
					return int(effet_split[2])
		
		logger.debug(f"\t[{self.nom}] ne possede pas de carte donnant une reduction")
		return 0
	
	def possede_cartes_couleur(self, couleur: str) -> list:
		"""
		Renvoie une liste de carte de la même couleur que celle en parametre.

		:param couleur: la couleur a rechercher.
		:return: une liste de carte.
		"""
		
		logger.debug(f"[{self.nom}] possede_cartes_couleur avec la couleur \'{couleur}\'")
		
		liste_cartes_couleur = []
		for carte in self.cartes:
			if carte.couleur == couleur:
				logger.debug(f"\t[{self.nom}] la carte \'{carte.nom}\' est de la même couleur")
				liste_cartes_couleur.append(carte)
		
		return liste_cartes_couleur
	
	def compter_point_victoire(self) -> None:
		"""
		Ajoute les points de victoires des differents objets (Carte, Jeton, Merveille)
		"""
		# compter points victoire avec les cartes
		for carte in self.cartes:
			for effet in carte.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire":
					self.points_victoire += int(effet_split[1])
		
		# compter points de victoire avec les merveilles
		for merveille in self.merveilles:
			for effet in merveille.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire":
					self.points_victoire += int(effet_split[1])
		
		# compter points de victoire avec les jetons
		for jeton in self.jetons:
			for effet in jeton.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire_par_jeton":
					self.points_victoire += int(effet_split[1]) * len(self.jetons)
				elif effet_split[0] == "point_victoire":
					self.points_victoire += int(effet_split[1])
				elif effet_split[0] == "point_victoire_fin_partie":
					self.points_victoire += int(effet_split[1])


def trouver_element_avec_nom(nom: str, liste: list):
	"""
	Trouver un element (carte, merveille) avec son nom dans une liste.

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


def demander_element_dans_une_liste(joueur: Joueur, type_element: str, liste_element: list):
	"""
	Renvoie l element contenu dans liste_element correspondant au nom renseigne par le joueur.

	:param joueur: le joueur a qui on demande l element.
	:param type_element: le type d element de que l on cherche (uniquement pour l'affichage) (carte, merveille, ..).
	:param liste_element: la liste ou l on cherche l element.
	:return: l element choisi.
	"""
	
	logger.debug(f"[{joueur.nom}] demander_element_dans_une_liste choisit \'{type_element}\' "
	             f"dans la liste : \n {afficher(liste_element)}")
	
	while True:
		print(f"* liste choix possibles *\n{afficher(liste_element)}")
		nom_element = input(f"[{joueur.nom}] Choix {type_element} ?\n > ")
		element_choisi = trouver_element_avec_nom(nom_element, liste_element)
		if element_choisi is None:
			print(f" * ERREUR * Aucun element ne repond au nom \'{nom_element}\', veuillez recommencer * ERREUR * ")
			continue
		else:
			break
	
	logger.debug(f"[{joueur.nom}] a choisit \'{element_choisi.nom}\'")
	return element_choisi


def selection_merveille(nbr_repetition: int, joueur: Joueur, liste_merveilles_alea: list) -> None:
	"""
	Selection d'un ou des merveilles pour le joueur parmis une liste de merveille.

	:param nbr_repetition: nombre de merveille a choisir.
	:param joueur: joueur qui choisi.
	:param liste_merveilles_alea: une liste de merveille ou choisir la/les merveille(s).
	"""
	if len(liste_merveilles_alea) == 1:
		print(f"\nAttribution de la derniere merveille ({liste_merveilles_alea[0].nom})"
		      f" au [{joueur.nom}]")
		joueur.merveilles.append(liste_merveilles_alea[0])
		liste_merveilles_alea.remove(liste_merveilles_alea[0])
	else:
		for _ in range(nbr_repetition):
			merveille_choisie = demander_element_dans_une_liste(joueur, "merveille", liste_merveilles_alea)
			joueur.merveilles.append(merveille_choisie)
			liste_merveilles_alea.remove(merveille_choisie)


def afficher(liste: list) -> str:
	"""
	Affiche une liste de Carte, Merveille, ...

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


class Jeu:
	"""
	Classe Jeu
	"""
	
	def __init__(self, joueur1: Joueur, joueur2: Joueur, choix_auto_merveilles: bool = True):
		"""
		Constructeur de la classe jeu.

		:param joueur1: premier joueur.
		:param joueur2: deuxieme joueur.
		:param choix_auto_merveilles: boolean indiquant si le choix des merveilles est automatique ou non.
		"""
		self.joueur1 = joueur1
		self.joueur2 = joueur2
		self.joueur_qui_joue = None
		
		#
		self.choix_auto_merveilles = choix_auto_merveilles
		self.monnaie_banque = 86  # 14 de valeur 1, 10 de valeur 3, 7 de valeur 6
		self.age = 1
		
		#  0: neutre
		# +9: victoire militaire joueur1
		# -9: victoire militaire joueur2
		self.position_jeton_militaire = 0
		self.jetons_militaire = [
			JetonMilitaire("5piecesJ1", None, 5, 10),
			JetonMilitaire("2piecesJ1", None, 2, 5),
			JetonMilitaire("0piecesJ1", None, 0, 2),
			JetonMilitaire("0piecesJ2", None, 0, 2),
			JetonMilitaire("2piecesJ2", None, 2, 5),
			JetonMilitaire("5piecesJ2", None, 5, 10)
		]
		
		# liste des jetons progres, constructeur : JetonProgres(nom, effets)
		self.jetons_progres = [
			JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"]),
			JetonProgres("architecture", None, ["reduc_merveille"]),
			JetonProgres("economie", None, ["gain_monnaie_adversaire"]),
			JetonProgres("loi", None, ["symbole_scientifique"]),
			JetonProgres("maconnerie", None, ["reduc_carte bleu"]),
			JetonProgres("philosophie", None, ["point_victoire_fin_partie 7"]),
			JetonProgres("mathematiques", None, ["point_victoire_par_jeton 3", "point_victoire 3"]),
			JetonProgres("strategie", None, ["bonus_attaque"]),
			JetonProgres("theologie", None, ["rejouer"]),
			JetonProgres("urbanisme", None, ["monnaie 6", "bonus_monnaie_chainage 4"]),
		]
		# jeton choisi et place sur le plateau
		self.jetons_progres_plateau = []
		
		# pour stocker les cartes defaussees
		self.cartes_defaussees = []
		
		# listes des cartes, constructeur : Carte(nom, chemin_image, effets, couts, nom_carte_chainage, couleur, age)
		self.cartes_age_I = [  # initialisation cartes age I
			Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1),
			Carte("exploitation", None, ["ressource bois 1"], ["monnaie 1"], None, "marron", age=1),
			Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1),
			Carte("cavite", None, ["ressource argile 1"], ["monnaie 1"], None, "marron", age=1),
			Carte("gisement", None, ["ressource pierre 1"], None, None, "marron", age=1),
			Carte("mine", None, ["ressource pierre 1"], ["monnaie 1"], None, "marron", age=1),
			Carte("verrerie", None, ["ressource verre 1"], ["monnaie 1"], None, "grise", age=1),
			Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1),
			Carte("tour de garde", None, "attaquer 1", None, None, "rouge", age=1),
			Carte("atelier", None, ["symbole_scientifique pendule", "point_victoire 1"], ["ressource papurys 1"],
				None, "vert", age=1),
			Carte("apothicaire", None, ["symbole_scientifique roue", "point_victoire 1"], ["ressource verre 1"],
				None, "vert", age=1),
			Carte("depot de pierre", None, ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1),
			Carte("depot d argile", None, ["reduc_ressource argile 1"], ["monnaie 3"], None, "jaune", age=1),
			Carte("depot de bois", None, ["reduc_ressource bois 1"], ["monnaie 3"], None, "jaune", age=1),
			Carte("ecuries", None, ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1),
			Carte("caserne", None, ["attaquer 1"], ["ressource argile 1"], None, "rouge", age=1),
			Carte("palissade", None, ["attaquer 1"], ["monnaie 2"], None, "rouge", age=1),
			Carte("scriptorium", None, ["symbole_scientifique plume"], ["monnaie 2"], None, "vert", age=1),
			Carte("officine", None, ["symbole_scientifique pilon"], ["monnaie 2"], None, "vert", age=1),
			Carte("theatre", None, ["point_victoire 3"], None, None, "blue", age=1),
			Carte("autel", None, ["point_victoire 3"], None, None, "blue", age=1),
			Carte("bains", None, ["point_victoire 3"], ["ressource pierre 1"], None, "bleu", age=1),
			Carte("taverne", None, ["monnaie 4"], None, None, "jaune", age=1)
		]
		self.cartes_age_II = [  # initialisation cartes age II
			Carte("scierie", None, ["ressource bois 2"], ["monnaie 2"], None, "marron", age=2),
			Carte("briqueterie", None, ["ressource argile 2"], ["monnaie 2"], None, "marron", age=2),
			Carte("carriere", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2),
			Carte("soufflerie", None, ["ressource verre 1"], None, None, "gris", age=2),
			Carte("sechoir", None, ["ressource papyrus 1"], None, None, "gris", age=2),
			Carte("muraille", None, ["attaquer 2"], ["ressource pierre 2"], None, "rouge", age=2),
			Carte("forum", None, ["ressource_au_choix verre papyrus"], ["monnaie 3", "ressource argile 1"],
				None, "jaune", age=2),
			Carte("caravanserail", None, ["ressource_au_choix bois argile pierre"],
				["monnaie 2", "ressource verre 1", "ressource papyrus 1"], None, "jaune", age=2),
			Carte("douanes", None, ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
				None, "jaune", age=2),
			Carte("tribunal", None, ["point_victoire 5"], ["ressource bois 2", "ressource verre 1"], None,
				"bleu", age=2),
			Carte("haras", None, ["attaquer 1"], ["ressource argile 1", "ressource bois 1"], "ecuries", "rouge", age=2),
			Carte("baraquements", None, ["attaquer 1"], ["monnaie 3"], "caserne", "rouge", age=2),
			Carte("champ de tir", None, ["attaquer 2"],
				["ressource pierre 1", "ressource bois 1", "ressource papyrus 1"],
				None, "rouge", age=2),
			Carte("place d'armes", None, ["attaquer 2"], ["ressource argile 2", "ressource verre 1"], None, "rouge",
				age=2),
			Carte("bibliotheque", None, ["symbole_scientifique plume", "point_victoire 2"],
				["ressource pierre 1", "ressource bois 1", "ressource verre 1"], "scriptorium", "vert", age=2),
			Carte("dispensaire", None, ["symbole_scientifique pilon", "point_victoire 2"],
				["ressource argile 2", "ressource verre 1"], "officine", "vert", age=2),
			Carte("ecole", None, ["symbole_scientifique roue", "point_victoire 1"],
				["ressource papyrus 2", "ressource bois 1"], None, "vert", age=2),
			Carte("laboratoire", None, ["symbole_scientifique pendule", "point_victoire 1"],
				["ressource verre 2", "ressource bois 1"], None, "vert", age=2),
			Carte("statue", None, ["point_victoire 4"], ["ressource argile 2"], "theatre", "bleu", age=2),
			Carte("temple", None, ["point_victoire 4"], ["ressource papyrus 1", "ressource bois 1"], "autel",
				"bleu", age=2),
			Carte("aqueduc", None, ["point_victoire 5"], ["ressource pierre 3"], "bains", "bleu", age=2),
			Carte("rostres", None, ["point_victoire 4"], ["ressource pierre 1", "ressource bois 1"],
				None, "bleu", age=2),
			Carte("brasserie", None, ["monnaie 6"], None, "taverne", "jaune", age=2)
		]
		self.cartes_age_III = [  # initialisation cartes age III
			Carte("arsenal", None, ["attaquer 3"], ["ressource argile 3", "ressource bois 2"], None, "rouge", age=3),
			Carte("pretoire", None, ["attaquer 3"], ["monnaie 8"], None, "rouge", age=3),
			Carte("academie", None, ["symbole_scientifique cadran_solaire", "point_victoire 3"],
				["ressource pierre 1", "ressource bois 1", "ressource verre 2"], None, "vert", age=3),
			Carte("etude", None, ["symbole_scientifique cadran_solaire", "point_victoire 3"],
				["ressource papyrus 1", "ressource bois 2", "ressource verre 1"], None, "vert", age=3),
			Carte("chambre de commerce", None, ["monnaie_par_carte grise 3", "point_victoire 3"],
				["ressource papyrus 2"], None, "jaune", age=3),
			Carte("port", None, ["monnaie_par_carte marron 2", "point_victoire 3"],
				["ressource verre 1", "ressource bois 1", "ressource papyrus 1"], None, "jaune", age=3),
			Carte("armurie", None, ["monnaie_par_carte rouge 1", "point_victoire 3"],
				["ressource pierre 2", "ressource verre 1"], None, "jaune", age=3),
			Carte("palace", None, ["point_victoire 7"],
				["ressource argile 1", "ressource pierre 1", "ressource bois 1", "ressource verre 2"],
				None, "bleu", age=3),
			Carte("hôtel de ville", None, ["point_victoire 7"], ["ressource pierre 3", "ressource bois 2"],
				None, "bleu", age=3),
			Carte("obelisque", None, ["point_victoire 5"], ["ressource pierre 2", "ressource verre 1"],
				None, "bleu", age=3),
			Carte("fortification", None, ["attaquer 2"],
				["ressource pierre 2", "ressource argile 1", "ressource papyrus 1"],
				"palissade", "rouge", age=3),
			Carte("atelier de siege", None, ["attaquer 2"], ["ressource bois 3", "ressource verre 1"],
				"champ de tir", "rouge", age=3),
			Carte("cirque", None, ["attaquer 2"], ["ressource argile 2", "ressource pierre 2"],
				"place d'arme", "rouge", age=3),
			Carte("universite", None, ["symbole_scientifique sphere_armillaire", "point_victoire 2"],
				["ressource argile 1", "ressource verre 1", "ressource papyrus 1"], "ecole", "vert", age=3),
			Carte("observatoire", None, ["symbole_scientifique sphere_armillaire", "point_victoire 2"],
				["ressource pierre 1", "ressource papyrus 2"], "laboratoire", "vert", age=3),
			Carte("jardin", None, ["point_victoire 6"], ["ressource argile 2", "ressource bois 2"], "statue",
				"bleu", age=3),
			Carte("pantheon", None, ["point_victoire 6"],
				["ressource argile 1", "ressource bois 1", "ressource papyrus 2"],
				"temple", "bleu", age=3),
			Carte("senat", None, ["point_victoire 5"],
				["ressource argile 2", "ressource pierre 1", "ressource papyrus 2"],
				"rostres", "bleu", age=3),
			Carte("phare", None, ["monnaie_par_carte jaune 1", "point_victoire 3"],
				["ressource argile 2", "ressource verre 1"], "taverne", "jaune", age=3),
			Carte("arene", None, ["monnaie_par_merveille 2", "point_victoire 3"],
				["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3),
		]
		
		#  TODO : Ajouter cartes guilde dans ageIII
		# carte sur le plateau de jeu
		self.cartes_plateau = []
		
		# liste des merveilles, constructeur : Merveille(nom, chemin_image, effets)
		self.merveilles = [
			Merveille("circus maximus", None,
				["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
				["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
				),
			Merveille("colosse", None,
				["attaquer 2", "point_victoire 3"],
				["ressource argile 3", "ressource verre 1"]
				),
			Merveille("grand phare", None,
				["ressource_au_choix bois argile pierre", "point_victoire 4"],
				["ressource bois 1", "ressource pierre 1", "ressource papyrus 2"]
				),
			Merveille("jardin suspendus", None,
				["monnaie 6", "rejouer", "point_victoire 3"],
				["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"]
				),
			Merveille("grande bibliotheque", None,
				["jeton_progres_aleatoire", "point_victoire 4"],
				["ressource bois 3", "ressource verre 1", "ressource papyrus 1"]
				),
			Merveille("mausolee", None,
				["construction_fausse_gratuite", "point_victoire 2"],
				["ressource argile 2", "ressource verre 2", "ressource papyrus 1"]
				),
			Merveille("piree", None,
				["ressource_au_choix papyrus verre", "rejouer", "point_victoire 2"],
				["ressource bois 2", "ressource pierre 1", "ressource argile 1"]
				),
			Merveille("pyramides", None,
				["point_victoire 9"],
				["ressource pierre 3", "ressource papyrus 1"]
				),
			Merveille("sphinx", None,
				["rejouer", "point_victoire 6"],
				["ressource pierre 1", "ressource argile 1", "ressource verre 2"]
				),
			Merveille("statue de zeus", None,
				["defausse_carte_adversaire marron", "attaquer 1", "point_victoire 3"],
				["ressource pierre 1", "ressource bois 1",
					"ressource argile 1", "ressource papyrus 2"]
				),
			Merveille("temple d'artemis", None,
				["monnaie 12", "rejouer"],
				["ressource bois 1", "ressource pierre 1",
					"ressource verre 1", "ressource papyrus 1"]
				),
			Merveille("via appia", None,
				["monnaie 3", "adversaire_perd_monnaie 3", "rejouer", "point_victoire 3"],
				["ressource pierre 2", "ressource argile 2", "ressource papyrus 1"]
				)
		]
	
	def preparation_plateau(self) -> None:
		"""
		Prepare le plateau, les cartes, les jetons, la monnaie des joueurs, les merveilles des joueurs.
		"""
		logger.debug("preparation_plateau")
		self.preparation_cartes()
		self.preparation_jetons_progres()
		self.preparation_argent()
		self.preparation_merveilles()
	
	def preparation_cartes(self) -> None:
		"""
		Prepare les cartes, sort aleatoirement des cartes et le place selon une structure precise.
		"""
		logger.debug("preparation_cartes")
		# preparation de la structure des cartes en fonction de l age.
		if self.age == 1:
			logger.debug(f"\tpreparation_cartes age {self.age}")
			self.cartes_plateau = [
				[0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
				[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
			]
			liste_carte = self.cartes_age_I
		elif self.age == 2:
			logger.debug(f"\tpreparation_cartes age {self.age}")
			self.cartes_plateau = [
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
				[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
				[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
			]
			liste_carte = self.cartes_age_II
		else:  # Age 3
			logger.debug(f"\tpreparation_cartes age {self.age}")
			self.cartes_plateau = [
				[0, 0, 1, 0, 1, 0, 0],
				[0, 1, 0, 1, 0, 1, 0],
				[1, 0, 1, 0, 1, 0, 1],
				[0, 1, 0, 0, 0, 1, 0],
				[1, 0, 1, 0, 1, 0, 1],
				[0, 1, 0, 1, 0, 1, 0],
				[0, 0, 1, 0, 1, 0, 0]
			]
			liste_carte = self.cartes_age_III
		
		# remplissage de la structure avec des cartes aleatoires.
		for ligne in range(len(self.cartes_plateau)):
			for colonne in range(len(self.cartes_plateau[ligne])):
				if self.cartes_plateau[ligne][colonne] == 1:
					carte = random.choice(liste_carte)
					# suppresion carte choisie pour ne pas la choisir a nouveau
					liste_carte.remove(carte)
					# une ligne sur deux la carte sont face cachee, par defaut une carte
					# n est pas face cachee
					if ligne % 2 != 0:
						carte.cacher()
					self.cartes_plateau[ligne][colonne] = carte
	
	def preparation_jetons_progres(self) -> None:
		"""
		Prepare les 5 jetons progres aleatoire du plateau.
		"""
		logger.debug("preparation_jetons_progres")
		for _ in range(5):
			jeton_random = random.choice(self.jetons_progres)
			self.jetons_progres.remove(jeton_random)
			self.jetons_progres_plateau.append(jeton_random)
	
	def preparation_argent(self) -> None:
		"""
		Prepare les monnaies des deux joueurs.
		"""
		logger.debug("preparation_argent")
		self.joueur1.monnaie = self.joueur2.monnaie = 7
	
	def preparation_merveilles(self) -> None:
		"""
		Prepare les merveilles.
		Sort aleatoirement 4 merveiles, le joueur1 en choisie 1, puis le joueur2 en choisie 2,
		enfin le joueur1 prend la derniere.
		Sort aleatoirement 4 merveiles, le joueur2 en choisie 1, puis le joueur1 en choisie 2,
		enfin le joueur2 prend la derniere.
		"""
		logger.debug("preparation_merveilles")
		if not self.choix_auto_merveilles:
			logger.debug("\tchoix non automatique")
			print("\n * Premiere selection de merveille aleatoire * \n")
			# choix aleatoire des 4 premieres merveilles
			liste_merveilles_alea = []
			for _ in range(4):
				liste_merveilles_alea.append(random.choice(self.merveilles))
			
			# les joueurs choississent leurs 4 premieres merveilles
			selection_merveille(1, self.joueur1, liste_merveilles_alea)
			selection_merveille(2, self.joueur2, liste_merveilles_alea)
			selection_merveille(1, self.joueur1, liste_merveilles_alea)
			
			print("\n * Deuxieme selection de merveille aleatoire * \n")
			# choix aleatoire des 4 dernieres merveilles
			for _ in range(4):
				liste_merveilles_alea.append(random.choice(self.merveilles))
			
			# les joueurs choississent leurs 4 dernieres merveilles
			selection_merveille(1, self.joueur2, liste_merveilles_alea)
			selection_merveille(2, self.joueur1, liste_merveilles_alea)
			selection_merveille(1, self.joueur2, liste_merveilles_alea)
		
		else:  # choix automatique des merveilles (d'apres les regles)
			logger.debug("\tchoix automatique")
			self.joueur1.merveilles.append(trouver_element_avec_nom("pyramides", self.merveilles))
			self.joueur1.merveilles.append(trouver_element_avec_nom("grand phare", self.merveilles))
			self.joueur1.merveilles.append(trouver_element_avec_nom("temple d artemis", self.merveilles))
			self.joueur1.merveilles.append(trouver_element_avec_nom("statue de zeus", self.merveilles))
			
			self.joueur2.merveilles.append(trouver_element_avec_nom("circus maximus", self.merveilles))
			self.joueur2.merveilles.append(trouver_element_avec_nom("piree", self.merveilles))
			self.joueur2.merveilles.append(trouver_element_avec_nom("via appia", self.merveilles))
			self.joueur2.merveilles.append(trouver_element_avec_nom("colosse", self.merveilles))
	
	def enlever_carte(self, carte: Carte) -> None:
		"""
		Enleve une carte du plateau.

		:param carte: la carte a enlever.
		"""
		for ligne in range(len(self.cartes_plateau)):
			for colonne in range(len(self.cartes_plateau[ligne])):
				if self.cartes_plateau[ligne][colonne] == carte:
					self.cartes_plateau[ligne][colonne] = 0
					return
		print("La carte n'est pas sur le plateau.")
	
	def obtenir_adversaire(self):
		"""
		Renvoie le joueur adverse, le joueur qui n'est pas stocke dans l attribut joueur_qui_joue.

		:return: joueur adverse
		"""
		if self.joueur_qui_joue == self.joueur1:
			return self.joueur2
		else:
			return self.joueur1
	
	def demander_action_carte(self, carte: Carte):
		"""
		Demande a l'utilisateur l action qu'il souhaite faire avec la carte (defausser, ou piocher).

		:param carte: la carte choisie par le joueur.
		"""
		
		str_action = f"[{self.joueur_qui_joue.nom}] defausser ou piocher ?\n > "
		while True:
			action = input(str_action)
			
			# defausser
			if action == "defausser":
				self.cartes_defaussees.append(carte)
				self.joueur_qui_joue.monnaie = self.joueur_qui_joue.monnaie + 2
				
				# gain de une piece par carte jaune
				for carte_joueur in self.joueur_qui_joue.cartes:
					if carte_joueur.couleur == "jaune":
						self.joueur_qui_joue.monnaie += 1
				
				# fin action carte
				break
			
			# piocher
			elif action == "piocher":
				
				# construction de la carte gratuite via chainage
				if not self.joueur_qui_joue.possede_carte_chainage(carte):
					
					if carte.couts is None:
						# fin action carte
						break
					
					# verification ressources joueur
					liste_ressource_necessaire = self.joueur_qui_joue.couts_manquants(carte)
					
					# le joueur possede toutes les ressouces
					if len(liste_ressource_necessaire) == 0:
						
						# on retire uniquement la monnaie
						for cout in carte.couts:
							# monnaie x
							cout_split = cout.split(" ")
							if cout_split[0] == "monnaie":
								self.joueur_qui_joue.monnaie -= int(cout_split[1])
						
						# fin action carte
						break
					
					else:
						# manque des ressouces
						for ressource_manquante in liste_ressource_necessaire:
							ressource_manquante_split = ressource_manquante.split(" ")
							
							# manque monnaie
							if ressource_manquante_split[0] == "monnaie":
								print("Vous n'avez pas assez de monnaie pour construire la carte. "
								      "Vous devez defausser la carte")
								continue
						
						# manque des ressources autre que monnaie
						prix = self.acheter_ressources(liste_ressource_necessaire)
						if prix > self.joueur_qui_joue.monnaie:
							print("Impossible de faire le commerce, vous n'avez pas assez de monnaie. "
							      "Vous devez defausser la carte")
							continue
						else:
							self.joueur_qui_joue.monnaie -= prix
							self.monnaie_banque += prix
							
							# fin action carte
							break
				
				else:  # le joueur possde la carte chainage, construction gratuite
					# fin action carte
					break
			else:
				print("action carte inconnue.")
				continue
		
		# suppression de la carte du plateau
		self.enlever_carte(carte)
	
	def demander_action_merveille(self):
		"""
		Demande a l'utilisateur si il souhaite construire une merveille.
		"""
		
		str_action = f"[{self.joueur_qui_joue.nom}] construire une merveille (oui/non) ?\n > "
		while True:
			action = input(str_action)
			if action == "oui":
				# TODO : carte a sacrfier ?
				return demander_element_dans_une_liste(self.joueur_qui_joue, "merveille", self.joueur_qui_joue.merveilles)
			elif action == "non":
				return None
			else:
				print("action merveille inconnue")
	
	def acheter_ressources(self, ressources_manquantes: list) -> int:
		"""
		Permet au joueur qui joue d'acheter les ressources qui lui manque pour construire sa carte.

		:param ressources_manquantes: liste des ressources manquantes
		:return prixDesRessources
		"""
		
		prix_commerce = 0
		
		# Verification si le joueur adverse produit les ressources manquantes
		adversaire = self.obtenir_adversaire()
		carte_liste_ressource_adversaire = []
		for ressource_manquante in ressources_manquantes:
			carte_production = adversaire.production_type_ressources(ressource_manquante)
			if carte_production is not None:
				carte_liste_ressource_adversaire.append(carte_production)
		
		# si le joueur adverse ne produit aucune ressouces ressources manquantes
		if len(carte_liste_ressource_adversaire) == 0:
			for ressource_manquante in ressources_manquantes:
				ressource_manquante_split = ressource_manquante.split(" ")
				
				if self.joueur_qui_joue.possede_carte_reduction(ressource_manquante_split[1]) != 0:
					# (1 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le joueur
					prix_commerce += int(ressource_manquante_split[2])
				else:
					# (2 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le joueur
					prix_commerce += (2 * int(ressource_manquante_split[2]))
		
		# le joueur adverse produit des ressouces qui me manquent
		else:
			# les cartes jaunes ne compte pas dans le commerce
			for carte in carte_liste_ressource_adversaire:
				if carte.couleur == "jaune":
					carte_liste_ressource_adversaire.remove(carte)
			
			for ressource_manquante in ressources_manquantes:
				ressource_manquante_split = ressource_manquante.split(" ")
				
				# si le joueur adversaire produit la ressource
				ressource_trouve = False
				
				# parmis les cartes produisant la ressouce que j'achete
				for carteRessourceAdversaire in carte_liste_ressource_adversaire:
					
					# parmis les effets de cette carte
					for effet in carteRessourceAdversaire.effets:
						ressource_adversaire_split = effet.split(" ")
						
						# joueur adversaire produit ressource qu'il me manque ?
						if ressource_manquante_split[1] == ressource_adversaire_split[1]:
							ressource_trouve = True
							
							# ai je une reduction sur cette ressource ?
							prix_reduc = self.joueur_qui_joue.possede_carte_reduction(ressource_manquante_split[1])
							if prix_reduc != 0:
								# (prix_reduc * quantite_ressource_necessaire pour le joueur)
								prix_commerce += (prix_reduc * int(ressource_manquante_split[2]))
							else:
								# (2 + quantite_ressource_adversaire) * quantite_ressource_necessaire pour le joueur
								prix_commerce += (
											(2 + int(ressource_adversaire_split[2])) * int(ressource_manquante_split[2]))
				
				# si l'adversaire ne produit pas la ressource
				if not ressource_trouve:
					prix_commerce += (2 * int(ressource_manquante_split[2]))
		
		return prix_commerce
	
	def reste_des_cartes(self) -> bool:
		"""
		Indique s'il reste des cartes sur le plateau.

		:return: vrai/ faux
		"""
		for ligne_carte in self.cartes_plateau:
			for carte in ligne_carte:
				if carte != 0:
					return True
		return False
	
	def changement_age(self) -> None:
		"""
		Permet de changer d'âge et de changer la structure des cartes du plateau.
		"""
		
		if self.age != 3:
			self.age += 1
			self.preparation_cartes()
		else:
			self.fin_de_partie()
	
	def cartes_prenable(self, ligne: int, colonne: int) -> bool:
		"""
		Indique si une carte est prenable ou non. C'est a dire qu'aucune autre carte n'est posee par dessus.

		:param ligne: ligne de la carte
		:param colonne: colonne de la carte.
		:return: vrai/ faux.
		"""
		
		if ligne == 4:
			return True
		elif ligne == 0:
			if colonne == 0:
				return self.cartes_plateau[ligne + 1][colonne + 1] == 0
			elif colonne == len(self.cartes_plateau[ligne]) - 1:
				return self.cartes_plateau[ligne + 1][colonne - 1] == 0
		else:
			return (self.cartes_plateau[ligne + 1][colonne - 1] == 0) \
			       and (self.cartes_plateau[ligne + 1][colonne + 1] == 0)
	
	def liste_cartes_prenables(self):
		"""
		Renvoie la liste des cartes prenable sur le plateau.

		:return: list carte prenable.
		"""
		cartes_prenable = []
		for ligne in range(len(self.cartes_plateau)):
			for colonne in range(len(self.cartes_plateau[ligne])):
				if self.cartes_plateau[ligne][colonne] != 0 and self.cartes_prenable(ligne, colonne):
					cartes_prenable.append(self.cartes_plateau[ligne][colonne])
		
		return cartes_prenable
	
	def defausser_carte_adversaire(self, couleur: str) -> None:
		"""
		Retire une carte de couleur de l'adversaire pour l'ajouter dans la liste des cartes faussees.

		:param couleur: la couleur de la carte a defausser.
		"""
		
		adversaire = self.obtenir_adversaire()
		while True:
			print(f"\n * liste choix possibles *\n{afficher(adversaire.cartes)}")
			type_element = input(f"[{self.joueur_qui_joue.nom}] Choix d'une carte {couleur}?\n > ")
			element_choisi = trouver_element_avec_nom(type_element, adversaire.cartes)
			if element_choisi is None or element_choisi.couleur != couleur:
				print("Choix incorrect")
				continue
			else:
				break
		
		adversaire.cartes.remove(element_choisi)
		self.cartes_defaussees.append(element_choisi)
	
	def gain_jeton_progres_alea(self) -> None:
		"""
		Le joueur gain 1 jeton parmis 3 jetons aleatoire non selectionnes au debut de la partie.
		"""
		
		# tirage aleatoire des 3 jetons
		liste_jetons = []
		for _ in range(3):
			jeton_random = random.choice(self.jetons_progres)
			liste_jetons.append(jeton_random)
			self.jetons_progres.remove(jeton_random)
		
		# le joueur en choisit 1
		jeton_choisi = demander_element_dans_une_liste(self.joueur_qui_joue, "jetons progres", liste_jetons)
		liste_jetons.remove(jeton_choisi)
		
		# les autres sont remis dans la boite
		for jeton in liste_jetons:
			self.jetons_progres.append(jeton)
	
	def construction_carte_defausser(self) -> None:
		"""
		Le joueur construit gratuitement une carte defaussee.
		"""
		
		carte_choisie = demander_element_dans_une_liste(self.joueur_qui_joue, "carte defausser", self.cartes_defaussees)
		self.joueur_qui_joue.cartes.append(carte_choisie)
		self.appliquer_effets_carte(carte_choisie)
	
	def demander_ressource_au_choix(self, liste_ressources: list) -> str:
		"""
		Si une carte possede l'effet "ressource_au_choix" le joueur doit choisir quel ressource il souhaite produire.

		:param liste_ressources: la liste des ressources au choix.
		:return: un nouvel effet, "ressource x 1", avec x la ressource choisit.
		"""
		
		ressource = "ressource "
		str_demande = f"[{self.joueur_qui_joue.nom}] Nom de la ressource choisie ?\n > "
		print(f"\n * liste des ressources *\n", liste_ressources)
		nom_ressource = input(str_demande)
		while nom_ressource not in liste_ressources:
			print("Ressource inconnu, veuillez recommencer")
			nom_ressource = input(str_demande)
		return ressource + nom_ressource + " 1"
	
	def gain_symbole_scientifique(self, nom_symbole_scientifique: str) -> bool:
		for ma_carte in self.joueur_qui_joue.cartes:
			for effet_ma_carte in ma_carte.effets:
				effet_ma_carte_split = effet_ma_carte.split(" ")
				
				# si possede une carte donnant le même symbole
				if effet_ma_carte_split[0] == "symbole_scientifique" and effet_ma_carte_split[1] == nom_symbole_scientifique:
					# 2 symboles identiques => gain jeton
					jeton_choisi = demander_element_dans_une_liste(self.joueur_qui_joue, "jeton", self.jetons_progres_plateau)
					self.joueur_qui_joue.jetons.append(jeton_choisi)
					
					# Suppression du jeton du plateau
					self.jetons_progres_plateau.remove(jeton_choisi)
					
					# suppression de l'effet gain symbole scientifique
					ma_carte.effets.remove(effet_ma_carte)
					return True
		return False
	
	def deplacer_pion_miltaire(self, nbr_deplacement: int):
		pass
	
	def appliquer_effets_carte(self, carte: Carte):
		for effet in carte.effets:
			effet_split = effet.split(" ")
			if effet_split[0] == "attaquer":
				self.deplacer_pion_miltaire(int(effet_split[1]))
			elif effet_split[0] == "symbole_scientifique":
				if self.gain_symbole_scientifique(effet_split[1]):
					carte.effets.remove(effet)
			elif effet_split[0] == "point_victoire":
				self.joueur_qui_joue.points_victoire += int(effet_split[1])
			elif effet_split[0] == "monnaie":
				self.joueur_qui_joue.monnaie += int(effet_split[1])
			elif effet_split[0] == "ressource_au_choix":
				# remplace effet ressource au choix par un ressource classique
				ressource = ""
				# "ressource_au_choix x y"
				if len(effet_split) == 3:
					ressource = self.demander_ressource_au_choix([effet_split[1], effet_split[2]])
				# "ressource_au_choix x y z"
				elif len(effet_split) == 4:
					ressource = self.demander_ressource_au_choix([effet_split[1], effet_split[2], effet_split[3]])
				carte.effets = [ressource]
			elif effet_split[0] == "monnaie_par_carte":
				for maCarte in self.joueur_qui_joue.cartes:
					if maCarte.couleur == effet_split[1]:
						self.joueur_qui_joue.monnaie += int(effet_split[2])
	
	def appliquer_effet_merveille(self, merveille: Merveille):
		for effet in merveille.effets:
			effet_split = effet.split(" ")
			if effet_split[0] in ["attaquer", "symbole_scientifique", "point_victoire", "monnaie", "monnaie_par_carte"]:
				self.appliquer_effets_carte(merveille)
			elif effet_split[0] == "defausse_carte_adversaire":
				if len(self.obtenir_adversaire().possede_cartes_couleur(effet_split[2])) != 0:
					self.defausser_carte_adversaire(effet_split[1])
				else:
					print("Le joueur adverse ne possede aucune carte de cette couleur.")
			elif effet_split[0] == "rejouer":
				return "rejouer"
			elif effet_split[0] == "jeton_progres_aleatoire":
				self.gain_jeton_progres_alea()
			elif effet_split[0] == "construction_fausse_gratuite":
				self.construction_carte_defausser()
			elif effet_split[0] == "adversaire_perd_monnaie":
				adversaire = self.obtenir_adversaire()
				adversaire.monnaie -= int(effet_split[1])
	
	def changement_joueur(self) -> None:
		"""
		Change le joueur qui joue.
		"""
		self.joueur_qui_joue = self.obtenir_adversaire()
	
	def fin_de_partie(self):
		"""
		documentation
		"""
		# sommePointVictoireJ1 = self.joueur1.compter_point_victoire()
		pass
	
	def boucle_principale(self):
		"""
		Boucle principale du jeu
		"""
		
		self.joueur_qui_joue = self.joueur1
		while True:
			if not self.reste_des_cartes():
				self.changement_age()
			
			carte_choisie = demander_element_dans_une_liste(self.joueur_qui_joue, "carte", self.liste_cartes_prenables())
			self.demander_action_carte(carte_choisie)
			self.appliquer_effets_carte(carte_choisie)
			self.joueur_qui_joue.cartes.append(carte_choisie)
			
			merveille = self.demander_action_merveille()
			sortie_effet = ""
			if merveille is not None:
				sortie_effet = self.appliquer_effet_merveille(merveille)
			
			if sortie_effet != "rejouer":
				self.changement_joueur()
	
	def lancer(self):
		"""
		Lance le jeu, prepare le plateau et lance la boucle principale.
		"""
		
		self.preparation_plateau()
		self.boucle_principale()


if __name__ == '__main__':
	j1 = Joueur("pierre")
	j2 = Joueur("paul")
	jeu = Jeu(j1, j2, True)
	jeu.lancer()
