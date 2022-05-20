import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES_MERVEILLES
from src.interface_graphique.src.MonSprite import MonSprite
from src.utils.Merveille import Merveille


class SpriteMerveille(MonSprite):
    def __init__(self, merveille: Merveille, haut_gauche_x: float, haut_gauche_y: float, ration_longeur_fenetre: float):
        super().__init__(haut_gauche_x, haut_gauche_y, ration_longeur_fenetre)

        self.merveille = merveille

        self.chemin_image = None
        self.image = None
        self.est_construite = False

        self.preparer_image()

    def charger_image(self):
        self.chemin_image = f"{DOSSIER_IMAGES_MERVEILLES}{self.merveille.nom}.jpg"
        self.image = pygame.image.load(self.chemin_image).convert()

    def pivoter(self):
        super(SpriteMerveille, self).pivoter()
        x, nouv_y = self.rect.topleft
        nouv_y -= self.rect.width
        self.rect.topleft = x, nouv_y
