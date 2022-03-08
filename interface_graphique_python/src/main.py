import pygame
import Boutton

FOND_ECRAN = \
    "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/fond.jpg"
FOND_JEUX = "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/fond-jeux.jpg"
LARGEUR_BOUTON_MENU = 50
LONGUEUR_BOUTON_MENU = 150
LARGEUR_TITRE = 250
LONGUEUR_TITRE = 350

MUTE_SOUND = 0
MENU_ACCUEILLE = 0
MENU_JOUER = 1
MENU_OPTIONS = 2
MENU_DIFICULTER = 3
JOUER = 5

jeux = 0

NIVEAU_DIFICULTER = -1
blank_color = (255, 255, 255)


def musique(path, volume):
    music = pygame.mixer.Sound(path)
    music.set_volume(volume)
    music.play()


def tableau_image():
    tab_image = [
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/titre.jpeg",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/play.jpg",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/settings.jpg",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/exit.jpg",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/sound_ON.png",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/sound_OFF.png",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/jouer1.jpg",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/retour.jpeg",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/image_test.jpg",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/verso_carte.jpg"

    ]
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

    bouton_titre = Boutton.Button(image_menu[0], image_menu[0], (taille[0]/2)-140, (taille[1]/2)-400,
                                  LONGUEUR_TITRE, LARGEUR_TITRE)
    bouton_titre.affichage_du_bouton(window_surface)

    bouton_jouer = Boutton.Button(image_menu[1], image_menu[1], (taille[0]/2)-50, taille[1]/2-30,
                                  LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_jouer.affichage_du_bouton(window_surface)

    bouton_options = Boutton.Button(image_menu[2], image_menu[2], (taille[0]/2)-50, (taille[1]/2) + 110,
                                    LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_options.affichage_du_bouton(window_surface)

    bouton_quitter = Boutton.Button(image_menu[3], image_menu[3], (taille[0]/2)-50, (taille[1]/2) + 40,
                                    LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_quitter.affichage_du_bouton(window_surface)

    bouton_son_on = Boutton.Button(image_menu[4], image_menu[4], (taille[0]/12), (taille[1] - (taille[1]/6)), 75, 75)
    bouton_son_on.affichage_du_bouton(window_surface)

    bouton_son_off = Boutton.Button(image_menu[5], image_menu[5], (taille[0]/12), (taille[1] - (taille[1]/6)), 75, 75)

    pygame.display.flip()
    status_son = 0
    launched = True
    while launched:
        musique("/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/"
                "maxkomusic-medieval-fantasy.wav", 0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_son_on.reactangle.collidepoint(event.pos) and status_son == 0:
                    print("on off")
                    window_surface.blit(window_surface, [0, 0])
                    bouton_son_off.affichage_du_bouton(window_surface)
                    pygame.mixer.pause()
                    MUTE_SOUND = 1
                    status_son = 1
                    break
                elif event.button == 1 and bouton_son_on.reactangle.collidepoint(event.pos) and status_son == 1:
                    musique("/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/"
                            "maxkomusic-medieval-fantasy.wav", 0.5)
                    MUTE_SOUND = 0
                    print("off on")
                    window_surface.blit(window_surface, [0, 0])
                    bouton_son_on.affichage_du_bouton(window_surface)
                    pygame.mixer.unpause()
                    status_son = 0
                    break
                elif event.button == 1 and bouton_quitter.reactangle.collidepoint(event.pos):
                    launched = False
                elif event.button == 1 and bouton_jouer.reactangle.collidepoint(event.pos):
                    launched = False
                    choix_menu = MENU_JOUER
                    break
                elif event.button == 1 and bouton_options.reactangle.collidepoint(event.pos):
                    launched = False
                    choix_menu = MENU_OPTIONS
                    break
        if launched == False:
            break
        pygame.display.flip()
    return choix_menu


'#MENU DU BOUTON OPTIONS'


def affichage_mode_jouer():

    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_ECRAN)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])
    image_mode_jouer = tableau_image()

    bouton_titre_jouer = Boutton.Button(image_mode_jouer[0], image_mode_jouer[0], (taille[0]/2)-140, (taille[1]/2)-400,
                                        LONGUEUR_TITRE, LARGEUR_TITRE)
    bouton_titre_jouer.affichage_du_bouton(window_surface)

    bouton_jvj = Boutton.Button(image_mode_jouer[6], image_mode_jouer[6], (taille[0]/2)-50, (taille[1]/2)-30,
                                LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_jvj.affichage_du_bouton(window_surface)

    bouton_jvo = Boutton.Button(image_mode_jouer[6], image_mode_jouer[6], (taille[0]/2)-50, (taille[1]/2)+40,
                                LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_jvo.affichage_du_bouton(window_surface)

    bouton_dificulter = Boutton.Button(image_mode_jouer[6], image_mode_jouer[6], (taille[0] / 2) - 50, (taille[1] / 2) +
                                       110, LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU)
    bouton_dificulter.affichage_du_bouton(window_surface)

    bouton_retour = Boutton.Button(image_mode_jouer[7], image_mode_jouer[7],
                                   (taille[0]/12), (taille[1] - (taille[1]/6)), 75, 75)
    bouton_retour.affichage_du_bouton(window_surface)

    pygame.display.flip()
    launched = True
    while launched:
        musique(
            "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/"
            "ressources/son/maxkomusic-medieval-fantasy.wav",
            0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_jvj.reactangle.collidepoint(event.pos):
                    launched = False
                    jeux = 1
                    choix_menu = JOUER
                elif event.button == 1 and bouton_jvo.reactangle.collidepoint(event.pos):
                    launched = False
                    jeux = 2
                    choix_menu = JOUER
                    break
                elif event.button == 1 and bouton_dificulter.reactangle.collidepoint(event.pos):
                    launched = False
                    choix_menu = MENU_DIFICULTER
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
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_ECRAN)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])
    image_menu_difficulter = tableau_image()

    bouton_titre_difficulter = Boutton.Button(image_menu_difficulter[0], image_menu_difficulter[0], (taille[0] / 2) -
                                              140, (taille[1] / 2) - 400, LONGUEUR_TITRE, LARGEUR_TITRE)
    bouton_titre_difficulter.affichage_du_bouton(window_surface)

    bouton_difficulter_facile = Boutton.Button(image_menu_difficulter[6], image_menu_difficulter[6],
                                               (taille[0] / 2) - 50, (taille[1] / 2) - 30, LONGUEUR_BOUTON_MENU,
                                               LARGEUR_BOUTON_MENU)
    bouton_difficulter_facile.affichage_du_bouton(window_surface)

    bouton_difficulter_moyen = Boutton.Button(image_menu_difficulter[6], image_menu_difficulter[6],
                                              (taille[0] / 2) - 50, (taille[1] / 2) + 40, LONGUEUR_BOUTON_MENU,
                                              LARGEUR_BOUTON_MENU)
    bouton_difficulter_moyen.affichage_du_bouton(window_surface)

    bouton_difficulter_difficile = Boutton.Button(image_menu_difficulter[6], image_menu_difficulter[6],
                                                  (taille[0] / 2) - 50, (taille[1] / 2) + 110, LONGUEUR_BOUTON_MENU,
                                                  LARGEUR_BOUTON_MENU)
    bouton_difficulter_difficile.affichage_du_bouton(window_surface)

    bouton_retour = Boutton.Button(image_menu_difficulter[7], image_menu_difficulter[7],
                                   (taille[0] / 12), (taille[1] - (taille[1] / 6)), 75, 75)
    bouton_retour.affichage_du_bouton(window_surface)

    pygame.display.flip()
    launched = True
    while launched:
        musique(
            "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/"
            "ressources/son/maxkomusic-medieval-fantasy.wav",
            0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_difficulter_facile.reactangle.collidepoint(event.pos):
                    launched = False
                    NIVEAU_DIFICULTER = 1
                elif event.button == 1 and bouton_difficulter_moyen.reactangle.collidepoint(event.pos):
                    launched = False
                    NIVEAU_DIFICULTER = 2
                    break
                elif event.button == 1 and bouton_difficulter_difficile.reactangle.collidepoint(event.pos):
                    launched = False
                    NIVEAU_DIFICULTER = 3
                    break
                elif event.button == 1 and bouton_retour.rectangle.collidepoint(event.pos):
                    launched = False
                    choix_menu = MENU_JOUER
                    break
        if launched == False:
            break
        pygame.display.flip()
    return choix_menu, NIVEAU_DIFICULTER


'#MENU DE L AGE I'


def age_2():
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_JEUX)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])
    image_carte = tableau_image()

    for i in range(6):
        bouton_carte = Boutton.Button(image_carte[8], image_carte[8], (taille[0]/2) - (260 - 100*i), (taille[1]/2) - 400, 90, 140)
        bouton_carte.affichage_du_bouton(window_surface)

    for i in range(5):
        bouton_carte = Boutton.Button(image_carte[9], image_carte[9], (taille[0]/2) - (210 - 100*i), (taille[1]/2) - 340, 90, 140)
        bouton_carte.affichage_du_bouton(window_surface)

    for i in range(4):
        bouton_carte = Boutton.Button(image_carte[8], image_carte[8], (taille[0]/2) - (160 - 100*i), (taille[1]/2) - 280, 90, 140)
        bouton_carte.affichage_du_bouton(window_surface)

    for i in range(3):
        bouton_carte = Boutton.Button(image_carte[9], image_carte[9], (taille[0]/2) - (110 - 100*i), (taille[1]/2) - 220, 90, 140)
        bouton_carte.affichage_du_bouton(window_surface)

    for i in range(2):
        bouton_carte = Boutton.Button(image_carte[8], image_carte[8], (taille[0]/2) - (60 - 100*i), (taille[1]/2) - 160, 90, 140)
        bouton_carte.affichage_du_bouton(window_surface)

    pygame.display.flip()
    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False


age_2()
