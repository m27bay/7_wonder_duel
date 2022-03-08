import pygame

from src.interface_graphique.src.m_test.Constantes import IMAGE_TEST


class SpriteCarte(pygame.sprite.Sprite):
	
	def __init__(self, x: int, y: int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(IMAGE_TEST).convert()
		larg, haut = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (larg*2/3, haut*2/3))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		
		