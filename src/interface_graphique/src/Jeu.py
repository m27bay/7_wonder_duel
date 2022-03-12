from src.interface_graphique.src.Fenetre import Fenetre
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

if __name__ == '__main__':
	plateau = Plateau(Joueur("j1"), Joueur("j2"))
	
	# plateau.age = 2
	plateau.age = 3
	
	plateau.preparation_plateau()
	
	fenetre = Fenetre("test", plateau)
	fenetre.boucle_principale()
