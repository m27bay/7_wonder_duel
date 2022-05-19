class Couleurs:
	OK = '\033[92m'  # GREEN
	WARNING = '\033[93m'  # YELLOW
	FAIL = '\033[91m'  # RED
	
	RESET = '\033[0m'  # RESET COLOR
	
	
if __name__ == '__main__':
	print(f"{Couleurs.OK}ceci est un message en vert{Couleurs.RESET}")
	print(f"{Couleurs.WARNING}ceci est un message en jaune{Couleurs.RESET}")
	print(f"{Couleurs.FAIL}ceci est un message en rouge{Couleurs.RESET}")