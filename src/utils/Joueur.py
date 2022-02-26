"""
Fichier de la classe Joueur.
"""
from src.utils.Carte import Carte
from src.utils.Outils import logger_test, demander_element_dans_une_liste


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
		self.jetons = []  # liste des jetons gagnés
		
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
		que le nom_joueur ne possede pas pour construire une carte.

		:param carte: carte a construire.
		:return: une liste avec les ressources_manquantes manquantes.
		"""
		
		logger_test.debug(f"[{self.nom}] couts_manquants avec la carte [{carte}]")
		
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
					
					logger_test.debug(f"\t[{self.nom}] manque {monnaie_manquante}")
				
				else:
					# ce n'est pas un cout manquant
					couts_manquants_carte.remove(cout_manquant)
					logger_test.debug(f"\t[{self.nom}] possede argent necessaire")
			
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
								
								logger_test.debug(f"\t[{self.nom}] manque {ressource_manquante}")
							
							else:
								# ce n'est pas un cout manquant
								couts_manquants_carte.remove(cout_manquant)
								logger_test.debug(f"\t[{self.nom}] possede {cout_manquant_split[1]}")
		
		return couts_manquants_carte
	
	def possede_carte_chainage(self, carte: Carte):
		"""
		Indique si le nom_joueur possede la carte de chainage de la carte en parametre.

		:param carte: la carte dont on cherche la carte de chainage.
		:return: vrai/ faux.
		"""
		
		logger_test.debug(f"[{self.nom}] possede_carte_chainage avec la carte \'{carte}\'")
		
		# si la carte ne possede pas de carte de chainage
		if carte.nom_carte_chainage is None:
			logger_test.debug(f"\t[{self.nom}] la carte n a pas de carte de chainage")
			return False
		
		#
		for ma_carte in self.cartes:
			if ma_carte.nom == carte.nom_carte_chainage:
				logger_test.debug(f"\t[{self.nom}] possede la carte chainage")
				return True
		
		logger_test.debug(f"\t[{self.nom}] ne possede pas carte chainage")
		return False
	
	def production_type_ressources(self, ressource: str):
		"""
		Retourne la carte produisant la ressource.

		:param ressource: la ressource dont on veut la carte.
		:return: une carte si elle existe, None sinon.
		"""
		
		logger_test.debug(f"[{self.nom}] production_type_ressources avec la ressource \'{ressource}\'")
		
		ressource_split = ressource.split(" ")
		for carte in self.cartes:
			for effet in carte.effets:
				effet_split = effet.split(" ")
				
				# ressource type quantite
				if effet_split[0] == "ressource" and effet_split[1] == ressource_split[1]:
					logger_test.debug(f"\t[{self.nom}] possede une carte qui produit la ressource")
					return carte
		
		logger_test.debug(f"\t[{self.nom}] ne possede pas de carte qui produit la ressource")
		return None
	
	def possede_carte_reduction(self, ressource: str):
		"""
		Renvoie le prix de la reduction de la ressource.

		:param ressource: la ressource dont on cherche la reduction.
		:return: le prix reduit si le nom_joueur possede une carte reduction de la ressource, 0 sinon.
		"""
		
		logger_test.debug(f"[{self.nom}] possede_carte_reduction avec la ressource \'{ressource}\'")
		
		for carte in self.cartes:
			for effet in carte.effets:
				effet_split = effet.split(" ")
				
				# reduc_ressource type prixReduc
				if effet_split[0] == "reduc_ressource" and effet_split[1] == ressource:
					logger_test.debug(f"\t[{self.nom}] possede une carte donnant une reduction")
					return int(effet_split[2])
		
		logger_test.debug(f"\t[{self.nom}] ne possede pas de carte donnant une reduction")
		return 0
	
	def possede_cartes_couleur(self, couleur: str) -> list:
		"""
		Renvoie une liste de carte de la même couleur que celle en parametre.

		:param couleur: la couleur a rechercher.
		:return: une liste de carte.
		"""
		
		logger_test.debug(f"[{self.nom}] possede_cartes_couleur avec la couleur \'{couleur}\'")
		
		liste_cartes_couleur = []
		for carte in self.cartes:
			if carte.couleur == couleur:
				logger_test.debug(f"\t[{self.nom}] la carte \'{carte.nom}\' est de la même couleur")
				liste_cartes_couleur.append(carte)
		
		return liste_cartes_couleur
	
	def compter_point_victoire(self) -> None:
		"""
		Ajoute les points de victoires des differents objets (Carte, Jeton, Merveille)
		"""
		
		logger_test.debug(f"[{self.nom}] compter_point_victoire()")
		
		# compter points victoire avec les cartes
		for carte in self.cartes:
			for effet in carte.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire":
					
					logger_test.debug(f"\t[{self.nom}] carte \'{carte.nom}\' donne {effet_split[1]} points de victoire")
					
					self.points_victoire += int(effet_split[1])
		
		# compter points de victoire avec les merveilles
		for merveille in self.merveilles:
			for effet in merveille.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire":
					
					logger_test.debug(f"\t[{self.nom}] merveille \'{merveille.nom}\' donne "
						f"{effet_split[1]} points de victoire")
					
					self.points_victoire += int(effet_split[1])
		
		# compter points de victoire avec les jetons
		for jeton in self.jetons:
			for effet in jeton.effets:
				
				# decoupe l effet
				effet_split = effet.split(" ")
				if effet_split[0] == "point_victoire_par_jeton":
					
					logger_test.debug(f"\t[{self.nom}] jeton \'{jeton.nom}\' donne "
					             f"{effet_split[1]} points de victoire par jeton")
					
					self.points_victoire += int(effet_split[1]) * len(self.jetons)
					
				elif effet_split[0] == "point_victoire":
					
					logger_test.debug(f"\t[{self.nom}] jeton \'{jeton.nom}\' donne "
					             f"{effet_split[1]} points de victoire par jeton")
					
					self.points_victoire += int(effet_split[1])
				
				elif effet_split[0] == "point_victoire_fin_partie":
					
					logger_test.debug(f"\t[{self.nom}] jeton \'{jeton.nom}\' donne "
					             f"{effet_split[1]} points de victoire en fin de partie")
					
					self.points_victoire += int(effet_split[1])
	
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
					