import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES_JETONS_MILITAIRE
from src.interface_graphique.src.MonSprite import MonSprite
from src.utils.JetonMilitaire import JetonMilitaire


class SpriteJetonsMilitaire(MonSprite):
	def __init__(self, jeton: JetonMilitaire, haut_gauche_x: float, haut_gauche_y: float, ration_longeur_fenetre: float):
		super().__init__(haut_gauche_x, haut_gauche_y, ration_longeur_fenetre)
		
		self.jeton = jeton
		
		self.chemin_image = None
		self.image = None
		
		self.preparer_image()
	
	def charger_image(self):
		self.chemin_image = f"{DOSSIER_IMAGES_JETONS_MILITAIRE}{self.jeton.nom[0:len(self.jeton.nom)-2]}.jpg"
		self.image = pygame.image.load(self.chemin_image).convert()
		