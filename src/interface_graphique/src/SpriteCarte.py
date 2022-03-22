from typing import Any

import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES_CARTES
from src.interface_graphique.src.Element import Element
from src.utils.Carte import Carte



class SpriteCarte(Element):
	def __init__(self, carte: Carte, haut_gauche_x: float, haut_gauche_y: float, ration_longeur_fenetre: float):
		super().__init__(haut_gauche_x, haut_gauche_y)
		
		self.carte = carte
		
		self.ration_longeur_fenetre = ration_longeur_fenetre
		self.angle = 0
		
		self.chemin_image_recto = None
		self.chemin_image_verso = None
		self.image = None
		
		self.preparer_image()
	
	def modifier_taille_image(self):
		larg, haut = self.image.get_size()
		ration_image = haut / larg
		
		if self.largeur_zoom == 0:
			larg = larg * self.ration_longeur_fenetre
		else:
			larg = larg * self.largeur_zoom
		
		haut = ration_image * larg
		self.image = pygame.transform.scale(self.image, (larg, haut))
	
	def charger_image(self):
		self.chemin_image_recto = f"{DOSSIER_IMAGES_CARTES}{self.carte.nom}.jpg"
		if not self.carte.nom.__contains__("guilde"):
			self.chemin_image_verso = f"{DOSSIER_IMAGES_CARTES}recto age {self.carte.age}.jpg"
		else:
			self.chemin_image_verso = f"{DOSSIER_IMAGES_CARTES}recto guilde.jpg"
		
		if not self.carte.est_face_cachee:
			self.image = pygame.image.load(self.chemin_image_recto).convert()
		else:
			self.image = pygame.image.load(self.chemin_image_verso).convert()
			
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
			
			