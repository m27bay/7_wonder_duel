"""
fichier principale
"""

from src.utils.Jeu import Jeu
from src.utils.Joueur import Joueur


if __name__ == '__main__':
	j1 = Joueur("pierre")
	j2 = Joueur("paul")
	jeu = Jeu(j1, j2)
	jeu.lancer()
	