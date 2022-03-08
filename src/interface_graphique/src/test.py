import pygame
import Boutton

FOND_JEUX = "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/image/fond-jeux.jpg"

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

def tableau_musique():
    tab_musique = [
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/maxkomusic-medieval-fantasy.wav",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/musique_boba.wav",
        "/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/resistance.wav"

    ]
    return tab_musique


def popl():
    sound1 = pygame.mixer.Sound("/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/musique_boba.wav")
    sound1.play()

def musique():
    mus = tableau_musique()
    tempo = len(mus)
    for i in range(tempo):
        tempo_musique = pygame.mixer.Sound(mus[i])
        tempo_musique.play()
        if i == tempo:
            tempo = 0

def playlist():
    sound1 = pygame.mixer.Sound("/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/musique_boba.wav")
    sound2 = pygame.mixer.Sound("/home/chalaud/Bureau/git/projet_perso/interface_graphique_python/ressources/son/resistance.wav")
    pygame.mixer.find_channel(True).play(sound1)

pygame.init()


pygame.mixer.init()

launched = True
while launched:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False


'#affichage pour superpose des cartes pour les cartes du joueurs'
def affichage_age1():
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_JEUX)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])
    image_carte = tableau_image()

    bouton_carte1 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 140, (taille[1] / 2) - 400,
                                   90, 140)
    bouton_carte1.affichage_du_bouton(window_surface)

    bouton_carte2 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 140, (taille[1] / 2) - 370,
                                   90, 140)
    bouton_carte2.affichage_du_bouton(window_surface)

    pygame.display.flip()
    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False

def affichage_age1():
    taille = taille_ecran()
    window_surface = pygame.display.set_mode(taille)
    backgroud = pygame.image.load(FOND_JEUX)
    backgroud.convert()
    window_surface.blit(backgroud, [0, 0])
    image_carte = tableau_image()

    bouton_carte1 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 260, (taille[1] / 2) - 400,
                                   90, 140)
    bouton_carte1.affichage_du_bouton(window_surface)

    bouton_carte2 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 160, (taille[1] / 2) - 400,
                                   90, 140)
    bouton_carte2.affichage_du_bouton(window_surface)

    bouton_carte3 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 60, (taille[1] / 2) - 400,
                                   90, 140)
    bouton_carte3.affichage_du_bouton(window_surface)

    bouton_carte4 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) + 40, (taille[1] / 2) - 400,
                                   90, 140)
    bouton_carte4.affichage_du_bouton(window_surface)

    bouton_carte5 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) + 140, (taille[1] / 2) - 400,
                                   90, 140)
    bouton_carte5.affichage_du_bouton(window_surface)

    bouton_carte6 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) + 240, (taille[1] / 2) - 400,
                                   90, 140)
    bouton_carte6.affichage_du_bouton(window_surface)

    bouton_carte7 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) - 210, (taille[1] / 2) - 340,
                                   90, 140)
    bouton_carte7.affichage_du_bouton(window_surface)

    bouton_carte8 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) - 110, (taille[1] / 2) - 340,
                                   90, 140)
    bouton_carte8.affichage_du_bouton(window_surface)

    bouton_carte9 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) - 10, (taille[1] / 2) - 340,
                                   90, 140)
    bouton_carte9.affichage_du_bouton(window_surface)

    bouton_carte10 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) + 90, (taille[1] / 2) - 340, 90, 140)
    bouton_carte10.affichage_du_bouton(window_surface)

    bouton_carte11 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) + 190, (taille[1] / 2) - 340, 90, 140)
    bouton_carte11.affichage_du_bouton(window_surface)

    bouton_carte12 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 160, (taille[1] / 2) - 280, 90, 140)
    bouton_carte12.affichage_du_bouton(window_surface)

    bouton_carte13 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 60, (taille[1] / 2) - 280, 90, 140)
    bouton_carte13.affichage_du_bouton(window_surface)

    bouton_carte14 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) + 40, (taille[1] / 2) - 280,
                                   90, 140)
    bouton_carte14.affichage_du_bouton(window_surface)

    bouton_carte15 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) + 140, (taille[1] / 2) - 280,
                                   90, 140)
    bouton_carte15.affichage_du_bouton(window_surface)

    bouton_carte16 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) - 110, (taille[1] / 2) - 220,
                                   90, 140)
    bouton_carte16.affichage_du_bouton(window_surface)

    bouton_carte17 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) - 10, (taille[1] / 2) - 220,
                                   90, 140)
    bouton_carte17.affichage_du_bouton(window_surface)

    bouton_carte18 = Boutton.Button(image_carte[9], image_carte[9], (taille[0] / 2) + 90, (taille[1] / 2) - 220,
                                    90, 140)
    bouton_carte18.affichage_du_bouton(window_surface)

    bouton_carte19 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) - 60, (taille[1] / 2) - 160,
                                    90, 140)
    bouton_carte19.affichage_du_bouton(window_surface)

    bouton_carte20 = Boutton.Button(image_carte[8], image_carte[8], (taille[0] / 2) +40, (taille[1] / 2) - 160,
                                    90, 140)
    bouton_carte20.affichage_du_bouton(window_surface)


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
