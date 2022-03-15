import pygame.sprite


class Element(pygame.sprite.Sprite):
	def __init__(self, haut_gauche_x: float, haut_gauche_y: float):
		pygame.sprite.Sprite.__init__(self)
		
		self.haut_gauche_x = haut_gauche_x
		self.haut_gauche_y = haut_gauche_y

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
		