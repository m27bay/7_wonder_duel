import pygame

from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.utils.Carte import Carte
from src.utils.Plateau import Plateau

FOND = "../ressources/images/fond_jeux.jpg"

class Fenetre:
	def __init__(self, titre: str, plateau: Plateau):
		pygame.init()
		
		self.plateau = plateau
		
		self.ecran = pygame.display.set_mode()
		self.largeur, self.hauteur = self.ecran.get_size()
		
		pygame.display.set_caption(titre)
		
		self.sprites = pygame.sprite.Group()
		self.dessiner_carte()
		
		image_fond = pygame.image.load(FOND).convert()
		self.image_fond = pygame.transform.scale(image_fond, (self.largeur, self.hauteur))
		
	def __dessiner_carte_age_I(self):
		sprite_carte = SpriteCarte(Carte("academie", None, None, None, None, 3), 0, 0)
		hauteur_sprite = sprite_carte.rect.height
		largeur_spirte = sprite_carte.rect.width
		
		origine_cartes = self.largeur / 2 - largeur_spirte
		
		haut_gauche_x = origine_cartes
		haut_gauche_y = 0
		
		for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
			for num_colone, carte in enumerate(ligne_cartes):
				
				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y)
					self.sprites.add(sprite_carte)
					
					# coords carte suivante
					haut_gauche_x += largeur_spirte
			
			# coords changement ligne
			haut_gauche_x = origine_cartes - (num_ligne+1) * largeur_spirte/2
			haut_gauche_y += hauteur_sprite/2
	
	def __dessiner_carte_age_II(self):
		sprite_carte = SpriteCarte(Carte("academie", None, None, None, None, 3), 0, 0)
		hauteur_sprite = sprite_carte.rect.height
		largeur_spirte = sprite_carte.rect.width
		
		origine_cartes = self.largeur/2 - 3*largeur_spirte
		
		haut_gauche_x = origine_cartes
		haut_gauche_y = 0
		
		for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
			for num_colone, carte in enumerate(ligne_cartes):
				
				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y)
					self.sprites.add(sprite_carte)
					
					# coords carte suivante
					haut_gauche_x += largeur_spirte
			
			# coords changement ligne
			haut_gauche_x = origine_cartes + (num_ligne+1) * largeur_spirte/2
			haut_gauche_y += hauteur_sprite/2
			
	def __dessiner_carte_age_III(self):
		sprite_carte = SpriteCarte(Carte("academie", None, None, None, None, 3), 0, 0)
		hauteur_sprite = sprite_carte.rect.height
		largeur_spirte = sprite_carte.rect.width
		
		origine_cartes = self.largeur / 2 - largeur_spirte
		
		haut_gauche_x = origine_cartes
		haut_gauche_y = 0

		for num_ligne in range(3):
			ligne_cartes = self.plateau.cartes_plateau[num_ligne]
			for num_colone in range(len(ligne_cartes)):
				carte = ligne_cartes[num_colone]

				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y)
					self.sprites.add(sprite_carte)

					# coords carte suivante
					haut_gauche_x += largeur_spirte

			# coords changement ligne
			haut_gauche_x = origine_cartes - (num_ligne+1) * largeur_spirte/2
			haut_gauche_y += hauteur_sprite/2
			
		#
		haut_gauche_x = origine_cartes - largeur_spirte/2
		carte = self.plateau.cartes_plateau[3][1]
		self.sprites.add(SpriteCarte(carte, haut_gauche_x, haut_gauche_y))
		
		#
		haut_gauche_x = origine_cartes + largeur_spirte + largeur_spirte / 2
		carte = self.plateau.cartes_plateau[3][5]
		self.sprites.add(SpriteCarte(carte, haut_gauche_x, haut_gauche_y))
		haut_gauche_y += hauteur_sprite/2
		
		#
		haut_gauche_x = origine_cartes - largeur_spirte
		for num_ligne in range(4, len(self.plateau.cartes_plateau)):
			ligne_cartes = self.plateau.cartes_plateau[num_ligne]
			for num_colone in range(len(ligne_cartes)):
				carte = ligne_cartes[num_colone]

				if carte != 0:
					# dessin
					sprite_carte = SpriteCarte(carte, haut_gauche_x, haut_gauche_y)
					self.sprites.add(sprite_carte)

					# coords carte suivante
					haut_gauche_x += largeur_spirte

			# coords changement ligne
			haut_gauche_x = origine_cartes - largeur_spirte + (num_ligne-4+1) * largeur_spirte / 2
			haut_gauche_y += hauteur_sprite/2
		
	
	def dessiner_carte(self):
		if self.plateau.age == 1:
			self.__dessiner_carte_age_I()
		elif self.plateau.age == 2:
			self.__dessiner_carte_age_II()
		else:
			self.__dessiner_carte_age_III()
			
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
					if event.button == 1:
						for sprit in self.sprites:
							clic_x, clic_y = event.pos
							if sprit.rect.collidepoint(clic_x, clic_y):
								if isinstance(sprit, SpriteCarte):
									sprit.deplacer(0, 0)
			
			# PARTIE Update
			self.sprites.update()
			
			# PARTIE Draw / render
			self.ecran.blit(self.image_fond, (0, 0))
			self.sprites.draw(self.ecran)
			
			# after drawing everything, flip this display
			pygame.display.flip()
		
		pygame.quit()
		