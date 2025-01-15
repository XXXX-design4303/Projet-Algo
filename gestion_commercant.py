from modules.auth import *
import os
import pandas as pd


def menu_modif():
    while True:  

        print("Que souhaitez-vous faire ?")
        print("1. Modifier")
        print("2. Supprimer")
        print("3. Quitter")

        print()

        choix = input("Entrez votre choix : ")

        if choix == '1':
            print("\Modification en cours...")  
            modif_commer()
        elif choix == '2':
            print("\nSuppression en cours...")  
            supp_commer()
        elif choix == '3':
            arriere()  
        else:
            print("\nChoix invalide. Veuillez essayer à nouveau.")     



def modif_commer():
    # Demande du nom d'utilisateur et du mot de passe actuel pour valider la connexion
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")

    try:
        with open('data_user.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Charger toutes les lignes dans une liste

            utilisateur_trouve = False
            for i, row in enumerate(rows):
                stored_username = row[2]
                stored_password = row[3]
                
                # Vérification des informations de connexion
                if stored_username == username and stored_password == password:
                    utilisateur_trouve = True
                    print("Connexion réussie!")

                    # Demande de modification de l'information (mot de passe ou nom d'utilisateur)
                    choix = input("Que souhaitez-vous modifier ? (1) Mot de passe (2) Nom d'utilisateur: ")
                    
                    if choix == '1':
                        nouveau_mdp = input("Entrez votre nouveau mot de passe: ")
                        # Hachage du mot de passe
                        password_hash = hashlib.md5(nouveau_mdp.encode()).hexdigest()
                        rows[i][3] = password_hash  # Mise à jour du mot de passe hashé
                        print("Mot de passe modifié avec succès!")
                    
                    elif choix == '2':
                        nouveau_username = input("Entrez votre nouveau nom d'utilisateur: ")
                        rows[i][2] = nouveau_username  # Mise à jour de l'username
                        print("Nom d'utilisateur modifié avec succès!")
                    else:
                        print("Choix invalide.")
                    break
            
            if not utilisateur_trouve:
                print("Nom d'utilisateur ou mot de passe incorrect.")

        # Réécriture du fichier avec les modifications
        if utilisateur_trouve:
            with open('data_user.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)  # Sauvegarder les modifications dans le fichier CSV

    except FileNotFoundError:
        print("Le fichier data_user.csv n'existe pas.")

def supp_commer():
    username_to_delete = input("Entrez le nom d'utilisateur du commerçant à supprimer: ")

    # Suppression dans le fichier data_user.csv
    try:
        with open('data_user.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Charger toutes les lignes dans une liste
            utilisateur_trouve = False

            for i, row in enumerate(rows):
                stored_username = row[2]
                
                # Vérifie si le commerçant à supprimer est trouvé
                if stored_username == username_to_delete:
                    utilisateur_trouve = True
                    print(f"Utilisateur {username_to_delete} trouvé dans le fichier CSV.")
                    
                    # Suppression de la ligne contenant l'utilisateur
                    rows.pop(i)
                    break

            if utilisateur_trouve:
                # Réécriture du fichier CSV sans la ligne supprimée
                with open('data_user.csv', mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)  # Sauvegarder les modifications dans le fichier CSV
                print(f"Utilisateur {username_to_delete} supprimé avec succès du fichier data_user.csv.")
            else:
                print("Utilisateur non trouvé dans le fichier.")

    except FileNotFoundError:
        print("Le fichier data_user.csv n'existe pas.")

    # Suppression du fichier CSV spécifique dans le dossier data
    try:
        user_file_path = f"data/{username_to_delete}.csv"
        if os.path.exists(user_file_path):
            os.remove(user_file_path)
            print(f"Fichier {username_to_delete}.csv supprimé avec succès dans le dossier data.")
        else:
            print(f"Aucun fichier associé à {username_to_delete} trouvé dans le dossier data.")

    except Exception as e:
        print(f"Erreur lors de la suppression du fichier utilisateur : {e}")

        
def arriere():
    print("Au revoir !")
    sys.exit()  # Termine le programme