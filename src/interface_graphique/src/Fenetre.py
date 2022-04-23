# TODO : optimiser affichage pour avoir moins de lattence
import math

import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES
from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.interface_graphique.src.SpriteJetonsMilitaire import SpriteJetonsMilitaire
from src.interface_graphique.src.SpriteJetonsProgres import SpriteJetonsProgres
from src.interface_graphique.src.SpriteMerveille import SpriteMerveille
from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres
from src.utils.Plateau import Plateau
from src.utils.Stategie import alpha_beta, alpha_beta_avec_merveille

RATIO_IMAGE = 0.15
RATIO_MERVEILLE = 0.10
RATIO_JETONS_PROGRES = 0.155
RATIO_JETONS_MILITAIRE2 = 0.18
RATIO_JETONS_MILITAIRE5 = 0.16
RATIO_MONNAIES_6 = 0.16
RATIO_MONNAIES_3 = 0.18
RATIO_MONNAIES_1 = 0.16

RATIO_PLATEAU = 0.50
RATIO_BANQUE = 0.05
RATIO_ZOOM_CARTE = 0.65
RATIO_ZOOM_MERVEILLE = 0.45
RATIO_ZOOM_JETONS_SCIENTIFIQUES = 0.60


class Fenetre:
	def __init__(self, titre: str, plateau: Plateau, difficulte_profondeur):
		pygame.init()
		
		self.plateau = plateau
		self.difficulte_profondeur = difficulte_profondeur
		
		self.ecran = pygame.display.set_mode()
		self.largeur, self.hauteur = self.ecran.get_size()
		
		pygame.display.set_caption(titre)
		
		default_sprite_image = SpriteCarte(Carte("academie", None, None, None, None, 3), 0, 0, RATIO_IMAGE)
		self.default_hauteur_sprite = default_sprite_image.rect.height
		self.default_largeur_sprite = default_sprite_image.rect.width
		
		default_sprite_merveille = SpriteMerveille(CarteFille("piree", None, None), 0, 0, RATIO_MERVEILLE)
		self.default_hauteur_merveille = default_sprite_merveille.rect.height
		self.default_largeur_merveille = default_sprite_merveille.rect.width
		
		default_sprite_jetons_progres = SpriteJetonsProgres(JetonProgres("agriculture", None), 0, 0, RATIO_JETONS_PROGRES)
		self.default_hauteur_jetons_progres = default_sprite_jetons_progres.rect.height
		self.default_largeur_jetons_progres = default_sprite_jetons_progres.rect.width
		
		self.sprite_cartes_plateau = pygame.sprite.Group()
		self.sprite_cartes_defaussees = pygame.sprite.Group()
		
		self.sprite_j1 = [
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group()
		]
		self.sprite_j2 = [
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group(),
			pygame.sprite.Group()
		]
		
		self.sprite_carte_j1_zoomer = None
		self.sprite_jeton_j1_zoomer = None
		self.sprite_merveille_j1_zoomer = None
		self.choix_jeton = False
		
		self.sprite_carte_j2_zoomer = None
		
		self.espace_entre_carte = self.largeur * 0.005
		
		image_fond = pygame.image.load(DOSSIER_IMAGES + "fond_jeux.jpg").convert()
		self.image_fond = pygame.transform.scale(image_fond, (self.largeur, self.hauteur))
		
		image_plateau = pygame.image.load(DOSSIER_IMAGES + "plateau_sans_fond.png")
		image_plateau.set_colorkey((255, 255, 255))
		larg_plat, haut_plat = image_plateau.get_size()
		ration_plat = haut_plat / larg_plat
		larg_plat = RATIO_PLATEAU * self.largeur
		haut_plat = ration_plat * larg_plat
		self.image_plateau = pygame.transform.scale(image_plateau, (larg_plat, haut_plat))
		self.rect_image_plateau = self.image_plateau.get_rect()
		self.rect_image_plateau.topleft = (
			(self.largeur / 2 - self.image_plateau.get_width() / 2,
			2 * self.espace_entre_carte)
		)
		
		image_banque = pygame.image.load(DOSSIER_IMAGES + "banque_icon.png").convert_alpha()
		larg_banque, haut_banque = image_banque.get_size()
		ration_banque = haut_banque / larg_banque
		larg_banque = RATIO_BANQUE * self.largeur
		haut_banque = ration_banque * larg_banque
		self.image_banque = pygame.transform.scale(image_banque, (larg_banque, haut_banque))
		self.rect_image_banque = self.image_banque.get_rect()
		self.rect_image_banque.topleft = (
			(self.largeur / 2 + self.rect_image_plateau.width / 4 - self.image_banque.get_width() / 2,
			self.hauteur - 2 * self.espace_entre_carte - self.image_banque.get_height())
		)
		
		self.merveille_j1 = pygame.sprite.Group()
		self.merveille_j2 = pygame.sprite.Group()
		self.__dessiner_merveille()
		
		self.jetons_progres_plateau = pygame.sprite.Group()
		self.jetons_progres_j1 = pygame.sprite.Group()
		self.jetons_progres_j2 = pygame.sprite.Group()
		self.__dessiner_jetons_scientifiques()
		self.__dessiner_carte()
		
		top_x = self.largeur / 2
		top_x -= 12
		_, top_y = self.rect_image_plateau.bottomleft
		top_y /= 2
		top_y -= 5
		top = (top_x, top_y)
		
		larg = 26
		long = 56
		
		self.rect_jeton_conflit = pygame.Rect(top, (larg, long))
		
		self.sprite_jetons_militaire = pygame.sprite.Group()
		self.__dessiner_jetons_militaire()
		
	def __dessiner_carte_age_I(self):
		origine_cartes = self.largeur / 2 - self.default_largeur_sprite - self.espace_entre_carte / 2
		
		haut_gauche_x = origine_cartes
		_, haut_gauche_y = self.rect_image_plateau.bottomright
		haut_gauche_y += self.espace_entre_carte
		
		for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
			for num_colone, carte in enumerate(ligne_cartes):
				
				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.sprite_cartes_plateau.add(sprite_carte)
					
					# coords carte suivante
					haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte
			
			# coords changement ligne
			haut_gauche_x = origine_cartes - (num_ligne + 1) * self.default_largeur_sprite / 2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite / 2
	
	def __dessiner_carte_age_II(self):
		origine_cartes = self.largeur / 2 - 3 * self.default_largeur_sprite - self.espace_entre_carte / 2
		
		haut_gauche_x = origine_cartes
		_, haut_gauche_y = self.rect_image_plateau.bottomright
		haut_gauche_y += self.espace_entre_carte
		
		for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
			for num_colone, carte in enumerate(ligne_cartes):
				
				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.sprite_cartes_plateau.add(sprite_carte)
					
					# coords carte suivante
					haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte
			
			# coords changement ligne
			haut_gauche_x = origine_cartes + (num_ligne+1) * self.default_largeur_sprite / 2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite/2
			
	def __dessiner_carte_age_III(self):
		origine_cartes = self.largeur / 2 - self.default_largeur_sprite - self.espace_entre_carte / 2
		
		haut_gauche_x = origine_cartes
		_, haut_gauche_y = self.rect_image_plateau.bottomright
		haut_gauche_y += self.espace_entre_carte

		for num_ligne in range(3):
			ligne_cartes = self.plateau.cartes_plateau[num_ligne]
			for num_colone in range(len(ligne_cartes)):
				carte = ligne_cartes[num_colone]

				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.sprite_cartes_plateau.add(sprite_carte)

					# coords carte suivante
					haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte

			# coords changement ligne
			haut_gauche_x = origine_cartes - (num_ligne + 1) * self.default_largeur_sprite / 2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite / 2
			
		#
		haut_gauche_x = origine_cartes - self.default_largeur_sprite / 2
		carte = self.plateau.cartes_plateau[3][1]
		self.sprite_cartes_plateau.add(SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE))
		
		#
		haut_gauche_x = origine_cartes + self.default_largeur_sprite + self.default_largeur_sprite / 2
		carte = self.plateau.cartes_plateau[3][5]
		self.sprite_cartes_plateau.add(SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE))
		haut_gauche_y += self.default_hauteur_sprite/2
		
		#
		haut_gauche_x = origine_cartes - self.default_largeur_sprite - self.espace_entre_carte
		for num_ligne in range(4, len(self.plateau.cartes_plateau)):
			ligne_cartes = self.plateau.cartes_plateau[num_ligne]
			for num_colone in range(len(ligne_cartes)):
				carte = ligne_cartes[num_colone]

				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.sprite_cartes_plateau.add(sprite_carte)

					# coords carte suivante
					haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte

			# coords changement ligne
			haut_gauche_x = origine_cartes - self.default_largeur_sprite + \
							(num_ligne - 4 + 1) * self.default_largeur_sprite / 2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite/2
	
	def __dessiner_carte(self):
		if self.plateau.age == 1:
			self.__dessiner_carte_age_I()
		elif self.plateau.age == 2:
			self.__dessiner_carte_age_II()
		else:
			self.__dessiner_carte_age_III()
			
	def __dessiner_merveille(self):
		compteur = 0
		for merveille in self.plateau.joueur1.merveilles:
			coord_x, coord_y = self.rect_image_plateau.bottomleft
			coord_x += self.espace_entre_carte
			
			coord_y += compteur * (self.default_largeur_merveille + self.espace_entre_carte)
			coord_y += compteur * (self.default_hauteur_sprite / 4)
			
			merveille_sprite = SpriteMerveille(merveille, coord_x, coord_y, RATIO_MERVEILLE)
			merveille_sprite.angle = -90
			self.merveille_j1.add(merveille_sprite)
			
			compteur += 1
		
		compteur = 0
		for merveille in self.plateau.joueur2.merveilles:
			coord_x, coord_y = self.rect_image_plateau.bottomright
			coord_x -= self.default_hauteur_merveille
			coord_x -= self.espace_entre_carte
			
			coord_y += compteur * (self.default_largeur_merveille + self.espace_entre_carte)
			coord_y += compteur * (self.default_hauteur_sprite / 4)
			
			sprite_merveille = SpriteMerveille(merveille, coord_x, coord_y, RATIO_MERVEILLE)
			sprite_merveille.angle = 90
			self.merveille_j2.add(sprite_merveille)
			
			compteur += 1
			
	def __dessiner_merveille_sacrifier(self, merveille_a_construire: SpriteMerveille, carte_a_sacrifier: SpriteCarte):
		for merveille_j1 in self.merveille_j1:
			
			if isinstance(merveille_j1, SpriteMerveille) \
					and merveille_j1.merveille == merveille_a_construire.merveille:
				
				carte_a_sacrifier.carte.cacher()
				
				coord_x, coord_y = merveille_a_construire.rect.topleft
				coord_y += self.default_largeur_sprite / 5
				
				# TODO : adapter image à la taille de la merveille
				carte_a_sacrifier.changer_coords(coord_x, coord_y)
				
		self.merveille_j1.remove(merveille_a_construire)
		self.merveille_j1.add(carte_a_sacrifier)
		self.merveille_j1.add(merveille_a_construire)
		
	def __dessiner_jetons_scientifiques(self):
		coord_x, coord_y = self.rect_image_plateau.topleft
		coord_x += 1 / 4 * self.rect_image_plateau.width
		
		coord_y += self.espace_entre_carte
		
		for jeton in self.plateau.jetons_progres_plateau:
			sprite_jetons_progres = SpriteJetonsProgres(
				jeton, coord_x, coord_y, RATIO_JETONS_PROGRES
			)
			self.jetons_progres_plateau.add(sprite_jetons_progres)
			
			coord_x += 1 / 50 * self.rect_image_plateau.width + self.default_largeur_jetons_progres
	
	def __dessiner_monnaies(self):
		# j1
		if self.plateau.joueur1.monnaie > 0:
			coord_x, coord_y = self.rect_image_plateau.bottomleft
			coord_x /= 4
			coord_y /= 4
			
			repartition = self.plateau.joueur1.trouver_repartition_monnaies()
			
			piece1 = None
			for piece, qte in repartition.items():
				if qte != 0:
					piece1 = piece
					break
			
			chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece1}.xcf"
			image_monnaies = pygame.image.load(chemin_monnaies).convert_alpha()
			
			larg, haut = image_monnaies.get_size()
			larg *= RATIO_MONNAIES_6
			
			image_monnaies = pygame.transform.scale(image_monnaies, (larg, larg))
			self.ecran.blit(image_monnaies, (coord_x, coord_y))
			
			repartition[piece1] -= 1
			
			for piece, qte in repartition.items():
				for _ in range(qte):
					chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece}.xcf"
					image_monnaies = pygame.image.load(chemin_monnaies).convert_alpha()
					
					coord_x += larg / 2
					
					larg, haut = image_monnaies.get_size()
					if piece == 6:
						larg *= RATIO_MONNAIES_6
					elif piece == 3:
						larg *= RATIO_MONNAIES_3
					else:
						larg *= RATIO_MONNAIES_1
					
					image_monnaies = pygame.transform.scale(image_monnaies, (larg, larg))
					self.ecran.blit(image_monnaies, (coord_x, coord_y))
		
		# j2
		if self.plateau.joueur2.monnaie > 0:
			coord_x, coord_y = self.rect_image_plateau.bottomright
			coord_x += 10
			coord_y /= 4
			
			repartition = self.plateau.joueur2.trouver_repartition_monnaies()
			
			piece1 = None
			for piece, qte in repartition.items():
				if qte != 0:
					piece1 = piece
					break
			
			chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece1}.xcf"
			image_monnaies = pygame.image.load(chemin_monnaies).convert_alpha()
			
			larg, haut = image_monnaies.get_size()
			larg *= RATIO_MONNAIES_6
			
			image_monnaies = pygame.transform.scale(image_monnaies, (larg, larg))
			self.ecran.blit(image_monnaies, (coord_x, coord_y))
			
			repartition[piece1] -= 1
			
			for piece, qte in repartition.items():
				for _ in range(qte):
					chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece}.xcf"
					image_monnaies = pygame.image.load(chemin_monnaies).convert_alpha()
					
					coord_x += larg / 2
					
					larg, haut = image_monnaies.get_size()
					if piece == 6:
						larg *= RATIO_MONNAIES_6
					elif piece == 3:
						larg *= RATIO_MONNAIES_3
					else:
						larg *= RATIO_MONNAIES_1
					
					image_monnaies = pygame.transform.scale(image_monnaies, (larg, larg))
					self.ecran.blit(image_monnaies, (coord_x, coord_y))
		
	def __deplacer_jeton_attaque(self):
		top_x, top_y, larg, long = self.rect_jeton_conflit
		
		nbr_deplacement = abs(self.plateau.position_jeton_conflit - 9)
		decalage = 37
		
		top_x = self.largeur / 2
		top_x -= 12
		
		if self.plateau.position_jeton_conflit > 9:
			top_x += nbr_deplacement * decalage
		elif self.plateau.position_jeton_conflit < 9:
			top_x -= nbr_deplacement * decalage
		
		self.rect_jeton_conflit = (top_x, top_y, larg, long)
		
		for jeton_militaire in self.plateau.jetons_militaire:
			for sprite_jeton_militaire in self.sprite_jetons_militaire:
				if isinstance(sprite_jeton_militaire, SpriteJetonsMilitaire):
					if jeton_militaire.est_utilise and jeton_militaire == sprite_jeton_militaire.jeton:
						self.sprite_jetons_militaire.remove(sprite_jeton_militaire)
						
	def __deplacer_jeton_scientifique(self, sprite_jeton: SpriteJetonsProgres):
		if self.plateau.joueur_qui_joue == self.plateau.joueur1:
			coord_x, coord_y = self.rect_image_plateau.bottomleft
			coord_x /= 8
			coord_y /= 8
			
			for _ in self.jetons_progres_j1:
				coord_x += self.default_largeur_sprite
				
			sprite_jeton.changer_coords(coord_x, coord_y)
			self.jetons_progres_j1.add(sprite_jeton)
			self.jetons_progres_plateau.remove(sprite_jeton)
			
		else:
			coord_x, coord_y = self.rect_image_plateau.bottomright
			coord_x += 10
			coord_y /= 8
			
			for _ in self.jetons_progres_j2:
				coord_x += self.default_largeur_sprite
			
			sprite_jeton.changer_coords(coord_x, coord_y)
			self.jetons_progres_j2.add(sprite_jeton)
			self.jetons_progres_plateau.remove(sprite_jeton)
		
	def __dessiner_jetons_militaire(self):
		plat_long = self.rect_image_plateau.width
		plat_larg = self.rect_image_plateau.height
		
		top_x, top_y = self.rect_image_plateau.topright
		top_x -= plat_long * 0.35
		top_y += plat_larg * (3 / 4)
		self.sprite_jetons_militaire.add(
			SpriteJetonsMilitaire(self.plateau.jetons_militaire[4], top_x, top_y, RATIO_JETONS_MILITAIRE2))
		
		top_x += plat_long * 0.13
		self.sprite_jetons_militaire.add(
			SpriteJetonsMilitaire(self.plateau.jetons_militaire[5], top_x, top_y, RATIO_JETONS_MILITAIRE5))
		
		top_x, _ = self.rect_image_plateau.topleft
		top_x += plat_long * 0.25
		self.sprite_jetons_militaire.add(
			SpriteJetonsMilitaire(self.plateau.jetons_militaire[1], top_x, top_y, RATIO_JETONS_MILITAIRE2))

		top_x -= plat_long * 0.13
		self.sprite_jetons_militaire.add(
			SpriteJetonsMilitaire(self.plateau.jetons_militaire[0], top_x, top_y, RATIO_JETONS_MILITAIRE5))
	
	def __position_type_carte(self, carte: Carte):
		if not isinstance(carte, CarteFille):
			liste_couleur = ["marron", "gris", "bleu", "vert", "jaune", "rouge"]
			if carte.couleur in liste_couleur:
				return liste_couleur.index(carte.couleur)
		else:
			if carte.nom.__contains__("guilde"):
				return 6
			
	def __dessiner_piocher(self, sprite_carte: SpriteCarte):
		ret = self.plateau.piocher(sprite_carte.carte)
		
		if ret == -1:
			self.__dessiner_defausser(sprite_carte)
			
		else:
			self.plateau.joueur_qui_joue.cartes.append(sprite_carte.carte)
			self.plateau.enlever_carte(sprite_carte.carte)
			
			if ret == 2:
				self.choix_jeton = True
				
			type_carte = self.__position_type_carte(sprite_carte.carte)
			
			sprite_carte.angle = 90
			
			if self.plateau.joueur_qui_joue == self.plateau.joueur1:
				sprite_joueur_qui_joue = self.sprite_j1
				sprite_carte.angle = -sprite_carte.angle
				coord_x, _ = self.rect_image_plateau.bottomleft
				coord_x -= self.espace_entre_carte
				coord_x -= self.default_hauteur_sprite
				decalage_x = -(len(sprite_joueur_qui_joue[type_carte]) * (self.default_hauteur_sprite / 4))
			else:
				sprite_joueur_qui_joue = self.sprite_j2
				coord_x, _ = self.rect_image_plateau.bottomright
				coord_x += self.espace_entre_carte
				decalage_x = len(sprite_joueur_qui_joue[type_carte]) * (self.default_hauteur_sprite / 4)
			
			if type_carte == 0:
				coord_y = type_carte * self.default_largeur_sprite
			else:
				coord_y = type_carte * (
						self.default_largeur_sprite + self.espace_entre_carte
				)
			
			coord_y -= self.rect_image_plateau.height*1/4
			coord_y += self.default_largeur_sprite
			coord_x += decalage_x
			
			sprite_joueur_qui_joue[type_carte].add(sprite_carte)
			sprite_carte.changer_coords(coord_x, coord_y)
			
	def __dessiner_defausser(self, carte_prenable: SpriteCarte):
		self.plateau.defausser(carte_prenable.carte)
		self.sprite_cartes_defaussees.add(carte_prenable)
		
		coord_x = self.largeur / 2 - self.rect_image_plateau.width / 4
		coord_y = self.hauteur - (self.default_hauteur_sprite + self.espace_entre_carte)
		carte_prenable.changer_coords(coord_x, coord_y)
		
	def boucle_principale(self):
		en_cours = True
		while en_cours:
			if self.plateau.joueur_gagnant is not None:
				en_cours = False
			
			# PARTIE Process input (events)
			for event in pygame.event.get():
				
				# quitter avec la croix
				if event.type == pygame.QUIT:
					en_cours = False
				
				# quitter avec la touche echap
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						en_cours = False
				
				if self.plateau.joueur_qui_joue == self.plateau.joueur1:
					
					if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
						
						clic_x, clic_y = event.pos
						
						if self.sprite_jeton_j1_zoomer is None \
							and self.sprite_merveille_j1_zoomer is None:
						
							for sprit in self.sprite_cartes_plateau:
								
								if sprit.rect.collidepoint(clic_x, clic_y):
									
									if isinstance(sprit, SpriteCarte):
										
										if sprit.carte in self.plateau.liste_cartes_prenables():
											
											if self.sprite_carte_j1_zoomer is None:
												
												sprit.zoomer(RATIO_ZOOM_CARTE, (self.largeur / 2, self.hauteur / 2))
												self.sprite_carte_j1_zoomer = sprit
												self.sprite_cartes_plateau.remove(self.sprite_carte_j1_zoomer)
												self.sprite_cartes_plateau.add(self.sprite_carte_j1_zoomer)
											
											else:
												if sprit == self.sprite_carte_j1_zoomer:
													
													sprit.dezoomer()
													self.sprite_carte_j1_zoomer = None
						
						bottomleft_x, bottomleft_y = self.rect_image_plateau.bottomleft
						
						if (clic_x < bottomleft_x and clic_y > bottomleft_y
							and self.plateau.joueur_qui_joue == self.plateau.joueur1):
							
							if self.sprite_carte_j1_zoomer is not None:
								
								if self.sprite_carte_j1_zoomer.carte in self.plateau.liste_cartes_prenables():
									
									self.sprite_carte_j1_zoomer.dezoomer()
									self.__dessiner_piocher(self.sprite_carte_j1_zoomer)
									self.sprite_cartes_plateau.remove(self.sprite_carte_j1_zoomer)
									self.plateau.joueur_qui_joue = self.plateau.adversaire()
									self.sprite_carte_j1_zoomer = None
						
						if self.rect_image_banque.collidepoint(clic_x, clic_y):
							
							if self.sprite_carte_j1_zoomer is not None:
								
								self.sprite_carte_j1_zoomer.dezoomer()
								self.__dessiner_defausser(self.sprite_carte_j1_zoomer)
								self.sprite_cartes_plateau.remove(self.sprite_carte_j1_zoomer)
								self.plateau.joueur_qui_joue = self.plateau.adversaire()
								self.sprite_carte_j1_zoomer = None
						
						if self.sprite_carte_j1_zoomer is None \
							and self.sprite_merveille_j1_zoomer is None \
							and self.choix_jeton:
							
							for jeton in self.jetons_progres_plateau:
								
								if jeton.rect.collidepoint(clic_x, clic_y):
									
									if isinstance(jeton, SpriteJetonsProgres):
										
										if self.sprite_jeton_j1_zoomer is None:
											
											jeton.zoomer(RATIO_ZOOM_CARTE, (self.largeur / 2, self.hauteur / 2))
											self.sprite_jeton_j1_zoomer = jeton
											self.jetons_progres_plateau.remove(self.sprite_jeton_j1_zoomer)
											self.jetons_progres_plateau.add(self.sprite_jeton_j1_zoomer)
										
										else:
											if jeton == self.sprite_jeton_j1_zoomer:
												
												if (clic_x < bottomleft_x and clic_y > bottomleft_y and
													self.plateau.joueur_qui_joue == self.plateau.joueur1):
													
													jeton.dezoomer()
													self.__deplacer_jeton_scientifique(jeton)
													self.choix_jeton = False
													self.sprite_jeton_j1_zoomer = None
							
						if self.sprite_jeton_j1_zoomer is None:
							
							for merveille in self.merveille_j1:
								
								if merveille.rect.collidepoint(clic_x, clic_y) \
									and isinstance(merveille, SpriteMerveille):
									
									if self.sprite_carte_j1_zoomer is None:
									
										if self.sprite_merveille_j1_zoomer is None:
											
											merveille.zoomer(RATIO_ZOOM_MERVEILLE, (self.largeur / 2, self.hauteur / 2))
											merveille.angle = 0
											merveille.pivoter()
											
											self.sprite_merveille_j1_zoomer = merveille
											self.merveille_j1.remove(self.sprite_merveille_j1_zoomer)
											self.merveille_j1.add(self.sprite_merveille_j1_zoomer)
											
										else:
											if merveille == self.sprite_merveille_j1_zoomer:
												
												merveille.dezoomer()
												merveille.angle = 90
												merveille.pivoter()
												self.sprite_merveille_j1_zoomer = None
												
									else:
										
										if merveille.rect.collidepoint(clic_x, clic_y) \
											and isinstance(merveille, SpriteMerveille):
											
											ret = self.plateau.construire_merveille(
												merveille.merveille,
											)
											
											if ret != -1:
												
												self.sprite_carte_j1_zoomer.dezoomer()
												self.__dessiner_merveille_sacrifier(merveille, self.sprite_carte_j1_zoomer)
												self.sprite_cartes_plateau.remove(self.sprite_carte_j1_zoomer)
												self.sprite_carte_j1_zoomer = None
												
				else:
					nbr_noeuds = 0
					_, carte_a_prendre, nbr_noeuds = alpha_beta(self.plateau, self.difficulte_profondeur,
						-math.inf, math.inf, True, nbr_noeuds)
					
					for sprite_carte in self.sprite_cartes_plateau:
						
						if isinstance(sprite_carte, SpriteCarte):
							
							if sprite_carte.carte == carte_a_prendre:
								
								if self.sprite_carte_j2_zoomer is None:
									
									sprite_carte.zoomer(RATIO_ZOOM_CARTE, (self.largeur / 2, self.hauteur / 2))
									self.sprite_carte_j2_zoomer = sprite_carte
									self.sprite_cartes_plateau.remove(self.sprite_carte_j2_zoomer)
									self.sprite_cartes_plateau.add(self.sprite_carte_j2_zoomer)
								
								else:
									
									if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
										
										clic_x, clic_y = event.pos
										
										if sprite_carte.rect.collidepoint(clic_x, clic_y):
										
											self.sprite_carte_j2_zoomer.dezoomer()
											self.sprite_carte_j2_zoomer = None
											self.__dessiner_piocher(sprite_carte)
											self.plateau.joueur_qui_joue = self.plateau.adversaire()
											
			# PARTIE Update
			if self.plateau.changement_age() == 1:
				self.__dessiner_carte()
			
			for group_sprit in self.sprite_j1:
				group_sprit.update()
			# TODO : superposition inversé avec j2
			for group_sprit in self.sprite_j2:
				group_sprit.update()
			
			self.merveille_j1.update()
			self.merveille_j2.update()
			
			self.sprite_jetons_militaire.update()
			
			self.jetons_progres_plateau.update()
			self.sprite_cartes_plateau.update()
			self.merveille_j1.update()
			self.merveille_j2.update()
			self.sprite_cartes_defaussees.update()
			
			# PARTIE Draw / render
			self.ecran.blit(self.image_fond, (0, 0))
			self.ecran.blit(
				self.image_plateau,
				self.rect_image_plateau.topleft
			)
			self.ecran.blit(
				self.image_banque,
				self.rect_image_banque.topleft
			)
			self.__dessiner_monnaies()
			
			for sprite_carte_j1 in self.sprite_j1:
				sprite_carte_j1.draw(self.ecran)
			for sprite_carte_j2 in self.sprite_j2:
				sprite_carte_j2.draw(self.ecran)
			
			self.merveille_j1.draw(self.ecran)
			self.merveille_j2.draw(self.ecran)
			
			pygame.draw.ellipse(self.ecran, (255, 0, 0), self.rect_jeton_conflit, 50)
			self.__deplacer_jeton_attaque()
			self.sprite_jetons_militaire.draw(self.ecran)
			
			if self.sprite_carte_j1_zoomer is not None:
				self.jetons_progres_plateau.draw(self.ecran)
				self.merveille_j1.draw(self.ecran)
				self.merveille_j2.draw(self.ecran)
				self.sprite_cartes_defaussees.draw(self.ecran)
				self.sprite_cartes_plateau.draw(self.ecran)
				
			elif self.sprite_merveille_j1_zoomer is not None:
				self.jetons_progres_plateau.draw(self.ecran)
				self.sprite_cartes_plateau.draw(self.ecran)
				self.merveille_j2.draw(self.ecran)
				self.sprite_cartes_defaussees.draw(self.ecran)
				self.merveille_j1.draw(self.ecran)
				
			elif self.sprite_jeton_j1_zoomer is not None:
				self.sprite_cartes_plateau.draw(self.ecran)
				self.merveille_j1.draw(self.ecran)
				self.merveille_j2.draw(self.ecran)
				self.sprite_cartes_defaussees.draw(self.ecran)
				self.jetons_progres_plateau.draw(self.ecran)
			
			else:
				self.jetons_progres_plateau.draw(self.ecran)
				self.sprite_cartes_plateau.draw(self.ecran)
				self.merveille_j1.draw(self.ecran)
				self.merveille_j2.draw(self.ecran)
				self.sprite_cartes_defaussees.draw(self.ecran)
				
			# after drawing everything, flip this display
			pygame.display.flip()


		format_texte = pygame.font.SysFont("arial", 70)
		tempo = self.plateau.joueur_gagnant.nom
		texte = ""
		if tempo == "joueur":
			texte = format_texte.render("VICTOIRE JOUEUR 1 ", True, (1, 159,255))
		elif tempo == "ordi":
			texte = format_texte.render("VICTOIRE JOUEUR 2 ", True, (1, 159,255))
		self.ecran.blit(texte, [100, 40])

		pygame.display.flip()
		continuer = True

		while continuer:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					continuer = False

		pygame.quit()
		