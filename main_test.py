from src.interface_graphique.src.Fenetre import Fenetre
from src.utils.JetonProgres import JetonProgres
from src.utils.Joueur import Joueur
from src.utils.Plateau import Plateau

if __name__ == '__main__':
    # choix auto merveille
    # plateau = Plateau(Joueur("joueur"), Joueur("ordi"))
    plateau = Plateau(Joueur("joueur"), Joueur("ordi"), False)

    plateau.preparation_plateau()

    plateau.joueur1.ressources = {
        "bois": 5,
        "pierre": 5,
        "argile": 5,
        "verre": 5,
        "papyrus": 5
    }
    plateau.joueur1.symb_scientifique = {
        "sphere_armillaire": 1,
        "roue": 1,
        "cadran_solaire": 1,
        "pilon": 1,
        "compas_maconniques": 1,
        "plume": 0
    }
    plateau.jetons_progres_plateau.clear()
    plateau.jetons_progres_plateau.append(JetonProgres(
                    "urbanisme", ["monnaie 6", "bonus_monnaie_chainage 4"]))

    # plateau.joueur1.jetons_progres.append(JetonProgres("strategie", ["bonus_attaque"]))
    # print(plateau.joueur1.possede_jeton_scientifique("strategie"))

    # facile = 5
    # normal = 7
    # difficile = 9
    # fenetre = Fenetre("7 wonder Duel", plateau, 7)
    fenetre = Fenetre("7 wonder Duel", plateau, 7, True)

    fenetre.boucle_principale()
