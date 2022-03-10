from typing import Any

import pygame

from src.interface_graphique.src.Constantes import IMAGE_TEST, RATION_CARTE, IMAGE_TEST_CACHEE


class SpriteCarte(pygame.sprite.Sprite):
	
	def __init__(self, haut_gauche_x: int, haut_gauche_y: int, face_cachee: bool):
		pygame.sprite.Sprite.__init__(self)
		
		if face_cachee:
			chemin_img = IMAGE_TEST_CACHEE
		else:
			chemin_img = IMAGE_TEST
		self.image = pygame.image.load(chemin_img).convert()
		larg, haut = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (larg*RATION_CARTE, haut*RATION_CARTE))
		
		self.rect = self.image.get_rect()
		self.rect.topleft = (haut_gauche_x, haut_gauche_y)
		
		self.nouv_coords = None
		
	def deplacer(self, dx: int, dy: int):
		self.nouv_coords = (dx, dy)
	
	def update(self, *args: Any, **kwargs: Any) -> None:
		if self.nouv_coords is not None:
			self.rect.topleft = self.nouv_coords
			self.nouv_coords = None
		
			