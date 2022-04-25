import pygame

from src.interface_graphique.src.SpriteCarte import SpriteCarte
from src.utils.Carte import Carte


class FenetreDefausserCarteCouleur:
	def __init__(self):
		pygame.init()
		
		self.ecran = pygame.display.set_mode((600, 400))
		
	def set_liste_sprite_carte(self, liste_sprite_carte: pygame.sprite.Group):
		self.liste_sprite_carte = pygame.sprite.Group()
		for sprite_carte in liste_sprite_carte:
			if isinstance(sprite_carte, SpriteCarte):
				sprite = SpriteCarte(sprite_carte.carte, sprite_carte.haut_gauche_x,
					sprite_carte.haut_gauche_y, sprite_carte.ration_longeur_fenetre)
				self.liste_sprite_carte.add(sprite)
		
	def dessiner_cartes(self):
		coordx = 0
		coordy = 0
		cpt = 0
		for carte in self.liste_sprite_carte:
			if isinstance(carte, SpriteCarte):
				carte.changer_coords(coordx, coordy)
				cpt += 1
				if cpt == 4:
					cpt = 0
					coordx = 0
					coordy += carte.haut + 10
				else:
					coordx += carte.larg + 10
				
	def adapter_fenetre(self):
		larg, haut =
		self.ecran = pygame.display.set_mode((4 * self.liste_sprite_carte[0].larg, ))
		
	def boucler_principale(self):
		en_cours = True
		
		while en_cours:
			# PARTIE Process input (events)
			for event in pygame.event.get():
				
				# quitter avec la croix
				if event.type == pygame.QUIT:
					en_cours = False
					
			self.liste_sprite_carte.update()
			self.liste_sprite_carte.draw(self.ecran)
			
			pygame.display.flip()
		
		pygame.quit()
	