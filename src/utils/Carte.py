"""
Fichier de la classe.
"""


class Carte:
	"""
	Classe representant une carte.
	"""
	
	def __init__(self, nom, effets, couts, nom_carte_chainage, couleur, age):
		"""
		Constructeur de la classe Carte.

		:param nom: nom de la carte.
		:param effets: liste d effets que donne la carte respectant un pattern precis.
		:param couts: liste de couts pour construire la carte respactant un pattern precis.
		:param nom_carte_chainage: nom de la carte permettant de construire gratuitement la carte.
		:param couleur: couleur de la carte.
		:param age: age de la carte (entre 1 et 3).
		"""
		
		self.nom = nom
		self.effets = effets
		self.couts = couts
		self.nom_carte_chainage = nom_carte_chainage
		self.couleur = couleur
		self.age = age
		self.est_face_cachee = False
	
	def devoiler(self):
		"""
		Devoile la carte, indique que la carte n est plus face cachee.
		"""
		self.est_face_cachee = False
	
	def cacher(self):
		"""
		Cacher la carte, indique que la carte est face cachee.
		"""
		self.est_face_cachee = True
	
	def __eq__(self, other):
		"""
		Redefinition de l operateur == pour une Carte.
		Deux cartes sont identiques si elles ont le meme nom.

		:param other: une autre carte a comparer.
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
			f"effets : {str(self.effets)}, " \
			f"couts : {str(self.couts)}, " \
			f"cout chainage : {self.nom_carte_chainage}, " \
			f"couleur : {self.couleur}, " \
			f"age : {self.age}, " \
			f"face cachee : {self.est_face_cachee}"
	