import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES_CARTES
from src.interface_graphique.src.MonSprite import MonSprite
from src.utils.Carte import Carte


class SpriteCarte(MonSprite):
	def __init__(self, carte: Carte, haut_gauche_x: float, haut_gauche_y: float, ration_longeur_fenetre: float):
		super().__init__(haut_gauche_x, haut_gauche_y, ration_longeur_fenetre)
		
		self.carte = carte
		
		self.chemin_image_recto = None
		self.chemin_image_verso = None
		self.image = None
		
		self.preparer_image()
	
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
		