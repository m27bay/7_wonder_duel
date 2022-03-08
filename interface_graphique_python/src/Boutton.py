import pygame


class Button:

    def __init__(self, image, nouv_image, coordone_x, coordone_y, largeur, longueur):
        self.point_x = coordone_x
        self.point_y = coordone_y

        self.reactangle = pygame.Rect(coordone_x, coordone_y, largeur, longueur)

        self.chargement_image = pygame.image.load(image)
        self.image_affiche = pygame.transform.scale(self.chargement_image, (int(largeur), int(longueur)))

        self.nouv_chargement_image = pygame.image.load(nouv_image)
        self.nouv_image_affiche = pygame.transform.scale(self.nouv_chargement_image, (int(largeur), int(longueur)))

    def affichage_du_bouton(self, fenetre):
        fenetre.blit(self.image_affiche, (self.point_x, self.point_y))

    def affichage_nouveau_bouton(self, fenetre):

        fenetre.blit(self.nouv_image_affiche, (self.point_x, self.point_y))

    def detection_bouton(self, fenetre, position_sourris):
        detection = self.reactangle.collidepoint(position_sourris)

        if detection:
            self.affichage_nouveau_bouton(fenetre)
        else:
            self.affichage_du_bouton(fenetre)