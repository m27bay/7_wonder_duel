from src.interface_graphique.src.Fenetre import Fenetre
from src.utils.Constantes import CARTES_AGE_I
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

if __name__ == '__main__':
	plateau = Plateau(Joueur("j1"), Joueur("j2"))
	
	# plateau.age = 2
	# plateau.age = 3
	
	plateau.preparation_plateau()
	# plateau.cartes_plateau = [
	# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	# 	[CARTES_AGE_I[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	# ]
	plateau.joueur_qui_joue = plateau.joueur1
	
	fenetre = Fenetre("test", plateau)
	fenetre.boucle_principale()
