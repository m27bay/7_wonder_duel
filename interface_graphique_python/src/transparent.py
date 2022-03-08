import pygame

pygame.init()
clock = pygame.time.Clock()

CIEL = 0, 200, 255
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0

def lol():

    fenetre = pygame.display.set_mode((640, 480))
    loop = True
    green_color = GREEN
    white_color = WHITE
    while loop:
        background = pygame.image.load("/home/chalaud/Bureau/interface_graphique_python/ressources/image/142654.jpg")
        background.convert()

        # Ajout du fond dans la fenêtre
        fenetre.blit(background, (0, 0))

        # Draw a rectangle outline
        rect_white = pygame.draw.rect(fenetre, white_color, [75, 10, 100, 50], 5)
        # Draw a solid rectangle
        rect_green = pygame.draw.rect(fenetre, green_color, [250, 10, 100, 50])

        # retourne 1 si le curseur est au dessus du rectangle
        mouse_xy = pygame.mouse.get_pos()
        over_white = rect_white.collidepoint(mouse_xy)
        over_green = rect_green.collidepoint(mouse_xy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            # si clic, le vert devient rouge
            elif event.type == pygame.MOUSEBUTTONDOWN and over_green:
                green_color = RED
            # le rectangle se cache
            elif event.type == pygame.MOUSEBUTTONDOWN and over_white:
                white_color = CIEL

        # Actualisation de l'affichage
        pygame.display.flip()
        # 10 fps
        clock.tick(10)

if __name__ == '__main__':
    lol()
