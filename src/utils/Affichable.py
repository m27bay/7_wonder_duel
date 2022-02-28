"""
Fichier de la classe Affichable.
"""


class Affichable:
	"""
	Classe Affichable.
	Stocke le nom et le chemin de l'image des objets present dans
	le plateau comme les cartes, les merveilles, les jetons.
	"""
	
	def __init__(self, nom, chemin_image):
		self.nom = nom
		self.chemin_image = chemin_image
		