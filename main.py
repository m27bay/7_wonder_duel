import pygame
import time

from src.interface_graphique.src import Boutton
from src.interface_graphique.src.Fenetre import Fenetre
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

FOND_ECRAN = "src/interface_graphique/ressources/images/image_menu/fond.jpg"
LARGEUR_BOUTON_MENU = 75
LONGUEUR_BOUTON_MENU = 175
LARGEUR_TITRE = 300
LONGUEUR_TITRE = 400

MUTE_SOUND = 0
MENU_ACCUEILLE = 0
MENU_JOUER = 1
MENU_OPTIONS = 2
MENU_DIFICULTER = 3
JOUER_JVO = 5
JOUER_JVJ = 6
blank_color = (255, 255, 255)

def musique():

    pygame.mixer.init()

    playlist = list()
    playlist.append("src/interface_graphique/ressources/sons/Thomas-Bergersen-Immortal-_2011_.wav")
    playlist.append("src/interface_graphique/ressources/sons/Two-Steps-From-Hell-Protectors-of-the-Earth.wav")
    playlist.append("src/interface_graphique/ressources/sons/maxkomusic-medieval-fantasy.wav")

    pygame.mixer.music.load(playlist.pop())  # Get the first track from the playlist
    pygame.mixer.music.queue(playlist.pop())  # Queue the 2nd song
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Setup the end track event
    pygame.mixer.music.play()  # Play the music
    pygame.mixer.music.set_volume(0.5)

    if len(playlist) > 0:  # If there are more tracks in the queue...
        pygame.mixer.music.queue(playlist.pop())  # Q


tab_image = [
    "src/interface_graphique/ressources/images/image_menu/Titre.png",
    "src/interface_graphique/ressources/images/image_menu/Jouer.png",
    "src/interface_graphique/ressources/images/image_menu/Options.png",
    "src/interface_graphique/ressources/images/image_menu/Quitter.png",
    "src/interface_graphique/ressources/images/image_menu/Musique.png",
    "src/interface_graphique/ressources/images/image_menu/Musique_off.png",
    "src/interface_graphique/ressources/images/image_menu/P1contreOrdi.png",
    "src/interface_graphique/ressources/images/image_menu/P1contreP2.png",
    "src/interface_graphique/ressources/images/image_menu/Retour.xcf",
    "src/interface_graphique/ressources/images/image_menu/TypedeDifficulte.png",
    "src/interface_graphique/ressources/images/image_menu/Facile.png",
    "src/interface_graphique/ressources/images/image_menu/Normale.png",
    "src/interface_graphique/ressources/images/image_menu/Difficile.png",
    "src/interface_graphique/ressources/images/image_menu/Argiles.jpg",
    "src/interface_graphique/ressources/images/image_menu/Pierre.jpg",
    "src/interface_graphique/ressources/images/image_menu/Bois.jpg",
    "src/interface_graphique/ressources/images/image_menu/Papier.jpg",
    "src/interface_graphique/ressources/images/image_menu/Verre.jpg"
]
def tableau_image():
    return tab_image


def taille_ecran():
    fenetre = pygame.display.set_mode()
    x, y = fenetre.get_size()
    tab_size = [x, y]
    pygame.display.quit()

    return tab_size


pygame.init()
pygame.display.set_caption("my game")


'#MENU d ACCUEILLE DU JEUX'


def affichage_menu_accueille():

    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_ECRAN)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])

    image_menu = tableau_image()

    bouton_titre = Boutton.Button(image_menu[0], image_menu[0], (taille[0]/2)-175, (taille[1]/2)-400,
                                  LONGUEUR_TITRE, LARGEUR_TITRE)
    bouton_titre.affichage_du_bouton(window_surface)

    bouton_jouer = Boutton.Button(image_menu[1], image_menu[1], (taille[0]/2)-75, taille[1]/2,
                                  LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_jouer.affichage_du_bouton(window_surface)

    bouton_quitter = Boutton.Button(image_menu[3], image_menu[3], (taille[0]/2)-75, (taille[1]/2) + 140,
                                    LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_quitter.affichage_du_bouton(window_surface)
    window_tempo = window_surface

    bouton_son_on = Boutton.Button(image_menu[4], image_menu[4], (taille[0]/12), (taille[1] - (taille[1]/6)), 150, 115)
    bouton_son_on.affichage_du_bouton(window_surface)

    bouton_son_off = Boutton.Button(image_menu[5], image_menu[5], (taille[0]/12), (taille[1] - (taille[1]/6)), 150, 115)

    pygame.display.flip()
    status_son = 0
    launched = True
    while launched:
        #musique()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_son_on.rectangle.collidepoint(event.pos) and status_son == 0:
                    bouton_son_off.affichage_du_bouton(window_tempo)
                    pygame.mixer.music.pause()
                    MUTE_SOUND = 1
                    status_son = 1
                    break
                elif event.button == 1 and bouton_son_on.rectangle.collidepoint(event.pos) and status_son == 1:
                    MUTE_SOUND = 0
                    bouton_son_on.affichage_du_bouton(window_tempo)
                    pygame.mixer.music.unpause()
                    status_son = 0
                    break
                elif event.button == 1 and bouton_quitter.rectangle.collidepoint(event.pos):
                    launched = False
                elif event.button == 1 and bouton_jouer.rectangle.collidepoint(event.pos):
                    launched = False
                    choix_menu = MENU_JOUER
                    break
        if launched == False:
            break
        pygame.display.flip()
    return choix_menu


'#MENU DU BOUTON OPTIONS'


def affichage_mode_jouer():

    jeux = 0
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_ECRAN)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])
    image_mode_jouer = tableau_image()

    bouton_titre_jouer = Boutton.Button(image_mode_jouer[0], image_mode_jouer[0], (taille[0]/2)-175, (taille[1]/2)-400,
                                        LONGUEUR_TITRE, LARGEUR_TITRE)
    bouton_titre_jouer.affichage_du_bouton(window_surface)

    bouton_jvj = Boutton.Button(image_mode_jouer[7], image_mode_jouer[7], (taille[0]/2)-75, (taille[1]/2),
                                LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_jvj.affichage_du_bouton(window_surface)

    bouton_jvo = Boutton.Button(image_mode_jouer[6], image_mode_jouer[6], (taille[0]/2)-75, (taille[1]/2)+140,
                                LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_jvo.affichage_du_bouton(window_surface)

    bouton_retour = Boutton.Button(image_mode_jouer[8], image_mode_jouer[8],
                                   (taille[0]/12), (taille[1] - (taille[1]/6)), 90, 90)
    bouton_retour.affichage_du_bouton(window_surface)

    pygame.display.flip()
    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_jvj.rectangle.collidepoint(event.pos):
                    launched = False
                    jeux = 1
                    choix_menu = JOUER_JVJ
                elif event.button == 1 and bouton_jvo.rectangle.collidepoint(event.pos):
                    launched = False
                    jeux = 2
                    choix_menu = JOUER_JVO
                    break
                elif event.button == 1 and bouton_retour.rectangle.collidepoint(event.pos):
                    launched = False
                    choix_menu = MENU_ACCUEILLE
                    break
        if launched == False:
            break
        pygame.display.flip()
    return choix_menu, jeux


'#MENU DU BOUTON DIFFICULTER'


def affichage_menu_difficulter():
    niveau_diff = 0
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_ECRAN)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])
    image_menu_difficulter = tableau_image()

    bouton_titre_difficulter = Boutton.Button(image_menu_difficulter[0], image_menu_difficulter[0], (taille[0] / 2) -
                                              175, (taille[1] / 2) - 400, LONGUEUR_TITRE, LARGEUR_TITRE)
    bouton_titre_difficulter.affichage_du_bouton(window_surface)

    bouton_difficulter_facile = Boutton.Button(image_menu_difficulter[10], image_menu_difficulter[10],
                                               (taille[0] / 2) - 75, (taille[1] / 2) - 30, LONGUEUR_BOUTON_MENU,
                                               LARGEUR_BOUTON_MENU)
    bouton_difficulter_facile.affichage_du_bouton(window_surface)

    bouton_difficulter_moyen = Boutton.Button(image_menu_difficulter[11], image_menu_difficulter[11],
                                              (taille[0] / 2) - 75, (taille[1] / 2) + 70, LONGUEUR_BOUTON_MENU,
                                              LARGEUR_BOUTON_MENU)
    bouton_difficulter_moyen.affichage_du_bouton(window_surface)

    bouton_difficulter_difficile = Boutton.Button(image_menu_difficulter[12], image_menu_difficulter[12],
                                                  (taille[0] / 2) - 75, (taille[1] / 2) + 170, LONGUEUR_BOUTON_MENU,
                                                  LARGEUR_BOUTON_MENU)
    bouton_difficulter_difficile.affichage_du_bouton(window_surface)

    bouton_retour = Boutton.Button(image_menu_difficulter[8], image_menu_difficulter[8],
                                   (taille[0] / 12), (taille[1] - (taille[1] / 6)), 90, 90)
    bouton_retour.affichage_du_bouton(window_surface)

    pygame.display.flip()
    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_difficulter_facile.rectangle.collidepoint(event.pos):
                    launched = False
                    niveau_diff = 5
                    choix_menu = MENU_DIFICULTER
                elif event.button == 1 and bouton_difficulter_moyen.rectangle.collidepoint(event.pos):
                    launched = False
                    niveau_diff = 7
                    choix_menu = MENU_DIFICULTER
                    break
                elif event.button == 1 and bouton_difficulter_difficile.rectangle.collidepoint(event.pos):
                    launched = False
                    niveau_diff = 9
                    choix_menu = MENU_DIFICULTER
                    break
                elif event.button == 1 and bouton_retour.rectangle.collidepoint(event.pos):
                    launched = False
                    choix_menu = MENU_JOUER
                    break
        if launched == False:
            break
        pygame.display.flip()
    return choix_menu, niveau_diff


def jouer_vs_boot(difficulter):
    plateau = Plateau(Joueur("joueur"), Joueur("ordi"))
    plateau.preparation_plateau()
    fenetre = Fenetre("7 wonder Duel", plateau, difficulter)
    fenetre.boucle_principale()


def affichage_enssemble():
    pygame.init()

    running = True

    quel_menu = MENU_ACCUEILLE

    niveau_difficulter = -1
    mode_de_jeux = 0

    musique()
    while running:
        if quel_menu == MENU_ACCUEILLE:
            quel_menu = affichage_menu_accueille()
        elif quel_menu == MENU_JOUER:
            quel_menu, mode_de_jeux = affichage_mode_jouer()
        elif quel_menu == JOUER_JVO:
            quel_menu, niveau_difficulter = affichage_menu_difficulter()
        elif quel_menu == JOUER_JVJ:
            break
        elif quel_menu == MENU_DIFICULTER:
            jouer_vs_boot(niveau_difficulter)
            break
        else:
            break


'#affichage_mode_jouer()'
if __name__ == '__main__':
    affichage_enssemble()
