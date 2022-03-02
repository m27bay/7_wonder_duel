"""
Fichier classe Plateau
"""
import random

from src.logger.Logger import logger

from src.utils.Carte import Carte
from src.utils.Joueur import Joueur
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres

from src.utils.Outils import monStrListe
from src.utils.Outils import trouver_element_avec_nom
from src.utils.Outils import demander_element_dans_une_liste
from src.utils.Outils import demander_ressource_dans_une_liste

from src.utils.Constantes import MERVEILLES
from src.utils.Constantes import CARTES_GUILDE
from src.utils.Constantes import CARTES_AGE_I
from src.utils.Constantes import CARTES_AGE_II
from src.utils.Constantes import CARTES_AGE_III
from src.utils.Constantes import JETONS_PROGRES
from src.utils.Constantes import JETONS_MILITAIRES
from src.utils.Constantes import SYMBOLE_SCIENTIFIQUES


class Plateau:
	"""
	Classe pPlateau de plateau
	"""
	
	def __init__(self, joueur1: Joueur, joueur2: Joueur, choix_auto_merveilles: bool = True):
		"""
		Constructeur de la classe plateau.

		:param joueur1: premier nom_joueur.
		:param joueur2: deuxieme nom_joueur.
		:param choix_auto_merveilles: boolean indiquant si le choix
			des merveilles est automatique ou non.
		"""
		
		self.joueur1 = joueur1
		self.joueur2 = joueur2
		self.joueur_qui_joue = None
		
		#
		self.choix_auto_merveilles = choix_auto_merveilles
		
		# TODO : Changer en dicionnaire ? [valeur, quantite] ?
		self.monnaie_banque = 86  # 14 de valeur 1, 10 de valeur 3, 7 de valeur 6
		self.age = 1
		
		# 9 : neutre
		# 0 : victoire militaire joueur2
		# 18: victoire militaire joueur1
		self.position_jeton_conflit = 9
		self.jetons_militaire = JETONS_MILITAIRES
		
		# liste des jetons progres, constructeur : JetonProgres(nom, effets)
		self.jetons_progres = JETONS_PROGRES
		
		# jeton choisi et place sur le plateau
		self.jetons_progres_plateau = []
		
		# pour stocker les cartes defaussees
		self.cartes_defaussees = []
		
		# listes des cartes
		self.cartes_age_I = CARTES_AGE_I
		self.cartes_age_II = CARTES_AGE_II
		self.cartes_age_III = CARTES_AGE_III
		
		self.cartes_guilde = CARTES_GUILDE
		
		# carte_a_enlever sur le plateau de plateau
		self.cartes_plateau = []
		
		# liste des merveilles
		self.merveilles = MERVEILLES
	
	def preparation_plateau(self) -> None:
		"""
		Prepare le plateau, les cartes, les jetons_progres, la monnaie des joueurs, les merveilles des joueurs.
		"""
		logger.debug("preparation_plateau")
		self.__preparation_cartes()
		self.__preparation_jetons_progres()
		self.__preparation_monnaies_joueurs()
		self.__preparation_merveilles()
	
	def __preparation_cartes(self) -> None:
		"""
		Methode privee.
		
		Prepare les cartes, sort aleatoirement des cartes et le place selon
		une structure precise.
		"""
		
		logger.debug(f"__preparation_cartes age {self.age}")
		
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
		
		logger.debug("\tplacement carte sur la plateau")
		
		# remplissage de la structure avec des cartes aleatoires.
		for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
			for num_colonne, _ in enumerate(ligne_carte):
				if self.cartes_plateau[num_ligne][num_colonne] == 1:
					
					# choix de la carte
					nouvelle_carte = random.choice(liste_carte)
					
					# suppresion carte choisie pour ne pas la choisir a nouveau
					liste_carte.remove(nouvelle_carte)
					
					# une ligne sur deux la carte sont face cachee,
					# par defaut une carte n est pas face cachee
					if num_ligne % 2 != 0:
						nouvelle_carte.cacher()
					
					# placement de la carte dans la structure
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
		
		logger.debug("__preparation_monnaies_joueurs")
		
		self.joueur1.monnaie = 7
		logger.debug(f"\t[{self.joueur1.nom}] gain de 7 monnaies")
		
		self.joueur2.monnaie = 7
		logger.debug(f"\t[{self.joueur2.nom}] gain de 7 monnaies")
		
		self.monnaie_banque -= 14
		logger.debug("\tbanque perd 14 monnaies")
	
	def __preparation_merveilles(self) -> None:
		"""
		Methode privee.
		
		Prepare les merveilles.
		Sort aleatoirement 4 merveiles, le joueur1 en choisie 1, puis le joueur2 en choisie 2,
		enfin le joueur1 prend la derniere.
		Sort aleatoirement 4 merveiles, le joueur2 en choisie 1, puis le joueur1 en choisie 2,
		enfin le joueur2 prend la derniere.
		"""
		
		logger.debug("__preparation_merveilles")
		
		if not self.choix_auto_merveilles:
			
			logger.debug("\tchoix non automatique")
			print("\n * Premiere selection de merveille aleatoire * \n")
			
			# choix aleatoire des 4 premieres merveilles
			liste_merveilles_alea = []
			for _ in range(4):
				liste_merveilles_alea.append(random.choice(self.merveilles))
			
			# les joueurs choississent leurs 4 premieres merveilles
			self.joueur1.selection_merveille(1, liste_merveilles_alea)
			self.joueur2.selection_merveille(2, liste_merveilles_alea)
			self.joueur1.selection_merveille(1, liste_merveilles_alea)
			
			print("\n * Deuxieme selection de merveille aleatoire * \n")
			# choix aleatoire des 4 dernieres merveilles
			
			for _ in range(4):
				liste_merveilles_alea.append(random.choice(self.merveilles))
			
			# les joueurs choississent leurs 4 dernieres merveilles
			self.joueur2.selection_merveille(1, liste_merveilles_alea)
			self.joueur1.selection_merveille(2, liste_merveilles_alea)
			self.joueur2.selection_merveille(1, liste_merveilles_alea)
		
		else:  # choix automatique des merveilles (d'apres les regles)
			logger.debug("\tchoix automatique")
			
			self.joueur1.merveilles.append(trouver_element_avec_nom("pyramides", self.merveilles))
			self.joueur1.merveilles.append(trouver_element_avec_nom("grand phare", self.merveilles))
			self.joueur1.merveilles.append(trouver_element_avec_nom("temple d artemis", self.merveilles))
			self.joueur1.merveilles.append(trouver_element_avec_nom("statue de zeus", self.merveilles))
			logger.debug(f"\t[{self.joueur1.nom}] liste merveilles : "
							f"\'pyramides\', \'grand phare\', \'temple d artemis\', \'statue de zeus\'")
			
			self.joueur2.merveilles.append(trouver_element_avec_nom("circus maximus", self.merveilles))
			self.joueur2.merveilles.append(trouver_element_avec_nom("piree", self.merveilles))
			self.joueur2.merveilles.append(trouver_element_avec_nom("via appia", self.merveilles))
			self.joueur2.merveilles.append(trouver_element_avec_nom("colosse", self.merveilles))
			logger.debug(f"\t[{self.joueur2.nom}] liste merveilles : "
							f"\'circus maximus\', \'piree\', \'via appia\', \'colosse\'")
	
	#
	#
	# Partie outils
	#
	#
	
	def obtenir_adversaire(self):
		"""
		Renvoie le nom_joueur adverse, le nom_joueur qui n'est pas stocke dans l attribut joueur_qui_joue.

		:return: nom_joueur adverse
		"""
		if self.joueur_qui_joue == self.joueur1:
			return self.joueur2
		else:
			return self.joueur1
	
	def enlever_carte(self, carte_a_enlever: Carte) -> None:
		"""
		Enleve une carte du plateau.

		:param carte_a_enlever: la carte a enlever.
		"""
		
		logger.debug(f"[{self.joueur_qui_joue.nom}] enlever_carte(\'{carte_a_enlever.nom}\')")
		carte_trouvee = False
		
		for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
			for num_colonne, carte in enumerate(ligne_carte):
				if carte == carte_a_enlever:
					
					logger.debug(f"\t[{self.joueur_qui_joue.nom}] carte enleve du plateau")
					self.cartes_plateau[num_ligne][num_colonne] = 0
					carte_trouvee = True
		
		if not carte_trouvee:
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] la carte n'est pas sur le plateau")
	
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
		"""
		TODO : documentation a faire

		:param ligne:
		:param colonne:
		:return:
		"""
		
		if ligne == 4:
			return True
		elif ligne == 0:
			if colonne == 0:
				return self.cartes_plateau[ligne + 1][colonne + 1] == 0
			elif colonne == len(self.cartes_plateau[ligne]) - 1:
				return self.cartes_plateau[ligne + 1][colonne - 1] == 0
		else:
			return (self.cartes_plateau[ligne + 1][colonne - 1] == 0) and (
						self.cartes_plateau[ligne + 1][colonne + 1] == 0)
	
	def liste_cartes_prenables(self):
		"""
		TODO : documentation a faire
		
		:return:
		"""
		cartes_prenable = []
		for num_ligne, ligne_carte in enumerate(self.cartes_plateau):
			for num_colonne, carte in enumerate(ligne_carte):
				if carte != 0 and self.cartes_prenable(num_ligne, num_colonne):
					cartes_prenable.append(carte)
		
		return cartes_prenable
	
	def changement_age(self):
		"""
		TODO : documentation a faire
		
		"""
		
		if self.age == 3:
			# fin de la partie
			return self.fin_de_partie("cartes_vide")
			
		else:
			# changement d'age
			self.age += 1
			self.__preparation_cartes()
			
			return "none", "none"
	
	def fin_de_partie(self, raison_fin: str):
		"""
		TODO : documentation a faire

		:param raison_fin:
		"""
		
		if raison_fin == "militaire":
			if self.position_jeton_conflit == 0:
				print(f"victoire militaire de \'{self.joueur2.nom}\'")
				return raison_fin, self.joueur2.nom
			elif self.position_jeton_conflit == 18:
				print(f"victoire militaire de \'{self.joueur1.nom}\'")
				return raison_fin, self.joueur2.nom
		
		elif raison_fin == "scientifique":
			print(f"victoire scientifiques de \'{self.joueur_qui_joue.nom}\'")
			return raison_fin, self.joueur_qui_joue.nom
		
		elif raison_fin == "cartes_vide":
			self.joueur_qui_joue.compter_point_victoire()
			self.obtenir_adversaire().compter_point_victoire()
			
			if self.joueur1.points_victoire > self.joueur2.points_victoire:
				print(f"victoire par points de \'{self.joueur1.nom}\' "
						f"({self.joueur1.points_victoire}, {self.joueur2.points_victoire})")
				return "points victoire", self.joueur1.nom
			
			elif self.joueur1.points_victoire < self.joueur2.points_victoire:
				print(f"victoire par points de \'{self.joueur2.nom}\' "
						f"({self.joueur1.points_victoire}, {self.joueur2.points_victoire})")
				return "points victoire", self.joueur2.nom
			else:
				print(f"Egalite ({self.joueur1.points_victoire}, {self.joueur2.points_victoire})")
				return "points victoire", "none"
				
	def gain_argent_banque(self, somme_gagnee: int):
		"""
		TODO : Documentation a faire

		:param somme_gagnee:
		:return:
		"""
		
		logger.debug(f"[{self.joueur_qui_joue.nom}] gain_argent_banque({somme_gagnee})")
		
		if somme_gagnee == 0:
			return 0
		
		if self.monnaie_banque == 0:
			gain = 0
			print("plus d'argent dans la banque")
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] plus d'argent dans la banque")
		
		elif self.monnaie_banque < somme_gagnee:
			gain = self.monnaie_banque
			self.monnaie_banque = 0
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] plus assez d'argent dans la banque, gain de {gain} monnaies")
		
		else:
			gain = somme_gagnee
			self.monnaie_banque -= somme_gagnee
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] gain de {gain} monnaies")
		
		return gain
	
	def acheter_ressources(self, ressources_manquantes: list) -> int:
		"""
		Permet au nom_joueur qui joue d'acheter les ressources qui lui manque pour construire sa carte.

		:param ressources_manquantes: liste des ressources manquantes
		:return prixDesRessources
		"""
		
		prix_commerce = 0
		
		# Verification si le nom_joueur adverse produit les ressources manquantes
		adversaire = self.obtenir_adversaire()
		carte_liste_ressource_adversaire = []
		for ressource_manquante in ressources_manquantes:
			carte_production = adversaire.production_type_ressources(ressource_manquante)
			if carte_production is not None:
				carte_liste_ressource_adversaire.append(carte_production)
		
		# si le nom_joueur adverse ne produit aucune ressouces ressources manquantes
		if len(carte_liste_ressource_adversaire) == 0:
			for ressource_manquante in ressources_manquantes:
				ressource_manquante_split = ressource_manquante.split(" ")
				
				if self.joueur_qui_joue.possede_carte_reduction(ressource_manquante_split[1]) != 0:
					# (1 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le nom_joueur
					prix_commerce += int(ressource_manquante_split[2])
				else:
					# (2 * quantite_ressource_adversaire = 0) * quantite_ressource_necessaire pour le nom_joueur
					prix_commerce += (2 * int(ressource_manquante_split[2]))
		
		# le nom_joueur adverse produit des ressouces qui me manquent
		else:
			# les cartes jaunes ne compte pas dans le commerce
			for carte in carte_liste_ressource_adversaire:
				if carte.couleur == "jaune":
					carte_liste_ressource_adversaire.remove(carte)
			
			for ressource_manquante in ressources_manquantes:
				ressource_manquante_split = ressource_manquante.split(" ")
				
				# si le nom_joueur adversaire produit la ressource
				ressource_trouve = False
				
				# parmis les cartes produisant la ressouce que j'achete
				for carteRessourceAdversaire in carte_liste_ressource_adversaire:
					
					# parmis les effets de cette carte
					for effet in carteRessourceAdversaire.effets:
						ressource_adversaire_split = effet.split(" ")
						
						# nom_joueur adversaire produit ressource qu'il me manque ?
						if ressource_manquante_split[1] == ressource_adversaire_split[1]:
							ressource_trouve = True
							
							# ai je une reduction sur cette ressource ?
							prix_reduc = self.joueur_qui_joue.possede_carte_reduction(ressource_manquante_split[1])
							if prix_reduc != 0:
								# (prix_reduc * quantite_ressource_necessaire pour le nom_joueur)
								prix_commerce += (prix_reduc * int(ressource_manquante_split[2]))
							else:
								# (2 + quantite_ressource_adversaire) * quantite_ressource_necessaire pour le nom_joueur
								prix_commerce += (
										(2 + int(ressource_adversaire_split[2])) * int(ressource_manquante_split[2]))
				
				# si l'adversaire ne produit pas la ressource
				if not ressource_trouve:
					prix_commerce += (2 * int(ressource_manquante_split[2]))
		
		return prix_commerce
		
	#
	#
	# Partie interaction utilisateur
	#
	#
	
	def demander_action_carte(self, carte: Carte):
		"""
		Demande a l'utilisateur l action qu'il souhaite faire avec la carte (defausser, ou piocher).

		:param carte: la carte choisie par le nom_joueur.
		"""
		
		str_action = f"[{self.joueur_qui_joue.nom}] defausser ou piocher ?\n > "
		while True:
			action = input(str_action)
			
			# defausser
			if action == "defausser":
				self.cartes_defaussees.append(carte)
				self.joueur_qui_joue.monnaie += self.gain_argent_banque(2)
				
				# gain de une piece par carte jaune
				for carte_joueur in self.joueur_qui_joue.cartes:
					if carte_joueur.couleur == "jaune":
						self.joueur_qui_joue.monnaie += self.gain_argent_banque(2)
				
				# fin action
				break
			
			# piocher
			elif action == "piocher":
				
				# construction de la carte gratuite via chainage
				if not self.joueur_qui_joue.possede_carte_chainage(carte):
					
					# la carte ne coute rien
					if carte.couts is None or len(carte.couts) == 0:
						# fin action
						break
						
					if carte.couleur == "bleu" and self.joueur_qui_joue.possede_jeton_scientifique("maconnerie"):
						self.reduction_couts_construction_carte(carte)
					
					# verification ressources nom_joueur
					liste_ressource_necessaire = self.joueur_qui_joue.couts_manquants(carte)
					
					# le nom_joueur possede toutes les ressouces
					if len(liste_ressource_necessaire) == 0:
						
						# on retire uniquement la monnaie
						for cout in carte.couts:
							# monnaie x
							cout_split = cout.split(" ")
							if cout_split[0] == "monnaie":
								self.joueur_qui_joue.monnaie -= int(cout_split[1])
						
						# fin action
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
							if self.obtenir_adversaire().possede_jeton_scientifique("economie"):
								self.obtenir_adversaire().monnaie += prix
							else:
								self.monnaie_banque += prix
							self.joueur_qui_joue.monnaie -= prix
						
							# fin action
							break
				
				else:  # le nom_joueur possde la carte chainage, construction gratuite
					# application effet jeton "urbanisme"
					if self.joueur_qui_joue.possede_jeton_scientifique("urbanisme"):
						self.joueur_qui_joue.monnaie += self.gain_argent_banque(4)
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
				merveille_a_construire = demander_element_dans_une_liste(
					self.joueur_qui_joue.nom, "merveille",
					self.joueur_qui_joue.merveilles
				)
				
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
					break
				
				else:
					# manque des ressouces
					for ressource_manquante in liste_ressource_necessaire:
						ressource_manquante_split = ressource_manquante.split(" ")
						
						# manque monnaie
						if ressource_manquante_split[0] == "monnaie":
							print("Vous n'avez pas assez de monnaie pour construire la merveille")
							break
					
					# manque des ressources autre que monnaie
					prix = self.acheter_ressources(liste_ressource_necessaire)
					if prix > self.joueur_qui_joue.monnaie:
						print("Impossible de faire le commerce, vous n'avez pas assez de monnaie")
						break
					else:
						return merveille_a_construire
						
			elif action == "non":
				break
			else:
				print("action merveille inconnue")
		
		return None
	
	def demander_ressource_au_choix(self, liste_ressources: list) -> str:
		"""
		Si une carte possede l'effet "ressource_au_choix" le nom_joueur doit choisir
		quel ressource il souhaite produire.

		:param liste_ressources: la liste des ressources au choix.
		:return: un nouvel effet, "ressource x 1", avec x la ressource choisit.
		"""
		
		ressource = "ressource "
		str_demande = f"[{self.joueur_qui_joue.nom}] Nom de la ressource choisie ?\n > "
		print("\n * liste des ressources *\n", liste_ressources)
		nom_ressource = input(str_demande)
		while nom_ressource not in liste_ressources:
			print("Ressource inconnu, veuillez recommencer")
			nom_ressource = input(str_demande)
		return ressource + nom_ressource + " 1"
	
	#
	#
	# Partie effets
	#
	#
	
	def demande_symbole_scientifique(self):
		"""
		TODO : documentation a faire

		"""
		
		logger.debug(f"[{self.joueur_qui_joue.nom}] demande_symbole_scientifique")
		
		while True:
			print(f"* liste choix possibles *\n{SYMBOLE_SCIENTIFIQUES}")
			nom_symbole = input(f"[{self.joueur_qui_joue.nom}] Choix symbole scientifique ?\n > ")
			
			index_symbole_choisit = 0
			try:
				index_symbole_choisit = SYMBOLE_SCIENTIFIQUES.index(nom_symbole)
			except ValueError:
				print(f" * ERREUR * Aucune ressource ne repond au nom \'{nom_symbole}\', veuillez recommencer")
				continue
			else:
				break
		
		symbole_scientifique = SYMBOLE_SCIENTIFIQUES[index_symbole_choisit]
		logger.debug(f"[{self.joueur_qui_joue.nom}] a choisit \'{symbole_scientifique}\'")
		
		self.joueur_qui_joue.cartes.append(
			Carte("carte_custom", None, [symbole_scientifique], [], None, None, None)
		)
	
	def reduction_couts_construction_carte(self, carte: Carte):
		"""
		Le joueur choisit 2 ressources parmis les couts de la carte qui seront gratuit.
		
		:param carte: la carte dont on regarde les couts.
		"""
		
		logger.debug(f"[{self.joueur_qui_joue.nom}] reduction_couts_construction_carte(\'{carte.nom}\')")
		
		# separation cout monnaie et cout ressource
		couts_sans_monnaies = []
		for cout in carte.couts:
			
			# decoupage
			cout_split = cout.split(" ")
			
			if cout_split[0] == "ressource":
				couts_sans_monnaies.append(cout)
		
		logger.debug(f"\t[{self.joueur_qui_joue.nom}] couts_sans_monnaies : {couts_sans_monnaies}")
		
		# liste des ressources choisies
		ressources_choisies = []
		for _ in range(2):
			# output ressource_demandee : nom_ressource, ressource_choisie
			nom_ressource, ressource_choisie = demander_ressource_dans_une_liste(
				self.joueur_qui_joue.nom,
				couts_sans_monnaies
			)
			
			ressources_choisies.append(nom_ressource)
			
			# suppression de la ressource choisie pour le prochaine choix
			ressource_demandee_split = ressource_choisie.split(" ")
			if int(ressource_demandee_split[2]) > 1:
				diff_quantite = str(int(ressource_demandee_split[2]) - 1)
				nouv_ressource = "ressource " + nom_ressource + " " + diff_quantite
				couts_sans_monnaies[couts_sans_monnaies.index(ressource_choisie)] = nouv_ressource
			else:
				couts_sans_monnaies.remove(ressource_choisie)
		
		logger.debug(f"\t[{self.joueur_qui_joue.nom}] ressources_choisies : {ressources_choisies}")
		
		# suppression ressources choisies
		copy_couts = carte.couts.copy()
		for cout in carte.couts:
			
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] cout carte : {cout}")
			
			# decoupage
			cout_split = cout.split(" ")
			
			for ressource_choisie in ressources_choisies:
				
				logger.debug(f"\t[{self.joueur_qui_joue.nom}] ressource_choisie : {ressource_choisie}")
				
				if (cout_split[0] == "ressource" and
					cout_split[1] == ressource_choisie):
					
					quantite_ressource_choisie = ressources_choisies.count(ressource_choisie)
					
					if int(cout_split[2]) == quantite_ressource_choisie:
						copy_couts.remove(cout)
						
						logger.debug(f"\t[{self.joueur_qui_joue.nom}] "
										f"suppression total de la ressource : {cout}")
						
					elif int(cout_split[2]) > quantite_ressource_choisie:
						quantite_reduction = int(cout_split[2]) - quantite_ressource_choisie
						nouv_cout = cout_split[0] + " " + cout_split[1] + " " + str(quantite_reduction)
						copy_couts[copy_couts.index(cout)] = nouv_cout
						
						logger.debug(f"\t[{self.joueur_qui_joue.nom}] "
										f"suppression partiel de la ressource : {cout}")
		
		# remplassement cout
		carte.couts = copy_couts
		
		logger.debug(f"\t[{self.joueur_qui_joue.nom}] "
						f"nouveau couts de la carte : {carte.couts}")
	
	def defausser_carte_adversaire(self, couleur: str) -> None:
		"""
		Retire une carte de couleur de l'adversaire pour l'ajouter dans la liste des cartes faussees.

		:param couleur: la couleur de la carte a defausser.
		"""
		
		adversaire = self.obtenir_adversaire()
		while True:
			print("\n * liste choix possibles *\n", monStrListe(adversaire.cartes))
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
		Le nom_joueur gain 1 jeton parmis 3 jetons_progres aleatoire non selectionnes au debut de la partie.
		"""
		
		# tirage aleatoire des 3 jetons_progres
		liste_jetons = []
		for _ in range(3):
			jeton_random = random.choice(self.jetons_progres)
			liste_jetons.append(jeton_random)
			self.jetons_progres.remove(jeton_random)
		
		# le nom_joueur en choisit 1
		jeton_choisi = demander_element_dans_une_liste(
			self.joueur_qui_joue.nom, "jeton progres", liste_jetons
		)
		liste_jetons.remove(jeton_choisi)
		
		# les autres sont remis dans la boite
		for jeton in liste_jetons:
			self.jetons_progres.append(jeton)
	
	def construction_carte_defausser(self) -> None:
		"""
		Le nom_joueur construit gratuitement une carte defaussee.
		"""
		
		carte_choisie = demander_element_dans_une_liste(
			self.joueur_qui_joue.nom, "carte defausser", self.cartes_defaussees
		)
		self.joueur_qui_joue.cartes.append(carte_choisie)
		self.appliquer_effets_carte(carte_choisie)
	
	def gain_symbole_scientifique(self, nom_symbole_scientifique: str) -> bool:
		"""
		TODO : Documentation a faire

		:param nom_symbole_scientifique:
		:return:
		"""
		
		logger.debug(f"[{self.joueur_qui_joue.nom}] gain_symbole_scientifique(\'{nom_symbole_scientifique}\')")
		
		for ma_carte in self.joueur_qui_joue.cartes:
			for effet_ma_carte in ma_carte.effets:
				effet_ma_carte_split = effet_ma_carte.split(" ")
				
				# si possede une carte donnant le même symbole
				if effet_ma_carte_split[0] == "symbole_scientifique" \
						and effet_ma_carte_split[1] == nom_symbole_scientifique:
					# 2 symboles identiques => gain jeton
					jeton_choisi = demander_element_dans_une_liste(
						self.joueur_qui_joue.nom, "jeton progres", self.jetons_progres_plateau
					)
					
					logger.debug(
						f"[{self.joueur_qui_joue.nom}] ajout du jeton (\'{jeton_choisi.nom}\')")
					
					self.joueur_qui_joue.jetons_progres.append(jeton_choisi)
					
					self.appliquer_effets_jeton(jeton_choisi)
					
					# Suppression du jeton du plateau
					self.jetons_progres_plateau.remove(jeton_choisi)
					
					# suppression de l'effet gain symbole scientifique
					ma_carte.effets.remove(effet_ma_carte)
					return True
		return False
	
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
		"""
		TODO : documentation a faire

		:param nbr_deplacement:
		"""
		
		logger.debug(f"[{self.joueur_qui_joue.nom}] deplacer_pion_miltaire(\'{nbr_deplacement}\')")
		
		# On deplace le pion case par case
		for _ in range(nbr_deplacement):
			
			if self.joueur_qui_joue == self.joueur2:
				self.position_jeton_conflit -= 1
			else:
				self.position_jeton_conflit += 1
			
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] deplacement du pion conflit, nouvelle position "
							f"{self.position_jeton_conflit}")
			
			# si le pion se situe au bou du plateau militaire, il y a une victoire militaire
			if self.position_jeton_conflit in [0, 18]:
				logger.debug(
					f"\t[{self.joueur_qui_joue.nom}] le jeton est à la fin de plateau ({self.position_jeton_conflit})")
				return self.fin_de_partie("militaire")
			
			else:
				numero_jeton = self.numero_jeton_militaire()
				logger.debug(f"\t[{self.joueur_qui_joue.nom}] position du jeton militaire : {numero_jeton}")
				
				if numero_jeton != -1:
					jeton = self.jetons_militaire[numero_jeton]
					
					if not jeton.est_utilise:
						logger.debug(f"\t[{self.joueur_qui_joue.nom}] prend le jeton {numero_jeton}, "
										f"gagne {jeton.points_victoire} points de victoire, l'adversaire perd "
										f"{jeton.pieces} monnaies")
						
						self.joueur_qui_joue.points_victoire += jeton.points_victoire
						self.obtenir_adversaire().monnaie -= jeton.pieces
						self.monnaie_banque += jeton.pieces
						jeton.est_utilise = True
		
		return "none", "none"
	
	def appliquer_effets_carte(self, carte: Carte):
		"""
		TODO : documentation a faire

		:param carte:
		"""
		
		logger.debug(f"[{self.joueur_qui_joue.nom}] appliquer_effets_carte(\'{carte.nom}\')")
		
		for effet in carte.effets:
			
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] \'{effet}\'")
			effet_split = effet.split(" ")
			
			if effet_split[0] == "ressource":
				self.joueur_qui_joue.ressources[effet_split[1]] += 1
			
			elif effet_split[0] == "attaquer":
				nbr_bouclier = int(effet_split[1])
				
				if self.joueur_qui_joue.possede_jeton_scientifique("strategie"):
					logger.debug(f"[{self.joueur_qui_joue.nom}] bonus attaquer du jeton \'strategie\'")
					nbr_bouclier += 1
					
				return self.deplacer_pion_miltaire(nbr_bouclier)
			
			elif effet_split[0] == "symbole_scientifique":
				if self.gain_symbole_scientifique(effet_split[1]):
					carte.effets.remove(effet)
					
					if len(self.joueur_qui_joue.jetons_progres) == 6:
						return self.fin_de_partie("scientifique")
			
			elif effet_split[0] == "point_victoire":
				logger.debug(f"[{self.joueur_qui_joue.nom}] gain de {effet_split[1]} points de victoire")
				self.joueur_qui_joue.points_victoire += int(effet_split[1])
			
			elif effet_split[0] == "monnaie":
				logger.debug(f"[{self.joueur_qui_joue.nom}] gain de {effet_split[1]} monnaies")
				self.joueur_qui_joue.monnaie += self.gain_argent_banque(int(effet_split[1]))
			
			elif effet_split[0] == "ressource_au_choix":
				# remplace effet ressource au choix par un ressource classique
				ressource = ""
				# "ressource_au_choix x y"
				if len(effet_split) == 3:
					ressource = self.demander_ressource_au_choix([effet_split[1], effet_split[2]])
				# "ressource_au_choix x y z"
				elif len(effet_split) == 4:
					ressource = self.demander_ressource_au_choix([effet_split[1], effet_split[2], effet_split[3]])
				
				logger.debug(f"[{self.joueur_qui_joue.nom}] choix : {ressource}")
				carte.effets.remove(effet)
				carte.effets.append(ressource)
				
				ressource_split = ressource.split(" ")
				self.joueur_qui_joue.ressources[ressource_split[1]] += 1
			
			elif effet_split[0] == "monnaie_par_carte":
				logger.debug(f"[{self.joueur_qui_joue.nom}] monnaie_par_carte : {effet_split[1]}")
				for ma_carte in self.joueur_qui_joue.cartes:
					if ma_carte.couleur == effet_split[1]:
						self.joueur_qui_joue.monnaie += self.gain_argent_banque(int(effet_split[2]))
						
		return "none", "none"
	
	def appliquer_effets_merveille(self, merveille: CarteFille):
		"""
		TODO : documentation a faire
		
		:param merveille:
		:return:
		"""
		
		logger.debug(f"\t[{self.joueur_qui_joue.nom}] appliquer_effets_merveille(\'{merveille.nom}\')")
		
		for effet in merveille.effets:
			
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] \'{effet}\'")
			effet_split = effet.split(" ")
			
			# effet commun avec certains carte
			if effet_split[0] in ["symbole_scientifique", "point_victoire", "monnaie",
				"monnaie_par_carte", "ressource_au_choix"]:
				
				return self.appliquer_effets_carte(merveille)
				
			elif effet_split[0] == "attaquer":
				return self.deplacer_pion_miltaire(int(effet_split[1]))
			
			elif effet_split[0] == "defausse_carte_adversaire":
				if len(self.obtenir_adversaire().possede_cartes_couleur(effet_split[2])) != 0:
					self.defausser_carte_adversaire(effet_split[1])
				else:
					print("Le nom_joueur adverse ne possede aucune carte de cette couleur.")
			
			elif effet_split[0] == "rejouer" or self.joueur_qui_joue.possede_jeton_scientifique("theologie"):
				return "none", "rejouer"
			
			elif effet_split[0] == "jeton_progres_aleatoire":
				self.gain_jeton_progres_alea()
			
			elif effet_split[0] == "construction_fausse_gratuite":
				self.construction_carte_defausser()
			
			elif effet_split[0] == "adversaire_perd_monnaie":
				self.obtenir_adversaire().monnaie -= int(effet_split[1])
				self.monnaie_banque += int(effet_split[1])
		
		return "none", "none"
		
	def appliquer_effets_jeton(self, jeton: JetonProgres):
		"""
		TODO : documentation a faire

		:param jeton:
		"""
		logger.debug(f"\t[{self.joueur_qui_joue.nom}] appliquer_effets_jeton(\'{jeton.nom}\')")
		
		if jeton.nom in ["agriculture", "urbanisme"]:
			
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] gain de 6 monnaies")
			self.joueur_qui_joue -= 6
			self.monnaie_banque += 6
		
		elif jeton.nom == "philosophie":
			
			logger.debug(f"\t[{self.joueur_qui_joue.nom}] gain de 7 points de victoire")
			self.joueur_qui_joue.points_victoire += 7
			
		elif jeton.nom == "loi":
			
			self.demande_symbole_scientifique()
		