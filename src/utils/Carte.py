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

	def constructeur_par_copie(self):
		carte = Carte(None, None, None, None, None, None)
		
		carte.nom = self.nom
		
		if self.effets is not None:
			carte.effets = self.effets.copy()
		if self.couts is not None:
			carte.couts = self.couts.copy()
		
		carte.nom_carte_chainage = self.nom_carte_chainage
		carte.couleur = self.couleur
		carte.age = self.age
		carte.est_face_cachee = self.est_face_cachee
		
		return carte
		
	def __eq__(self, other):
		if isinstance(other, Carte):
			return self.nom == other.nom \
				and self.effets == other.effets \
				and self.couts == other.couts \
				and self .nom_carte_chainage == other.nom_carte_chainage \
				and self.couleur == other.couleur \
				and self.age == other.age \
				and self.est_face_cachee == other.est_face_cachee
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
	