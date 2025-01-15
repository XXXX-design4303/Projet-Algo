import csv
import os
import hashlib
import requests
from colorama import Fore, Style, init
from email.mime.text import MIMEText
import smtplib
import datetime
from modules.gestion_produits import *
from modules.auth import *
from modules.gestion_commercant import menu_modif

def send_email_alert(dest_email, subject, body):
    """
    Envoie un e-mail d'alerte à l'utilisateur via SMTP.
    """
    sender_email = "eliot4517@gmail.com"
    sender_password = "dpnz ovii sxho tmhg"  # Mot de passe d'application Gmail

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = dest_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(Fore.GREEN + f"[MAIL] Alerte envoyée à {dest_email}.")
    except Exception as e:
        print(Fore.RED + f"[MAIL] Erreur lors de l'envoi de l'e-mail: {e}")

def verif_mdp(password):
    """
    Vérifie si le mot de passe a été compromis en comparant son hash MD5 à une liste.
    """
    password_hash = hashlib.md5(password.encode()).hexdigest()
    try:
        with open('mdp_compromis.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == password_hash:
                    return True
        return False
    except FileNotFoundError:
        return False

def ecrire_historique(username, password, compromis):
    """
    Écrit un historique des tentatives de connexion avec une indication de compromission.
    """
    date_activite = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    compromis_str = 'oui' if compromis > 0 else 'non'

    with open('histo.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if file.tell() == 0:  # Ajouter l'en-tête si le fichier est vide
            writer.writerow(["Date d'activite", "Nom d'utilisateur", "Mot de passe", "Compromis"])

        writer.writerow([date_activite, username, password_hash, compromis_str])

def verif_api(username, password):
    """
    Vérifie si le mot de passe est compromis via l'API Have I Been Pwned.
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    headers = {'User-Agent': 'UserAgent/1.0'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f'Erreur {response.status_code}, veuillez réessayer plus tard.')
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                compromis = int(count)
                ecrire_historique(username, password, compromis)
                return compromis
        ecrire_historique(username, password, 0)
        return 0
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {e}")
        return 0

def inscription():
    """
    Inscription d'un nouvel utilisateur avec vérification de mot de passe.
    """
    id = input("Entrez votre numéro d'identifiant: ")
    nom = input("Entrez votre nom: ")
    username = input("Entrez votre nom d'utilisateur: ")
    mail = input("Entrez votre adresse mail: ")

    while True:
        password = input("Entrez votre mot de passe: ")
        if verif_mdp(password):
            print("Ce mot de passe est compromis. Veuillez en choisir un autre.")
        else:
            break

    salt = os.urandom(16).hex()
    salted_password = salt + password
    password_hash = hashlib.sha256(salted_password.encode()).hexdigest()

    with open('data_user.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["ID", "Adresse mail", "Nom", "Username", "Password", "Salt"])
        writer.writerow([id, mail, nom, username, password_hash, salt])

    print("Inscription réussie!")
    send_email_alert(
        mail,
        "Bienvenue sur notre plateforme",
        f"Bonjour {username},\n\nVotre inscription a été réussie ! Merci de votre confiance.\n\nCordialement,\nL'équipe."
    )

def connexion():
    """
    Connexion utilisateur avec vérification des identifiants et alerte si nécessaire.
    """
    username = input("Entrez votre nom d'utilisateur: ")
    password = input("Entrez votre mot de passe: ")

    try:
        with open('data_user.csv', mode='r') as file:
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
                            print("Connexion réussie!")
                            compromises = verif_api(username, password)
                            if compromises > 0:
                                print(f"Alerte : Ce mot de passe a été compromis {compromises} fois dans des violations de données.")
                                send_email_alert(
                                    stored_email,
                                    "Alerte de sécurité : Mot de passe compromis",
                                    f"Bonjour {username},\n\nVotre mot de passe a été compromis {compromises} fois. "
                                    "Nous vous recommandons de le changer immédiatement pour sécuriser votre compte.\n\n"
                                    "Cordialement,\nL'équipe de sécurité."
                                )
                                menu_modif()
                            else:
                                print("Le mot de passe semble sécurisé.")

                            menu_user(username)
                            return
        print("Nom d'utilisateur ou mot de passe incorrect.")
    except FileNotFoundError:
        print("Le fichier 'data_user.csv' est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

def quitter():
    """
    Quitte le programme proprement.
    """
    print("Au revoir !")
    exit()

init(autoreset=True)

def menu_user(username):
    """
    Menu principal utilisateur.
    """
    while True:
        print(Fore.BLUE + """
 ::::::::  :::::::::: :::::::: ::::::::::: ::::::::::: ::::::::  ::::    ::: 
:+:    :+: :+:       :+:    :+:    :+:         :+:    :+:    :+: :+:+:   :+: 
+:+        +:+       +:+           +:+         +:+    +:+    +:+ :+:+:+  +:+ 
:#:        +#++:++#  +#++:++#++    +#+         +#+    +#+    +:+ +#+ +:+ +#+ 
#+#   +#+# +#+              +#+    +#+         +#+    +#+    +#+ +#+  +#+#+# 
#+#    #+# #+#       #+#    #+#    #+#         #+#    #+#    #+# #+#   #+#+# 
 ########  ########## ########     ###     ########### ########  ###    ####
    """)

        print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
        print(Fore.MAGENTA + f"   Menu de {username}   ")
        print(Fore.LIGHTBLACK_EX + Style.BRIGHT + "==============================")
        print()

        print(Fore.CYAN + "Que souhaitez-vous faire ?")
        print(Fore.GREEN + "1. Créer")
        print(Fore.YELLOW + "2. Supprimer")
        print(Fore.BLUE + "3. Ajouter un produit")
        print(Fore.RED + "4. Afficher")
        print(Fore.LIGHTGREEN_EX + "5. Rechercher")
        print(Fore.LIGHTYELLOW_EX + "6. Trier")
        print(Fore.LIGHTYELLOW_EX + "7. Quitter")
        print()

        choix = input(Fore.LIGHTCYAN_EX + "Entrez votre choix : ")

        if choix == '1':
            create(username)
        elif choix == '2':
            supprimer(username)
        elif choix == '3':
            add_produit(username)
        elif choix == '4':
            afficher(username)
        elif choix == '5':
            rechercher_sequ(username)
        elif choix == '6':
            tri_bul(username)
        elif choix == '7':
            quitter()
        else:
            print(Fore.RED + Style.BRIGHT + "\nChoix invalide. Veuillez essayer à nouveau.")