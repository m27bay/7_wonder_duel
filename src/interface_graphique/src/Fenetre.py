import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES
from src.interface_graphique.src.MonSprite import MonSprite
from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.interface_graphique.src.SpriteJetonsProgres import SpriteJetonsProgres
from src.interface_graphique.src.SpriteMerveille import SpriteMerveille
from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres
from src.utils.Plateau import Plateau


RATION_FEN = 0
RATIO_IMAGE = 0.16
RATIO_MERVEILLE = 0.10
RATIO_JETONS_PROGRES = 0.15

RATIO_PLATEAU = 0.50
RATION_BANQUE = 0.05
RATIO_ZOOM = 0.90

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
		
		default_sprite_merveille = SpriteMerveille(CarteFille("piree", None, None), 0, 0, RATIO_MERVEILLE)
		self.default_hauteur_merveille = default_sprite_merveille.rect.height
		self.default_largeur_merveille = default_sprite_merveille.rect.width
		
		default_sprite_jetons_progres = SpriteJetonsProgres(JetonProgres("agriculture", None), 0, 0, RATIO_JETONS_PROGRES)
		self.default_hauteur_jetons_progres = default_sprite_jetons_progres.rect.height
		self.default_largeur_jetons_progres = default_sprite_jetons_progres.rect.width
		
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
		larg_banque = RATION_BANQUE * self.largeur
		haut_banque = ration_banque * larg_banque
		self.image_banque = pygame.transform.scale(image_banque, (larg_banque, haut_banque))
		self.rect_image_banque = self.image_banque.get_rect()
		self.rect_image_banque.topleft = (
			(self.largeur / 2 - self.image_banque.get_width() / 2,
			self.hauteur - 2 * self.espace_entre_carte - self.image_banque.get_height())
		)
		
		self.__dessiner_carte()
		
		self.double_clic = False
		
		self.merverille_j1 = pygame.sprite.Group()
		self.merverille_j2 = pygame.sprite.Group()
		self.__dessiner_merveille()
		
		self.jetons_progres_plateau = pygame.sprite.Group()
		
		self.__dessiner_jetons_scientifiques()
		
	def __dessiner_carte_age_I(self):
		origine_cartes = self.largeur / 2 - self.default_largeur_spirte - self.espace_entre_carte / 2
		
		haut_gauche_x = origine_cartes
		_, haut_gauche_y = self.rect_image_plateau.bottomright
		haut_gauche_y += self.espace_entre_carte
		
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
		_, haut_gauche_y = self.rect_image_plateau.bottomright
		haut_gauche_y += self.espace_entre_carte
		
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
		_, haut_gauche_y = self.rect_image_plateau.bottomright
		haut_gauche_y += self.espace_entre_carte

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
			
	def __dessiner_merveille(self):
		compteur = 0
		for merveille in self.plateau.joueur1.merveilles:
			coord_x, coord_y = self.rect_image_plateau.bottomleft
			coord_x += self.espace_entre_carte
			
			coord_y += compteur * (self.default_largeur_merveille + self.espace_entre_carte)
			coord_y += compteur * (self.default_hauteur_sprite / 4)
			
			merveille_sprite = SpriteMerveille(merveille, coord_x, coord_y, RATIO_MERVEILLE)
			merveille_sprite.angle = -90
			self.merverille_j1.add(merveille_sprite)
			
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
			self.merverille_j2.add(sprite_merveille)
			
			compteur += 1
			
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
	
	def __position_type_carte(self, carte: Carte):
		if not isinstance(carte, CarteFille):
			liste_couleur = ["marron", "gris", "bleu", "vert", "jaune", "rouge"]
			if carte.couleur in liste_couleur:
				return liste_couleur.index(carte.couleur)
		else:
			if carte.nom.__contains__("guilde"):
				return 6
			
	def __piocher_carte(self, sprite_carte: SpriteCarte):
		self.cartes_plateau.remove(sprite_carte)
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
			coord_y = type_carte * self.default_largeur_spirte
		else:
			coord_y = type_carte * (
					self.default_largeur_spirte + self.espace_entre_carte)
			
		coord_y -= self.rect_image_plateau.height*1/4
		coord_y += self.default_largeur_spirte
		coord_x += decalage_x
			
		sprite_joueur_qui_joue[type_carte].add(sprite_carte)
		self.plateau.enlever_carte(sprite_carte.carte)
		
		sprite_carte.changer_coords(coord_x, coord_y)
		
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
							
							# clic droit
							if event.button == 3:
								if isinstance(sprit, SpriteCarte):
									if sprit.carte in self.plateau.liste_cartes_prenables():
										
										if self.sprite_zoomer is None:
											sprit.zoomer(RATIO_ZOOM, (self.largeur/2, self.hauteur/2))
											self.sprite_zoomer = sprit
											self.cartes_plateau.remove(self.sprite_zoomer)
											self.cartes_plateau.add(self.sprite_zoomer)
											
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
			if len(self.cartes_plateau) == 0 and self.plateau.age != 3:
				self.plateau.age += 1
				self.plateau.preparation_cartes()
				self.__dessiner_carte()
				
			self.cartes_plateau.update()
			for group_sprit in self.sprite_j1:
				group_sprit.update()
			for group_sprit in self.sprite_j2:
				group_sprit.update()
			self.merverille_j1.update()
			self.merverille_j2.update()
			self.jetons_progres_plateau.update()
				
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
			
			self.cartes_plateau.draw(self.ecran)
			for group_sprit in self.sprite_j1:
				group_sprit.draw(self.ecran)
			for group_sprit in self.sprite_j2:
				group_sprit.draw(self.ecran)
			self.merverille_j1.draw(self.ecran)
			self.merverille_j2.draw(self.ecran)
			self.jetons_progres_plateau.draw(self.ecran)
			
			# OUTIL DEBUG #
			# pygame.draw.line(self.ecran, (255, 0, 0), (self.largeur/2, 0), (self.largeur/2, self.hauteur))
			pygame.draw.line(self.ecran, (255, 0, 0), self.rect_image_plateau.topleft,
				self.rect_image_plateau.bottomleft)
			pygame.draw.line(self.ecran, (255, 0, 0), self.rect_image_plateau.topright,
				self.rect_image_plateau.bottomright)
			pygame.draw.line(self.ecran, (255, 0, 0), self.rect_image_plateau.bottomright,
				self.rect_image_plateau.bottomleft)
			
			x, y = self.rect_image_plateau.topleft
			x += 1 / 4 * self.rect_image_plateau.width
			_, y2 = self.rect_image_plateau.bottomleft
			pygame.draw.line(self.ecran, (255, 0, 0), (x, y), (x, y2))
			
			# after drawing everything, flip this display
			pygame.display.flip()
		
		pygame.quit()
		