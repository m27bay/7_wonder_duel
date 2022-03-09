import pygame

from src.interface_graphique.src.m_test.Constantes import FOND, FEN_LARGEUR, FEN_HAUTEUR
from src.interface_graphique.src.m_test.SpriteCarte import SpriteCarte


class Fenetre:
	def __init__(self, titre: str):
		pygame.init()
		
		self.largeur, self.hauteur = FEN_LARGEUR, FEN_HAUTEUR
		self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
		
		pygame.display.set_caption(titre)
		
		self.sprites = pygame.sprite.Group()
		self.dessiner_carte()
		
		image_fond = pygame.image.load(FOND).convert()
		self.image_fond = pygame.transform.scale(image_fond, (self.largeur, self.hauteur))
	
	def __dessiner_carte_age_I(self):
		sprite_carte = SpriteCarte(0, 0, False)
		hauteur_sprite = sprite_carte.rect.height
		largeur_spirte = sprite_carte.rect.width
		
		origine_cartes = self.largeur/2 - 3*largeur_spirte
		
		nombre_carte_par_ligne_max = 6
		
		for num_ligne in range(5):
			
			haut_gauche_x = num_ligne * (largeur_spirte / 2) + origine_cartes
			haut_gauche_y = num_ligne * (hauteur_sprite / 2)
			
			for nombre_carte_par_ligne in range(nombre_carte_par_ligne_max):
				
				# dessin
				if num_ligne % 2 == 0:
					self.sprites.add(SpriteCarte(haut_gauche_x, haut_gauche_y, False))
				else:
					self.sprites.add(SpriteCarte(haut_gauche_x, haut_gauche_y, True))
				
				# calcul coords
				haut_gauche_x += largeur_spirte
			nombre_carte_par_ligne_max -= 1
			
	
	def dessiner_carte(self):
		self.__dessiner_carte_age_I()
	
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
		