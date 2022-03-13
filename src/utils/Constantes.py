"""
Ensembles des constantes utilisees dans le jeu.
"""
from src.utils.Carte import Carte
from src.utils.CarteFille import CarteFille
from src.utils.JetonProgres import JetonProgres
from src.utils.JetonMilitaire import JetonMilitaire


SYMBOLE_SCIENTIFIQUES = [
	"sphere_armillaire",
	"roue",
	"cadran_solaire",
	"pilon",
	"pendule",
	"plume"
]

JETONS_MILITAIRES = [
	JetonMilitaire("5piecesJ1", 5, 10),
	JetonMilitaire("2piecesJ1", 2, 5),
	JetonMilitaire("0piecesJ1", 0, 2),
	JetonMilitaire("0piecesJ2", 0, 2),
	JetonMilitaire("2piecesJ2", 2, 5),
	JetonMilitaire("5piecesJ2", 5, 10)
]

JETONS_PROGRES = [
	JetonProgres("agriculture", ["monnaie 6", "point_victoire 4"]),
	JetonProgres("architecture", ["reduc_merveille"]),
	JetonProgres("economie", ["gain_monnaie_adversaire"]),
	JetonProgres("loi", ["symbole_scientifique"]),
	JetonProgres("maconnerie", ["reduc_carte bleu"]),
	JetonProgres("philosophie", ["point_victoire_fin_partie 7"]),
	JetonProgres("mathematiques", ["point_victoire_par_jeton 3", "point_victoire 3"]),
	JetonProgres("strategie", ["bonus_attaque"]),
	JetonProgres("theologie", ["rejouer"]),
	JetonProgres("urbanisme", ["monnaie 6", "bonus_monnaie_chainage 4"]),
]

# constructeur : Carte(nom, chemin_image, effets, couts, nom_carte_chainage, couleur, age)
CARTES_AGE_I = [
	Carte("chantier", ["ressource bois 1"], None, None, "marron", age=1),
	Carte("exploitation", ["ressource bois 1"], ["monnaie 1"], None, "marron", age=1),
	Carte("bassin argileux", ["ressource argile 1"], None, None, "marron", age=1),
	Carte("cavite", ["ressource argile 1"], ["monnaie 1"], None, "marron", age=1),
	Carte("gisement", ["ressource pierre 1"], None, None, "marron", age=1),
	Carte("mine", ["ressource pierre 1"], ["monnaie 1"], None, "marron", age=1),
	Carte("verrerie", ["ressource verre 1"], ["monnaie 1"], None, "grise", age=1),
	Carte("presse", ["ressource papyrus 1"], ["monnaie 1"], None, "grise", age=1),
	Carte("tour de garde", ["attaquer 1"], None, None, "rouge", age=1),
	Carte("atelier",
		[f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}", "point_victoire 1"], ["ressource papurys 1"],
		None, "vert", age=1),
	Carte("apothicaire",
		[f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 1"], ["ressource verre 1"],
		None, "vert", age=1),
	Carte("depot de pierre", ["reduc_ressource pierre 1"], ["monnaie 3"], None, "jaune", age=1),
	Carte("depot d argile", ["reduc_ressource argile 1"], ["monnaie 3"], None, "jaune", age=1),
	Carte("depot de bois", ["reduc_ressource bois 1"], ["monnaie 3"], None, "jaune", age=1),
	Carte("ecurie", ["attaquer 1"], ["ressource bois 1"], None, "rouge", age=1),
	Carte("caserne", ["attaquer 1"], ["ressource argile 1"], None, "rouge", age=1),
	Carte("palissade", ["attaquer 1"], ["monnaie 2"], None, "rouge", age=1),
	Carte("scriptorium", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}"], ["monnaie 2"], None, "vert", age=1),
	Carte("officine", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}"], ["monnaie 2"], None, "vert", age=1),
	Carte("theatre", ["point_victoire 3"], None, None, "bleu", age=1),
	Carte("autel", ["point_victoire 3"], None, None, "bleu", age=1),
	Carte("bains", ["point_victoire 3"], ["ressource pierre 1"], None, "bleu", age=1),
	Carte("taverne", ["monnaie 4"], None, None, "jaune", age=1)
]

CARTES_AGE_II = [
	Carte("scierie", ["ressource bois 2"], ["monnaie 2"], None, "marron", age=2),
	Carte("briqueterie", ["ressource argile 2"], ["monnaie 2"], None, "marron", age=2),
	Carte("carriere", ["ressource pierre 2"], ["monnaie 2"], None, "marron", age=2),
	Carte("soufflerie", ["ressource verre 1"], None, None, "gris", age=2),
	Carte("sechoir", ["ressource papyrus 1"], None, None, "gris", age=2),
	Carte("muraille", ["attaquer 2"], ["ressource pierre 2"], None, "rouge", age=2),
	Carte("forum", ["ressource_au_choix verre papyrus"], ["monnaie 3", "ressource argile 1"],
		None, "jaune", age=2),
	Carte("caravanserail", ["ressource_au_choix bois argile pierre"],
		["monnaie 2", "ressource verre 1", "ressource papyrus 1"], None, "jaune", age=2),
	Carte("douane", ["reduc_ressource papyrus 1", "reduc_ressource verre 1"], ["monnaie 4"],
		None, "jaune", age=2),
	Carte("tribunal", ["point_victoire 5"], ["ressource bois 2", "ressource verre 1"], None,
		"bleu", age=2),
	Carte("haras", ["attaquer 1"], ["ressource argile 1", "ressource bois 1"], "ecuries", "rouge", age=2),
	Carte("baraquements", ["attaquer 1"], ["monnaie 3"], "caserne", "rouge", age=2),
	Carte("champs de tir", ["attaquer 2"],
		["ressource pierre 1", "ressource bois 1", "ressource papyrus 1"],
		None, "rouge", age=2),
	Carte("place d armes", ["attaquer 2"], ["ressource argile 2", "ressource verre 1"], None, "rouge",
		age=2),
	Carte("bibliotheque", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[5]}", "point_victoire 2"],
		["ressource pierre 1", "ressource bois 1", "ressource verre 1"], "scriptorium", "vert", age=2),
	Carte("dispensaire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[3]}", "point_victoire 2"],
		["ressource argile 2", "ressource verre 1"], "officine", "vert", age=2),
	Carte("ecole", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[1]}", "point_victoire 1"],
		["ressource papyrus 2", "ressource bois 1"], None, "vert", age=2),
	Carte("laboratoire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[4]}", "point_victoire 1"],
		["ressource verre 2", "ressource bois 1"], None, "vert", age=2),
	Carte("statue", ["point_victoire 4"], ["ressource argile 2"], "theatre", "bleu", age=2),
	Carte("temple", ["point_victoire 4"], ["ressource papyrus 1", "ressource bois 1"], "autel",
		"bleu", age=2),
	Carte("aqueduc", ["point_victoire 5"], ["ressource pierre 3"], "bains", "bleu", age=2),
	Carte("rostres", ["point_victoire 4"], ["ressource pierre 1", "ressource bois 1"],
		None, "bleu", age=2),
	Carte("brasserie", ["monnaie 6"], None, "taverne", "jaune", age=2)
]

CARTES_AGE_III = [
	Carte("arsenal", ["attaquer 3"], ["ressource argile 3", "ressource bois 2"], None, "rouge", age=3),
	Carte("pretoire", ["attaquer 3"], ["monnaie 8"], None, "rouge", age=3),
	Carte("academie", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[2]}", "point_victoire 3"],
		["ressource pierre 1", "ressource bois 1", "ressource verre 2"], None, "vert", age=3),
	Carte("etude", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[2]}", "point_victoire 3"],
		["ressource papyrus 1", "ressource bois 2", "ressource verre 1"], None, "vert", age=3),
	Carte("chambre de commerce", ["monnaie_par_carte grise 3", "point_victoire 3"],
		["ressource papyrus 2"], None, "jaune", age=3),
	Carte("port", ["monnaie_par_carte marron 2", "point_victoire 3"],
		["ressource verre 1", "ressource bois 1", "ressource papyrus 1"], None, "jaune", age=3),
	Carte("armurerie", ["monnaie_par_carte rouge 1", "point_victoire 3"],
		["ressource pierre 2", "ressource verre 1"], None, "jaune", age=3),
	Carte("palace", ["point_victoire 7"],
		["ressource argile 1", "ressource pierre 1", "ressource bois 1", "ressource verre 2"],
		None, "bleu", age=3),
	Carte("hotel de ville", ["point_victoire 7"], ["ressource pierre 3", "ressource bois 2"],
		None, "bleu", age=3),
	Carte("obelisque", ["point_victoire 5"], ["ressource pierre 2", "ressource verre 1"],
		None, "bleu", age=3),
	Carte("fortifications", ["attaquer 2"],
		["ressource pierre 2", "ressource argile 1", "ressource papyrus 1"],
		"palissade", "rouge", age=3),
	Carte("atelier de siege", ["attaquer 2"], ["ressource bois 3", "ressource verre 1"],
		"champ de tir", "rouge", age=3),
	Carte("cirque", ["attaquer 2"], ["ressource argile 2", "ressource pierre 2"],
		"place d arme", "rouge", age=3),
	Carte("universite", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[0]}", "point_victoire 2"],
		["ressource argile 1", "ressource verre 1", "ressource papyrus 1"], "ecole", "vert", age=3),
	Carte("observatoire", [f"symbole_scientifique {SYMBOLE_SCIENTIFIQUES[0]}", "point_victoire 2"],
		["ressource pierre 1", "ressource papyrus 2"], "laboratoire", "vert", age=3),
	Carte("jardins", ["point_victoire 6"], ["ressource argile 2", "ressource bois 2"], "statue",
		"bleu", age=3),
	Carte("pantheon", ["point_victoire 6"],
		["ressource argile 1", "ressource bois 1", "ressource papyrus 2"],
		"temple", "bleu", age=3),
	Carte("senat", ["point_victoire 5"],
		["ressource argile 2", "ressource pierre 1", "ressource papyrus 2"],
		"rostres", "bleu", age=3),
	Carte("phare", ["monnaie_par_carte jaune 1", "point_victoire 3"],
		["ressource argile 2", "ressource verre 1"], "taverne", "jaune", age=3),
	Carte("arene", ["monnaie_par_merveille 2", "point_victoire 3"],
		["ressource argile 1", "ressource pierre 1", "ressource bois 1"], "brasserie", "jaune", age=3),
]

CARTES_GUILDE = [
	CarteFille("guilde des commercants",
		["effet_guild_commercants 1"],
		["ressource argile 1", "ressource bois 1", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("guilde des armateurs",
		["effet_guild_armateurs 1"],
		["ressource argile 1", "ressource pierre 1", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("guilde des batisseurs",
		["effet_guild_batisseurs 1"],
		["ressource pierre 2", "ressource argile 1", "ressource bois 1",
			"ressource papyrus 1", "ressource verre 1"]
	),
	CarteFille("guilde des magistrats",
		["effet_guild_magistrats 1"],
		["ressource bois 2", "ressource argile 1", "ressource papyrus 1"]
	),
	CarteFille("guilde des scientifiques",
		["effet_guild_scientifiques 1"],
		["ressource argile 2", "ressource bois 2"]
	),
	CarteFille("guilde des usuriers",
		["effet_guild_usuriers 1"],
		["ressource pierre 2", "ressource bois 2"]
	),
	CarteFille("guilde des tacticiens",
		["effet_guild_tacticiens 1"],
		["ressource pierre 2", "ressource argile 1", "ressource papyrus 1"]
	)
]

# constructeur : CarteFille(nom, chemin_image, effets)
MERVEILLES = [
	CarteFille("circus maximus",
		["defausse_carte_adversaire grise", "attaquer 1", "point_victoire 3"],
		["ressource pierre 2", "ressource bois 1", "ressource verre 1"]
	),
	CarteFille("colosse",
		["attaquer 2", "point_victoire 3"],
		["ressource argile 3", "ressource verre 1"]
	),
	CarteFille("grand phare",
		["ressource_au_choix bois argile pierre", "point_victoire 4"],
		["ressource bois 1", "ressource pierre 1", "ressource papyrus 2"]
	),
	CarteFille("jardin suspendus",
		["monnaie 6", "rejouer", "point_victoire 3"],
		["ressource bois 2 ", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("grande bibliotheque",
		["jeton_progres_aleatoire", "point_victoire 4"],
		["ressource bois 3", "ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("mausolee",
		["construction_fausse_gratuite", "point_victoire 2"],
		["ressource argile 2", "ressource verre 2", "ressource papyrus 1"]
	),
	CarteFille("piree",
		["ressource_au_choix papyrus verre", "rejouer", "point_victoire 2"],
		["ressource bois 2", "ressource pierre 1", "ressource argile 1"]
	),
	CarteFille("pyramides",
		["point_victoire 9"],
		["ressource pierre 3", "ressource papyrus 1"]
	),
	CarteFille("sphinx",
		["rejouer", "point_victoire 6"],
		["ressource pierre 1", "ressource argile 1", "ressource verre 2"]
	),
	CarteFille("statue de zeus",
		["defausse_carte_adversaire marron", "attaquer 1", "point_victoire 3"],
		["ressource pierre 1", "ressource bois 1",
			"ressource argile 1", "ressource papyrus 2"]
	),
	CarteFille("temple d artemis",
		["monnaie 12", "rejouer"],
		["ressource bois 1", "ressource pierre 1",
			"ressource verre 1", "ressource papyrus 1"]
	),
	CarteFille("via appia",
		["monnaie 3", "adversaire_perd_monnaie 3", "rejouer", "point_victoire 3"],
		["ressource pierre 2", "ressource argile 2", "ressource papyrus 1"]
	)
]
