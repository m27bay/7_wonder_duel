import pygame

from src.interface_graphique.src.m_test.Constantes import FOND


class Fenetre:
	def __init__(self, titre: str):
		pygame.init()
		self.largeur, self.hauteur = 1024, 512
		self.ecran = pygame.display.set_mode((self.largeur, self.hauteur))
		pygame.display.set_caption(titre)
		# self.horloge = pygame.time.Clock()
		# self.sprites = pygame.sprite.Group()
		
		image_fond = pygame.image.load(FOND).convert()
		self.image_fond = pygame.transform.scale(image_fond, (self.largeur, self.hauteur))
		
	def boucle_principale(self):
		en_cours = True
		while en_cours:
			# PARTIE Process input (events)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					en_cours = False
			
			# PARTIE Update
			# self.sprites.update()
			
			# PARTIE Draw / render
			self.ecran.blit(self.image_fond, (0, 0))
			# self.sprites.draw(self.ecran)
			
			# after drawing everything, flip this display
			pygame.display.flip()
			
		pygame.quit()
		