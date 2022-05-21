from src.interface_graphique.src.Fenetre import Fenetre
from src.utils.JetonProgres import JetonProgres
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

if __name__ == '__main__':
    # choix auto merveille
    # plateau = Plateau(Joueur("joueur"), Joueur("ordi"))
    plateau = Plateau(Joueur("joueur"), Joueur("ordi"), False)

    plateau.preparation_plateau()

    # facile = 5
    # normal = 7
    # difficile = 9
    fenetre = Fenetre("7 wonder Duel", plateau, 7)
    # fenetre = Fenetre("7 wonder Duel", plateau, 7, True)

    fenetre.boucle_principale()
