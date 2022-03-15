import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES
from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille
from src.utils.Plateau import Plateau

RATIO_IMAGE = 0.2
RATIO_PLATEAU = 0.55
RATIO_ZOOM = 1.20

class Fenetre:
	def __init__(self, titre: str, plateau: Plateau):
		pygame.init()
		
		self.plateau = plateau
		
		self.ecran = pygame.display.set_mode()
		self.largeur, self.hauteur = self.ecran.get_size()
		
		pygame.display.set_caption(titre)
		
		default_sprite_image = SpriteCarte(Carte("academie", None, None, None, None, 3), 0, 0, RATIO_IMAGE)
		self.default_hauteur_sprite = default_sprite_image.rect.height
		self.default_largeur_spirte = default_sprite_image.rect.width
		
		self.cartes_plateau = pygame.sprite.Group()
		
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
		
		self.sprite_zoomer = None
		
		self.espace_entre_carte = self.largeur * 0.005
		self.__dessiner_carte()
		
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
		
	def __dessiner_carte_age_I(self):
		origine_cartes = self.largeur / 2 - self.default_largeur_spirte - self.espace_entre_carte / 2
		
		haut_gauche_x = origine_cartes
		haut_gauche_y = self.hauteur * 1 / 3
		
		for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
			for num_colone, carte in enumerate(ligne_cartes):
				
				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.cartes_plateau.add(sprite_carte)
					
					# coords carte suivante
					haut_gauche_x += self.default_largeur_spirte + self.espace_entre_carte
			
			# coords changement ligne
			haut_gauche_x = origine_cartes - (num_ligne + 1) * self.default_largeur_spirte / 2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite / 2
	
	def __dessiner_carte_age_II(self):
		origine_cartes = self.largeur / 2 - 3 * self.default_largeur_spirte - self.espace_entre_carte / 2
		
		haut_gauche_x = origine_cartes
		haut_gauche_y = self.hauteur * 1 / 3
		
		for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
			for num_colone, carte in enumerate(ligne_cartes):
				
				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.cartes_plateau.add(sprite_carte)
					
					# coords carte suivante
					haut_gauche_x += self.default_largeur_spirte + self.espace_entre_carte
			
			# coords changement ligne
			haut_gauche_x = origine_cartes + (num_ligne+1) * self.default_largeur_spirte/2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite/2
			
	def __dessiner_carte_age_III(self):
		origine_cartes = self.largeur / 2 - self.default_largeur_spirte - self.espace_entre_carte / 2
		
		haut_gauche_x = origine_cartes
		haut_gauche_y = self.hauteur * 1 / 3

		for num_ligne in range(3):
			ligne_cartes = self.plateau.cartes_plateau[num_ligne]
			for num_colone in range(len(ligne_cartes)):
				carte = ligne_cartes[num_colone]

				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.cartes_plateau.add(sprite_carte)

					# coords carte suivante
					haut_gauche_x += self.default_largeur_spirte + self.espace_entre_carte

			# coords changement ligne
			haut_gauche_x = origine_cartes - (num_ligne + 1) * self.default_largeur_spirte / 2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite / 2
			
		#
		haut_gauche_x = origine_cartes - self.default_largeur_spirte/2
		carte = self.plateau.cartes_plateau[3][1]
		self.cartes_plateau.add(SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE))
		
		#
		haut_gauche_x = origine_cartes + self.default_largeur_spirte + self.default_largeur_spirte / 2
		carte = self.plateau.cartes_plateau[3][5]
		self.cartes_plateau.add(SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE))
		haut_gauche_y += self.default_hauteur_sprite/2
		
		#
		haut_gauche_x = origine_cartes - self.default_largeur_spirte - self.espace_entre_carte
		for num_ligne in range(4, len(self.plateau.cartes_plateau)):
			ligne_cartes = self.plateau.cartes_plateau[num_ligne]
			for num_colone in range(len(ligne_cartes)):
				carte = ligne_cartes[num_colone]

				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
					self.cartes_plateau.add(sprite_carte)

					# coords carte suivante
					haut_gauche_x += self.default_largeur_spirte + self.espace_entre_carte

			# coords changement ligne
			haut_gauche_x = origine_cartes - self.default_largeur_spirte + \
							(num_ligne - 4 + 1) * self.default_largeur_spirte / 2 - self.espace_entre_carte
			haut_gauche_y += self.default_hauteur_sprite/2
	
	def __dessiner_carte(self):
		if self.plateau.age == 1:
			self.__dessiner_carte_age_I()
		elif self.plateau.age == 2:
			self.__dessiner_carte_age_II()
		else:
			self.__dessiner_carte_age_III()
			
	def __position_type_carte(self, carte: Carte):
		if not isinstance(carte, CarteFille):
			liste_couleur = ["marron", "grise", "bleu", "vert", "jaune", "rouge"]
			if carte.couleur in liste_couleur:
				return liste_couleur.index(carte.couleur)
		else:
			if carte.nom.__contains__("guilde"):
				return 6
			
	def __piocher_carte(self, sprite_carte: SpriteCarte):
		self.cartes_plateau.remove(sprite_carte)
		type_carte = self.__position_type_carte(sprite_carte.carte)
		
		sprite_carte.angle = 90
		coord_x = self.rect_image_plateau.x
		
		if self.plateau.joueur_qui_joue == self.plateau.joueur1:
			sprite_joueur_qui_joue = self.sprite_j1
			sprite_carte.angle = -sprite_carte.angle
			coord_x -= self.default_hauteur_sprite
			decalage_x = -(len(sprite_joueur_qui_joue[type_carte]) * (self.default_hauteur_sprite / 3))
		else:
			sprite_joueur_qui_joue = self.sprite_j2
			coord_x += + self.rect_image_plateau.width
			decalage_x = len(sprite_joueur_qui_joue[type_carte]) * (self.default_hauteur_sprite / 3)
		
		if type_carte == 0:
			coord_y = self.rect_image_plateau.height + type_carte * self.default_largeur_spirte
		else:
			coord_y = self.rect_image_plateau.height + type_carte * (
					self.default_largeur_spirte + self.espace_entre_carte)
		
		sprite_joueur_qui_joue[type_carte].add(sprite_carte)
		self.plateau.enlever_carte(sprite_carte.carte)
		
		sprite_carte.pivoter()
		
		sprite_carte.changer_coords(coord_x + decalage_x, coord_y)
		
	def boucle_principale(self):
		en_cours = True
		while en_cours:
			# PARTIE Process input (events)
			for event in pygame.event.get():
				
				# quitter avec la croix
				if event.type == pygame.QUIT:
					en_cours = False
					
				# quitter avec la touche echap
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						en_cours = False
					
				if event.type == pygame.MOUSEBUTTONDOWN:
					
					for sprit in self.cartes_plateau:
						clic_x, clic_y = event.pos
						if sprit.rect.collidepoint(clic_x, clic_y):
							
							# système de zoom avec le clic droit
							if event.button == 3:
								if isinstance(sprit, SpriteCarte):
									if sprit.carte in self.plateau.liste_cartes_prenables():
										
										if self.sprite_zoomer is None:
											sprit.zoomer(RATIO_ZOOM, (self.largeur/2, self.hauteur/2))
											self.sprite_zoomer = sprit
											
										else:
											if sprit == self.sprite_zoomer:
												sprit.dezoomer()
												self.sprite_zoomer = None
							
							# piocher carte/ merveille ou défauffer avec clic gauche
							elif event.button == 1:
								if isinstance(sprit, SpriteCarte):
									if self.sprite_zoomer is None:
										if sprit.carte in self.plateau.liste_cartes_prenables():
											
											self.__piocher_carte(sprit)
		
											for carte in self.plateau.liste_cartes_prenables():
												carte.est_face_cachee = False
		
											self.plateau.joueur_qui_joue = self.plateau.obtenir_adversaire()
								
			# PARTIE Update
			self.cartes_plateau.update()
			for group_sprit in self.sprite_j1:
				group_sprit.update()
			for group_sprit in self.sprite_j2:
				group_sprit.update()
				
			# PARTIE Draw / render
			self.ecran.blit(self.image_fond, (0, 0))
			self.ecran.blit(
				self.image_plateau,
				(self.largeur / 2 - self.image_plateau.get_width() / 2,
				2 * self.espace_entre_carte)
			)
			self.rect_image_plateau.topleft = (
				(self.largeur / 2 - self.image_plateau.get_width() / 2,
				2 * self.espace_entre_carte)
			)
			
			self.cartes_plateau.draw(self.ecran)
			for group_sprit in self.sprite_j1:
				group_sprit.draw(self.ecran)
			for group_sprit in self.sprite_j2:
				group_sprit.draw(self.ecran)
			
			# pygame.draw.line(self.ecran, (255, 0, 0), (self.largeur/2, 0), (self.largeur/2, self.hauteur))
			# pygame.draw.line(self.ecran, (255, 0, 0), self.rect_image_plateau.topleft,
			# 	self.rect_image_plateau.bottomleft)
			
			# after drawing everything, flip this display
			pygame.display.flip()
		
		pygame.quit()
		