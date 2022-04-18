from src.interface_graphique.src.Fenetre import Fenetre
from src.logger.Logger import LOGGER
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

if __name__ == '__main__':
	plateau = Plateau(Joueur("joueur"), Joueur("ordi"))
	plateau.preparation_plateau()
	
	fenetre = Fenetre("7 wonder Duel", plateau)
	fenetre.boucle_principale()
	