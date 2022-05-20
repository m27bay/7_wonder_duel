import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES_JETONS_PROGRES
from src.interface_graphique.src.MonSprite import MonSprite
from src.utils.JetonProgres import JetonProgres


class SpriteJetonsProgres(MonSprite):
    def __init__(self, jeton: JetonProgres, haut_gauche_x: float, haut_gauche_y: float,
                 ration_longeur_fenetre: float):
        super().__init__(haut_gauche_x, haut_gauche_y, ration_longeur_fenetre)

        self.jeton = jeton

        self.chemin_image = None
        self.image = None

        self.preparer_image()

    def charger_image(self):
        self.chemin_image = f"{DOSSIER_IMAGES_JETONS_PROGRES}{self.jeton.nom}.xcf"
        self.image = pygame.image.load(self.chemin_image).convert_alpha()
