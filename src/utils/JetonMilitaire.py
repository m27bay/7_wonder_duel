class JetonMilitaire:
    """
    Classe representant un jeton militaire.
    """

    def __init__(self, nom, pieces, points_victoire):
        self.nom = nom
        self.est_utilise = False
        self.pieces = pieces
        self.points_victoire = points_victoire

    def __eq__(self, other):
        if isinstance(other, JetonMilitaire):
            return self.nom == other.nom \
                and self.est_utilise == other.est_utilise \
                and self.pieces == other.pieces \
                and self.points_victoire == other.points_victoire
        
        return False

    def __str__(self):
        return f"JetonMilitaire({self.nom}, {self.pieces}, {self.points_victoire}), " \
            f"est_utilise : {self.est_utilise}"

    def constructeur_par_copie(self):
        jeton = JetonMilitaire(None, None, None)

        jeton.nom = self.nom
        jeton.est_utilise = self.est_utilise
        jeton.pieces = self.pieces
        jeton.points_victoire = self.points_victoire

        return jeton
