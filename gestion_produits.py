import os
import pandas as pd
import sys



def create(username):
    folder_path = 'data'  # Dossier 'data'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Crée le dossier 'data' s'il n'existe pas

    txt = os.path.join(folder_path, f'{username}.csv')  # Création du chemin complet vers le fichier
    if not os.path.exists(txt):
        # Crée un DataFrame vide et enregistre le fichier CSV
        df = pd.DataFrame(columns=["ID", "Nom", "Prix (EUR)"])
        df.to_csv(txt, index=False)
        print(f"Le fichier '{txt}' a été créé.")
    else:
        print(f"Le fichier '{txt}' existe déjà.")




def supprimer(username):
    folder_path = 'data'  # Dossier 'data'
    txt = os.path.join(folder_path, f'{username}.csv')  # Création du chemin complet vers le fichier

    if os.path.exists(txt):
        os.remove(txt)
        print(f"Le fichier '{txt}' a été supprimé.")
    else:
        print(f"Le fichier '{txt}' n'existe pas.")



def afficher(username):
    folder_path = 'data'  # Le dossier où se trouvent les fichiers CSV
    txt = os.path.join(folder_path, f'{username}.csv')  # Construire le chemin complet du fichier

    if os.path.exists(txt):  # Vérifier si le fichier existe
        try:
            df = pd.read_csv(txt)  # Tenter de lire le fichier CSV

            # Vérifier si le DataFrame est vide
            if df.empty:
                print(f"Le fichier '{txt}' est vide.")
            else:
                # Afficher uniquement le contenu du fichier
                print(df)  # Affiche les données du fichier CSV

        except pd.errors.EmptyDataError:
            print(f"Le fichier '{txt}' est vide ou mal formaté.")
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier '{txt}': {e}")
    else:
        print(f"Le fichier '{txt}' n'existe pas.")
    
    input("Appuyez sur une touche pour revenir au menu...")  # Attente de l'utilisateur avant de revenir au menu







def add_produit(username):
    folder_path = 'data'  
    txt = os.path.join(folder_path, f'{username}.csv') 
    if not os.path.exists(txt):
        # Créer un DataFrame vide avec les colonnes si le fichier n'existe pas
        df = pd.DataFrame(columns=["ID", "Nom", "Prix (EUR)"])
        df.to_csv(txt, index=False)  # Créer le fichier vide
        print(f"Le fichier {txt} a été créé.")
    else:
        try:
            df = pd.read_csv(txt)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=["ID", "Nom", "Prix (EUR)"])

    name = input("Quel est le nom de votre produit ? ")
    prix = float(input("Quel est le prix de votre produit (au kilo en euro) ? "))
    id = int(input("Quel est l'identifiant de votre produit ? "))
    
    new_product = pd.DataFrame([[id, name, prix]], columns=["ID", "Nom", "Prix (EUR)"])
    df = pd.concat([df, new_product], ignore_index=True)
    
    df.to_csv(txt, index=False)
    print("Produit ajouté.")



def rechercher_sequ(username):
    folder_path = 'data'  
    txt = os.path.join(folder_path, f'{username}.csv')     
    if os.path.exists(txt):
        try:
            df = pd.read_csv(txt)
            
            if 'Nom' not in df.columns:
                print(f"La colonne 'Nom' est introuvable dans le fichier '{txt}'.")
                return

            recherche = input("Quel produit voulez-vous rechercher ? ").strip().lower()

            if not recherche:
                print("Vous devez entrer un nom de produit.")
                return

            # Recherche de produits qui contiennent la chaîne de recherche (insensible à la casse)
            df_filtered = df[df['Nom'].str.contains(recherche, case=False, na=False)]

            # Vérifier si des produits ont été trouvés et afficher les résultats
            if not df_filtered.empty:
                print(f"Produit(s) trouvé(s) :\n{df_filtered}")
            else:
                print(f"Aucun produit ne correspond à '{recherche}'.")
        
        except pd.errors.EmptyDataError:
            print(f"Le fichier '{txt}' est vide ou mal formaté.")
        except Exception as e:
            print(f"Erreur lors de la lecture ou de la recherche dans le fichier '{txt}': {e}")
    else:
        print(f"Le fichier '{txt}' n'existe pas.")




def tri_bul(username):
    folder_path = 'data'  
    file_path = os.path.join(folder_path, f'{username}.csv') 
    if os.path.exists(file_path): 
        try:
            df = pd.read_csv(file_path)  
            if 'Nom' not in df.columns:
                print(f"La colonne 'Nom' est introuvable dans le fichier '{file_path}'.")
                return

            print(f"Produits avant tri :\n{df}")  

            df = df.sort_values(by="Nom")

            print(f"Produits après tri :\n{df}")  

            df.to_csv(file_path, index=False)
            print("Les produits ont été triés par nom dans le fichier.")

        except Exception as e: 
            print(f"Erreur lors du tri des produits dans le fichier '{file_path}': {e}")
    else:
        print(f"Le fichier '{file_path}' n'existe pas.")  