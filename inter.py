import os
import pandas as pd
import hashlib
import csv  # Ajoutez cette ligne pour importer le module csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from modules.auth import *
# from modules.gestion_commercant import *
from modules.gestion_produits import *
def menu_modif(username, password):
    clear_frame()
    modif_frame = tk.Frame(root, bg="#f4f4f4")
    modif_frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(modif_frame, text="Modifier vos informations", font=("Helvetica", 16, 'bold'), fg="#2e2e2e", bg="#f4f4f4")
    title_label.pack(pady=20)

    tk.Label(modif_frame, text="Nom d'utilisateur:", font=("Helvetica", 12), bg="#f4f4f4", fg="#5a5a5a").pack(pady=10)
    username_entry = tk.Entry(modif_frame, font=("Helvetica", 12), fg="black", relief="solid", bd=1, width=30, bg="#eaeaea")
    username_entry.insert(0, username)
    username_entry.pack(pady=5)

    tk.Label(modif_frame, text="Mot de passe:", font=("Helvetica", 12), bg="#f4f4f4", fg="#5a5a5a").pack(pady=10)
    password_entry = tk.Entry(modif_frame, font=("Helvetica", 12), fg="black", relief="solid", bd=1, width=30, show="*", bg="#eaeaea")
    password_entry.insert(0, password)
    password_entry.pack(pady=5)

    def handle_modification():
        new_username = username_entry.get()
        new_password = password_entry.get()
        if not new_username or not new_password:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if verif_mdp(new_password):
            messagebox.showerror("Erreur", "Ce mot de passe est compromis. Veuillez en choisir un autre.")
            return

        df = pd.read_csv('data_user.csv', encoding='latin-1')

        user_index = df[df['Username'] == username].index
        if len(user_index) > 0: 
            old_file_path = os.path.join('data', f'{username}.csv')
            new_file_path = os.path.join('data', f'{new_username}.csv')
            
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            
            salt = os.urandom(16).hex()
            salted_password = salt + new_password
            password_hash = hashlib.sha256(salted_password.encode()).hexdigest()
            
            df.loc[user_index, 'Username'] = new_username
            df.loc[user_index, 'Password'] = password_hash
            df.loc[user_index, 'Salt'] = salt
            
            df.to_csv('data_user.csv', index=False, encoding='latin-1')
            
            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
            
            messagebox.showinfo("Succès", "Vos informations ont été modifiées avec succès!")
            modif_frame.destroy()
            menu_user(new_username)
        else:
            messagebox.showerror("Erreur", "Utilisateur non trouvé.")

    btn_modify = tk.Button(modif_frame, text="Valider la modification", font=("Helvetica", 12), command=handle_modification, bg="#4a90e2", fg="white", relief="flat")
    btn_modify.pack(pady=20)

    btn_back = tk.Button(modif_frame, text="Retour", font=("Helvetica", 12), command=lambda: menu_user(username), bg="#7f8c8d", fg="white", relief="flat")
    btn_back.pack(pady=10)


def inscription():
    clear_frame()

    inscription_frame = tk.Frame(root, bg="#f4f4f4")
    inscription_frame.pack(fill=tk.BOTH, expand=True)

    title_label = tk.Label(inscription_frame, text="Formulaire d'Inscription", font=("Helvetica", 16, 'bold'), fg="#2e2e2e", bg="#f4f4f4")
    title_label.pack(pady=20)

    tk.Label(inscription_frame, text="Numéro d'identifiant:", font=("Helvetica", 12), bg="#f4f4f4", fg="#5a5a5a").pack(pady=10)
    id_entry = tk.Entry(inscription_frame, font=("Helvetica", 12), fg="black", relief="solid", bd=1, width=30, bg="#eaeaea")
    id_entry.pack(pady=5)

    tk.Label(inscription_frame, text="Nom:", font=("Helvetica", 12), bg="#f4f4f4", fg="#5a5a5a").pack(pady=10)
    nom_entry = tk.Entry(inscription_frame, font=("Helvetica", 12), fg="black", relief="solid", bd=1, width=30, bg="#eaeaea")
    nom_entry.pack(pady=5)

    tk.Label(inscription_frame, text="Nom d'utilisateur:", font=("Helvetica", 12), bg="#f4f4f4", fg="#5a5a5a").pack(pady=10)
    username_entry = tk.Entry(inscription_frame, font=("Helvetica", 12), fg="black", relief="solid", bd=1, width=30, bg="#eaeaea")
    username_entry.pack(pady=5)

    tk.Label(inscription_frame, text="Adresse mail:", font=("Helvetica", 12), bg="#f4f4f4", fg="#5a5a5a").pack(pady=10)
    mail_entry = tk.Entry(inscription_frame, font=("Helvetica", 12), fg="black", relief="solid", bd=1, width=30, bg="#eaeaea")
    mail_entry.pack(pady=5)

    tk.Label(inscription_frame, text="Mot de passe:", font=("Helvetica", 12), bg="#f4f4f4", fg="#5a5a5a").pack(pady=10)
    password_entry = tk.Entry(inscription_frame, font=("Helvetica", 12), fg="black", relief="solid", bd=1, width=30, show="*", bg="#eaeaea")
    password_entry.pack(pady=5)

    def handle_inscription():
        id_user = id_entry.get()
        nom_user = nom_entry.get()
        username_user = username_entry.get()
        mail_user = mail_entry.get()
        password_user = password_entry.get()

        if not all([id_user, nom_user, username_user, mail_user, password_user]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if verif_mdp(password_user):
            messagebox.showerror("Erreur", "Ce mot de passe est compromis. Veuillez en choisir un autre.")
            return

        salt = os.urandom(16).hex()
        salted_password = salt + password_user
        password_hash = hashlib.sha256(salted_password.encode()).hexdigest()

        file_path = 'data_user.csv'

        try:
            if not os.path.exists(file_path):
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Adresse mail", "Nom", "Username", "Password", "Salt"])

            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([id_user, mail_user, nom_user, username_user, password_hash, salt])

            messagebox.showinfo("Succès", "Inscription réussie!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'inscription : {str(e)}")


    btn_submit = tk.Button(inscription_frame, text="S'inscrire", font=("Helvetica", 12), bg="#4a90e2", fg="white", relief="flat", width=20, height=2, command=handle_inscription)
    btn_submit.pack(pady=20)

    # Bouton de retour
    btn_back = tk.Button(inscription_frame, text="Retour", font=("Helvetica", 12), fg="white", bg="#7f8c8d", relief="flat", height=2, command=lambda: (clear_frame(), menu_gui()))
    btn_back.pack(pady=10, fill=tk.X, padx=50)

    
    
    
    
    
    
    
def create(username):
    clear_frame()

    folder_path = 'data'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    txt = os.path.join(folder_path, f'{username}.csv')
    if not os.path.exists(txt):
        df = pd.DataFrame(columns=["ID", "Nom", "Prix (EUR)"])
        df.to_csv(txt, index=False)
        messagebox.showinfo("Succès", f"Le fichier '{txt}' a été créé.")
    else:
        messagebox.showinfo("Info", f"Le fichier '{txt}' existe déjà.")

    back_button = tk.Button(root, text="Retour", command=lambda: menu_user(username),
                            font=("Helvetica", 12),
                            bg="#5A9EC9",
                            fg="white",
                            relief="flat",
                            padx=20,
                            pady=10)
    back_button.pack(pady=20)

    back_button.bind("<Enter>", lambda e: back_button.config(bg="#4A8BBE"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg="#5A9EC9"))




def supprimer(username):
    clear_frame()

    folder_path = 'data'
    txt = os.path.join(folder_path, f'{username}.csv')

    if os.path.exists(txt):
        os.remove(txt)
        messagebox.showinfo("Succès", f"Le fichier '{txt}' a été supprimé.")
    else:
        messagebox.showerror("Erreur", f"Le fichier '{txt}' n'existe pas.")

    back_button = tk.Button(root, text="Retour", command=lambda: menu_user(username),
                            font=("Helvetica", 12),
                            bg="#5A9EC9",
                            fg="white",
                            relief="flat",
                            padx=20,
                            pady=10)
    back_button.pack(pady=20)

    back_button.bind("<Enter>", lambda e: back_button.config(bg="#4A8BBE"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg="#5A9EC9"))

def afficher(username):
    clear_frame()

    display_frame = tk.Frame(root, bg="#f4f4f4")
    display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    title_label = tk.Label(display_frame, text="Affichage des produits", font=("Helvetica", 16, "bold"), fg="#2e2e2e", bg="#f4f4f4")
    title_label.pack(pady=20)

    folder_path = 'data'
    txt = os.path.join(folder_path, f'{username}.csv')

    if os.path.exists(txt):
        try:
            df = pd.read_csv(txt)
            if df.empty:
                messagebox.showinfo("Info", f"Le fichier '{txt}' est vide.")
            else:
                # Création d'un widget Treeview pour afficher les données sous forme de tableau
                tree = ttk.Treeview(display_frame, columns=list(df.columns), show="headings")
                
                # Configuration des en-têtes de colonnes
                for col in df.columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor="center", width=100)

                # Ajout des données dans le tableau
                for _, row in df.iterrows():
                    tree.insert("", "end", values=list(row))

                # Ajout d'une barre de défilement
                scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)

                tree.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

        except pd.errors.EmptyDataError:
            messagebox.showerror("Erreur", f"Le fichier '{txt}' est vide ou mal formaté.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier '{txt}': {e}")
    else:
        messagebox.showerror("Erreur", f"Le fichier '{txt}' n'existe pas.")
    
    back_button = tk.Button(display_frame, text="Retour", command=lambda: menu_user(username),
                            font=("Helvetica", 12),
                            bg="#5A9EC9",
                            fg="white",
                            relief="flat",
                            padx=20,
                            pady=10)
    back_button.pack(pady=20)

    back_button.bind("<Enter>", lambda e: e.widget.config(bg="#4A8BBE"))
    back_button.bind("<Leave>", lambda e: e.widget.config(bg="#5A9EC9"))


def rechercher_sequ(username, frame):
    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def perform_search():
        folder_path = 'data'
        txt = os.path.join(folder_path, f'{username}.csv')

        if os.path.exists(txt):
            try:
                df = pd.read_csv(txt)
                if 'Nom' not in df.columns:
                    messagebox.showerror("Erreur", f"La colonne 'Nom' est introuvable dans le fichier '{txt}'.")
                    return

                recherche = entry_recherche.get().strip().lower()
                if not recherche:
                    messagebox.showerror("Erreur", "Vous devez entrer un nom de produit.")
                    return

                df_filtered = df[df['Nom'].str.contains(recherche, case=False, na=False)]
                if not df_filtered.empty:
                    messagebox.showinfo("Résultat", f"Produit(s) trouvé(s) :\n{df_filtered}")
                else:
                    messagebox.showinfo("Résultat", f"Aucun produit ne correspond à '{recherche}'.")
            except pd.errors.EmptyDataError:
                messagebox.showerror("Erreur", f"Le fichier '{txt}' est vide ou mal formaté.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la lecture ou de la recherche dans le fichier '{txt}': {e}")
        else:
            messagebox.showerror("Erreur", f"Le fichier '{txt}' n'existe pas.")

    clear_frame()

    search_frame = tk.Frame(frame, bg="#f4f4f4")
    search_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    title_label = tk.Label(search_frame, text="Recherche de produits", font=("Helvetica", 16, "bold"), fg="#2e2e2e", bg="#f4f4f4")
    title_label.pack(pady=20)

    label_recherche = tk.Label(search_frame, text="Entrez le nom du produit à rechercher :", font=("Helvetica", 12), fg="#5a5a5a", bg="#f4f4f4")
    label_recherche.pack(pady=10)

    entry_recherche = tk.Entry(search_frame, font=("Helvetica", 12), width=30, bg="white", fg="#2e2e2e", relief="solid", bd=1)
    entry_recherche.pack(pady=10)

    search_button = tk.Button(search_frame, text="Rechercher", command=perform_search, font=("Helvetica", 12), bg="#4a90e2", fg="white", relief="flat", padx=20, pady=5)
    search_button.pack(pady=20)

    btn_back = tk.Button(search_frame, text="Retour", command=lambda: menu_user(username), font=("Helvetica", 12), bg="#7f8c8d", fg="white", relief="flat", padx=20, pady=5)
    btn_back.pack(pady=10)

    search_button.bind("<Enter>", lambda e: e.widget.config(bg="#3a7bc8"))
    search_button.bind("<Leave>", lambda e: e.widget.config(bg="#4a90e2"))
    btn_back.bind("<Enter>", lambda e: e.widget.config(bg="#6f7c7d"))
    btn_back.bind("<Leave>", lambda e: e.widget.config(bg="#7f8c8d"))


def tri_bul(username, frame):
    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def perform_sort():
        folder_path = 'data'
        file_path = os.path.join(folder_path, f'{username}.csv')

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if 'Nom' not in df.columns:
                    messagebox.showerror("Erreur", f"La colonne 'Nom' est introuvable dans le fichier '{file_path}'.")
                    return

                df_sorted = df.sort_values(by="Nom")
                df_sorted.to_csv(file_path, index=False)
                messagebox.showinfo("Succès", "Les produits ont été triés et enregistrés.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du tri des produits dans le fichier '{file_path}': {e}")
        else:
            messagebox.showerror("Erreur", f"Le fichier '{file_path}' n'existe pas.")

    clear_frame()

    sort_frame = tk.Frame(frame, bg="#f4f4f4")
    sort_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    title_label = tk.Label(sort_frame, text="Tri des produits", font=("Helvetica", 16, "bold"), fg="#2e2e2e", bg="#f4f4f4")
    title_label.pack(pady=20)

    sort_button = tk.Button(sort_frame, text="Trier les produits par nom", command=perform_sort, font=("Helvetica", 12), bg="#4a90e2", fg="white", relief="flat", padx=20, pady=5)
    sort_button.pack(pady=20)

    btn_back = tk.Button(sort_frame, text="Retour", command=lambda: menu_user(username), font=("Helvetica", 12), bg="#7f8c8d", fg="white", relief="flat", padx=20, pady=5)
    btn_back.pack(pady=10)

    sort_button.bind("<Enter>", lambda e: e.widget.config(bg="#3a7bc8"))
    sort_button.bind("<Leave>", lambda e: e.widget.config(bg="#4a90e2"))
    btn_back.bind("<Enter>", lambda e: e.widget.config(bg="#6f7c7d"))
    btn_back.bind("<Leave>", lambda e: e.widget.config(bg="#7f8c8d"))

def create_interface(username):
    global frame

    root = tk.Tk()
    root.title("Gestion des Produits")

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    root.mainloop()

import tkinter as tk

def menu_user(username):
    clear_frame()
    menu_user_frame = tk.Frame(root, bg="#ffffff")
    menu_user_frame.pack(fill=tk.BOTH, expand=True)

    label_title = tk.Label(menu_user_frame, text=f"Menu de {username}", font=("Helvetica", 20), fg="black")
    label_title.pack(pady=40)

    button_bg = "#5A9EC9"
    button_fg = "white"
    button_hover_bg = "#4A8BBE"

    def on_enter(e):
        e.widget['background'] = button_hover_bg

    def on_leave(e):
        e.widget['background'] = button_bg

    buttons = [
        ("Créer un fichier", lambda: create(username)),
        ("Supprimer un fichier", lambda: supprimer(username)),
        ("Afficher un fichier", lambda: afficher(username)),
        ("Rechercher un produit", lambda: rechercher_sequ(username, menu_user_frame)),
        ("Ajouter un produit", lambda: ajouter_produit(username)),
        ("Trier les produits", lambda: tri_bul(username, menu_user_frame)),
        ("Modifier mes informations", lambda: menu_modif(username, "")),
        ("Se déconnecter", open_connexion_window)
    ]

    for text, command in buttons:
        btn = tk.Button(menu_user_frame, text=text, font=("Helvetica", 12), command=command, bg=button_bg, fg=button_fg, relief="flat")
        btn.pack(pady=10, fill=tk.X, padx=50)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

def tri_bul(username, frame):
    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def perform_sort():
        folder_path = 'data'
        file_path = os.path.join(folder_path, f'{username}.csv')
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if 'Nom' not in df.columns:
                    messagebox.showerror("Erreur", f"La colonne 'Nom' est introuvable dans le fichier '{file_path}'.")
                    return

                df_sorted = df.sort_values(by="Nom")
                messagebox.showinfo("Résultat", f"Produits triés par nom :\n{df_sorted}")
                df_sorted.to_csv(file_path, index=False)
                messagebox.showinfo("Succès", "Les produits ont été triés et enregistrés.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du tri des produits dans le fichier '{file_path}': {e}")
        else:
            messagebox.showerror("Erreur", f"Le fichier '{file_path}' n'existe pas.")

    clear_frame()
    sort_button = tk.Button(frame, text="Trier les produits par nom", command=perform_sort)
    sort_button.pack(pady=10)
    back_button = tk.Button(frame, text="Retour", command=lambda: menu_user(username))
    back_button.pack(pady=10)

def ajouter_produit(username):
    clear_frame()  # On vide l'écran actuel pour afficher le menu utilisateur

    add_product_window = tk.Frame(root)
    add_product_window.pack(fill=tk.BOTH, expand=True)

    tk.Label(add_product_window, text="Nom du produit:", font=("Helvetica", 12)).pack(pady=10)
    product_name_entry = tk.Entry(add_product_window, font=("Helvetica", 12), fg="black")
    product_name_entry.pack(pady=5)

    tk.Label(add_product_window, text="Prix du produit (EUR):", font=("Helvetica", 12)).pack(pady=10)
    product_price_entry = tk.Entry(add_product_window, font=("Helvetica", 12), fg="black")
    product_price_entry.pack(pady=5)

    def handle_add_product():
        # Récupérer les valeurs des champs
        product_name = product_name_entry.get()
        product_price = product_price_entry.get()

        if not product_name or not product_price:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            # Vérification si le prix est valide
            product_price = float(product_price)
        except ValueError:
            messagebox.showerror("Erreur", "Le prix doit être un nombre valide.")
            return

        # Ouvrir le fichier CSV correspondant à l'utilisateur (avec le username + ".csv")
        file_path = os.path.join('data', f'{username}.csv')

        if not os.path.exists(file_path):
            # Si le fichier n'existe pas, on le crée
            df = pd.DataFrame(columns=["ID", "Nom", "Prix (EUR)"])
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Info", "Le fichier produit a été créé.")

        # Lire le fichier CSV existant
        try:
            df = pd.read_csv(file_path)

            # Ajout du nouveau produit
            new_product_id = len(df) + 1  # Création d'un ID unique pour chaque produit
            new_product = pd.DataFrame([[new_product_id, product_name, product_price]], columns=["ID", "Nom", "Prix (EUR)"])
            df = pd.concat([df, new_product], ignore_index=True)

            # Sauvegarder les changements dans le fichier
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Succès", "Produit ajouté avec succès!")

            # Nettoyer les champs après l'ajout
            product_name_entry.delete(0, tk.END)
            product_price_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'ajout du produit : {e}")

    # Bouton pour valider l'ajout du produit
    btn_add_product_submit = tk.Button(add_product_window, text="Ajouter le produit", font=("Helvetica", 12), command=handle_add_product)
    btn_add_product_submit.pack(pady=20)

    btn_back = tk.Button(add_product_window, text="Retour", command=lambda: menu_user(username))
    btn_back.pack(pady=10)

def go_back():
    menu_gui()
def open_connexion_window():
    clear_frame()

    login_frame = tk.Frame(root, bg="#f4f4f4")
    login_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(login_frame, text="Nom d'utilisateur", font=("Helvetica", 12), fg="grey", bg="#f4f4f4").pack(pady=10)
    username_entry = tk.Entry(login_frame, font=("Helvetica", 12), fg="black")
    username_entry.pack(pady=5, fill=tk.X, padx=50)

    tk.Label(login_frame, text="Mot de passe", font=("Helvetica", 12), fg="grey", bg="#f4f4f4").pack(pady=10)
    password_entry = tk.Entry(login_frame, font=("Helvetica", 12), fg="black", show="*")
    password_entry.pack(pady=5, fill=tk.X, padx=50)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        file_path = 'data_user.csv'
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) >= 6:
                        stored_email = row[1]
                        stored_username = row[3]
                        stored_password = row[4]
                        stored_salt = row[5]

                        if stored_username == username:
                            salted_password = stored_salt + password
                            password_hash = hashlib.sha256(salted_password.encode()).hexdigest()

                            if stored_password == password_hash:
                                messagebox.showinfo("Succès", "Connexion réussie!")

                                compromises = verif_api(username, password)
                                if compromises > 0:
                                    messagebox.showwarning("Alerte", f"Ce mot de passe a été compromis {compromises} fois. Vous allez être redirigé vers la page de modification du mot de passe.")
                                    send_email_alert(
                                        dest_email=stored_email,
                                        subject="Alerte de sécurité : Mot de passe compromis",
                                        body=(
                                            f"Bonjour {username},\n\n"
                                            f"Votre mot de passe a été compromis {compromises} fois. "
                                            "Nous vous recommandons de le changer immédiatement pour sécuriser votre compte.\n\n"
                                            "Cordialement,\nL'équipe de sécurité."
                                        )
                                    )
                                    menu_modif(username, password)
                                else:
                                    menu_user(username)
                                return
                messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Le fichier utilisateur est introuvable.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue est survenue : {e}")

    #bouton pour se connecter
    btn_login = tk.Button(login_frame, text="Se connecter", font=("Helvetica", 12), fg="white", bg="#000000", relief="flat", height=2, command=handle_login)
    btn_login.pack(pady=20, fill=tk.X, padx=50)

    # Bouton de retour
    btn_back = tk.Button(login_frame, text="Retour", font=("Helvetica", 12), fg="white", bg="#7f8c8d", relief="flat", height=2, command=lambda: (clear_frame(), menu_gui()))
    btn_back.pack(pady=10, fill=tk.X, padx=50)




# Fonction pour nettoyer l'écran
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Fonction principale de l'interface graphhique
import tkinter as tk

# Fonction pour le menu principal
import tkinter as tk

import tkinter as tk

def menu_gui():
        global root
        root = tk.Tk()
        root.title("Menu Principal")
        root.geometry("700x550")
        root.config(bg="#e9f1f7")  # Fond de la fenêtre gris clair

        # Créer un cadre pour le menu
        menu_frame = tk.Frame(root, bg="#f4f4f4")  # Fond clair pour la fenêtre
        menu_frame.pack(fill=tk.BOTH, expand=True)

        # Titre avec texte sombre
        label_title = tk.Label(menu_frame, text="Bienvenue", font=("Helvetica", 20), fg="black", bg="#f4f4f4")
        label_title.pack(pady=40)

        # Sous-titre
        label_subtitle = tk.Label(menu_frame, text="Sélectionnez une option", font=("Helvetica", 12), fg="#2e2e2e", bg="#f4f4f4")
        label_subtitle.pack(pady=10)

        # Définir les couleurs pour les boutons
        button_bg = "#000000"  # Couleur de fond des boutons (noir)
        button_fg = "white"    # Texte des boutons en blanc
        button_hover_bg = "#808080"  # Couleur plus foncée au survol

        # Fonction pour changer la couleur du bouton au survol
        def on_enter(e):
            e.widget['background'] = button_hover_bg

        def on_leave(e):
            e.widget['background'] = button_bg

        # Créer les boutons
        btn_connexion = tk.Button(menu_frame, text="Connexion", font=("Helvetica", 12), command=open_connexion_window, bg=button_bg, fg=button_fg, relief="flat")
        btn_connexion.pack(pady=10, fill=tk.X, padx=50)
        btn_connexion.bind("<Enter>", on_enter)
        btn_connexion.bind("<Leave>", on_leave)

        btn_inscription = tk.Button(menu_frame, text="Inscription", font=("Helvetica", 12), command=inscription, bg=button_bg, fg=button_fg, relief="flat")
        btn_inscription.pack(pady=10, fill=tk.X, padx=50)
        btn_inscription.bind("<Enter>", on_enter)
        btn_inscription.bind("<Leave>", on_leave)

        btn_quitter = tk.Button(menu_frame, text="Quitter", font=("Helvetica", 12), command=root.quit, bg=button_bg, fg=button_fg, relief="flat")
        btn_quitter.pack(pady=30, fill=tk.X, padx=50)
        btn_quitter.bind("<Enter>", on_enter)
        btn_quitter.bind("<Leave>", on_leave)

        root.mainloop()






menu_gui()