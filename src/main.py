import logging
import random


logging.basicConfig(filename="../logger.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Generique:
	def __init__(self, nom, cheminImg):
		self.nom = nom
		self.cheminImg = cheminImg


class Carte(Generique):
	"""
	Classe representant une carte.
	"""

	def __init__(self, nom, cheminImg, effets, couts, carteChainage, couleur, age):
		"""
		Constructeur de la classe Carte.

		:param nom: nom de la carte.
		:param cheminImg: chemin pour afficher la carte.
		:param effets: liste d effets que donne la carte respectant un pattern precis.
		:param couts: liste de couts pour construire la carte respactant un pattern precis.
		:param carteChainage: nom de la carte permettant de construire gratuitement la carte.
		:param couleur: couleur de la carte.
		:param age: age de la carte (entre 1 et 3).
		"""
		super().__init__(nom, cheminImg)
		self.effets = effets
		self.couts = couts
		self.carteChainage = carteChainage
		self.couleur = couleur
		self.age = age
		self.faceCachee = False

	def devoiler(self):
		"""
		Devoile la carte, indique que la carte n est plus face cachee.
		"""
		logger.debug(f"devoilement carte {self.nom}")
		self.faceCachee = False

	def cacher(self):
		"""
		Cacher la carte, indique que la carte est face cachee.
		"""
		logger.debug(f"cachement carte {self.nom}")
		self.faceCachee = True

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
		       f"image : {self.cheminImg}, " \
		       f"effets : {str(self.effets)}, " \
		       f"couts : {str(self.couts)}, " \
		       f"cout chainage : {self.carteChainage}, " \
		       f"couleur : {self.couleur}, " \
		       f"age : {self.age}, " \
		       f"face cachee : {self.faceCachee}"


class Merveille(Carte):
	"""
	Classe representant une merveille, une classe fille de la classe Carte.
	"""

	def __init__(self, nom, cheminImg, effets, couts):
		"""
		Constructeur de la classe Merveille.

		:param nom: nom de la merveille.
		:param cheminImg: chemin pour afficher la merveille.
		:param effets: liste d effets que donne la merveille respectant un pattern precis.
		:param couts: liste de couts pour construire la merveille respactant un pattern precis.
		"""
		super().__init__(nom, cheminImg, effets, couts, None, None, None)


class JetonProgres(Generique):
	"""
	Classe representant un jeton progres
	"""

	def __init__(self, nom, cheminImg, effets):
		"""
		Constructeur de la classe JetonProgres.

		:param nom: nom du jeton.
		:param effets: liste des effets du jeton.
		"""
		super().__init__(nom, cheminImg)
		self.effets = effets

	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
		       f"cheminImg : {self.cheminImg}, " \
		       f"effets : {str(self.effets)}"


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
		self.pointVictoire = 0
		self.jetons = []

	def coutsManquant(self, carte: Carte):
		"""
		Renvoie une liste des ressourcesManquantes (monnaie ou matiere premiere/ produit manufacture)
		que le joueur ne possede pas pour construire une carte.

		:param carte: carte a construire.
		:return: une liste avec les ressourcesManquantes manquantes.
		"""

		logger.debug(f"[{self.nom}] coutsManquant avec la carte [{carte}]")

		# Cout ou Effet
		# "monnaie prix"
		# "ressource type quantite"
		listeCoutsManquant = carte.couts.copy()
		for coutManquant in carte.couts:

			# decoupage couts de la carte
			coutManquantSplit = coutManquant.split(" ")

			# cout monnetaire
			if coutManquantSplit[0] == "monnaie":

				if self.monnaie < int(coutManquantSplit[1]):
					# changement du cout avec le cout manquant
					prixManquant = str(int(coutManquantSplit[1]) - self.monnaie)
					nouvMonnaie = "monnaie " + prixManquant
					listeCoutsManquant[listeCoutsManquant.index(coutManquant)] = nouvMonnaie

					logger.debug(f"\t[{self.nom}] manque {nouvMonnaie}")

				else:
					# ce n'est pas un cout manquant
					listeCoutsManquant.remove(coutManquant)
					logger.debug(f"\t[{self.nom}] possede argent necessaire")

			# cout ressource
			else:
				for maCarte in self.cartes:
					for effet in maCarte.effets:

						# decoupage effets
						effetSplit = effet.split(" ")

						# si c'est la même ressource
						if coutManquantSplit[1] == effetSplit[1]:

							if int(effetSplit[2]) < int(coutManquantSplit[2]):
								# changement du cout avec le cout manquant
								quantiteManquante = str(int(coutManquantSplit[2]) - int(effetSplit[2]))
								nouvEffet = effetSplit[0] + " " + effetSplit[1] + " " + quantiteManquante
								listeCoutsManquant[listeCoutsManquant.index(coutManquant)] = nouvEffet

								logger.debug(f"\t[{self.nom}] manque {nouvEffet}")

							else:
								# ce n'est pas un cout manquant
								listeCoutsManquant.remove(coutManquant)
								logger.debug(f"\t[{self.nom}] possede {coutManquantSplit[1]}")

		return listeCoutsManquant

	def possedeCarteChainage(self, carte: Carte):
		"""
		Indique si le joueur possede la carte de chainage de la carte en parametre.

		:param carte: la carte dont on cherche la carte de chainage.
		:return: vrai/ faux.
		"""

		logger.debug(f"[{self.nom}] possedeCarteChainage avec la carte \'{carte}\'")

		# si la carte ne possede pas de carte de chainage
		if carte.carteChainage is None:
			logger.debug(f"\t[{self.nom}] la carte n a pas de carte de chainage")
			return False

		#
		for maCarte in self.cartes:
			if maCarte.nom == carte.carteChainage:
				logger.debug(f"\t[{self.nom}] possede la carte chainage")
				return True

		logger.debug(f"\t[{self.nom}] ne possede pas carte chainage")
		return False

	def productionTypeRessources(self, ressource: str):
		"""
		Retourne la carte produisant la ressource.

		:param ressource: la ressource dont on veut la carte.
		:return: une carte si elle existe, None sinon.
		"""

		logger.debug(f"[{self.nom}] productionTypeRessources avec la ressource \'{ressource}\'")

		ressourceSplit = ressource.split(" ")
		for carte in self.cartes:
			for effet in carte.effets:
				effetSplit = effet.split(" ")

				# ressource type quantite
				if effetSplit[0] == "ressource" and effetSplit[1] == ressourceSplit[1]:

					logger.debug(f"\t[{self.nom}] possede une carte qui produit la ressource")
					return carte

		logger.debug(f"\t[{self.nom}] ne possede pas de carte qui produit la ressource")
		return None

	def possedeReduction(self, ressource: str):
		"""
		Renvoie le prix de la reduction de la ressource.

		:param ressource: la ressource dont on cherche la reduction.
		:return: le prix reduit si le joueur possede une carte reduction de la ressource, 0 sinon.
		"""

		logger.debug(f"[{self.nom}] possedeReduction avec la ressource \'{ressource}\'")

		for carte in self.cartes:
			for effet in carte.effets:
				effetSplit = effet.split(" ")

				# reduc_ressource type prixReduc
				if effetSplit[0] == "reduc_ressource" and effetSplit[1] == ressource:

					logger.debug(f"\t[{self.nom}] possede une carte donnant une reduction")
					return int(effetSplit[2])

		logger.debug(f"\t[{self.nom}] ne possede pas de carte donnant une reduction")
		return 0

	def cartesCouleur(self, couleur: str) -> list:
		"""
		Renvoie une liste de carte de la même couleur que celle en parametre.

		:param couleur: la couleur a rechercher.
		:return: une liste de carte.
		"""

		logger.debug(f"[{self.nom}] cartesCouleur avec la couleur \'{couleur}\'")

		listeCartesCouleur = []
		for carte in self.cartes:
			if carte.couleur == couleur:

				logger.debug(f"\t[{self.nom}] la carte \'{carte.nom}\' est de la même couleur")
				listeCartesCouleur.append(carte)

		return listeCartesCouleur


def trouverElmentAvecNom(nom: str, liste: list):
	"""
	Trouver un element (carte, merveille) avec son nom dans une liste.

	:param nom: nom de l element a chercher.
	:param liste: liste des objets ou chercher l element.
	:return: l element si trouvee, None sinon.
	"""

	logger.debug(f"trouverElmentAvecNom avec le nom \'{nom}\' dans la liste : \n {afficher(liste)}")

	for element in liste:
		if element.nom == nom:

			logger.debug(f"\t\'{nom}\' est dans la liste")
			return element

	logger.debug(f"\t\'{nom}\' n'est pas dans la liste")
	return None


def demanderElementDansUneListe(joueur: Joueur, typeElement: str, listeElement: list):
	"""
	Renvoie l element contenu dans listeElement correspondant au nom renseigne par le joueur.

	:param joueur: le joueur a qui on demande l element.
	:param typeElement: le type d element de que l on cherche (uniquement pour l'affichage) (carte, merveille, ..).
	:param listeElement: la liste ou l on cherche l element.
	:return: l element choisi.
	"""

	logger.debug(f"[{joueur.nom}] demanderElementDansUneListe choisit \'{typeElement}\' "
	             f"dans la liste : \n {afficher(listeElement)}")

	while True:
		print(f"* liste choix possibles *\n{afficher(listeElement)}")
		nomElement = input(f"[{joueur.nom}] Choix {typeElement} ?\n > ")
		elementChoisi = trouverElmentAvecNom(nomElement, listeElement)
		if elementChoisi is None:
			print(f" * ERREUR * Aucun element ne repond au nom \'{nomElement}\', veuillez recommencer * ERREUR * ")
			continue
		else:
			break

	logger.debug(f"[{joueur.nom}] a choisit \'{elementChoisi.nom}\'")
	return elementChoisi


def selectionMerveille(nbrRepetition: int, joueur: Joueur, listeMerveillesAlea: list) -> None:
	"""
	Selection d'un ou des merveilles pour le joueur parmis une liste de merveille.

	:param nbrRepetition: nombre de merveille a choisir.
	:param joueur: joueur qui choisi.
	:param listeMerveillesAlea: une liste de merveille ou choisir la/les merveille(s).
	"""
	if len(listeMerveillesAlea) == 1:
		print(f"\nAttribution de la derniere merveille ({listeMerveillesAlea[0].nom})"
		      f" au [{joueur.nom}]")
		joueur.merveilles.append(listeMerveillesAlea[0])
		listeMerveillesAlea.remove(listeMerveillesAlea[0])
	else:
		for _ in range(nbrRepetition):
			merveilleChoisie = demanderElementDansUneListe(joueur, "merveille", listeMerveillesAlea)
			joueur.merveilles.append(merveilleChoisie)
			listeMerveillesAlea.remove(merveilleChoisie)


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

	def __init__(self, joueur1: Joueur, joueur2: Joueur, choixAutoMerveilles: bool = True):
		"""
		Constructeur de la classe jeu.

		:param joueur1: premier joueur.
		:param joueur2: deuxieme joueur.
		:param choixAutoMerveilles: boolean indiquant si le choix des merveilles est automatique ou non.
		"""
		self.joueur1 = joueur1
		self.joueur2 = joueur2
		self.quiJoue = None

		#
		self.choixAutoMerveilles = choixAutoMerveilles
		self.monnaieMax = 86  # 14 de valeur 1, 10 de valeur 3, 7 de valeur 6
		self.age = 1

		#  0: neutre
		# +9: victoire militaire joueur2
		# -9: victoire militaire joueur1
		self.positionJetonMilitaire = 0

		# liste des jetons progres, constructeur : JetonProgres(nom, effets)
		self.jetonsProgres = [
			JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"]),
			JetonProgres("architecture", None, "reduc_merveille"),
			JetonProgres("economie", None, "gain_monnaie_adversaire"),
			JetonProgres("loi", None, "symbole_scientifique"),
			JetonProgres("maconnerie", None, "reduc_carte bleu"),
			JetonProgres("philosophie", None, "point_victoire_fin_partie 7"),
			JetonProgres("mathematiques", None, ["point_victoire_par_jeton 3", "point_victoire 3"]),
			JetonProgres("strategie", None, "bonus_attaque"),
			JetonProgres("theologie", None, "rejouer"),
			JetonProgres("urbanisme", None, ["monnaie 6", "bonus_monnaie_chainage 4"]),
		]
		# jeton choisi et place sur le plateau
		self.jetonsProgresPlateau = []

		# pour stocker les cartes defaussees
		self.fausseCarte = []

		# listes des cartes, constructeur : Carte(nom, cheminImg, effets, couts, carteChainage, couleur, age)
		self.cartesAgeI = [  # initialisation cartes age I
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
		self.cartesAgeII = [  # initialisation cartes age II
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
		self.cartesAgeIII = [  # initialisation cartes age III
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
		self.cartesPlateau = []

		# liste des merveilles, constructeur : Merveille(nom, cheminImg, effets)
		self.merveilles = [
			Merveille("circus maximus", None, ["ressource pierre 2", "ressource bois 1", "ressource verre 1"],
			          ["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"]),
			Merveille("colosse", None, ["ressource argile 3", "ressource verre 1"],
			          ["attaquer 2", "point_victoire 3"]),
			Merveille("grand phare", None, ["ressource bois 1", "ressource pierre 1", "ressource papyrus 2"],
			          ["ressource_au_choix bois argile pierre", "point_victoire 4"]),
			Merveille("jardin suspendus", None, ["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"],
			          ["monnaie 6", "rejouer", "point_victoire 3"]),
			Merveille("grande bibliotheque", None, ["ressource bois 3", "ressource verre 1", "ressource papyrus 1"],
			          ["jeton_progres_aleatoire", "point_victoire 4"]),
			Merveille("mausolee", None, ["ressource argile 2", "ressource verre 2", "ressource papyrus 1"],
			          ["construction_fausse_gratuite", "point_victoire 2"]),
			Merveille("piree", None, ["ressource bois 2", "ressource pierre 1", "ressource argile 1"],
			          ["ressource_au_choix papyrus verre", "rejouer", "point_victoire 2"]),
			Merveille("pyramides", None, ["ressource pierre 3", "ressource papyrus 1"],
			          "point_victoire 9"),
			Merveille("sphinx", None, ["ressource pierre 1", "ressource argile 1", "ressource verre 2"],
			          ["rejouer", "point_victoire 6"]),
			Merveille("statue de zeus", None, ["ressource pierre 1", "ressource bois 1", "ressource argile 1",
			                                   "ressource papyrus 2"],
			          ["defausse_carte_adversaire marron", "attaquer 1", "point_victoire 3"]),
			Merveille("temple d'artemis", None, ["ressource bois 1", "ressource pierre 1", "ressource verre 1",
			                                     "ressource papyrus 1"],
			          ["monnaie 12", "rejouer"]),
			Merveille("via appia", None, ["ressource pierre 2", "ressource argile 2", "ressource papyrus 1"],
			          ["monnaie 3", "adversaire_perd_monnaie 3", "rejouer", "point_victoire 3"])
		]

	def preparationPlateau(self) -> None:
		"""
		Prepare le plateau, les cartes, les jetons, la monnaie des joueurs, les merveilles des joueurs.
		"""
		logger.debug("preparationPlateau")
		self.preparationCartes()
		self.preparationJetonsProgres()
		self.preparationArgent()
		self.preparationMerveilles()

	def preparationCartes(self) -> None:
		"""
		Prepare les cartes, sort aleatoirement des cartes et le place selon une structure precise.
		"""
		logger.debug("preparationCartes")
		# preparation de la structure des cartes en fonction de l age.
		if self.age == 1:
			logger.debug(f"\tpreparationCartes age {self.age}")
			self.cartesPlateau = [
				[0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
				[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
			]
			listeCarte = self.cartesAgeI
		elif self.age == 2:
			logger.debug(f"\tpreparationCartes age {self.age}")
			self.cartesPlateau = [
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
				[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
				[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
			]
			listeCarte = self.cartesAgeII
		else:  # Age 3
			logger.debug(f"\tpreparationCartes age {self.age}")
			self.cartesPlateau = [
				[0, 0, 1, 0, 1, 0, 0],
				[0, 1, 0, 1, 0, 1, 0],
				[1, 0, 1, 0, 1, 0, 1],
				[0, 1, 0, 0, 0, 1, 0],
				[1, 0, 1, 0, 1, 0, 1],
				[0, 1, 0, 1, 0, 1, 0],
				[0, 0, 1, 0, 1, 0, 0]
			]
			listeCarte = self.cartesAgeIII

		# remplissage de la structure avec des cartes aleatoires.
		for ligne in range(len(self.cartesPlateau)):
			for colonne in range(len(self.cartesPlateau[ligne])):
				if self.cartesPlateau[ligne][colonne] == 1:
					carte = random.choice(listeCarte)
					# suppresion carte choisie pour ne pas la choisir a nouveau
					listeCarte.remove(carte)
					# une ligne sur deux la carte sont face cachee, par defaut une carte
					# n est pas face cachee
					if ligne % 2 != 0:
						carte.cacher()
					self.cartesPlateau[ligne][colonne] = carte

	def preparationJetonsProgres(self) -> None:
		"""
		Prepare les 5 jetons progres aleatoire du plateau.
		"""
		logger.debug("preparationJetonsProgres")
		for _ in range(5):
			jetonRandom = random.choice(self.jetonsProgres)
			self.jetonsProgres.remove(jetonRandom)
			self.jetonsProgresPlateau.append(jetonRandom)

	def preparationArgent(self) -> None:
		"""
		Prepare les monnaies des deux joueurs.
		"""
		logger.debug("preparationArgent")
		self.joueur1.monnaie = self.joueur2.monnaie = 7

	def preparationMerveilles(self) -> None:
		"""
		Prepare les merveilles.
		Sort aleatoirement 4 merveiles, le joueur1 en choisie 1, puis le joueur2 en choisie 2,
		enfin le joueur1 prend la derniere.
		Sort aleatoirement 4 merveiles, le joueur2 en choisie 1, puis le joueur1 en choisie 2,
		enfin le joueur2 prend la derniere.
		"""
		logger.debug("preparationMerveilles")
		if not self.choixAutoMerveilles:
			logger.debug("\tchoix non automatique")
			print("\n * Premiere selection de merveille aleatoire * \n")
			# choix aleatoire des 4 premieres merveilles
			listeMerveillesAlea = []
			for _ in range(4):
				listeMerveillesAlea.append(random.choice(self.merveilles))

			# les joueurs choississent leurs 4 premieres merveilles
			selectionMerveille(1, self.joueur1, listeMerveillesAlea)
			selectionMerveille(2, self.joueur2, listeMerveillesAlea)
			selectionMerveille(1, self.joueur1, listeMerveillesAlea)

			print("\n * Deuxieme selection de merveille aleatoire * \n")
			# choix aleatoire des 4 dernieres merveilles
			for _ in range(4):
				listeMerveillesAlea.append(random.choice(self.merveilles))

			# les joueurs choississent leurs 4 dernieres merveilles
			selectionMerveille(1, self.joueur2, listeMerveillesAlea)
			selectionMerveille(2, self.joueur1, listeMerveillesAlea)
			selectionMerveille(1, self.joueur2, listeMerveillesAlea)

		else:  # choix automatique des merveilles (d'apres les regles)
			logger.debug("\tchoix automatique")
			self.joueur1.merveilles.append(trouverElmentAvecNom("pyramides", self.merveilles))
			self.joueur1.merveilles.append(trouverElmentAvecNom("grand phare", self.merveilles))
			self.joueur1.merveilles.append(trouverElmentAvecNom("temple d artemis", self.merveilles))
			self.joueur1.merveilles.append(trouverElmentAvecNom("statue de zeus", self.merveilles))

			self.joueur2.merveilles.append(trouverElmentAvecNom("circus maximus", self.merveilles))
			self.joueur2.merveilles.append(trouverElmentAvecNom("piree", self.merveilles))
			self.joueur2.merveilles.append(trouverElmentAvecNom("via appia", self.merveilles))
			self.joueur2.merveilles.append(trouverElmentAvecNom("colosse", self.merveilles))

	def enleverCarte(self, carte: Carte) -> None:
		"""
		Enleve une carte du plateau.

		:param carte: la carte a enlever.
		"""
		for ligne in range(len(self.cartesPlateau)):
			for colonne in range(len(self.cartesPlateau[ligne])):
				if self.cartesPlateau[ligne][colonne] == carte:
					self.cartesPlateau[ligne][colonne] = 0
					return
		print("La carte n'est pas sur le plateau.")

	def obtenirAdversaire(self):
		"""
		Renvoie le joueur adverse, le joueur qui n'est pas stocke dans l attribut quiJoue.

		:return: joueur adverse
		"""
		if self.quiJoue == self.joueur1:
			return self.joueur2
		else:
			return self.joueur1

	def demanderActionCarte(self, carte: Carte):
		"""
		Demande a l'utilisateur l action qu'il souhaite faire avec la carte (defausser, ou piocher).

		:param carte: la carte choisie par le joueur.
		"""

		strAction = f"[{self.quiJoue.nom}] defausser ou piocher ?\n > "
		while True:
			action = input(strAction)

			# defausser
			if action == "defausser":
				self.fausseCarte.append(carte)
				self.quiJoue.monnaie = self.quiJoue.monnaie + 2

				# gain de une piece par carte jaune
				for carteJoueur in self.quiJoue.cartes:
					if carteJoueur.couleur == "jaune":
						self.quiJoue.monnaie += 1

				# fin action carte
				break

			# piocher
			elif action == "piocher":

				# construction de la carte gratuite via chainage
				if not self.quiJoue.possedeCarteChainage(carte):

					if carte.couts is None:
						# fin action carte
						break

					# verification ressources joueur
					listeRessourceNecessaire = self.quiJoue.coutsManquant(carte)

					# le joueur possede toutes les ressouces
					if len(listeRessourceNecessaire) == 0:

						# on retire uniquement la monnaie
						for cout in carte.couts:
							# monnaie x
							coutSplit = cout.split(" ")
							if coutSplit[0] == "monnaie":
								self.quiJoue.monnaie -= int(coutSplit[1])

						# fin action carte
						break

					else:
						# manque des ressouces
						for ressourceManquante in listeRessourceNecessaire:
							ressourceManquanteSplit = ressourceManquante.split(" ")

							# manque monnaie
							if ressourceManquanteSplit[0] == "monnaie":
								print("Vous n'avez pas assez de monnaie pour construire la carte. "
								      "Vous devez defausser la carte")
								continue

						# manque des ressources autre que monnaie
						prix = self.acheterRessource(listeRessourceNecessaire)
						if prix > self.quiJoue.monnaie:
							print("Impossible de faire le commerce, vous n'avez pas assez de monnaie. "
							      "Vous devez defausser la carte")
							continue
						else:
							self.quiJoue.monnaie -= prix
							self.monnaieMax += prix

							# fin action carte
							break

				else:  # le joueur possde la carte chainage, construction gratuite
					# fin action carte
					break
			else:
				print("action carte inconnue.")
				continue

		# suppression de la carte du plateau
		self.enleverCarte(carte)

	def demanderActionMerveille(self):
		"""
		Demande a l'utilisateur si il souhaite construire une merveille.
		"""

		strAction = f"[{self.quiJoue.nom}] construire une merveille (oui/non) ?\n > "
		while True:
			action = input(strAction)
			if action == "oui":
				# TODO : carte a sacrfier ?
				return demanderElementDansUneListe(self.quiJoue, "merveille", self.quiJoue.merveilles)
			elif action == "non":
				return None
			else:
				print("action merveille inconnue")

	def acheterRessource(self, ressourcesManquantes: list) -> int:
		"""
		Permet au joueur qui joue d'acheter les ressources qui lui manque pour construire sa carte.

		:param ressourcesManquantes: liste des ressources manquantes
		:return prixDesRessources
		"""

		prixCommerce = 0

		# Verification si le joueur adverse produit les ressources manquantes
		adversaire = self.obtenirAdversaire()
		carteListeRessourceAdversaire = []
		for ressourceManquante in ressourcesManquantes:
			carteProduction = adversaire.productionTypeRessources(ressourceManquante)
			if carteProduction is not None:
				carteListeRessourceAdversaire.append(carteProduction)

		# si le joueur adverse ne produit aucune ressouces ressources manquantes
		if len(carteListeRessourceAdversaire) == 0:
			for ressourceManquante in ressourcesManquantes:
				ressourceManquanteSplit = ressourceManquante.split(" ")

				if self.quiJoue.possedeReduction(ressourceManquanteSplit[1]) != 0:
					# (1 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le joueur
					prixCommerce += int(ressourceManquanteSplit[2])
				else:
					# (2 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le joueur
					prixCommerce += (2 * int(ressourceManquanteSplit[2]))

		# le joueur adverse produit des ressouces qui me manquent
		else:
			# les cartes jaunes ne compte pas dans le commerce
			for carte in carteListeRessourceAdversaire:
				if carte.couleur == "jaune":
					carteListeRessourceAdversaire.remove(carte)

			for ressourceManquante in ressourcesManquantes:
				ressourceManquanteSplit = ressourceManquante.split(" ")

				# si le joueur adversaire produit la ressource
				ressourceTrouve = False

				# parmis les cartes produisant la ressouce que j'achete
				for carteRessourceAdversaire in carteListeRessourceAdversaire:

					# parmis les effets de cette carte
					for effet in carteRessourceAdversaire.effets:
						ressourceAdversaireSplit = effet.split(" ")

						# joueur adversaire produit ressource qu'il me manque ?
						if ressourceManquanteSplit[1] == ressourceAdversaireSplit[1]:
							ressourceTrouve = True

							# ai je une reduction sur cette ressource ?
							prixReduc = self.quiJoue.possedeReduction(ressourceManquanteSplit[1])
							if prixReduc != 0:
								# (prixReduc * quantite_ressource_necessaire pour le joueur)
								prixCommerce += (prixReduc * int(ressourceManquanteSplit[2]))
							else:
								# (2 + quantite_ressource_adversaire) * quantite_ressource_necessaire pour le joueur
								prixCommerce += ((2 + int(ressourceAdversaireSplit[2])) * int(ressourceManquanteSplit[2]))

				# si l'adversaire ne produit pas la ressource
				if not ressourceTrouve:
					prixCommerce += (2 * int(ressourceManquanteSplit[2]))

		return prixCommerce

	def resteDesCartes(self) -> bool:
		"""
		Indique s'il reste des cartes sur le plateau.

		:return: vrai/ faux
		"""
		for ligneCarte in self.cartesPlateau:
			for carte in ligneCarte:
				if carte != 0:
					return True
		return False

	def changementAge(self) -> None:
		"""
		Permet de changer d'âge et de changer la structure des cartes du plateau.
		"""

		if self.age != 3:
			self.age += 1
			self.preparationCartes()
		else:
			self.finDePartie()

	def cartePrenable(self, ligne: int, colonne: int) -> bool:
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
				return self.cartesPlateau[ligne + 1][colonne + 1] == 0
			elif colonne == len(self.cartesPlateau[ligne]) - 1:
				return self.cartesPlateau[ligne + 1][colonne - 1] == 0
		else:
			return (self.cartesPlateau[ligne + 1][colonne - 1] == 0) \
			       and (self.cartesPlateau[ligne + 1][colonne + 1] == 0)

	def listeCartesPrenable(self):
		"""
		Renvoie la liste des cartes prenable sur le plateau.

		:return: list carte prenable.
		"""
		cartesPrenable = []
		for ligne in range(len(self.cartesPlateau)):
			for colonne in range(len(self.cartesPlateau[ligne])):
				if self.cartesPlateau[ligne][colonne] != 0 and self.cartePrenable(ligne, colonne):
					cartesPrenable.append(self.cartesPlateau[ligne][colonne])

		return cartesPrenable

	def defausserCarteAdversaire(self, couleur: str) -> None:
		"""
		Retire une carte de couleur de l'adversaire pour l'ajouter dans la liste des cartes faussees.

		:param couleur: la couleur de la carte a defausser.
		"""

		adversaire = self.obtenirAdversaire()
		while True:
			print(f"\n * liste choix possibles *\n{afficher(adversaire.cartes)}")
			typeElement = input(f"[{self.quiJoue.nom}] Choix d'une carte {couleur}?\n > ")
			elementChoisi = trouverElmentAvecNom(typeElement, adversaire.cartes)
			if elementChoisi is None or elementChoisi.couleur != couleur:
				print("Choix incorrect")
				continue
			else:
				break

		adversaire.cartes.remove(elementChoisi)
		self.fausseCarte.append(elementChoisi)

	def gainJetonProgresAleatoire(self) -> None:
		"""
		Le joueur gain 1 jeton parmis 3 jetons aleatoire non selectionnes au debut de la partie.
		"""

		# tirage aleatoire des 3 jetons
		listeJetons = []
		for _ in range(3):
			jetonRandom = random.choice(self.jetonsProgres)
			listeJetons.append(jetonRandom)
			self.jetonsProgres.remove(jetonRandom)

		# le joueur en choisit 1
		jetonChoisi = demanderElementDansUneListe(self.quiJoue, "jetons progres", listeJetons)
		listeJetons.remove(jetonChoisi)

		# les autres sont remis dans la boite
		for jeton in listeJetons:
			self.jetonsProgres.append(jeton)

	def constructionCarteDefausser(self) -> None:
		"""
		Le joueur construit gratuitement une carte defaussee.
		"""

		carteChoisie = demanderElementDansUneListe(self.quiJoue, "carte defausser", self.fausseCarte)
		self.quiJoue.cartes.append(carteChoisie)
		self.appliquerEffetCarte(carteChoisie)

	def demanderRessourceAuChoix(self, listeRessources: list) -> str:
		"""
		Si une carte possede l'effet "ressource_au_choix" le joueur doit choisir quel ressource il souhaite produire.

		:param listeRessources: la liste des ressources au choix.
		:return: un nouvel effet, "ressource x 1", avec x la ressource choisit.
		"""

		ressource = "ressource "
		strDemande = f"[{self.quiJoue.nom}] Nom de la ressource choisie ?\n > "
		print(f"\n * liste des ressources *\n", listeRessources)
		nomRessource = input(strDemande)
		while nomRessource not in listeRessources:
			print("Ressource inconnu, veuillez recommencer")
			nomRessource = input(strDemande)
		return ressource + nomRessource + " 1"

	def gainSymboleScientifique(self, nomSymboleScientifique: str) -> bool:
		for maCarte in self.quiJoue.cartes:
			for effetMaCarte in maCarte.effets:
				effetMaCarteSplit = effetMaCarte.split(" ")

				# si possede une carte donnant le même symbole
				if effetMaCarteSplit[0] == "symbole_scientifique" and effetMaCarteSplit[1] == nomSymboleScientifique:

					# 2 symboles identiques => gain jeton
					jetonChoisi = demanderElementDansUneListe(self.quiJoue, "jeton", self.jetonsProgresPlateau)
					self.quiJoue.jetons.append(jetonChoisi)

					# Suppression du jeton du plateau
					self.jetonsProgresPlateau.remove(jetonChoisi)

					# suppression de l'effet gain symbole scientifique
					maCarte.effets.remove(effetMaCarte)
					return True
		return False

	def appliquerEffetCarte(self, carte: Carte):
		for effet in carte.effets:
			effetSplit = effet.split(" ")
			if effetSplit[0] == "attaquer":
				self.positionJetonMilitaire += int(effetSplit[1])
			elif effetSplit[0] == "symbole_scientifique":
				if self.gainSymboleScientifique(effetSplit[1]):
					carte.effets.remove(effet)
			elif effetSplit[0] == "point_victoire":
				self.quiJoue.pointVictoire += int(effetSplit[1])
			elif effetSplit[0] == "monnaie":
				self.quiJoue.monnaie += int(effetSplit[1])
			elif effetSplit[0] == "ressource_au_choix":
				# remplace effet ressource au choix par un ressource classique
				ressource = ""
				# "ressource_au_choix x y"
				if len(effetSplit) == 3:
					ressource = self.demanderRessourceAuChoix([effetSplit[1], effetSplit[2]])
				# "ressource_au_choix x y z"
				elif len(effetSplit) == 4:
					ressource = self.demanderRessourceAuChoix([effetSplit[1], effetSplit[2], effetSplit[3]])
				carte.effets = [ressource]
			elif effetSplit[0] == "monnaie_par_carte":
				for maCarte in self.quiJoue.cartes:
					if maCarte.couleur == effetSplit[1]:
						self.quiJoue.monnaie += int(effetSplit[2])

	def appliquerEffetMerveille(self, merveille: Merveille):
		for effet in merveille.effets:
			effetSplit = effet.split(" ")
			if effetSplit[0] in ["attaquer", "symbole_scientifique", "point_victoire", "monnaie", "monnaie_par_carte"]:
				self.appliquerEffetCarte(merveille)
			elif effetSplit[0] == "defausse_carte_adversaire":
				if len(self.obtenirAdversaire().cartesCouleur(effetSplit[2])) != 0:
					self.defausserCarteAdversaire(effetSplit[1])
				else:
					print("Le joueur adverse ne possede aucune carte de cette couleur.")
			elif effetSplit[0] == "rejouer":
				return "rejouer"
			elif effetSplit[0] == "jeton_progres_aleatoire":
				self.gainJetonProgresAleatoire()
			elif effetSplit[0] == "construction_fausse_gratuite":
				self.constructionCarteDefausser()
			elif effetSplit[0] == "adversaire_perd_monnaie":
				adversaire = self.obtenirAdversaire()
				adversaire.monnaie -= int(effetSplit[1])

	def changementJoueur(self):
		self.quiJoue = self.obtenirAdversaire()

	def finDePartie(self):
		pass

	def bouclePrincipale(self):
		self.quiJoue = self.joueur1
		while True:
			if not self.resteDesCartes():
				self.changementAge()

			carteChoisie = demanderElementDansUneListe(self.quiJoue, "carte", self.listeCartesPrenable())
			self.demanderActionCarte(carteChoisie)
			self.appliquerEffetCarte(carteChoisie)
			self.quiJoue.cartes.append(carteChoisie)

			merveille = self.demanderActionMerveille()
			sortieEffet = ""
			if merveille is not None:
				sortieEffet = self.appliquerEffetMerveille(merveille)

			if sortieEffet != "rejouer":
				self.changementJoueur()

	def lancer(self):
		self.preparationPlateau()
		self.bouclePrincipale()


if __name__ == '__main__':
	j1 = Joueur("pierre")
	j2 = Joueur("paul")
	jeu = Jeu(j1, j2, True)
	jeu.lancer()
