from typing import Any

import pygame.sprite


class MonSprite(pygame.sprite.Sprite):
	def __init__(self, haut_gauche_x: float, haut_gauche_y: float, ration_longeur_fenetre: float):
		pygame.sprite.Sprite.__init__(self)
		
		self.haut_gauche_x = haut_gauche_x
		self.haut_gauche_y = haut_gauche_y
		
		self.ration_longeur_fenetre = ration_longeur_fenetre
		
		self.angle = 0
		self.largeur_zoom = 0
		self.coord_milieu_fen = None
		
	def changer_coords(self, nouv_x: int, nouv_y: int):
		self.haut_gauche_x = nouv_x
		self.haut_gauche_y = nouv_y
		
	def zoomer(self, largeur_zoom: float, coord_milieu_fen):
		self.largeur_zoom = largeur_zoom
		self.coord_milieu_fen = coord_milieu_fen

	def dezoomer(self):
		self.largeur_zoom = 0
		self.coord_milieu_fen = None
	
	def charger_image(self):
		pass
	
	def modifier_taille_image(self):
		larg, haut = self.image.get_size()
		ration_image = haut / larg
		
		if self.largeur_zoom == 0:
			larg *= int(self.ration_longeur_fenetre)
		else:
			larg *= int(self.largeur_zoom)
		
		haut = ration_image * larg
		self.image = pygame.transform.scale(self.image, (larg, haut))
	
	def deplacer_image(self):
		self.rect = self.image.get_rect()
		
		if self.largeur_zoom == 0:
			self.rect.topleft = (self.haut_gauche_x, self.haut_gauche_y)
		else:
			self.rect.center = self.coord_milieu_fen
	
	def preparer_image(self):
		self.charger_image()
		self.modifier_taille_image()
		self.deplacer_image()
	
	def pivoter(self):
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(topleft=self.rect.bottomleft)
	
	def update(self, *args: Any, **kwargs: Any) -> None:
		self.preparer_image()
		
		if self.angle != 0:
			self.pivoter()
		