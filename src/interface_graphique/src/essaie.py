import pygame

pygame.init()


def musique():
    window = (640, 400)
    window2 = pygame.display.set_mode(window)
    music = pygame.mixer.Sound("../ressources/son/musique_boba.ogg")
    music.play()

    pygame.display.flip()

    launched = True
    while launched:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                launched = False




if __name__ == '__main__':
    musique()

