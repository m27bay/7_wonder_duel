"""
Ensembles des constantes utilisees dans le jeu.
"""
from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres
from src.utils.JetonMilitaire import JetonMilitaire


JETONS_MILITAIRES = [
	JetonMilitaire("5piecesJ1", None, 5, 10),
	JetonMilitaire("2piecesJ1", None, 2, 5),
	JetonMilitaire("0piecesJ1", None, 0, 2),
	JetonMilitaire("0piecesJ2", None, 0, 2),
	JetonMilitaire("2piecesJ2", None, 2, 5),
	JetonMilitaire("5piecesJ2", None, 5, 10)
]

JETONS_PROGRES = [
	JetonProgres("agriculture", None, ["monnaie 6", "point_victoire 4"]),
	JetonProgres("architecture", None, ["reduc_merveille"]),
	JetonProgres("economie", None, ["gain_monnaie_adversaire"]),
	JetonProgres("loi", None, ["symbole_scientifique"]),
	JetonProgres("maconnerie", None, ["reduc_carte bleu"]),
	JetonProgres("philosophie", None, ["point_victoire_fin_partie 7"]),
	JetonProgres("mathematiques", None, ["point_victoire_par_jeton 3", "point_victoire 3"]),
	JetonProgres("strategie", None, ["bonus_attaque"]),
	JetonProgres("theologie", None, ["rejouer"]),
	JetonProgres("urbanisme", None, ["monnaie 6", "bonus_monnaie_chainage 4"]),
]

# constructeur : Carte(nom, chemin_image, effets, couts, nom_carte_chainage, couleur, age)
CARTES_AGE_I = [
	Carte("chantier", None, ["ressource bois 1"], None, None, "marron", age=1),
	Carte("exploitation", None, ["ressource bois 1"], ["monnaie 1"], None, "marron", age=1),
	Carte("bassin argileux", None, ["ressource argile 1"], None, None, "marron", age=1),
	Carte("cavite", None, ["ressource argile 1"], ["monnaie 1"], None, "marron", age=1),
	Carte("gisement", None, ["ressource pierre 1"], None, None, "marron", age=1),
	Carte("mine", None, ["ressource pierre 1"], ["monnaie 1"], None, "marron", age=1),
	Carte("verrerie", None, ["ressource verre 1"], ["monnaie 1"], None, "grise", age=1),
	Carte("presse", None, ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1),
	Carte("tour de garde", None, ["attaquer 1"], None, None, "rouge", age=1),
	Carte("atelier", None, ["symbole_scientifique pendule", "point_victoire 1"], ["ressource papurys 1"],
		None, "vert", age=1),
	Carte("apothicaire", None, ["symbole_scientifique roue", "point_victoire 1"], ["ressource verre 1"],
		None, "vert", age=1),
	Carte("depot de pierre", None, ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1),
	Carte("depot d argile", None, ["reduc_ressource argile 1"], ["monnaie 3"], None, "jaune", age=1),
	Carte("depot de bois", None, ["reduc_ressource bois 1"], ["monnaie 3"], None, "jaune", age=1),
	Carte("ecuries", None, ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1),
	Carte("caserne", None, ["attaquer 1"], ["ressource argile 1"], None, "rouge", age=1),
	Carte("palissade", None, ["attaquer 1"], ["monnaie 2"], None, "rouge", age=1),
	Carte("scriptorium", None, ["symbole_scientifique plume"], ["monnaie 2"], None, "vert", age=1),
	Carte("officine", None, ["symbole_scientifique pilon"], ["monnaie 2"], None, "vert", age=1),
	Carte("theatre", None, ["point_victoire 3"], None, None, "blue", age=1),
	Carte("autel", None, ["point_victoire 3"], None, None, "blue", age=1),
	Carte("bains", None, ["point_victoire 3"], ["ressource pierre 1"], None, "bleu", age=1),
	Carte("taverne", None, ["monnaie 4"], None, None, "jaune", age=1)
]

CARTES_AGE_II = [
	Carte("scierie", None, ["ressource bois 2"], ["monnaie 2"], None, "marron", age=2),
	Carte("briqueterie", None, ["ressource argile 2"], ["monnaie 2"], None, "marron", age=2),
	Carte("carriere", None, ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2),
	Carte("soufflerie", None, ["ressource verre 1"], None, None, "gris", age=2),
	Carte("sechoir", None, ["ressource papyrus 1"], None, None, "gris", age=2),
	Carte("muraille", None, ["attaquer 2"], ["ressource pierre 2"], None, "rouge", age=2),
	Carte("forum", None, ["ressource_au_choix verre papyrus"], ["monnaie 3", "ressource argile 1"],
		None, "jaune", age=2),
	Carte("caravanserail", None, ["ressource_au_choix bois argile pierre"],
		["monnaie 2", "ressource verre 1", "ressource papyrus 1"], None, "jaune", age=2),
	Carte("douanes", None, ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
		None, "jaune", age=2),
	Carte("tribunal", None, ["point_victoire 5"], ["ressource bois 2", "ressource verre 1"], None,
		"bleu", age=2),
	Carte("haras", None, ["attaquer 1"], ["ressource argile 1", "ressource bois 1"], "ecuries", "rouge", age=2),
	Carte("baraquements", None, ["attaquer 1"], ["monnaie 3"], "caserne", "rouge", age=2),
	Carte("champ de tir", None, ["attaquer 2"],
		["ressource pierre 1", "ressource bois 1", "ressource papyrus 1"],
		None, "rouge", age=2),
	Carte("place d'armes", None, ["attaquer 2"], ["ressource argile 2", "ressource verre 1"], None, "rouge",
		age=2),
	Carte("bibliotheque", None, ["symbole_scientifique plume", "point_victoire 2"],
		["ressource pierre 1", "ressource bois 1", "ressource verre 1"], "scriptorium", "vert", age=2),
	Carte("dispensaire", None, ["symbole_scientifique pilon", "point_victoire 2"],
		["ressource argile 2", "ressource verre 1"], "officine", "vert", age=2),
	Carte("ecole", None, ["symbole_scientifique roue", "point_victoire 1"],
		["ressource papyrus 2", "ressource bois 1"], None, "vert", age=2),
	Carte("laboratoire", None, ["symbole_scientifique pendule", "point_victoire 1"],
		["ressource verre 2", "ressource bois 1"], None, "vert", age=2),
	Carte("statue", None, ["point_victoire 4"], ["ressource argile 2"], "theatre", "bleu", age=2),
	Carte("temple", None, ["point_victoire 4"], ["ressource papyrus 1", "ressource bois 1"], "autel",
		"bleu", age=2),
	Carte("aqueduc", None, ["point_victoire 5"], ["ressource pierre 3"], "bains", "bleu", age=2),
	Carte("rostres", None, ["point_victoire 4"], ["ressource pierre 1", "ressource bois 1"],
		None, "bleu", age=2),
	Carte("brasserie", None, ["monnaie 6"], None, "taverne", "jaune", age=2)
]

CARTES_AGE_III = [
	Carte("arsenal", None, ["attaquer 3"], ["ressource argile 3", "ressource bois 2"], None, "rouge", age=3),
	Carte("pretoire", None, ["attaquer 3"], ["monnaie 8"], None, "rouge", age=3),
	Carte("academie", None, ["symbole_scientifique cadran_solaire", "point_victoire 3"],
		["ressource pierre 1", "ressource bois 1", "ressource verre 2"], None, "vert", age=3),
	Carte("etude", None, ["symbole_scientifique cadran_solaire", "point_victoire 3"],
		["ressource papyrus 1", "ressource bois 2", "ressource verre 1"], None, "vert", age=3),
	Carte("chambre de commerce", None, ["monnaie_par_carte grise 3", "point_victoire 3"],
		["ressource papyrus 2"], None, "jaune", age=3),
	Carte("port", None, ["monnaie_par_carte marron 2", "point_victoire 3"],
		["ressource verre 1", "ressource bois 1", "ressource papyrus 1"], None, "jaune", age=3),
	Carte("armurie", None, ["monnaie_par_carte rouge 1", "point_victoire 3"],
		["ressource pierre 2", "ressource verre 1"], None, "jaune", age=3),
	Carte("palace", None, ["point_victoire 7"],
		["ressource argile 1", "ressource pierre 1", "ressource bois 1", "ressource verre 2"],
		None, "bleu", age=3),
	Carte("hôtel de ville", None, ["point_victoire 7"], ["ressource pierre 3", "ressource bois 2"],
		None, "bleu", age=3),
	Carte("obelisque", None, ["point_victoire 5"], ["ressource pierre 2", "ressource verre 1"],
		None, "bleu", age=3),
	Carte("fortification", None, ["attaquer 2"],
		["ressource pierre 2", "ressource argile 1", "ressource papyrus 1"],
		"palissade", "rouge", age=3),
	Carte("atelier de siege", None, ["attaquer 2"], ["ressource bois 3", "ressource verre 1"],
		"champ de tir", "rouge", age=3),
	Carte("cirque", None, ["attaquer 2"], ["ressource argile 2", "ressource pierre 2"],
		"place d'arme", "rouge", age=3),
	Carte("universite", None, ["symbole_scientifique sphere_armillaire", "point_victoire 2"],
		["ressource argile 1", "ressource verre 1", "ressource papyrus 1"], "ecole", "vert", age=3),
	Carte("observatoire", None, ["symbole_scientifique sphere_armillaire", "point_victoire 2"],
		["ressource pierre 1", "ressource papyrus 2"], "laboratoire", "vert", age=3),
	Carte("jardin", None, ["point_victoire 6"], ["ressource argile 2", "ressource bois 2"], "statue",
		"bleu", age=3),
	Carte("pantheon", None, ["point_victoire 6"],
		["ressource argile 1", "ressource bois 1", "ressource papyrus 2"],
		"temple", "bleu", age=3),
	Carte("senat", None, ["point_victoire 5"],
		["ressource argile 2", "ressource pierre 1", "ressource papyrus 2"],
		"rostres", "bleu", age=3),
	Carte("phare", None, ["monnaie_par_carte jaune 1", "point_victoire 3"],
		["ressource argile 2", "ressource verre 1"], "taverne", "jaune", age=3),
	Carte("arene", None, ["monnaie_par_merveille 2", "point_victoire 3"],
		["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3),
]

CARTES_GUILDE = [
	CarteFille("guild des commercants", None,
		["effet_guild_commercants 1"],
		["ressource argile 1", "ressource bois 1", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("guild des armateurs", None,
		["effet_guild_armateurs 1"],
		["ressource argile 1", "ressource pierre 1", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("guild des batisseurs", None,
		["effet_guild_batisseurs 1"],
		["ressource pierre 2", "ressource argile 1", "ressource bois 1",
			"ressource papyrus 1", "ressource verre 1"]
	),
	CarteFille("guild des magistrats", None,
		["effet_guild_magistrats 1"],
		["ressource bois 2", "ressource argile 1", "ressource papyrus 1"]
	),
	CarteFille("guild des scientifiques", None,
		["effet_guild_scientifiques 1"],
		["ressource argile 2", "ressource bois 2"]
	),
	CarteFille("guild des usuriers", None,
		["effet_guild_usuriers 1"],
		["ressource pierre 2", "ressource bois 2"]
	),
	CarteFille("guild des tacticiens", None,
		["effet_guild_tacticiens 1"],
		["ressource pierre 2", "ressource argile 1", "ressource papyrus 1"]
	)
]

# constructeur : CarteFille(nom, chemin_image, effets)
MERVEILLES = [
	CarteFille("circus maximus", None,
		["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
		["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
	),
	CarteFille("colosse", None,
		["attaquer 2", "point_victoire 3"],
		["ressource argile 3", "ressource verre 1"]
	),
	CarteFille("grand phare", None,
		["ressource_au_choix bois argile pierre", "point_victoire 4"],
		["ressource bois 1", "ressource pierre 1", "ressource papyrus 2"]
	),
	CarteFille("jardin suspendus", None,
		["monnaie 6", "rejouer", "point_victoire 3"],
		["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("grande bibliotheque", None,
		["jeton_progres_aleatoire", "point_victoire 4"],
		["ressource bois 3", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("mausolee", None,
		["construction_fausse_gratuite", "point_victoire 2"],
		["ressource argile 2", "ressource verre 2", "ressource papyrus 1"]
	),
	CarteFille("piree", None,
		["ressource_au_choix papyrus verre", "rejouer", "point_victoire 2"],
		["ressource bois 2", "ressource pierre 1", "ressource argile 1"]
	),
	CarteFille("pyramides", None,
		["point_victoire 9"],
		["ressource pierre 3", "ressource papyrus 1"]
	),
	CarteFille("sphinx", None,
		["rejouer", "point_victoire 6"],
		["ressource pierre 1", "ressource argile 1", "ressource verre 2"]
	),
	CarteFille("statue de zeus", None,
		["defausse_carte_adversaire marron", "attaquer 1", "point_victoire 3"],
		["ressource pierre 1", "ressource bois 1",
			"ressource argile 1", "ressource papyrus 2"]
	),
	CarteFille("temple d'artemis", None,
		["monnaie 12", "rejouer"],
		["ressource bois 1", "ressource pierre 1",
			"ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("via appia", None,
		["monnaie 3", "adversaire_perd_monnaie 3", "rejouer", "point_victoire 3"],
		["ressource pierre 2", "ressource argile 2", "ressource papyrus 1"]
	)
]
