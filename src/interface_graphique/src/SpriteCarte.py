from typing import Any

import pygame

from src.utils.Carte import Carte

cheminDossierImage = "../ressources/images/cartes/"
RATION_CARTE = 1/5

class SpriteCarte(pygame.sprite.Sprite):
	def __init__(self, carte: Carte, haut_gauche_x: int, haut_gauche_y: int):
		pygame.sprite.Sprite.__init__(self)
		
		self.carte = carte
		
		self.cheminImageRecto = f"{cheminDossierImage}{carte.nom}.jpg"
		if not carte.nom.__contains__("guilde"):
			self.cheminImageVeso = f"{cheminDossierImage}recto age {self.carte.age}.jpg"
		else:
			self.cheminImageVeso = f"{cheminDossierImage}recto guilde.jpg"
			
		if not carte.est_face_cachee:
			self.image = pygame.image.load(self.cheminImageRecto).convert()
		else:
			self.image = pygame.image.load(self.cheminImageVeso).convert()
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
		
			