import pygame

from src.interface_graphique.src.m_test.Constantes import VERT


class SpriteCarte(pygame.sprite.Sprite):
	"""
	Documentation
	"""
	
	def __init__(self, x: int, y: int):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((50, 50))
		self.image.fill(VERT)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		