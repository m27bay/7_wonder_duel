import math
import random
import time

import pygame

from src.interface_graphique.src.Constantes import DOSSIER_IMAGES
from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.interface_graphique.src.SpriteJetonsMilitaire import SpriteJetonsMilitaire
from src.interface_graphique.src.SpriteJetonsProgres import SpriteJetonsProgres
from src.interface_graphique.src.SpriteMerveille import SpriteMerveille
from src.utils.Carte import Carte
from src.utils.CarteGuilde import CarteGuilde
from src.utils.Colours import Couleurs
from src.utils.Merveille import Merveille
from src.utils.JetonProgres import JetonProgres
from src.utils.Plateau import Plateau
from src.utils.Stategie import alpha_beta, alpha_beta_avec_merveille

RATIO_IMAGE = 0.15
RATIO_MERVEILLE = 0.10
RATIO_JETONS_PROGRES = 0.155
RATIO_JETONS_MILITAIRE2 = 0.18
RATIO_JETONS_MILITAIRE5 = 0.16
RATIO_MONNAIES_6 = 0.16
RATIO_MONNAIES_3 = 0.18
RATIO_MONNAIES_1 = 0.16

RATIO_PLATEAU = 0.50
RATIO_BANQUE = 0.05
RATIO_ZOOM_CARTE = 0.65
RATIO_ZOOM_MERVEILLE = 0.45
RATIO_ZOOM_JETONS_SCIENTIFIQUES = 0.60


def print_sprite_group(sprite_groupe):
    if len(sprite_groupe) == 0:
        print("groupe vide", end=", ")
    for sprite in sprite_groupe:
        if isinstance(sprite, SpriteCarte):
            print(sprite.carte.nom, end=", ")
        else:
            print("sprite n'est pas une carte")


def print_sprite_mega_group(sprite_groupe):
    for num, groupe in enumerate(sprite_groupe):
        print(f"groupe n° {num}", end=": ")
        print_sprite_group(groupe)
        print()


class Fenetre:
    def __init__(self, titre: str, plateau: Plateau, difficulte_profondeur, mode_1_vs_1: bool = False):
        pygame.init()

        self.plateau = plateau
        self.difficulte_profondeur = difficulte_profondeur
        self.mode_1_vs_1 = mode_1_vs_1

        self.ecran = pygame.display.set_mode((1536, 864))
        self.largeur, self.hauteur = self.ecran.get_size()

        pygame.display.set_caption(titre)

        default_sprite_image = SpriteCarte(
            Carte("academie", None, None, None, None, 3), 0, 0, RATIO_IMAGE)
        self.default_hauteur_sprite = default_sprite_image.rect.height
        self.default_largeur_sprite = default_sprite_image.rect.width

        default_sprite_merveille = SpriteMerveille(
            Merveille("piree", None, None), 0, 0, RATIO_MERVEILLE)
        self.default_hauteur_merveille = default_sprite_merveille.rect.height
        self.default_largeur_merveille = default_sprite_merveille.rect.width

        default_sprite_jetons_progres = SpriteJetonsProgres(
            JetonProgres("agriculture", None), 0, 0, RATIO_JETONS_PROGRES)
        self.default_hauteur_jetons_progres = default_sprite_jetons_progres.rect.height
        self.default_largeur_jetons_progres = default_sprite_jetons_progres.rect.width

        self.sprite_cartes_plateau = pygame.sprite.Group()
        self.sprite_cartes_defaussees = pygame.sprite.Group()

        self.sprite_j1 = [
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group()
        ]
        self.sprite_j2 = [
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group(),
            pygame.sprite.Group()
        ]

        self.sprite_carte_j1_zoomer = None
        self.sprite_jeton_j1_zoomer = None
        self.sprite_merveille_j1_zoomer = None

        self.sprite_carte_j2_zoomer = None
        self.sprite_jeton_j2_zoomer = None
        self.sprite_merveille_j2_zoomer = None

        self.espace_entre_carte = self.largeur * 0.005

        image_fond = pygame.image.load(
            DOSSIER_IMAGES + "fond_jeux.jpg").convert()
        self.image_fond = pygame.transform.scale(
            image_fond, (self.largeur, self.hauteur))

        image_plateau = pygame.image.load(
            DOSSIER_IMAGES + "plateau_sans_fond.png")
        image_plateau.set_colorkey((255, 255, 255))
        larg_plat, haut_plat = image_plateau.get_size()
        ration_plat = haut_plat / larg_plat
        larg_plat = RATIO_PLATEAU * self.largeur
        haut_plat = ration_plat * larg_plat
        self.image_plateau = pygame.transform.scale(
            image_plateau, (larg_plat, haut_plat))
        self.rect_image_plateau = self.image_plateau.get_rect()
        self.rect_image_plateau.topleft = (
            (self.largeur / 2 - self.image_plateau.get_width() / 2,
             2 * self.espace_entre_carte)
        )

        image_banque = pygame.image.load(
            DOSSIER_IMAGES + "banque_icon.png").convert_alpha()
        larg_banque, haut_banque = image_banque.get_size()
        ration_banque = haut_banque / larg_banque
        larg_banque = RATIO_BANQUE * self.largeur
        haut_banque = ration_banque * larg_banque
        self.image_banque = pygame.transform.scale(
            image_banque, (larg_banque, haut_banque))
        self.rect_image_banque = self.image_banque.get_rect()
        self.rect_image_banque.topleft = (
            (self.largeur / 2 + self.rect_image_plateau.width / 4 - self.image_banque.get_width() / 2,
             self.hauteur - 2 * self.espace_entre_carte - self.image_banque.get_height())
        )

        self.merveille_j1 = pygame.sprite.Group()
        self.merveille_j2 = pygame.sprite.Group()
        self.__dessiner_merveille()

        self.sprite_jetons_progres_plateau = pygame.sprite.Group()
        self.sprite_jetons_progres_j1 = pygame.sprite.Group()
        self.sprite_jetons_progres_j2 = pygame.sprite.Group()
        self.__dessiner_jetons_scientifiques()
        self.__dessiner_carte()

        top_x = self.largeur / 2
        top_x -= 12
        _, top_y = self.rect_image_plateau.bottomleft
        top_y /= 2
        top_y -= 5
        top = (top_x, top_y)

        larg = 26
        long = 56

        self.rect_jeton_conflit = pygame.Rect(top, (larg, long))

        self.sprite_jetons_militaire = pygame.sprite.Group()
        self.__dessiner_jetons_militaire()

    def __dessiner_carte_age_I(self):
        origine_cartes = self.largeur / 2 - \
            self.default_largeur_sprite - self.espace_entre_carte / 2

        haut_gauche_x = origine_cartes
        _, haut_gauche_y = self.rect_image_plateau.bottomright
        haut_gauche_y += self.espace_entre_carte

        for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
            for _, carte in enumerate(ligne_cartes):

                if carte != 0:
                    # dessin
                    sprite_carte = SpriteCarte(
                        carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
                    self.sprite_cartes_plateau.add(sprite_carte)

                    # coords carte suivante
                    haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte

            # coords changement ligne
            haut_gauche_x = origine_cartes - \
                (num_ligne + 1) * self.default_largeur_sprite / \
                2 - self.espace_entre_carte
            haut_gauche_y += self.default_hauteur_sprite / 2

    def __dessiner_carte_age_II(self):
        origine_cartes = self.largeur / 2 - 3 * \
            self.default_largeur_sprite - self.espace_entre_carte / 2

        haut_gauche_x = origine_cartes
        _, haut_gauche_y = self.rect_image_plateau.bottomright
        haut_gauche_y += self.espace_entre_carte

        for num_ligne, ligne_cartes in enumerate(self.plateau.cartes_plateau):
            for _, carte in enumerate(ligne_cartes):

                if carte != 0:
                    # dessin
                    sprite_carte = SpriteCarte(
                        carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
                    self.sprite_cartes_plateau.add(sprite_carte)

                    # coords carte suivante
                    haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte

            # coords changement ligne
            haut_gauche_x = origine_cartes + \
                (num_ligne+1) * self.default_largeur_sprite / \
                2 - self.espace_entre_carte
            haut_gauche_y += self.default_hauteur_sprite/2

    def __dessiner_carte_age_III(self):
        origine_cartes = self.largeur / 2 - \
            self.default_largeur_sprite - self.espace_entre_carte / 2

        haut_gauche_x = origine_cartes
        _, haut_gauche_y = self.rect_image_plateau.bottomright
        haut_gauche_y += self.espace_entre_carte

        for num_ligne in range(3):
            ligne_cartes = self.plateau.cartes_plateau[num_ligne]
            for num_colone in range(len(ligne_cartes)):
                carte = ligne_cartes[num_colone]

                if carte != 0:
                    # dessin
                    sprite_carte = SpriteCarte(
                        carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
                    self.sprite_cartes_plateau.add(sprite_carte)

                    # coords carte suivante
                    haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte

            # coords changement ligne
            haut_gauche_x = origine_cartes - \
                (num_ligne + 1) * self.default_largeur_sprite / \
                2 - self.espace_entre_carte
            haut_gauche_y += self.default_hauteur_sprite / 2

        #
        haut_gauche_x = origine_cartes - self.default_largeur_sprite / 2
        carte = self.plateau.cartes_plateau[3][1]
        self.sprite_cartes_plateau.add(SpriteCarte(
            carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE))

        #
        haut_gauche_x = origine_cartes + self.default_largeur_sprite + \
            self.default_largeur_sprite / 2
        carte = self.plateau.cartes_plateau[3][5]
        self.sprite_cartes_plateau.add(SpriteCarte(
            carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE))
        haut_gauche_y += self.default_hauteur_sprite/2

        #
        haut_gauche_x = origine_cartes - \
            self.default_largeur_sprite - self.espace_entre_carte
        for num_ligne in range(4, len(self.plateau.cartes_plateau)):
            ligne_cartes = self.plateau.cartes_plateau[num_ligne]
            for num_colone in range(len(ligne_cartes)):
                carte = ligne_cartes[num_colone]

                if carte != 0:
                    # dessin
                    sprite_carte = SpriteCarte(
                        carte, haut_gauche_x, haut_gauche_y, RATIO_IMAGE)
                    self.sprite_cartes_plateau.add(sprite_carte)

                    # coords carte suivante
                    haut_gauche_x += self.default_largeur_sprite + self.espace_entre_carte

            # coords changement ligne
            haut_gauche_x = origine_cartes - self.default_largeur_sprite + \
                (num_ligne - 4 + 1) * self.default_largeur_sprite / \
                2 - self.espace_entre_carte
            haut_gauche_y += self.default_hauteur_sprite/2

    def __dessiner_carte(self):
        if self.plateau.age == 1:
            self.__dessiner_carte_age_I()
        elif self.plateau.age == 2:
            self.__dessiner_carte_age_II()
        else:
            self.__dessiner_carte_age_III()

    def __dessiner_merveille(self):
        compteur = 0
        for merveille in self.plateau.joueur1.merveilles:
            coord_x, coord_y = self.rect_image_plateau.bottomleft
            coord_x += self.espace_entre_carte

            coord_y += compteur * \
                (self.default_largeur_merveille + self.espace_entre_carte)
            coord_y += compteur * (self.default_hauteur_sprite / 4)

            merveille_sprite = SpriteMerveille(
                merveille, coord_x, coord_y, RATIO_MERVEILLE)
            merveille_sprite.angle = -90
            self.merveille_j1.add(merveille_sprite)

            compteur += 1

        compteur = 0
        for merveille in self.plateau.joueur2.merveilles:
            coord_x, coord_y = self.rect_image_plateau.bottomright
            coord_x -= self.default_hauteur_merveille
            coord_x -= self.espace_entre_carte

            coord_y += compteur * \
                (self.default_largeur_merveille + self.espace_entre_carte)
            coord_y += compteur * (self.default_hauteur_sprite / 4)

            sprite_merveille = SpriteMerveille(
                merveille, coord_x, coord_y, RATIO_MERVEILLE)
            sprite_merveille.angle = 90
            self.merveille_j2.add(sprite_merveille)

            compteur += 1

    def __dessiner_merveille_sacrifier(self, merveille_a_construire: SpriteMerveille, carte_a_sacrifier: SpriteCarte):
        carte_a_sacrifier.carte.cacher()

        #
        if self.plateau.joueur_qui_joue == self.plateau.joueur1:
            liste_sprite_merveille = self.merveille_j1
        else:
            liste_sprite_merveille = self.merveille_j2

        #
        for merveille in liste_sprite_merveille:

            if isinstance(merveille, SpriteMerveille) \
                    and merveille.merveille == merveille_a_construire.merveille:

                coord_x, coord_y = merveille_a_construire.rect.topleft
                coord_y += self.default_largeur_sprite / 5

                carte_a_sacrifier.changer_coords(coord_x, coord_y)

        self.sprite_cartes_plateau.remove(carte_a_sacrifier)
        liste_sprite_merveille.remove(merveille_a_construire)
        liste_sprite_merveille.add(carte_a_sacrifier)
        liste_sprite_merveille.add(merveille_a_construire)

        self.plateau.joueur_qui_joue.merveilles.append(
            merveille_a_construire.merveille)
        self.plateau.enlever_carte(carte_a_sacrifier.carte)

    def __dessiner_jetons_scientifiques(self):
        coord_x, coord_y = self.rect_image_plateau.topleft
        coord_x += 1 / 4 * self.rect_image_plateau.width

        coord_y += self.espace_entre_carte

        for jeton in self.plateau.jetons_progres_plateau:
            sprite_jetons_progres = SpriteJetonsProgres(
                jeton, coord_x, coord_y, RATIO_JETONS_PROGRES
            )
            self.sprite_jetons_progres_plateau.add(sprite_jetons_progres)

            coord_x += 1 / 50 * self.rect_image_plateau.width + \
                self.default_largeur_jetons_progres

    def __dessiner_monnaies(self):
        # j1
        if self.plateau.joueur1.monnaie > 0:
            coord_x, coord_y = self.rect_image_plateau.bottomleft
            coord_x /= 8
            coord_y /= 20

            repartition = self.plateau.joueur1.trouver_repartition_monnaies()

            piece1 = None
            for piece, qte in repartition.items():
                if qte != 0:
                    piece1 = piece
                    break

            chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece1}.xcf"
            image_monnaies = pygame.image.load(chemin_monnaies).convert_alpha()

            larg, _ = image_monnaies.get_size()
            larg *= RATIO_MONNAIES_6

            image_monnaies = pygame.transform.scale(
                image_monnaies, (larg, larg))
            self.ecran.blit(image_monnaies, (coord_x, coord_y))

            repartition[piece1] -= 1

            for piece, qte in repartition.items():
                for _ in range(qte):
                    chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece}.xcf"
                    image_monnaies = pygame.image.load(
                        chemin_monnaies).convert_alpha()

                    coord_x += larg / 2

                    larg, _ = image_monnaies.get_size()
                    if piece == 6:
                        larg *= RATIO_MONNAIES_6
                    elif piece == 3:
                        larg *= RATIO_MONNAIES_3
                    else:
                        larg *= RATIO_MONNAIES_1

                    image_monnaies = pygame.transform.scale(
                        image_monnaies, (larg, larg))
                    self.ecran.blit(image_monnaies, (coord_x, coord_y))

        # j2
        if self.plateau.joueur2.monnaie > 0:
            coord_x, coord_y = self.rect_image_plateau.bottomright
            coord_x += 10
            coord_y /= 20

            repartition = self.plateau.joueur2.trouver_repartition_monnaies()

            piece1 = None
            for piece, qte in repartition.items():
                if qte != 0:
                    piece1 = piece
                    break

            chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece1}.xcf"
            image_monnaies = pygame.image.load(chemin_monnaies).convert_alpha()

            larg, _ = image_monnaies.get_size()
            larg *= RATIO_MONNAIES_6

            image_monnaies = pygame.transform.scale(
                image_monnaies, (larg, larg))
            self.ecran.blit(image_monnaies, (coord_x, coord_y))

            repartition[piece1] -= 1

            for piece, qte in repartition.items():
                for _ in range(qte):
                    chemin_monnaies = f"{DOSSIER_IMAGES}monnaies {piece}.xcf"
                    image_monnaies = pygame.image.load(
                        chemin_monnaies).convert_alpha()

                    coord_x += larg / 2

                    larg, _ = image_monnaies.get_size()
                    if piece == 6:
                        larg *= RATIO_MONNAIES_6
                    elif piece == 3:
                        larg *= RATIO_MONNAIES_3
                    else:
                        larg *= RATIO_MONNAIES_1

                    image_monnaies = pygame.transform.scale(
                        image_monnaies, (larg, larg))
                    self.ecran.blit(image_monnaies, (coord_x, coord_y))

    def __deplacer_jeton_attaque(self):
        top_x, top_y, larg, long = self.rect_jeton_conflit

        nbr_deplacement = abs(self.plateau.position_jeton_conflit - 9)
        decalage = 37

        top_x = self.largeur / 2
        top_x -= 12

        if self.plateau.position_jeton_conflit > 9:
            top_x += nbr_deplacement * decalage
        elif self.plateau.position_jeton_conflit < 9:
            top_x -= nbr_deplacement * decalage

        self.rect_jeton_conflit = (top_x, top_y, larg, long)

        for jeton_militaire in self.plateau.jetons_militaire:
            for sprite_jeton_militaire in self.sprite_jetons_militaire:
                if isinstance(sprite_jeton_militaire, SpriteJetonsMilitaire):
                    if jeton_militaire.est_utilise and jeton_militaire == sprite_jeton_militaire.jeton:
                        self.sprite_jetons_militaire.remove(
                            sprite_jeton_militaire)

    def __deplacer_jeton_scientifique(self, sprite_jeton: SpriteJetonsProgres):
        if self.plateau.joueur_qui_joue == self.plateau.joueur1:
            coord_x, coord_y = self.rect_image_plateau.bottomleft
            coord_x /= 8
            coord_y /= 4
            coord_y += 12

            for _ in self.sprite_jetons_progres_j1:
                coord_x += self.default_largeur_jetons_progres

            sprite_jeton.changer_coords(coord_x, coord_y)
            self.sprite_jetons_progres_j1.add(sprite_jeton)
            self.sprite_jetons_progres_plateau.remove(sprite_jeton)

        else:
            coord_x, coord_y = self.rect_image_plateau.bottomright
            coord_x += 10
            coord_y /= 4
            coord_y += 12

            for _ in self.sprite_jetons_progres_j2:
                coord_x += self.default_largeur_jetons_progres

            sprite_jeton.changer_coords(coord_x, coord_y)
            self.sprite_jetons_progres_j2.add(sprite_jeton)
            self.sprite_jetons_progres_plateau.remove(sprite_jeton)

    def __dessiner_jetons_militaire(self):
        plat_long = self.rect_image_plateau.width
        plat_larg = self.rect_image_plateau.height

        top_x, top_y = self.rect_image_plateau.topright
        top_x -= plat_long * 0.35
        top_y += plat_larg * (3 / 4)
        self.sprite_jetons_militaire.add(
            SpriteJetonsMilitaire(self.plateau.jetons_militaire[4], top_x, top_y, RATIO_JETONS_MILITAIRE2))

        top_x += plat_long * 0.13
        self.sprite_jetons_militaire.add(
            SpriteJetonsMilitaire(self.plateau.jetons_militaire[5], top_x, top_y, RATIO_JETONS_MILITAIRE5))

        top_x, _ = self.rect_image_plateau.topleft
        top_x += plat_long * 0.25
        self.sprite_jetons_militaire.add(
            SpriteJetonsMilitaire(self.plateau.jetons_militaire[1], top_x, top_y, RATIO_JETONS_MILITAIRE2))

        top_x -= plat_long * 0.13
        self.sprite_jetons_militaire.add(
            SpriteJetonsMilitaire(self.plateau.jetons_militaire[0], top_x, top_y, RATIO_JETONS_MILITAIRE5))

    def __position_type_carte(self, carte: Carte):
        if not isinstance(carte, CarteGuilde):
            liste_couleur = ["marron", "gris",
                             "bleu", "vert", "jaune", "rouge"]
            if carte.couleur in liste_couleur:
                return liste_couleur.index(carte.couleur)
        else:
            return 6

    def __piocher_plateau(self, sprite_carte: SpriteCarte):
        # print(f"{Couleurs.FAIL}monnaie avant piocher : {self.plateau.joueur_qui_joue.monnaie}{Couleurs.RESET}")
        ret = self.plateau.piocher(sprite_carte.carte)
        # print(f"{Couleurs.FAIL}monnaie après piocher : {self.plateau.joueur_qui_joue.monnaie}{Couleurs.RESET}")
        if ret == 0:

            ret2 = self.plateau.appliquer_effets_carte(sprite_carte.carte)
            if self.plateau.victoire is not None:
                return 2

            else:
                if ret2 == 2:
                    sprite_jeton = None
                    if len(self.sprite_jetons_progres_plateau) >= 1:
                        sprite_num = random.randint(
                            0, len(self.sprite_jetons_progres_plateau) - 1)
                    else:
                        sprite_num = 0

                    for num, sprite in enumerate(self.sprite_jetons_progres_plateau):
                        if num == sprite_num:
                            sprite_jeton = sprite
                            
                    ret = self.plateau.appliquer_effets_jeton(sprite_jeton.jeton)
                    self.__deplacer_jeton_scientifique(sprite_jeton)
                    
                    while ret == 2:
                        sprite_jeton = None
                        if len(self.sprite_jetons_progres_plateau) >= 1:
                            sprite_num = random.randint(
                                0, len(self.sprite_jetons_progres_plateau) - 1)
                        else:
                            sprite_num = 0
    
                        for num, sprite in enumerate(self.sprite_jetons_progres_plateau):
                            if num == sprite_num:
                                sprite_jeton = sprite
                                
                        ret = self.plateau.appliquer_effets_jeton(sprite_jeton.jeton)
                        self.__deplacer_jeton_scientifique(sprite_jeton)

                self.plateau.joueur_qui_joue.cartes.append(sprite_carte.carte)
                self.plateau.enlever_carte(sprite_carte.carte)

            self.__dessiner_piocher(sprite_carte)

        elif ret == -1:
            self.__dessiner_defausser(sprite_carte)

        return 0

    def __piocher_fausse(self, sprite_carte: SpriteCarte):
        ret = self.plateau.appliquer_effets_carte(sprite_carte.carte)
        if self.plateau.victoire is not None:
            return 2

        else:
            if ret == 2:
                sprite_jeton = None
                if len(self.sprite_jetons_progres_plateau) >= 1:
                    sprite_num = random.randint(
                        0, len(self.sprite_jetons_progres_plateau) - 1)

                else:
                    sprite_num = 0

                for num, sprite in enumerate(self.sprite_jetons_progres_plateau):
                    if num == sprite_num:
                        sprite_jeton = sprite
                self.__deplacer_jeton_scientifique(sprite_jeton)

            self.__dessiner_piocher(sprite_carte)

        return 0

    def __dessiner_piocher(self, sprite_carte: SpriteCarte):
        type_carte = self.__position_type_carte(sprite_carte.carte)

        sprite_carte.angle = 90

        if self.plateau.joueur_qui_joue == self.plateau.joueur1:
            sprite_joueur_qui_joue = self.sprite_j1
            sprite_carte.angle = -sprite_carte.angle
            coord_x, _ = self.rect_image_plateau.bottomleft
            coord_x -= self.espace_entre_carte
            coord_x -= self.default_hauteur_sprite
            decalage_x = - \
                (len(sprite_joueur_qui_joue[type_carte])
                 * (self.default_hauteur_sprite / 4))
        else:
            sprite_joueur_qui_joue = self.sprite_j2
            coord_x, _ = self.rect_image_plateau.bottomright
            coord_x += self.espace_entre_carte
            decalage_x = len(
                sprite_joueur_qui_joue[type_carte]) * (self.default_hauteur_sprite / 4)

        if type_carte == 0:
            coord_y = type_carte * self.default_largeur_sprite
        else:
            coord_y = type_carte * (
                self.default_largeur_sprite + self.espace_entre_carte
            )

        coord_y -= self.rect_image_plateau.height*1/4
        coord_y += self.default_largeur_sprite
        coord_x += decalage_x

        sprite_joueur_qui_joue[type_carte].add(sprite_carte)
        sprite_carte.changer_coords(coord_x, coord_y)

        return 0

    def __dessiner_defausser(self, carte_prenable: SpriteCarte):
        self.plateau.defausser(carte_prenable.carte)
        self.sprite_cartes_defaussees.add(carte_prenable)

        coord_x = self.largeur / 2 - self.rect_image_plateau.width / 4
        coord_y = self.hauteur - \
            (self.default_hauteur_sprite + self.espace_entre_carte)
        carte_prenable.changer_coords(coord_x, coord_y)

    def __construire_merveille(self, merveille: SpriteMerveille, sprite_carte_zoomer: SpriteCarte):
        ret = self.plateau.piocher(sprite_carte_zoomer.carte)
        if ret == -1:
            return -1
        rets = self.plateau.construire_merveille(merveille.merveille)
        if rets != (-1, None):
            self.__dessiner_merveille_sacrifier(merveille, sprite_carte_zoomer)

            if self.plateau.joueur_qui_joue == self.plateau.joueur1:
                sprite_cartes = self.sprite_j2
            else:
                sprite_cartes = self.sprite_j1

            for ret in rets:
                if type(ret) is tuple:
                    type_ret, obj = ret
                    if type_ret == "defausse_carte_adversaire" and isinstance(obj, Carte):
                        type_carte = self.__position_type_carte(obj)
                        sprite_carte_remove = None

                        for sprite_carte in sprite_cartes[type_carte]:
                            if isinstance(sprite_carte, SpriteCarte) and sprite_carte.carte == obj:
                                sprite_carte_remove = sprite_carte
                                break

                        if sprite_carte_remove is not None:
                            sprite_cartes[type_carte].remove(
                                sprite_carte_remove)
                            self.sprite_cartes_defaussees.add(
                                sprite_carte_remove)

                            sprite_carte_remove.angle = 0
                            sprite_carte_remove.pivoter()

                            coord_x = self.largeur / 2 - self.rect_image_plateau.width / 4
                            coord_y = self.hauteur - \
                                (self.default_hauteur_sprite +
                                 self.espace_entre_carte)
                            sprite_carte_remove.changer_coords(
                                coord_x, coord_y)

                    if type_ret == "jeton_progres_aleatoire":
                        if isinstance(obj, JetonProgres):
                            sprite_jeton_a_prendre = None
                            for sprite_jeton in self.sprite_jetons_progres_plateau:
                                if isinstance(sprite_jeton, SpriteJetonsProgres) and sprite_jeton.jeton == obj:
                                    sprite_jeton_a_prendre = sprite_jeton
                                    break
                            self.__deplacer_jeton_scientifique(
                                sprite_jeton_a_prendre)

                    if type_ret == "construction_fausse_gratuite":
                        if isinstance(obj, Carte):
                            if len(self.sprite_cartes_defaussees) != 0:
                                carte_defausee_a_construire = None
                                found = False
                                while not found:
                                    num_carte = random.randint(
                                        0, len(self.sprite_cartes_defaussees) - 1)
                                    for num_sprite, sprite_carte in enumerate(self.sprite_cartes_defaussees):
                                        if isinstance(sprite_carte, SpriteCarte) and num_sprite == num_carte:
                                            ret = self.plateau.piocher(
                                                sprite_carte.carte)
                                            if ret == 0:
                                                carte_defausee_a_construire = sprite_carte
                                                found = True
                                ret = self.__piocher_fausse(
                                    carte_defausee_a_construire)
                                if ret == 2:
                                    return 2

                else:
                    if type(ret) is str and ret == "rejouer":
                        return 1

        return 0

    def boucle_principale(self):
        en_cours = True

        coup_bot = True
        carte_bot, merveille_bot = None, None
        meilleur_eval = 0
        liste_temps = []
        liste_nbr_noeuds = []

        while en_cours:
            if self.plateau.victoire is not None:
                en_cours = False
                break

            # PARTIE Process input (events)
            for event in pygame.event.get():

                # quitter avec la croix
                if event.type == pygame.QUIT:
                    en_cours = False

                # quitter avec la touche echap
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    en_cours = False

                if self.plateau.joueur_qui_joue == self.plateau.joueur1:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                        clic_x, clic_y = event.pos

                        if self.sprite_jeton_j1_zoomer is None and self.sprite_merveille_j1_zoomer is None:

                            for sprit in self.sprite_cartes_plateau:

                                if sprit.rect.collidepoint(clic_x, clic_y) and isinstance(sprit, SpriteCarte) and sprit.carte in self.plateau.liste_cartes_prenables():
                                    if self.sprite_carte_j1_zoomer is None:

                                        sprit.zoomer(
                                            RATIO_ZOOM_CARTE, (self.largeur / 2, self.hauteur / 2))
                                        self.sprite_carte_j1_zoomer = sprit
                                        self.sprite_cartes_plateau.remove(
                                            self.sprite_carte_j1_zoomer)
                                        self.sprite_cartes_plateau.add(
                                            self.sprite_carte_j1_zoomer)

                                    else:
                                        if sprit == self.sprite_carte_j1_zoomer:
                                            sprit.dezoomer()
                                            self.sprite_carte_j1_zoomer = None

                        bottomleft_x, bottomleft_y = self.rect_image_plateau.bottomleft

                        if (clic_x < bottomleft_x and clic_y > bottomleft_y and self.plateau.joueur_qui_joue == self.plateau.joueur1) and self.sprite_carte_j1_zoomer is not None and self.sprite_carte_j1_zoomer.carte in self.plateau.liste_cartes_prenables():
                            self.sprite_carte_j1_zoomer.dezoomer()
                            ret = self.__piocher_plateau(
                                self.sprite_carte_j1_zoomer)
                            if ret == 2:
                                en_cours = False
                                break
                            self.sprite_cartes_plateau.remove(
                                self.sprite_carte_j1_zoomer)
                            self.plateau.joueur_qui_joue = self.plateau.adversaire()
                            self.sprite_carte_j1_zoomer = None

                        if self.rect_image_banque.collidepoint(clic_x, clic_y) and self.sprite_carte_j1_zoomer is not None:
                            self.sprite_carte_j1_zoomer.dezoomer()
                            self.__dessiner_defausser(
                                self.sprite_carte_j1_zoomer)
                            self.sprite_cartes_plateau.remove(
                                self.sprite_carte_j1_zoomer)
                            self.plateau.joueur_qui_joue = self.plateau.adversaire()
                            self.sprite_carte_j1_zoomer = None

                        if self.sprite_carte_j1_zoomer is None and self.sprite_merveille_j1_zoomer is None:

                            for jeton in self.sprite_jetons_progres_plateau:

                                if jeton.rect.collidepoint(clic_x, clic_y) and isinstance(jeton, SpriteJetonsProgres):
                                    if self.sprite_jeton_j1_zoomer is None:

                                        jeton.zoomer(
                                            RATIO_ZOOM_CARTE, (self.largeur / 2, self.hauteur / 2))
                                        self.sprite_jeton_j1_zoomer = jeton
                                        self.sprite_jetons_progres_plateau.remove(
                                            self.sprite_jeton_j1_zoomer)
                                        self.sprite_jetons_progres_plateau.add(
                                            self.sprite_jeton_j1_zoomer)

                                    else:
                                        if jeton == self.sprite_jeton_j1_zoomer:
                                            jeton.dezoomer()
                                            self.sprite_jeton_j1_zoomer = None

                        if self.sprite_jeton_j1_zoomer is None:

                            for merveille in self.merveille_j1:

                                if merveille.rect.collidepoint(clic_x, clic_y) and isinstance(merveille, SpriteMerveille):

                                    if self.sprite_carte_j1_zoomer is None:

                                        if self.sprite_merveille_j1_zoomer is None:

                                            merveille.zoomer(RATIO_ZOOM_MERVEILLE,
                                                             (self.largeur / 2, self.hauteur / 2))
                                            merveille.angle = 0
                                            merveille.pivoter()
                                            self.sprite_merveille_j1_zoomer = merveille
                                            self.merveille_j1.remove(
                                                self.sprite_merveille_j1_zoomer)
                                            self.merveille_j1.add(
                                                self.sprite_merveille_j1_zoomer)

                                        else:
                                            if merveille == self.sprite_merveille_j1_zoomer:
                                                merveille.dezoomer()
                                                merveille.angle = 90
                                                merveille.pivoter()
                                                self.sprite_merveille_j1_zoomer = None

                                    else:

                                        if merveille.rect.collidepoint(clic_x, clic_y) and isinstance(merveille,
                                                                                                      SpriteMerveille):
                                            self.sprite_carte_j1_zoomer.dezoomer()
                                            ret = self.__construire_merveille(
                                                merveille, self.sprite_carte_j1_zoomer)
                                            self.sprite_carte_j1_zoomer = None
                                            if ret == 0:
                                                self.plateau.joueur_qui_joue = self.plateau.adversaire()

                else:
                    if self.mode_1_vs_1:
                        if self.plateau.joueur_qui_joue == self.plateau.joueur2:
                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                                clic_x, clic_y = event.pos

                                if self.sprite_jeton_j2_zoomer is None and self.sprite_merveille_j2_zoomer is None:

                                    for sprit in self.sprite_cartes_plateau:

                                        if sprit.rect.collidepoint(clic_x, clic_y):

                                            if isinstance(sprit, SpriteCarte):

                                                if sprit.carte in self.plateau.liste_cartes_prenables():

                                                    if self.sprite_carte_j2_zoomer is None:

                                                        sprit.zoomer(RATIO_ZOOM_CARTE,
                                                                     (self.largeur / 2, self.hauteur / 2))
                                                        self.sprite_carte_j2_zoomer = sprit
                                                        self.sprite_cartes_plateau.remove(
                                                            self.sprite_carte_j2_zoomer)
                                                        self.sprite_cartes_plateau.add(
                                                            self.sprite_carte_j2_zoomer)

                                                    else:
                                                        if sprit == self.sprite_carte_j2_zoomer:
                                                            sprit.dezoomer()
                                                            self.sprite_carte_j2_zoomer = None

                                bottomright_x, bottomright_y = self.rect_image_plateau.bottomright

                                if (clic_x > bottomright_x and clic_y > bottomright_y and
                                        self.plateau.joueur_qui_joue == self.plateau.joueur2):

                                    if self.sprite_carte_j2_zoomer is not None:

                                        if self.sprite_carte_j2_zoomer.carte in self.plateau.liste_cartes_prenables():

                                            self.sprite_carte_j2_zoomer.dezoomer()
                                            ret = self.__piocher_plateau(
                                                self.sprite_carte_j2_zoomer)
                                            if ret == 2:
                                                en_cours = False
                                                break
                                            self.sprite_cartes_plateau.remove(
                                                self.sprite_carte_j2_zoomer)
                                            self.plateau.joueur_qui_joue = self.plateau.adversaire()
                                            self.sprite_carte_j2_zoomer = None

                                if self.rect_image_banque.collidepoint(clic_x, clic_y):

                                    if self.sprite_carte_j2_zoomer is not None:
                                        self.sprite_carte_j2_zoomer.dezoomer()
                                        self.__dessiner_defausser(
                                            self.sprite_carte_j2_zoomer)
                                        self.sprite_cartes_plateau.remove(
                                            self.sprite_carte_j2_zoomer)
                                        self.plateau.joueur_qui_joue = self.plateau.adversaire()
                                        self.sprite_carte_j2_zoomer = None

                                if self.sprite_carte_j2_zoomer is None and self.sprite_merveille_j2_zoomer is None:

                                    for jeton in self.sprite_jetons_progres_plateau:

                                        if jeton.rect.collidepoint(clic_x, clic_y):

                                            if isinstance(jeton, SpriteJetonsProgres):

                                                if self.sprite_jeton_j2_zoomer is None:

                                                    jeton.zoomer(
                                                        RATIO_ZOOM_CARTE, (self.largeur / 2, self.hauteur / 2))
                                                    self.sprite_jeton_j2_zoomer = jeton
                                                    self.sprite_jetons_progres_plateau.remove(
                                                        self.sprite_jeton_j2_zoomer)
                                                    self.sprite_jetons_progres_plateau.add(
                                                        self.sprite_jeton_j2_zoomer)

                                                else:
                                                    if jeton == self.sprite_jeton_j2_zoomer:
                                                        jeton.dezoomer()
                                                        self.sprite_jeton_j2_zoomer = None

                                if self.sprite_jeton_j2_zoomer is None:

                                    for merveille in self.merveille_j2:

                                        if merveille.rect.collidepoint(clic_x, clic_y) and isinstance(merveille,
                                                                                                      SpriteMerveille):

                                            if self.sprite_carte_j2_zoomer is None:

                                                if self.sprite_merveille_j2_zoomer is None:

                                                    merveille.zoomer(RATIO_ZOOM_MERVEILLE,
                                                                     (self.largeur / 2, self.hauteur / 2))
                                                    merveille.angle = 0
                                                    merveille.pivoter()
                                                    self.sprite_merveille_j2_zoomer = merveille
                                                    self.merveille_j2.remove(
                                                        self.sprite_merveille_j2_zoomer)
                                                    self.merveille_j2.add(
                                                        self.sprite_merveille_j2_zoomer)

                                                else:
                                                    if merveille == self.sprite_merveille_j2_zoomer:
                                                        merveille.dezoomer()
                                                        merveille.angle = 90
                                                        merveille.pivoter()
                                                        self.sprite_merveille_j2_zoomer = None

                                            else:
                                                if merveille.rect.collidepoint(clic_x, clic_y) and isinstance(merveille,
                                                                                                              SpriteMerveille):
                                                    self.sprite_carte_j2_zoomer.dezoomer()
                                                    ret = self.__construire_merveille(merveille,
                                                                                      self.sprite_carte_j2_zoomer)
                                                    self.sprite_carte_j2_zoomer = None
                                                    if ret == 0:
                                                        self.plateau.joueur_qui_joue = self.plateau.adversaire()
                    else:
                        if coup_bot:
                            deb = time.time()
                            nbr_noeuds = 0
                            meilleur_eval = 0
                            print(
                                f"{Couleurs.FAIL}debut alpha_beta_avec_merveille (meilleur_eval = {meilleur_eval}){Couleurs.RESET}")

                            meilleur_eval, carte_bot, merveille_bot, nbr_noeuds = alpha_beta_avec_merveille(self.plateau,
                                                                                                            self.difficulte_profondeur, -math.inf, math.inf, True, nbr_noeuds)
                            # meilleur_eval, carte_bot, nbr_noeuds = alpha_beta(self.plateau, self.difficulte_profondeur,
                            # 		-math.inf, math.inf, True, nbr_noeuds)

                            if carte_bot is not None:
                                print(
                                    f"{Couleurs.FAIL}fin alpha_beta_avec_merveille (meilleur_eval = {meilleur_eval}){Couleurs.RESET}")

                                fin = time.time()
                                temps_exe = fin - deb

                                if merveille_bot is None:
                                    print(f"{Couleurs.OK}carte_a_prendre : {carte_bot.nom}, temps execution : {temps_exe}, "
                                          f"nbr_noeuds : {nbr_noeuds}{Couleurs.RESET}")
                                else:
                                    print(f"{Couleurs.OK}carte_a_prendre : {carte_bot.nom}, merveille : {merveille_bot.nom}, "
                                          f"temps execution : {temps_exe}, nbr_noeuds : {nbr_noeuds}{Couleurs.RESET}")

                                liste_temps.append(temps_exe)
                                liste_nbr_noeuds.append(nbr_noeuds)
                                coup_bot = False
                            else:
                                coup_bot = True

                        if not coup_bot:
                            for sprite_carte in self.sprite_cartes_plateau:

                                if isinstance(sprite_carte, SpriteCarte):

                                    if sprite_carte.carte == carte_bot:

                                        if merveille_bot is None:

                                            if self.sprite_carte_j2_zoomer is None:

                                                sprite_carte.zoomer(
                                                    RATIO_ZOOM_CARTE, (self.largeur / 2, self.hauteur / 2))
                                                self.sprite_carte_j2_zoomer = sprite_carte
                                                self.sprite_cartes_plateau.remove(
                                                    self.sprite_carte_j2_zoomer)
                                                self.sprite_cartes_plateau.add(
                                                    self.sprite_carte_j2_zoomer)

                                            else:

                                                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                                                    clic_x, clic_y = event.pos

                                                    if sprite_carte.rect.collidepoint(clic_x, clic_y):
                                                        self.sprite_carte_j2_zoomer.dezoomer()
                                                        self.sprite_carte_j2_zoomer = None
                                                        ret = self.__piocher_plateau(
                                                            sprite_carte)
                                                        if ret == 2:
                                                            en_cours = False
                                                            break
                                                        self.plateau.joueur_qui_joue = self.plateau.adversaire()
                                                        coup_bot = True

                                        else:

                                            for merveille in self.merveille_j2:

                                                if isinstance(merveille, SpriteMerveille):

                                                    if merveille.merveille == merveille_bot:

                                                        if self.sprite_carte_j2_zoomer is None:

                                                            sprite_carte.zoomer(RATIO_ZOOM_CARTE,
                                                                                (self.largeur / 2, self.hauteur / 2))
                                                            self.sprite_carte_j2_zoomer = sprite_carte
                                                            self.sprite_cartes_plateau.remove(
                                                                self.sprite_carte_j2_zoomer)
                                                            self.sprite_cartes_plateau.add(
                                                                self.sprite_carte_j2_zoomer)

                                                        else:

                                                            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                                                                clic_x, clic_y = event.pos

                                                                if self.sprite_carte_j2_zoomer.rect.collidepoint(clic_x,
                                                                                                                 clic_y):
                                                                    self.sprite_carte_j2_zoomer.dezoomer()
                                                                    ret = self.__construire_merveille(merveille,
                                                                                                      self.sprite_carte_j2_zoomer)
                                                                    self.sprite_carte_j2_zoomer = None
                                                                    coup_bot = True
                                                                    if ret == 0:
                                                                        self.plateau.joueur_qui_joue = self.plateau.adversaire()

            # PARTIE Update
            if self.plateau.changement_age() == 1:
                self.__dessiner_carte()

            for group_sprit in self.sprite_j1:
                group_sprit.update()
            for group_sprit in self.sprite_j2:
                group_sprit.update()

            self.merveille_j1.update()
            self.merveille_j2.update()
            self.sprite_jetons_progres_j1.update()
            self.sprite_jetons_progres_j2.update()

            self.sprite_jetons_militaire.update()

            self.sprite_jetons_progres_plateau.update()
            self.sprite_cartes_plateau.update()
            self.merveille_j1.update()
            self.merveille_j2.update()
            self.sprite_cartes_defaussees.update()

            # PARTIE Draw / render
            self.ecran.blit(self.image_fond, (0, 0))
            self.ecran.blit(self.image_plateau,
                            self.rect_image_plateau.topleft)
            self.ecran.blit(self.image_banque, self.rect_image_banque.topleft)
            self.__dessiner_monnaies()

            for sprite_carte_j1 in self.sprite_j1:
                sprite_carte_j1.draw(self.ecran)
            for sprite_carte_j2 in self.sprite_j2:
                sprite_carte_j2.draw(self.ecran)

            self.merveille_j1.draw(self.ecran)
            self.merveille_j2.draw(self.ecran)

            pygame.draw.ellipse(self.ecran, (255, 0, 0),
                                self.rect_jeton_conflit, 50)
            self.__deplacer_jeton_attaque()
            self.sprite_jetons_militaire.draw(self.ecran)

            if self.sprite_carte_j1_zoomer is not None:
                self.sprite_jetons_progres_plateau.draw(self.ecran)
                self.merveille_j1.draw(self.ecran)
                self.merveille_j2.draw(self.ecran)
                self.sprite_cartes_defaussees.draw(self.ecran)
                self.sprite_cartes_plateau.draw(self.ecran)
                self.sprite_jetons_progres_j1.draw(self.ecran)
                self.sprite_jetons_progres_j2.draw(self.ecran)

            elif self.sprite_merveille_j1_zoomer is not None:
                self.sprite_jetons_progres_plateau.draw(self.ecran)
                self.sprite_cartes_plateau.draw(self.ecran)
                self.merveille_j2.draw(self.ecran)
                self.sprite_cartes_defaussees.draw(self.ecran)
                self.merveille_j1.draw(self.ecran)
                self.sprite_jetons_progres_j1.draw(self.ecran)
                self.sprite_jetons_progres_j2.draw(self.ecran)

            elif self.sprite_jeton_j1_zoomer is not None:
                self.sprite_cartes_plateau.draw(self.ecran)
                self.merveille_j1.draw(self.ecran)
                self.merveille_j2.draw(self.ecran)
                self.sprite_cartes_defaussees.draw(self.ecran)
                self.sprite_jetons_progres_plateau.draw(self.ecran)
                self.sprite_jetons_progres_j1.draw(self.ecran)
                self.sprite_jetons_progres_j2.draw(self.ecran)

            else:
                self.sprite_jetons_progres_plateau.draw(self.ecran)
                self.sprite_cartes_plateau.draw(self.ecran)
                self.merveille_j1.draw(self.ecran)
                self.merveille_j2.draw(self.ecran)
                self.sprite_cartes_defaussees.draw(self.ecran)
                self.sprite_jetons_progres_j1.draw(self.ecran)
                self.sprite_jetons_progres_j2.draw(self.ecran)

            # after drawing everything, flip this display
            pygame.display.flip()

        pygame.quit()
        if self.plateau.victoire is not None:
            print("victoire : ", self.plateau.victoire)
            print("joueur 1", self.plateau.joueur1.points_victoire)
            print("ordi", self.plateau.joueur2.points_victoire)
        if len(liste_temps) != 0 and len(liste_nbr_noeuds) != 0:
            moy_temps = sum(liste_temps) / len(liste_temps)
            moy_nbr_noeuds = sum(liste_nbr_noeuds) / len(liste_nbr_noeuds)
            print(
                f"temps moyen : {moy_temps}, nombre noeuds moyen : {int(moy_nbr_noeuds)}")
