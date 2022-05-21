import pygame

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
MENU_DIFFICULTE = 3
JOUER_JVO = 5
JOUER_JVJ = 6


def musique():

    pygame.mixer.init()

    playlist = [
        "src/interface_graphique/ressources/sons/Thomas-Bergersen-Immortal-_2011_.wav",
        "src/interface_graphique/ressources/sons/Two-Steps-From-Hell-Protectors-of-the-Earth.wav",
        "src/interface_graphique/ressources/sons/maxkomusic-medieval-fantasy.wav"
    ]

    # Get the first track from the playlist
    pygame.mixer.music.load(playlist.pop())
    pygame.mixer.music.queue(playlist.pop())  # Queue the 2nd song
    pygame.mixer.music.set_endevent(
        pygame.USEREVENT)  # Setup the end track event
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
    "src/interface_graphique/ressources/images/image_menu/Verre.jpg",
    "src/interface_graphique/ressources/images/image_menu/Alea.xcf",
    "src/interface_graphique/ressources/images/image_menu/Alea_off.xcf"
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
    global MUTE_SOUND
    choix_menu = None
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    background = pygame.image.load(FOND_ECRAN)
    background.convert()
    window_surface.blit(background, [0, 0])

    image_menu = tableau_image()

    bouton_titre = Boutton.Button(image_menu[0], image_menu[0], (taille[0]/2)-175, (taille[1]/2)-400,
                                  LONGUEUR_TITRE, LARGEUR_TITRE
                                  )
    bouton_titre.affichage_du_bouton(window_surface)

    bouton_jouer = Boutton.Button(image_menu[1], image_menu[1], (taille[0]/2)-75, taille[1]/2,
                                  LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU
                                  )
    bouton_jouer.affichage_du_bouton(window_surface)

    bouton_quitter = Boutton.Button(image_menu[3], image_menu[3], (taille[0]/2)-75, (taille[1]/2) + 140,
                                    LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU
                                    )

    bouton_quitter.affichage_du_bouton(window_surface)

    window_tempo = window_surface

    if MUTE_SOUND == 0:

        bouton_son_on = Boutton.Button(
            image_menu[4], image_menu[4], (taille[0]/12), (taille[1] - (taille[1]/6)), 150, 115)
        bouton_son_on.affichage_du_bouton(window_surface)

        bouton_son_off = Boutton.Button(
            image_menu[5], image_menu[5], (taille[0]/12), (taille[1] - (taille[1]/6)), 150, 115)

    elif MUTE_SOUND == 1:

        bouton_son_off = Boutton.Button(image_menu[5], image_menu[5], (taille[0] / 12), (taille[1] - (taille[1] / 6)),
                                        150, 115)

        bouton_son_off.affichage_du_bouton(window_surface)

        bouton_son_on = Boutton.Button(image_menu[4], image_menu[4], (taille[0] / 12), (taille[1] - (taille[1] / 6)),
                                       150, 115)

    pygame.display.flip()
    status_son = 0
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_son_on.rectangle.collidepoint(event.pos) and status_son == 0:
                    bouton_son_off.affichage_du_bouton(window_tempo)
                    pygame.mixer.music.pause()
                    status_son = 1
                    MUTE_SOUND = 1
                    break
                elif event.button == 1 and bouton_son_on.rectangle.collidepoint(event.pos) and status_son == 1:
                    bouton_son_on.affichage_du_bouton(window_tempo)
                    pygame.mixer.music.unpause()
                    status_son = 0
                    MUTE_SOUND = 0
                    break
                elif event.button == 1 and bouton_quitter.rectangle.collidepoint(event.pos):
                    en_cours = False
                elif event.button == 1 and bouton_jouer.rectangle.collidepoint(event.pos):
                    en_cours = False
                    choix_menu = MENU_JOUER
                    break
        if not en_cours:
            break
        pygame.display.flip()
    return choix_menu


'#MENU DU BOUTON OPTIONS'


def affichage_mode_jouer():
    choix_menu = None
    merveille_aleatoire = True
    jeux = 0
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    background = pygame.image.load(FOND_ECRAN)
    background.convert()
    window_surface.blit(background, [0, 0])
    image_mode_jouer = tableau_image()

    bouton_titre_jouer = Boutton.Button(image_mode_jouer[0], image_mode_jouer[0], (taille[0]/2)-175, (taille[1]/2)-400,
                                        LONGUEUR_TITRE, LARGEUR_TITRE
                                        )

    bouton_titre_jouer.affichage_du_bouton(window_surface)

    bouton_jvj = Boutton.Button(image_mode_jouer[7], image_mode_jouer[7], (taille[0]/2)-75, (taille[1]/2-30),
                                LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU
                                )

    bouton_jvj.affichage_du_bouton(window_surface)

    bouton_jvo = Boutton.Button(image_mode_jouer[6], image_mode_jouer[6], (taille[0]/2)-75, (taille[1]/2)+170,
                                LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU
                                )
    bouton_jvo.affichage_du_bouton(window_surface)

    bouton_retour = Boutton.Button(image_mode_jouer[8], image_mode_jouer[8],
                                   (taille[0]/12), (taille[1] -
                                                    (taille[1]/6)), 90, 90
                                   )
    bouton_retour.affichage_du_bouton(window_surface)

    window_tempo = window_surface

    bouton_merveille_aleatoire_non = Boutton.Button(image_mode_jouer[19], image_mode_jouer[19], (taille[0] / 2) - 75, (taille[1] / 2) + 70,
                                                    LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU
                                                    )
    bouton_merveille_aleatoire_non.affichage_du_bouton(window_surface)

    bouton_merveille_aleatoire_oui = Boutton.Button(image_mode_jouer[18], image_mode_jouer[18], (taille[0] / 2) - 75,
                                                    (taille[1] / 2) +
                                                    70, LONGUEUR_BOUTON_MENU, LARGEUR_BOUTON_MENU
                                                    )

    status_aleatoire = 0
    pygame.display.flip()
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_jvj.rectangle.collidepoint(event.pos):
                    en_cours = False
                    jeux = 1
                    choix_menu = JOUER_JVJ
                    break

                elif event.button == 1 and bouton_jvo.rectangle.collidepoint(event.pos):
                    en_cours = False
                    jeux = 2
                    choix_menu = JOUER_JVO
                    break

                elif event.button == 1 and bouton_merveille_aleatoire_non.rectangle.collidepoint(event.pos) and status_aleatoire == 0:
                    bouton_merveille_aleatoire_oui.affichage_du_bouton(
                        window_tempo)
                    merveille_aleatoire = False
                    print("changement alea")
                    status_aleatoire = 1
                    break

                elif event.button == 1 and bouton_merveille_aleatoire_non.rectangle.collidepoint(event.pos) and status_aleatoire == 1:
                    bouton_merveille_aleatoire_non.affichage_du_bouton(
                        window_tempo)
                    merveille_aleatoire = True
                    print("changement alea")
                    status_aleatoire = 0
                    break

                elif event.button == 1 and bouton_retour.rectangle.collidepoint(event.pos):
                    en_cours = False
                    choix_menu = MENU_ACCUEILLE
                    break

        if not en_cours:
            break
        pygame.display.flip()
    return choix_menu, jeux, merveille_aleatoire


'#MENU DU BOUTON DIFFICULTE'


def affichage_menu_difficulte():
    choix_menu = None
    niveau_diff = 0
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    background = pygame.image.load(FOND_ECRAN)
    background.convert()
    window_surface.blit(background, [0, 0])
    image_menu_difficulte = tableau_image()

    bouton_titre_difficulte = Boutton.Button(image_menu_difficulte[0], image_menu_difficulte[0], (taille[0] / 2) -
                                             175, (taille[1] / 2) -
                                             400, LONGUEUR_TITRE, LARGEUR_TITRE
                                             )

    bouton_titre_difficulte.affichage_du_bouton(window_surface)

    bouton_difficulte_facile = Boutton.Button(image_menu_difficulte[10], image_menu_difficulte[10],
                                              (taille[0] / 2) - 75, (taille[1] /
                                                                     2) - 30, LONGUEUR_BOUTON_MENU,
                                              LARGEUR_BOUTON_MENU
                                              )

    bouton_difficulte_facile.affichage_du_bouton(window_surface)

    bouton_difficulte_moyen = Boutton.Button(image_menu_difficulte[11], image_menu_difficulte[11],
                                             (taille[0] / 2) - 75, (taille[1] /
                                                                    2) + 70, LONGUEUR_BOUTON_MENU,
                                             LARGEUR_BOUTON_MENU
                                             )

    bouton_difficulte_moyen.affichage_du_bouton(window_surface)

    bouton_difficulte_difficile = Boutton.Button(image_menu_difficulte[12], image_menu_difficulte[12],
                                                 (taille[0] / 2) - 75, (taille[1] /
                                                                        2) + 170, LONGUEUR_BOUTON_MENU,
                                                 LARGEUR_BOUTON_MENU
                                                 )

    bouton_difficulte_difficile.affichage_du_bouton(window_surface)

    bouton_retour = Boutton.Button(image_menu_difficulte[8], image_menu_difficulte[8],
                                   (taille[0] / 12), (taille[1] - (taille[1] / 6)), 90, 90)
    bouton_retour.affichage_du_bouton(window_surface)

    pygame.display.flip()
    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bouton_difficulte_facile.rectangle.collidepoint(event.pos):
                    en_cours = False
                    niveau_diff = 5
                    choix_menu = MENU_DIFFICULTE
                    break

                elif event.button == 1 and bouton_difficulte_moyen.rectangle.collidepoint(event.pos):
                    en_cours = False
                    niveau_diff = 7
                    choix_menu = MENU_DIFFICULTE
                    break

                elif event.button == 1 and bouton_difficulte_difficile.rectangle.collidepoint(event.pos):
                    en_cours = False
                    niveau_diff = 9
                    choix_menu = MENU_DIFFICULTE
                    break

                elif event.button == 1 and bouton_retour.rectangle.collidepoint(event.pos):
                    en_cours = False
                    choix_menu = MENU_JOUER
                    break

        if not en_cours:
            break
        pygame.display.flip()
    return choix_menu, niveau_diff


def joueur_vs_ordi(difficulte, merveille_aleatoire):
    plateau = Plateau(Joueur("joueur"), Joueur("ordi"), merveille_aleatoire)
    plateau.preparation_plateau()
    fenetre = Fenetre("7 wonder Duel", plateau, difficulte)
    fenetre.boucle_principale()


def joueur_vs_joueur(merveille_aleatoire):
    plateau = Plateau(Joueur("joueur"), Joueur("ordi"), merveille_aleatoire)
    plateau.preparation_plateau()
    fenetre = Fenetre("7 wonder Duel", plateau, 1, True)
    fenetre.boucle_principale()


def affichage_ensemble():
    pygame.init()

    running = True

    quel_menu = MENU_ACCUEILLE

    niveau_difficulte = -1
    merveille_aleatoire = False

    musique()
    while running:
        if quel_menu == MENU_ACCUEILLE:
            quel_menu = affichage_menu_accueille()

        elif quel_menu == MENU_JOUER:
            quel_menu, mode_de_jeux, merveille_aleatoire = affichage_mode_jouer()

        elif quel_menu == JOUER_JVO:
            quel_menu, niveau_difficulte = affichage_menu_difficulte()

        elif quel_menu == JOUER_JVJ:
            joueur_vs_joueur(merveille_aleatoire)
            break

        elif quel_menu == MENU_DIFFICULTE:
            joueur_vs_ordi(niveau_difficulte, merveille_aleatoire)
            break

        else:
            break


'#affichage_mode_jouer()'
if __name__ == '__main__':
    affichage_ensemble()
