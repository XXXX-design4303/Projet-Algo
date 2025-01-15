from colorama import Fore, Style, init
from modules.auth import *
from modules.gestion_commercant import *
init(autoreset=True)

def menu():
    print(Fore.RED + """
ooo        ooooo oooooooooooo ooooo      ooo ooooo     ooo      
`88.       .888' `888'     `8 `888b.     `8' `888'     `8'      
 888b     d'888   888          8 `88b.    8   888       8       
 8 Y88. .P  888   888oooo8     8   `88b.  8   888       8       
 8  `888'   888   888    "     8     `88b.8   888       8       
 8    Y     888   888       o  8       `888   `88.    .8'       
o8o        o888o o888ooooood8 o8o        `8     `YbodP'         
    """)

    print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
    print(Fore.CYAN + "   Bienvenue dans le Menu   ")
    print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
    print()

    print(Fore.WHITE + "Que souhaitez-vous faire ?")
    print(Fore.LIGHTWHITE_EX + "1. Connexion")
    print(Fore.LIGHTWHITE_EX + "2. Inscription")
    print(Fore.LIGHTWHITE_EX + "3. Modfication")
    print()

    choix = input(Fore.LIGHTCYAN_EX + "Entrez votre choix : ")

    if choix == '1':
        print(Fore.GREEN + Style.BRIGHT + "\nConnexion en cours...")
        connexion()
    elif choix == '2':
        print(Fore.GREEN + Style.BRIGHT + "\nInscription en cours...")
        inscription()
    elif choix == '3':
        print(Fore.RED + Style.BRIGHT + "\nModification")
        menu_modif()
    else:
        print(Fore.RED + Style.BRIGHT + "\nChoix invalide. Veuillez essayer à nouveau.")
        menu()

menu()