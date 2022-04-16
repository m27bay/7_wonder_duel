"""
Fichier classe Plateau
"""
import random

from src.logger.Logger import logger

from src.utils.Carte import Carte
from src.utils.JetonMilitaire import JetonMilitaire
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres
from src.utils.Joueur import Joueur


from src.utils.Outils import mon_str_liste2D

SYMBOLE_SCIENTIFIQUES = [
	"sphere_armillaire",
	"roue",
	"cadran_solaire",
	"pilon",
	"pendule",
	"plume"
]


class Plateau:
	"""
	Classe Plateau
	"""
	
	def __init__(self, joueur1, joueur2, choix_auto_merveilles: bool = True):
		"""
		Constructeur de la classe plateau.

		:param joueur1: premier nom_joueur.
		:param joueur2: deuxieme nom_joueur.
		:param choix_auto_merveilles: boolean indiquant si le choix
			des merveilles est automatique ou non.
		"""
		
		if isinstance(joueur1, Joueur) and isinstance(joueur2, Joueur):
			self.joueur1 = joueur1
			self.joueur2 = joueur2
			self.joueur_qui_joue = None
			self.joueur_gagnant = None
			
			#
			self.choix_auto_merveilles = choix_auto_merveilles
			
			self.monnaie_banque = 86  # 14 de valeur 1, 10 de valeur 3, 7 de valeur 6
			self.age = 1
			
			# 9 : neutre
			# 0 : victoire militaire joueur2
			# 18: victoire militaire joueur1
			self.position_jeton_conflit = 9
			self.jetons_militaire = [
				JetonMilitaire("5piecesJ1", 5, 10),
				JetonMilitaire("2piecesJ1", 2, 5),
				JetonMilitaire("0piecesJ1", 0, 2),
				JetonMilitaire("0piecesJ2", 0, 2),
				JetonMilitaire("2piecesJ2", 2, 5),
				JetonMilitaire("5piecesJ2", 5, 10)]

			# matrice de 0 et Carte
			self.cartes_plateau = []
			self.cartes_defaussees = []
			self.jetons_progres_plateau = []
			
			# listes des cartes
			# constructeur : Carte(nom, chemin_image, effets, couts, nom_carte_chainage, couleur, age)
			self.cartes_age_I = [
				Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1),
				Carte("exploitation", ["ressource bois 1"], ["monnaie 1"], None, "marron", age=1),
				Carte("bassin argileux", ["ressource argile 1"], None, None, "marron", age=1),
				Carte("cavite", ["ressource argile 1"], ["monnaie 1"], None, "marron", age=1),
				Carte("gisement", ["ressource pierre 1"], None, None, "marron", age=1),
				Carte("mine", ["ressource pierre 1"], ["monnaie 1"], None, "marron", age=1),
				Carte("verrerie", ["ressource verre 1"], ["monnaie 1"], None, "gris", age=1),
				Carte("presse", ["ressource papyrus 1"], ["monnaie 1"], None, "gris", age=1),
				Carte("tour de garde", ["attaquer 1"], None, None, "rouge", age=1),
				Carte("atelier",
					[f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}", "point_victoire 1"], ["ressource papurys 1"],
					None, "vert", age=1),
				Carte("apothicaire",
					[f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 1"], ["ressource verre 1"],
					None, "vert", age=1),
				Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1),
				Carte("depot d argile", ["reduc_ressource argile 1"], ["monnaie 3"], None, "jaune", age=1),
				Carte("depot de bois", ["reduc_ressource bois 1"], ["monnaie 3"], None, "jaune", age=1),
				Carte("ecurie", ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1),
				Carte("caserne", ["attaquer 1"], ["ressource argile 1"], None, "rouge", age=1),
				Carte("palissade", ["attaquer 1"], ["monnaie 2"], None, "rouge", age=1),
				Carte("scriptorium", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}"], ["monnaie 2"], None, "vert", age=1),
				Carte("officine", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}"], ["monnaie 2"], None, "vert", age=1),
				Carte("theatre", ["point_victoire 3"], None, None, "bleu", age=1),
				Carte("autel", ["point_victoire 3"], None, None, "bleu", age=1),
				Carte("bains", ["point_victoire 3"], ["ressource pierre 1"], None, "bleu", age=1),
				Carte("taverne", ["monnaie 4"], None, None, "jaune", age=1)
			]
			
			self.cartes_age_II = [
				Carte("scierie", ["ressource bois 2"], ["monnaie 2"], None, "marron", age=2),
				Carte("briqueterie", ["ressource argile 2"], ["monnaie 2"], None, "marron", age=2),
				Carte("carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2),
				Carte("soufflerie", ["ressource verre 1"], None, None, "gris", age=2),
				Carte("sechoir", ["ressource papyrus 1"], None, None, "gris", age=2),
				Carte("muraille", ["attaquer 2"], ["ressource pierre 2"], None, "rouge", age=2),
				Carte("forum", ["ressource_au_choix verre papyrus"], ["monnaie 3", "ressource argile 1"],
					None, "jaune", age=2),
				Carte("caravanserail", ["ressource_au_choix bois argile pierre"],
					["monnaie 2", "ressource verre 1", "ressource papyrus 1"], None, "jaune", age=2),
				Carte("douane", ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
					None, "jaune", age=2),
				Carte("tribunal", ["point_victoire 5"], ["ressource bois 2", "ressource verre 1"], None,
					"bleu", age=2),
				Carte("haras", ["attaquer 1"], ["ressource argile 1", "ressource bois 1"], "ecuries", "rouge", age=2),
				Carte("baraquements", ["attaquer 1"], ["monnaie 3"], "caserne", "rouge", age=2),
				Carte("champs de tir", ["attaquer 2"],
					["ressource pierre 1", "ressource bois 1", "ressource papyrus 1"],
					None, "rouge", age=2),
				Carte("place d armes", ["attaquer 2"], ["ressource argile 2", "ressource verre 1"], None, "rouge",
					age=2),
				Carte("bibliotheque", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[5]}", "point_victoire 2"],
					["ressource pierre 1", "ressource bois 1", "ressource verre 1"], "scriptorium", "vert", age=2),
				Carte("dispensaire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 2"],
					["ressource argile 2", "ressource verre 1"], "officine", "vert", age=2),
				Carte("ecole", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 1"],
					["ressource papyrus 2", "ressource bois 1"], None, "vert", age=2),
				Carte("laboratoire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}", "point_victoire 1"],
					["ressource verre 2", "ressource bois 1"], None, "vert", age=2),
				Carte("statue", ["point_victoire 4"], ["ressource argile 2"], "theatre", "bleu", age=2),
				Carte("temple", ["point_victoire 4"], ["ressource papyrus 1", "ressource bois 1"], "autel",
					"bleu", age=2),
				Carte("aqueduc", ["point_victoire 5"], ["ressource pierre 3"], "bains", "bleu", age=2),
				Carte("rostres", ["point_victoire 4"], ["ressource pierre 1", "ressource bois 1"],
					None, "bleu", age=2),
				Carte("brasserie", ["monnaie 6"], None, "taverne", "jaune", age=2)
			]
			
			self.cartes_age_III = [
				Carte("arsenal", ["attaquer 3"], ["ressource argile 3", "ressource bois 2"], None, "rouge", age=3),
				Carte("pretoire", ["attaquer 3"], ["monnaie 8"], None, "rouge", age=3),
				Carte("academie", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[2]}", "point_victoire 3"],
					["ressource pierre 1", "ressource bois 1", "ressource verre 2"], None, "vert", age=3),
				Carte("etude", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[2]}", "point_victoire 3"],
					["ressource papyrus 1", "ressource bois 2", "ressource verre 1"], None, "vert", age=3),
				Carte("chambre de commerce", ["monnaie_par_carte gris 3", "point_victoire 3"],
					["ressource papyrus 2"], None, "jaune", age=3),
				Carte("port", ["monnaie_par_carte marron 2", "point_victoire 3"],
					["ressource verre 1", "ressource bois 1", "ressource papyrus 1"], None, "jaune", age=3),
				Carte("armurerie", ["monnaie_par_carte rouge 1", "point_victoire 3"],
					["ressource pierre 2", "ressource verre 1"], None, "jaune", age=3),
				Carte("palace", ["point_victoire 7"],
					["ressource argile 1", "ressource pierre 1", "ressource bois 1", "ressource verre 2"],
					None, "bleu", age=3),
				Carte("hotel de ville", ["point_victoire 7"], ["ressource pierre 3", "ressource bois 2"],
					None, "bleu", age=3),
				Carte("obelisque", ["point_victoire 5"], ["ressource pierre 2", "ressource verre 1"],
					None, "bleu", age=3),
				Carte("fortifications", ["attaquer 2"],
					["ressource pierre 2", "ressource argile 1", "ressource papyrus 1"],
					"palissade", "rouge", age=3),
				Carte("atelier de siege", ["attaquer 2"], ["ressource bois 3", "ressource verre 1"],
					"champ de tir", "rouge", age=3),
				Carte("cirque", ["attaquer 2"], ["ressource argile 2", "ressource pierre 2"],
					"place d arme", "rouge", age=3),
				Carte("universite", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[0]}", "point_victoire 2"],
					["ressource argile 1", "ressource verre 1", "ressource papyrus 1"], "ecole", "vert", age=3),
				Carte("observatoire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[0]}", "point_victoire 2"],
					["ressource pierre 1", "ressource papyrus 2"], "laboratoire", "vert", age=3),
				Carte("jardins", ["point_victoire 6"], ["ressource argile 2", "ressource bois 2"], "statue",
					"bleu", age=3),
				Carte("pantheon", ["point_victoire 6"],
					["ressource argile 1", "ressource bois 1", "ressource papyrus 2"],
					"temple", "bleu", age=3),
				Carte("senat", ["point_victoire 5"],
					["ressource argile 2", "ressource pierre 1", "ressource papyrus 2"],
					"rostres", "bleu", age=3),
				Carte("phare", ["monnaie_par_carte jaune 1", "point_victoire 3"],
					["ressource argile 2", "ressource verre 1"], "taverne", "jaune", age=3),
				Carte("arene", ["monnaie_par_merveille 2", "point_victoire 3"],
					["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3),
			]
			
			self.cartes_guilde = [
				CarteFille("guilde des commercants",
					["effet_guild_commercants 1"],
					["ressource argile 1", "ressource bois 1", "ressource verre 1", "ressource papyrus 1"]
				),
				CarteFille("guilde des armateurs",
					["effet_guild_armateurs 1"],
					["ressource argile 1", "ressource pierre 1", "ressource verre 1", "ressource papyrus 1"]
				),
				CarteFille("guilde des batisseurs",
					["effet_guild_batisseurs 1"],
					["ressource pierre 2", "ressource argile 1", "ressource bois 1",
						"ressource papyrus 1", "ressource verre 1"]
				),
				CarteFille("guilde des magistrats",
					["effet_guild_magistrats 1"],
					["ressource bois 2", "ressource argile 1", "ressource papyrus 1"]
				),
				CarteFille("guilde des scientifiques",
					["effet_guild_scientifiques 1"],
					["ressource argile 2", "ressource bois 2"]
				),
				CarteFille("guilde des usuriers",
					["effet_guild_usuriers 1"],
					["ressource pierre 2", "ressource bois 2"]
				),
				CarteFille("guilde des tacticiens",
					["effet_guild_tacticiens 1"],
					["ressource pierre 2", "ressource argile 1", "ressource papyrus 1"]
				)
			]
			
			# constructeur : CarteFille(nom, chemin_image, effets)
			self.merveilles = [
				CarteFille("circus maximus",
					["defausse_carte_adversaire gris", "attaquer 1", "point_victoire 3"],
					["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
				),
				CarteFille("colosse",
					["attaquer 2", "point_victoire 3"],
					["ressource argile 3", "ressource verre 1"]
				),
				CarteFille("grand phare",
					["ressource_au_choix bois argile pierre", "point_victoire 4"],
					["ressource bois 1", "ressource pierre 1", "ressource papyrus 2"]
				),
				CarteFille("jardin suspendus",
					["monnaie 6", "rejouer", "point_victoire 3"],
					["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"]
				),
				CarteFille("grande bibliotheque",
					["jeton_progres_aleatoire", "point_victoire 4"],
					["ressource bois 3", "ressource verre 1", "ressource papyrus 1"]
				),
				CarteFille("mausolee",
					["construction_fausse_gratuite", "point_victoire 2"],
					["ressource argile 2", "ressource verre 2", "ressource papyrus 1"]
				),
				CarteFille("piree",
					["ressource_au_choix papyrus verre", "rejouer", "point_victoire 2"],
					["ressource bois 2", "ressource pierre 1", "ressource argile 1"]
				),
				CarteFille("pyramides",
					["point_victoire 9"],
					["ressource pierre 3", "ressource papyrus 1"]
				),
				CarteFille("sphinx",
					["rejouer", "point_victoire 6"],
					["ressource pierre 1", "ressource argile 1", "ressource verre 2"]
				),
				CarteFille("statue de zeus",
					["defausse_carte_adversaire marron", "attaquer 1", "point_victoire 3"],
					["ressource pierre 1", "ressource bois 1",
						"ressource argile 1", "ressource papyrus 2"]
				),
				CarteFille("temple d artemis",
					["monnaie 12", "rejouer"],
					["ressource bois 1", "ressource pierre 1",
						"ressource verre 1", "ressource papyrus 1"]
				),
				CarteFille("via appia",
					["monnaie 3", "adversaire_perd_monnaie 3", "rejouer", "point_victoire 3"],
					["ressource pierre 2", "ressource argile 2", "ressource papyrus 1"]
				)
			]
			
			self.jetons_progres = [
				JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"]),
				JetonProgres("architecture", ["reduc_merveille"]),
				JetonProgres("economie", ["gain_monnaie_adversaire"]),
				JetonProgres("loi", ["symbole_scientifique"]),
				JetonProgres("maconnerie", ["reduc_carte bleu"]),
				JetonProgres("philosophie", ["point_victoire_fin_partie 7"]),
				JetonProgres("mathematiques", ["point_victoire_par_jeton 3", "point_victoire 3"]),
				JetonProgres("strategie", ["bonus_attaque"]),
				JetonProgres("theologie", ["rejouer"]),
				JetonProgres("urbanisme", ["monnaie 6", "bonus_monnaie_chainage 4"]),
			]
			
		else:
			self.joueur1 = None
			self.joueur2 = None
			self.joueur_qui_joue = None
			self.joueur_gagnant = None
			self.choix_auto_merveilles = None
			self.monnaie_banque = None
			self.age = None
			self.position_jeton_conflit = None
			
			self.jetons_militaire = []
			self.cartes_age_I = []
			self.cartes_age_II = []
			self.cartes_age_III = []
			self.cartes_guilde = []
			self.cartes_plateau = []
			self.cartes_defaussees = []
			self.merveilles = []
			self.jetons_progres = []
			self.jetons_progres_plateau = []
		
	def constructeur_par_copie(self):
		plateau = Plateau(None, None)
		
		plateau.joueur1 = self.joueur1.constructeur_par_copie()
		plateau.joueur2 = self.joueur2.constructeur_par_copie()
		
		if self.joueur_gagnant is not None:
			plateau.joueur_gagnant = self.joueur_gagnant.constructeur_par_copie()
		
		if self.joueur_qui_joue == self.joueur1:
			plateau.joueur_qui_joue = plateau.joueur1
		elif self.joueur_qui_joue == self.joueur2:
			plateau.joueur_qui_joue = plateau.joueur2
		
		plateau.choix_auto_merveilles = self.choix_auto_merveilles
		plateau.monnaie_banque = self.monnaie_banque
		plateau.age = self.age
		plateau.position_jeton_conflit = self.position_jeton_conflit
		
		for jetons_militaire in self.jetons_militaire:
			plateau.jetons_militaire.append(jetons_militaire.constructeur_par_copie())
			
		for carte in self.cartes_age_I:
			plateau.cartes_age_I.append(carte.constructeur_par_copie())
		for carte in self.cartes_age_II:
			plateau.cartes_age_II.append(carte.constructeur_par_copie())
		for carte in self.cartes_age_III:
			plateau.cartes_age_III.append(carte.constructeur_par_copie())
		for carte in self.cartes_guilde:
			plateau.cartes_guilde.append(carte.constructeur_par_copie())
		
		for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
			copie_ligne = []
			for num_colonne, carte in enumerate(ligne_carte):
				if carte != 0:
					copie_ligne.append(carte.constructeur_par_copie())
				else:
					copie_ligne.append(0)
			plateau.cartes_plateau.append(copie_ligne)
					
		for carte in self.cartes_defaussees:
			plateau.cartes_defaussees.append(carte.constructeur_par_copie())
		
		for merveille in self.merveilles:
			plateau.merveilles.append(merveille.constructeur_par_copie())
			
		plateau.jetons_progres = self.jetons_progres.copy()
		plateau.jetons_progres_plateau = self.jetons_progres_plateau.copy()
		
		return plateau
		
	def __eq__(self, other):
		if isinstance(other, Plateau):
			return self.joueur1 == other.joueur1 \
				and self.joueur2 == other.joueur2 \
				and self.joueur_qui_joue == other.joueur_qui_joue \
				and self.choix_auto_merveilles == other.choix_auto_merveilles \
				and self.monnaie_banque == other.monnaie_banque \
				and self.age == other.age \
				and self.position_jeton_conflit == other.position_jeton_conflit \
				and self.jetons_militaire == other.jetons_militaire \
				and self.cartes_age_I == other.cartes_age_I \
				and self.cartes_age_II == other.cartes_age_II \
				and self.cartes_age_III == other.cartes_age_III \
				and self.cartes_guilde == other.cartes_guilde \
				and self.cartes_plateau == other.cartes_plateau \
				and self.cartes_defaussees == other.cartes_defaussees \
				and self.merveilles == other.merveilles \
				and self.jetons_progres == other.jetons_progres \
				and self.jetons_progres_plateau == other.jetons_progres_plateau
		else:
			return False
		
	def __str__(self):
		return f"cartes_plateau : {mon_str_liste2D(self.cartes_plateau)}" \
			f"j1 : {str(self.joueur1)}\n" \
			f"j2 : {str(self.joueur2)}\n" \
			f"joueur_qui_joue : {self.joueur_qui_joue.nom}\n" \
			f"position_jeton_conflit : {self.position_jeton_conflit}\n"
	
	def preparation_plateau(self) -> None:
		"""
		Prepare le plateau, les cartes, les jetons_progres, la monnaie des joueurs, les merveilles des joueurs.
		"""
		logger.debug("preparation_plateau")
		self.__preparation_cartes()
		self.__preparation_jetons_progres()
		self.__preparation_monnaies_joueurs()
		self.__preparation_merveilles()
		self.joueur_qui_joue = self.joueur1
	
	def __preparation_cartes(self) -> None:
		"""
		Methode privee.
		
		Prepare les cartes, sort aleatoirement des cartes et le place selon
		une structure precise.
		"""
		
		# preparation de la structure des cartes en fonction de l age.
		if self.age == 1:
			self.cartes_plateau = [
				[0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
				[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
				[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
			]
			
			liste_carte = self.cartes_age_I
			
			# suppression de 3 cartes
			# il nous faut 20 cartes parmis les 23
			for _ in range(3):
				carte_random = random.choice(liste_carte)
				liste_carte.remove(carte_random)
		
		elif self.age == 2:
			self.cartes_plateau = [
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
				[0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
				[0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
				[0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
			]
			
			liste_carte = self.cartes_age_II
			
			# suppression de 3 cartes
			# il nous faut 20 cartes parmis les 23
			for _ in range(3):
				carte_random = random.choice(liste_carte)
				liste_carte.remove(carte_random)
		
		else:  # Age 3
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
			
			# suppression de 3 cartes
			# il nous faut 17 cartes parmis les 20
			for _ in range(3):
				carte_random = random.choice(liste_carte)
				liste_carte.remove(carte_random)
			
			# ajout de 3 cartes guilde
			for _ in range(3):
				carte_guild_random = random.choice(self.cartes_guilde)
				self.cartes_guilde.remove(carte_guild_random)
				liste_carte.append(carte_guild_random)
		
		# remplissage de la structure avec des cartes aleatoires.
		for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
			for num_colonne, _ in enumerate(ligne_carte):
				if self.cartes_plateau[num_ligne][num_colonne] == 1:
					
					nouvelle_carte = random.choice(liste_carte)
					liste_carte.remove(nouvelle_carte)
					
					# une ligne sur deux la carte sont face cachee,
					# par defaut une carte n est pas face cachee
					if num_ligne % 2 != 0:
						nouvelle_carte.cacher()
					
					self.cartes_plateau[num_ligne][num_colonne] = nouvelle_carte
	
	def __preparation_jetons_progres(self) -> None:
		"""
		Methode privee.
		
		Prepare les 5 jetons_progres progres aleatoire du plateau.
		"""
		
		logger.debug("__preparation_jetons_progres")
		
		for _ in range(5):
			jeton_random = random.choice(self.jetons_progres)
			self.jetons_progres.remove(jeton_random)
			self.jetons_progres_plateau.append(jeton_random)
			
			logger.debug(f"\tjetons aleatoire choisit : {jeton_random.nom}")
	
	def __preparation_monnaies_joueurs(self) -> None:
		"""
		Methode privee.
		
		Prepare les monnaies des deux joueurs.
		"""
		
		self.joueur1.monnaie = self.joueur2.monnaie = 7
		self.monnaie_banque -= 14
	
	def __preparation_merveilles(self) -> None:
		"""
		Methode privee.
		
		Prepare les merveilles.
		Sort aleatoirement 4 merveiles, le joueur1 en choisie 1, puis le joueur2 en choisie 2,
		enfin le joueur1 prend la derniere.
		Sort aleatoirement 4 merveiles, le joueur2 en choisie 1, puis le joueur1 en choisie 2,
		enfin le joueur2 prend la derniere.
		"""
		
		if not self.choix_auto_merveilles:
			logger.debug("choix merveilles par les joueurs")
			print("fonction \"__preparation_merveilles\" à faire")
		
		else:  # choix automatique des merveilles (d'apres les regles)
			logger.debug("choix merveilles automatique")
			
			self.joueur1.merveilles.append(self.merveilles[7])
			self.joueur1.merveilles.append(self.merveilles[2])
			self.joueur1.merveilles.append(self.merveilles[10])
			self.joueur1.merveilles.append(self.merveilles[9])
			logger.debug(f"[{self.joueur1.nom}] liste merveilles : "
				f"\'pyramides\', \'grand phare\', \'temple d artemis\', \'statue de zeus\'")
			
			self.joueur2.merveilles.append(self.merveilles[0])
			self.joueur2.merveilles.append(self.merveilles[6])
			self.joueur2.merveilles.append(self.merveilles[11])
			self.joueur2.merveilles.append(self.merveilles[1])
			logger.debug(f"[{self.joueur2.nom}] liste merveilles : "
				f"\'circus maximus\', \'piree\', \'via appia\', \'colosse\'")
	
	#
	#
	# Partie outils
	#
	#
	
	def adversaire(self):
		if self.joueur_qui_joue == self.joueur1:
			return self.joueur2
		else:
			return self.joueur1
	
	def enlever_carte(self, carte_a_enlever: Carte) -> None:
		"""
		Enleve une carte du plateau.

		:param carte_a_enlever: la carte a enlever.
		"""
		
		logger.debug(f"enlever_carte(\'{carte_a_enlever.nom}\')")
		carte_trouvee = False
		
		for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
			for num_colonne, carte in enumerate(ligne_carte):
				if carte == carte_a_enlever:
					
					self.cartes_plateau[num_ligne][num_colonne] = 0
					carte_trouvee = True
		
		if not carte_trouvee:
			logger.debug(f"la carte {carte_a_enlever.nom} n'est pas sur le plateau.")
			exit(-1)
		
		logger.debug(f"la carte {carte_a_enlever.nom} enlevee.")
		
		for carte in self.liste_cartes_prenables():
			carte.devoiler()
	
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
	
	def cartes_prenable(self, ligne: int, colonne: int) -> bool:
		# si la carte est sur la dernière ligne
		if ligne == len(self.cartes_plateau) - 1:
			return True
		# si la carte est sur le bord gauche, pas de "fils" à sa gauche
		elif colonne == 0:
			return self.cartes_plateau[ligne + 1][colonne + 1] == 0
		# si la carte est sur le bord droit, pas de "fils" à sa droite
		elif colonne == len(self.cartes_plateau[ligne]) - 1:
			return self.cartes_plateau[ligne + 1][colonne - 1] == 0
		# milieu de la matrice
		else:
			return (self.cartes_plateau[ligne + 1][colonne - 1] == 0) and (
						self.cartes_plateau[ligne + 1][colonne + 1] == 0)
	
	def liste_cartes_prenables(self):
		cartes_prenable = []
		for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
			for num_colonne, carte in enumerate(ligne_carte):
				if carte != 0 and self.cartes_prenable(num_ligne, num_colonne):
					cartes_prenable.append(carte)
		
		return cartes_prenable
	
	def changement_age(self):
		if not self.reste_des_cartes():
			
			if self.age == 3:
				self.fin_de_partie()
				return -1
			
			else:
				self.age += 1
				self.__preparation_cartes()
				return 1
			
		return 0
	
	def fin_de_partie(self):
		logger.debug("fin_de_partie()")
		
		if self.position_jeton_conflit == 0 or self.joueur2.nbr_symb_scientifique_diff == 6:
			logger.debug("victoire j2")
			self.joueur_gagnant = self.joueur2
		elif self.position_jeton_conflit == 18 or self.joueur1.nbr_symb_scientifique_diff == 6:
			logger.debug("victoire j1")
			self.joueur_gagnant = self.joueur1
		else:
			self.joueur1.compter_point_victoire()
			self.joueur2.compter_point_victoire()
			
			numero_jeton = self.numero_jeton_militaire()
			jeton = self.jetons_militaire[numero_jeton]
			if self.position_jeton_conflit > 9:
				self.joueur1.points_victoire += jeton.points_victoire
			elif self.position_jeton_conflit < 9:
				self.joueur2.points_victoire += jeton.points_victoire
			
			if self.joueur1.points_victoire > self.joueur2.points_victoire:
				self.joueur_gagnant = self.joueur1
				logger.debug("victoire j1")
			elif self.joueur1.points_victoire < self.joueur2.points_victoire:
				self.joueur_gagnant = self.joueur2
				logger.debug("victoire j2")
			else:
				self.joueur_gagnant = -1
				logger.debug("egalite")
				
	def gain_argent_banque(self, somme_gagnee: int):
		logger.debug(f"gain_argent_banque({somme_gagnee})")
		
		if somme_gagnee == 0:
			return 0
		
		if self.monnaie_banque == 0:
			gain = 0
			logger.debug("monnaie_banque == 0")
		
		elif self.monnaie_banque < somme_gagnee:
			gain = self.monnaie_banque
			self.monnaie_banque = 0
			logger.debug(f"monnaie_banque < somme_gagnee, gain = {gain}")
		
		else:
			gain = somme_gagnee
			self.monnaie_banque -= somme_gagnee
			logger.debug(f"gain = {gain}")
		
		return gain
	
	def acheter_ressources(self, ressources_manquantes: list) -> int:
		"""
		Permet au nom_joueur qui joue d'acheter les ressources qui lui manque pour construire sa carte.

		:param ressources_manquantes: liste des ressources manquantes
		:return prixDesRessources
		"""
		logger.debug(f"acheter_ressources({ressources_manquantes})")
		
		prix_commerce = 0
		
		# Verification si le nom_joueur adverse produit les ressources manquantes
		adversaire = self.adversaire()
		carte_liste_ressource_adversaire = []
		
		for ressource_manquante in ressources_manquantes:
			carte_production = adversaire.production_type_ressources(ressource_manquante)
			
			if carte_production is not None:
				carte_liste_ressource_adversaire.append(carte_production)
		
		# si le nom_joueur adverse ne produit aucune ressouces ressources manquantes
		if len(carte_liste_ressource_adversaire) == 0:
			
			logger.debug("carte_liste_ressource_adversaire = vide")
			
			for ressource_manquante in ressources_manquantes:
				
				ressource_manquante_split = ressource_manquante.split(" ")
				prix_reduc = self.joueur_qui_joue.possede_carte_reduction(ressource_manquante_split[1])
				
				if prix_reduc != 0:
					# (1 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le nom_joueur
					logger.debug(f"prix_reduc = {prix_reduc}")
					prix_commerce += prix_reduc * int(ressource_manquante_split[2])
					logger.debug(f"prix_commerce = {prix_commerce}")
				
				else:
					# (2 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le nom_joueur
					logger.debug("prix_reduc = 0")
					prix_commerce += (2 * int(ressource_manquante_split[2]))
					logger.debug(f"prix_commerce = {prix_commerce}")
		
		# le nom_joueur adverse produit des ressouces qui me manquent
		else:
			# les cartes jaunes ne compte pas dans le commerce
			for carte in carte_liste_ressource_adversaire:
				
				if carte.couleur == "jaune":
					carte_liste_ressource_adversaire.remove(carte)
			
			logger.debug(f"carte_liste_ressource_adversaire = {carte_liste_ressource_adversaire}")
			
			for ressource_manquante in ressources_manquantes:
				ressource_manquante_split = ressource_manquante.split(" ")
				
				# si le nom_joueur adversaire produit la ressource
				ressource_trouve = False
				
				# parmis les cartes produisant la ressouce que j'achete
				for carte_ressource_adversaire in carte_liste_ressource_adversaire:
					
					# parmis les effets de cette carte
					for effet in carte_ressource_adversaire.effets:
						ressource_adversaire_split = effet.split(" ")
						
						# nom_joueur adversaire produit ressource qu'il me manque ?
						if ressource_manquante_split[1] == ressource_adversaire_split[1]:
							ressource_trouve = True
							
							# ai je une reduction sur cette ressource ?
							prix_reduc = self.joueur_qui_joue.possede_carte_reduction(ressource_manquante_split[1])
							
							if prix_reduc != 0:
								# (prix_reduc * quantite_ressource_necessaire pour le nom_joueur)
								logger.debug(f"prix_reduc = {prix_reduc}")
								prix_commerce += (
									(prix_reduc + int(ressource_adversaire_split[2])) *
									int(ressource_manquante_split[2])
								)
								logger.debug(f"prix_commerce = {prix_commerce}")
								
							else:
								# (2 + quantite_ressource_adversaire) * quantite_ressource_necessaire pour le nom_joueur
								logger.debug("prix_reduc = 0")
								prix_commerce += (
										(2 + int(ressource_adversaire_split[2])) * int(ressource_manquante_split[2])
								)
								logger.debug(f"prix_commerce = {prix_commerce}")
				
				# si l'adversaire ne produit pas la ressource
				if not ressource_trouve:
					prix_commerce += (2 * int(ressource_manquante_split[2]))
		
		return prix_commerce
	
	def piocher(self, carte_prenable: Carte):
		# construction carte
		if not self.joueur_qui_joue.possede_carte_chainage(carte_prenable):
			
			# la carte ne coute rien
			if carte_prenable.couts is None or len(carte_prenable.couts) == 0:
				# fin action
				self.enlever_carte(carte_prenable)
				self.appliquer_effets_carte(carte_prenable)
				self.joueur_qui_joue.cartes.append(carte_prenable)
				return 1
			
			# if carte_prenable.couleur == "bleu" and self.joueur_qui_joue.possede_jeton_scientifique("maconnerie"):
				# self.reduction_couts_construction_carte(carte_prenable)
				# print("fonction \"reduction_couts_construction_carte\" à faire")
			
			# verification ressources nom_joueur
			liste_ressource_necessaire = self.joueur_qui_joue.couts_manquants(carte_prenable)
			
			# le nom_joueur possede toutes les ressouces
			if len(liste_ressource_necessaire) == 0:
				self.enlever_carte(carte_prenable)
				self.appliquer_effets_carte(carte_prenable)
				self.joueur_qui_joue.cartes.append(carte_prenable)
				return 1
			
			else:
				# manque des ressouces
				for ressource_manquante in liste_ressource_necessaire:
					ressource_manquante_split = ressource_manquante.split(" ")
					
					# manque monnaie
					if ressource_manquante_split[0] == "monnaie":
						return -1
				
				# manque des ressources autre que monnaie
				prix = self.acheter_ressources(liste_ressource_necessaire)
				if prix > self.joueur_qui_joue.monnaie:
					return -1
				else:
					if self.adversaire().possede_jeton_scientifique("economie"):
						self.adversaire().monnaie += prix
					else:
						self.monnaie_banque += prix
					self.joueur_qui_joue.monnaie -= prix
					
					# fin action
					self.enlever_carte(carte_prenable)
					self.appliquer_effets_carte(carte_prenable)
					self.joueur_qui_joue.cartes.append(carte_prenable)
					return 1
		
		else:  # le nom_joueur possde la carte chainage, construction gratuite
			# application effet jeton "urbanisme"
			if self.joueur_qui_joue.possede_jeton_scientifique("urbanisme"):
				self.joueur_qui_joue.monnaie += self.gain_argent_banque(4)
				
			self.enlever_carte(carte_prenable)
			self.appliquer_effets_carte(carte_prenable)
			self.joueur_qui_joue.cartes.append(carte_prenable)
			return 1
		
	def defausser(self, carte_prenable: Carte):
		self.joueur_qui_joue.monnaie += self.gain_argent_banque(2)
		
		# gain de une piece par carte jaune
		for carte_joueur in self.joueur_qui_joue.cartes:
			if carte_joueur.couleur == "jaune":
				self.joueur_qui_joue.monnaie += self.gain_argent_banque(2)
				
		self.enlever_carte(carte_prenable)
		self.cartes_defaussees.append(carte_prenable)
		
	def construire_merveille(self, merveille_a_construire: CarteFille):
		# verification ressources nom_joueur
		liste_ressource_necessaire = self.joueur_qui_joue.couts_manquants(merveille_a_construire)
		
		# le joueur possede toutes les ressouces
		if len(liste_ressource_necessaire) == 0:
			
			# on retire uniquement la monnaie
			for cout in merveille_a_construire.couts:
				# monnaie x
				cout_split = cout.split(" ")
				if cout_split[0] == "monnaie":
					self.joueur_qui_joue.monnaie -= int(cout_split[1])
					self.monnaie_banque += int(cout_split[1])
			
			# fin action
			return 1
		
		else:
			# manque des ressouces
			for ressource_manquante in liste_ressource_necessaire:
				ressource_manquante_split = ressource_manquante.split(" ")
				
				# manque monnaie
				if ressource_manquante_split[0] == "monnaie":
					return 1
			
			# manque des ressources autre que monnaie
			prix = self.acheter_ressources(liste_ressource_necessaire)
			if prix > self.joueur_qui_joue.monnaie:
				return 1
			
			else:
				return merveille_a_construire
			
	def numero_jeton_militaire(self):
		"""
		Renvoie le numero du jeton militaire dans le tableau en fonction de la postion
		du jeton conflit.

		:return: le numero du jeton militaire.
		"""
		
		if self.position_jeton_conflit in [1, 2, 3]:
			return 0
		elif self.position_jeton_conflit in [4, 5, 6]:
			return 1
		elif self.position_jeton_conflit in [7, 8]:
			return 2
		elif self.position_jeton_conflit in [10, 11]:
			return 3
		elif self.position_jeton_conflit in [12, 13, 14]:
			return 4
		elif self.position_jeton_conflit in [15, 16, 17]:
			return 5
		else:
			return -1
	
	def deplacer_pion_miltaire(self, nbr_deplacement: int):
		logger.debug(f"deplacer_pion_miltaire(\'{nbr_deplacement}\')")
		
		# On deplace le pion case par case
		for _ in range(nbr_deplacement):
			
			if self.joueur_qui_joue == self.joueur2:
				self.position_jeton_conflit -= 1
			else:
				self.position_jeton_conflit += 1
			
			logger.debug(f"Nouvelle position {self.position_jeton_conflit}")
			
			# si le pion se situe au bout du plateau militaire, il y a une victoire militaire
			if self.position_jeton_conflit in [0, 18]:
				return self.fin_de_partie()
			
			else:
				numero_jeton = self.numero_jeton_militaire()
				
				if numero_jeton != -1:
					jeton = self.jetons_militaire[numero_jeton]
					
					if not jeton.est_utilise:
						logger.debug(f"[{self.joueur_qui_joue.nom}] prend le jeton {numero_jeton}, "
							f"l'adversaire perd {jeton.pieces} monnaies")
						
						self.gain_argent_banque(jeton.pieces)
						jeton.est_utilise = True
	
	def appliquer_effets_carte(self, carte: Carte):
		logger.debug(f"appliquer_effets_carte({carte.nom})")
		
		for effet in carte.effets:
			
			effet_split = effet.split(" ")
			
			if effet_split[0] == "ressource":
				self.joueur_qui_joue.ressources[effet_split[1]] += 1
			
			elif effet_split[0] == "attaquer":
				nbr_bouclier = int(effet_split[1])
				
				if self.joueur_qui_joue.possede_jeton_scientifique("strategie"):
					nbr_bouclier += 1
					
				self.deplacer_pion_miltaire(nbr_bouclier)
			
			elif effet_split[0] == "monnaie":
				logger.debug(f"[{self.joueur_qui_joue.nom}] {effet}")
				self.joueur_qui_joue.monnaie += self.gain_argent_banque(int(effet_split[1]))
			
			elif effet_split[0] == "monnaie_par_carte":
				logger.debug(f"[{self.joueur_qui_joue.nom}] {effet}")
				
				for ma_carte in self.joueur_qui_joue.cartes:
					if ma_carte.couleur == effet_split[1]:
						self.joueur_qui_joue.monnaie += self.gain_argent_banque(int(effet_split[2]))
	
	def appliquer_effets_merveille(self, merveille: CarteFille):
		logger.debug(f"appliquer_effets_merveille({merveille.nom})")
		
		for effet in merveille.effets:
			
			effet_split = effet.split(" ")
			
			# effet commun avec certains carte
			if effet_split[0] in ["monnaie", "monnaie_par_carte"]:
				self.appliquer_effets_carte(merveille)
				
			elif effet_split[0] == "attaquer":
				self.deplacer_pion_miltaire(int(effet_split[1]))
			
			elif effet_split[0] == "adversaire_perd_monnaie":
				self.adversaire().monnaie -= int(effet_split[1])
				self.monnaie_banque += int(effet_split[1])
		
		return "none", "none"
		
	def appliquer_effets_jeton(self, jeton: JetonProgres):
		"""
		TODO : documentation a faire

		:param jeton:
		"""
		logger.debug(f"appliquer_effets_jeton(\'{jeton.nom}\')")
		
		if jeton.nom in ["agriculture", "urbanisme"]:
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] gain de 6 monnaies")
			self.joueur_qui_joue.monnaie -= 6
			self.monnaie_banque += 6
		
		elif jeton.nom == "philosophie":
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] gain de 7 points de victoire")
			self.joueur_qui_joue.points_victoire += 7
			
		elif jeton.nom == "loi":
			# self.demande_symbole_scientifique()
			print("fonction \"demande_symbole_scientifique\" à faire")
			