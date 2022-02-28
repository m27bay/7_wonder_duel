"""
Fichier de la classe.
"""
from src.utils.Affichable import Affichable


class Carte(Affichable):
	"""
	Classe representant une carte_a_enlever.
	"""
	
	def __init__(self, nom, chemin_image, effets, couts, nom_carte_chainage, couleur, age):
		"""
		Constructeur de la classe Carte.

		:param nom: nom de la carte_a_enlever.
		:param chemin_image: chemin pour afficher la carte_a_enlever.
		:param effets: liste d effets que donne la carte_a_enlever respectant un pattern precis.
		:param couts: liste de couts pour construire la carte_a_enlever respactant un pattern precis.
		:param nom_carte_chainage: nom de la carte_a_enlever permettant de construire gratuitement la carte_a_enlever.
		:param couleur: couleur de la carte_a_enlever.
		:param age: age de la carte_a_enlever (entre 1 et 3).
		"""
		super().__init__(nom, chemin_image)
		self.effets = effets
		self.couts = couts
		self.nom_carte_chainage = nom_carte_chainage
		self.couleur = couleur
		self.age = age
		self.est_face_cachee = False
	
	def devoiler(self):
		"""
		Devoile la carte_a_enlever, indique que la carte_a_enlever n est plus face cachee.
		"""
		self.est_face_cachee = False
	
	def cacher(self):
		"""
		Cacher la carte_a_enlever, indique que la carte_a_enlever est face cachee.
		"""
		self.est_face_cachee = True
	
	def __eq__(self, other):
		"""
		Redefinition de l operateur == pour une Carte.
		Deux cartes sont identiques si elles ont le meme nom.

		:param other: une autre carte_a_enlever a comparer.
		:return: vrai/ faux
		"""
		if isinstance(other, Carte):
			return self.nom == other.nom
		else:
			return False
	
	def __str__(self):
		"""
		Renvoie une chaine pour afficher les attributs.

		:return: chaine avec les attributs de la classe.
		"""
		return f"nom : {self.nom}, " \
			f"image : {self.chemin_image}, " \
			f"effets : {str(self.effets)}, " \
			f"couts : {str(self.couts)}, " \
			f"cout chainage : {self.nom_carte_chainage}, " \
			f"couleur : {self.couleur}, " \
			f"age : {self.age}, " \
			f"face cachee : {self.est_face_cachee}"
	