from typing import Any

import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES_CARTES
from src.utils.Carte import Carte



class SpriteCarte(pygame.sprite.Sprite):
	def __init__(self, carte: Carte, haut_gauche_x: float, haut_gauche_y: float, ration_longeur_fenetre: float):
		pygame.sprite.Sprite.__init__(self)
		
		self.carte = carte
		
		self.cheminImageRecto = f"{DOSSIER_IMAGES_CARTES}{carte.nom}.jpg"
		if not carte.nom.__contains__("guilde"):
			self.cheminImageVeso = f"{DOSSIER_IMAGES_CARTES}recto age {self.carte.age}.jpg"
		else:
			self.cheminImageVeso = f"{DOSSIER_IMAGES_CARTES}recto guilde.jpg"
			
		if not carte.est_face_cachee:
			self.image = pygame.image.load(self.cheminImageRecto).convert()
		else:
			self.image = pygame.image.load(self.cheminImageVeso).convert()
		larg, haut = self.image.get_size()
		ration_image = haut / larg
		larg = larg * ration_longeur_fenetre
		haut = ration_image * larg
		self.image = pygame.transform.scale(self.image, (larg, haut))
		
		self.rect = self.image.get_rect()
		self.rect.topleft = (haut_gauche_x, haut_gauche_y)
		
		self.nouv_coords = None
		
	def pivoter(self, angle):
		self.image = pygame.transform.rotate(self.image, angle)
		self.rect = self.image.get_rect(center=self.rect.center)
		
	def deplacer(self, dx: int, dy: int):
		self.nouv_coords = (dx, dy)
	
	def update(self, *args: Any, **kwargs: Any) -> None:
		if self.nouv_coords is not None:
			self.rect.topleft = self.nouv_coords
			self.nouv_coords = None
		
			