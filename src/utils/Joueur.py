"""
Fichier de la classe Joueur.
"""
from src.utils.Carte import Carte
from src.utils.Outils import logger
from src.utils.Outils import demander_element_dans_une_liste


class Joueur:
	"""
	Classe representant un nom_joueur.
	"""
	
	def __init__(self, nom):
		"""
		Constructeur de la classe Joueur.

		:param nom: nom du nom_joueur.
		"""
		self.nom = nom
		
		#
		self.cartes = []  # liste des cartes construites
		self.merveilles = []  # liste des merveilles construites
		self.jetons_progres = []  # liste des jetons_progres gagnés
		
		#
		self.monnaie = 0
		self.points_victoire = 0
		
	def retirer_monnaie(self, monnaie: int):
		"""
		

		:param monnaie:
		:return:
		"""
		if self.monnaie - monnaie < 0:
			return False
		else:
			self.monnaie -= monnaie
			return True
	
	def couts_manquants(self, carte: Carte):
		"""
		Renvoie une liste des ressources_manquantes (monnaie ou matiere premiere/ produit manufacture)
		que le nom_joueur ne possede pas pour construire une carte_a_enlever.

		:param carte: carte_a_enlever a construire.
		:return: une liste avec les ressources_manquantes manquantes.
		"""
		
		logger.debug(f"[{self.nom}] couts_manquants avec la carte_a_enlever [{carte}]")
		
		# Cout ou Effet
		# "monnaie prix"
		# "ressource type quantite"
		couts_manquants_carte = carte.couts.copy()
		for cout_manquant in carte.couts:
			
			# decoupage couts de la carte_a_enlever
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
		Indique si le nom_joueur possede la carte_a_enlever de chainage de la carte_a_enlever en parametre.

		:param carte: la carte_a_enlever dont on cherche la carte_a_enlever de chainage.
		:return: vrai/ faux.
		"""
		
		logger.debug(f"[{self.nom}] possede_carte_chainage avec la carte_a_enlever \'{carte}\'")
		
		# si la carte_a_enlever ne possede pas de carte_a_enlever de chainage
		if carte.nom_carte_chainage is None:
			logger.debug(f"\t[{self.nom}] la carte_a_enlever n a pas de carte_a_enlever de chainage")
			return False
		
		#
		for ma_carte in self.cartes:
			if ma_carte.nom == carte.nom_carte_chainage:
				logger.debug(f"\t[{self.nom}] possede la carte_a_enlever chainage")
				return True
		
		logger.debug(f"\t[{self.nom}] ne possede pas carte_a_enlever chainage")
		return False
	
	def production_type_ressources(self, ressource: str):
		"""
		Retourne la carte_a_enlever produisant la ressource.

		:param ressource: la ressource dont on veut la carte_a_enlever.
		:return: une carte_a_enlever si elle existe, None sinon.
		"""
		
		logger.debug(f"[{self.nom}] production_type_ressources avec la ressource \'{ressource}\'")
		
		ressource_split = ressource.split(" ")
		for carte in self.cartes:
			for effet in carte.effets:
				effet_split = effet.split(" ")
				
				# ressource type quantite
				if effet_split[0] == "ressource" and effet_split[1] == ressource_split[1]:
					logger.debug(f"\t[{self.nom}] possede une carte_a_enlever qui produit la ressource")
					return carte
		
		logger.debug(f"\t[{self.nom}] ne possede pas de carte_a_enlever qui produit la ressource")
		return None
	
	def possede_carte_reduction(self, ressource: str):
		"""
		Renvoie le prix de la reduction de la ressource.

		:param ressource: la ressource dont on cherche la reduction.
		:return: le prix reduit si le nom_joueur possede une carte_a_enlever reduction de la ressource, 0 sinon.
		"""
		
		logger.debug(f"[{self.nom}] possede_carte_reduction avec la ressource \'{ressource}\'")
		
		for carte in self.cartes:
			for effet in carte.effets:
				effet_split = effet.split(" ")
				
				# reduc_ressource type prixReduc
				if effet_split[0] == "reduc_ressource" and effet_split[1] == ressource:
					logger.debug(f"\t[{self.nom}] possede une carte_a_enlever donnant une reduction")
					return int(effet_split[2])
		
		logger.debug(f"\t[{self.nom}] ne possede pas de carte_a_enlever donnant une reduction")
		return 0
	
	def possede_cartes_couleur(self, couleur: str) -> list:
		"""
		Renvoie une liste de carte_a_enlever de la même couleur que celle en parametre.

		:param couleur: la couleur a rechercher.
		:return: une liste de carte_a_enlever.
		"""
		
		logger.debug(f"[{self.nom}] possede_cartes_couleur avec la couleur \'{couleur}\'")
		
		liste_cartes_couleur = []
		for carte in self.cartes:
			if carte.couleur == couleur:
				logger.debug(f"\t[{self.nom}] la carte_a_enlever \'{carte.nom}\' est de la même couleur")
				liste_cartes_couleur.append(carte)
		
		return liste_cartes_couleur
	
	def possede_jeton_scientifique(self, nom_jetons_progres: str):
		"""
		Indique si le joueur possede ou non un jetons progres precis.

		:param nom_jetons_progres: le nom du jeton que l'on cherche.
		:return: vrai/ faux
		"""
		for jeton in self.jetons_progres:
			if jeton.nom == nom_jetons_progres:
				return True
		return False
	
	def compter_point_victoire(self) -> None:
		"""
		Ajoute les points de victoires des differents objets (Carte, Jeton, CarteFille)
		"""
		
		logger.debug(f"[{self.nom}] compter_point_victoire()")
		
		# compter points victoire avec les cartes
		for carte in self.cartes:
			for effet in carte.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire":
					
					logger.debug(f"\t[{self.nom}] carte_a_enlever \'{carte.nom}\' donne {effet_split[1]} points de victoire")
					
					self.points_victoire += int(effet_split[1])
		
		# compter points de victoire avec les merveilles
		for merveille in self.merveilles:
			for effet in merveille.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire":
					
					logger.debug(f"\t[{self.nom}] merveille \'{merveille.nom}\' donne "
						f"{effet_split[1]} points de victoire")
					
					self.points_victoire += int(effet_split[1])
		
		# compter points de victoire avec les jetons_progres
		for jeton in self.jetons_progres:
			for effet in jeton.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire_par_jeton":
					
					logger.debug(f"\t[{self.nom}] jeton \'{jeton.nom}\' donne "
						f"{effet_split[1]} points de victoire par jeton")
					
					self.points_victoire += int(effet_split[1]) * len(self.jetons_progres)
					
				elif effet_split[0] == "point_victoire":
					
					logger.debug(f"\t[{self.nom}] jeton \'{jeton.nom}\' donne "
						f"{effet_split[1]} points de victoire par jeton")
					
					self.points_victoire += int(effet_split[1])
				
				elif effet_split[0] == "point_victoire_fin_partie":
					
					logger.debug(f"\t[{self.nom}] jeton \'{jeton.nom}\' donne "
						f"{effet_split[1]} points de victoire en fin de partie")
					
					self.points_victoire += int(effet_split[1])
			
		# effet jetons progres "mathematiques"
		if self.possede_jeton_scientifique("mathematiques"):
			self.points_victoire += ((len(self.jetons_progres) * 3) + 3)
	
	def selection_merveille(self, nbr_repetition: int, liste_merveilles_alea: list) -> None:
		"""
		Selection d'un ou des merveilles pour le nom_joueur parmis une liste de merveille.

		:param nbr_repetition: nombre de merveille a choisir.
		:param liste_merveilles_alea: une liste de merveille ou choisir la/les merveille(s).
		"""
		if len(liste_merveilles_alea) == 1:
			print(f"\nAttribution de la derniere merveille ({liste_merveilles_alea[0].nom})"
				f" au [{self.nom}]")
			self.merveilles.append(liste_merveilles_alea[0])
			liste_merveilles_alea.remove(liste_merveilles_alea[0])
		else:
			for _ in range(nbr_repetition):
				merveille_choisie = demander_element_dans_une_liste(self.nom, "merveille", liste_merveilles_alea)
				self.merveilles.append(merveille_choisie)
				liste_merveilles_alea.remove(merveille_choisie)
					