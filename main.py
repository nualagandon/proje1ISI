"""
Interface domotique maison - Tkinter

Fonctionnalités :
- Gestion des pièces : ajout, suppression
- Configuration de l'éclairage (statut, couleur, intensité)
- Configuration du chauffage (état, température, programme)
- Sauvegarde des réglages pièce par pièce
"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime



# -------------------------------------------------------------
# ---------Variables globales et configuration de base---------
# -------------------------------------------------------------

# Variable globale permettant de savoir la pièce séléctionnée
piece_actuelle = None

# Dictionnaire contenant la configuration de chaque pièce
configuration_pieces = {
    'salon': {
        'eclairage': {
            'statut': 'Allumer',
            'couleur': 'Blanc',
            'intensite': 100,
        },
        'chauffage': {
            'etat': 'Allumer',
            'temperature': 20,
            'programme': 'Hiver'
        },
    },
    'chambre': {
        'eclairage': {
            'statut': 'Allumer',
            'couleur': 'Blanc',
            'intensite': 100,
        },
        'chauffage': {
            'etat': 'Allumer',
            'temperature': 20,
            'programme': 'Hiver'
        },
    },
    'sdb': {
        'eclairage': {
            'statut': 'Allumer',
            'couleur': 'Blanc',
            'intensite': 100,
        },
        'chauffage': {
            'etat': 'Allumer',
            'temperature': 20,
            'programme': 'Hiver'
        }
    }
}

# -------------------------------------------------------------
# ---------------Fonctions de gestion des pièces---------------
# -------------------------------------------------------------
def ajouter_piece():
    """Fonction qui permet d'ajouter une pièce à la liste des pièces"""
    nom_piece = input_nom_piece.get().strip()
    if nom_piece and nom_piece not in configuration_pieces:
        # Ajouter la pièce à la liste
        listebox_pieces.insert(END, nom_piece)
        listebox_pieces.config(height=listebox_pieces.size())
        
        # Ajouter une configuration par défaut pour la pièce
        configuration_pieces[nom_piece] = {
            'eclairage': {'statut': 'Allumer','couleur': 'Blanc','intensite': 100,},
            'chauffage': {'etat': 'Allumer','temperature': 20,'programme': 'Hiver'}
        }
        
        # Réinitialiser le champ de saisie
        input_nom_piece.set("")

    # Affichage d'une erreur si la pièce existe déjà
    elif nom_piece in configuration_pieces:
        messagebox.showerror("Erreur","Cette pièce existe déjà !")
    # Affichage d'une erreur si l'entrée est vide ou invalide
    else:
        messagebox.showerror("Erreur","Veuillez entrer un nom de pièce valide.")

def supprimer_piece():
    """Fonction qui permet de supprimer une pièce à la liste des pièces"""
    nom_piece = input_nom_piece.get().strip() 
    # Empêche la suppression si une seule pièce dans la liste
    if listebox_pieces.size() <= 1:
        messagebox.showwarning("Alerte", "Vous ne pouvez pas supprimer la dernière pièce.")
        return
    # Tentative de suppression de la pièce dans la liste des pièces et dans le dictionnaire
    # où elle est stockée
    try:
        # Trouver l'index de la pièce à supprimer dans la Listbox
        index = listebox_pieces.get(0, END).index(input_nom_piece.get())
        # Supprimer la pièce de la Listbox
        listebox_pieces.delete(index)
        listebox_pieces.config(height=listebox_pieces.size())
        # Réinitialiser le champ de saisie
        input_nom_piece.set("")
        # Supprimer la pièce du dictionnaire de configuration si elle y est
        if nom_piece in configuration_pieces:
            del configuration_pieces[nom_piece]
        # Réinitialiser l'affichage en sélectionnant la première pièce
        listebox_pieces.selection_set(0)
        charger_configuration(None)
    # Si la pièce est introuvable dns la liste, affiche un message d'erreur
    except:
        messagebox.showerror("Erreur","La pièce que vous essayez de supprimer n'existe pas !")
        input_nom_piece.set("")

def charger_configuration(event):
    """Charge et applique la configuration enregistrée pour la pièce sélectionnée."""
    # Vérifie qu'une pièce est bien sélectionnée dans la liste
    selection = listebox_pieces.curselection()
    if not selection:
        return
    # Récupère le nom de la pièce sélectionnée et la définit comme pièce active
    piece_selectionnee = listebox_pieces.get(selection[0])
    global piece_actuelle
    piece_actuelle = piece_selectionnee
    # Met à jour le titre de la section dans la zone des réglages
    label_nom_piece_selectionnee.set(f"Réglage de la pièce {piece_actuelle}")
    # Si la pièce existe dans la configuration, on charge ses réglages
    if piece_selectionnee in configuration_pieces:
        config = configuration_pieces[piece_selectionnee]
        eclairage = config['eclairage']
        chauffage = config['chauffage']
        # Applique les réglages d'éclairage
        combobox_statut_eclairage.set(eclairage['statut'])
        combobox_couleur_eclairage.set(eclairage['couleur'])
        valeur_spinbox_intensite_eclairage.set(eclairage['intensite'])
        # Applique les réglages de chauffage
        combobox_etat_chauffage.set(chauffage['etat'])
        valeur_temperature.set(chauffage['temperature'])
        combobox_programme.set(chauffage['programme'])
        # Active/désactive les champs selon les états
        changer_etat_eclairage(None)
        changer_etat_chauffage(None)
    else:
        # Message d'erreur si problème dans la configuration
        messagebox.showerror("Erreur","La configuration de cette pièce est introuvable.")

def sauvegarder_configuration():
    """Enregistre les réglages actuels de la pièce sélectionnée 
    (éclairage et chauffage) dans le dictionnaire de configuration."""
    # Vérifie qu'une pièce est sélectionnée et existe dans la configuration
    if piece_actuelle and piece_actuelle in configuration_pieces:
        verifier_temperature() # Corrige les températures hors bornes si besoin
        config = configuration_pieces[piece_actuelle]

        # Sauvegarder les réglages de l'éclairage
        config['eclairage'] = {
            'statut': combobox_statut_eclairage.get(),
            'couleur': combobox_couleur_eclairage.get(),
            'intensite': int(valeur_spinbox_intensite_eclairage.get())
        }

        # Sauvegarder les réglages du chauffage
        config['chauffage'] = {
            'etat': combobox_etat_chauffage.get(),
            'temperature': int(spinbox_temperature.get()),
            'programme': combobox_programme.get()
        }
        # Affiche un message de confirmation
        messagebox.showinfo("Sauvegarde réussie",f"Configuration de la pièce « {piece_actuelle} »\nsauvegardée avec succès.")
    else:
        # Affiche un message d'erreur si aucune pièce n'est sélectionnée
        messagebox.showerror("Erreur","Aucune pièce sélectionnée.")


# -------------------------------------------------------------
# --------------Fonctions de gestion des réglages--------------
# -------------------------------------------------------------

def changer_etat_eclairage(event):
    """Active ou désactive les champs de de couleur et d'intensité de l'éclairage
    selon que l'éclairage est allumé ou éteint."""
    if combobox_statut_eclairage.get() == "Allumer":
        # Autorise la sélection de la couleur et de l’intensité
        combobox_couleur_eclairage.config(state= "normal")
        spinbox_intensite_eclairage.config(state='normal')
    else :
        # Désactive les champs si l’éclairage est éteint
        combobox_couleur_eclairage.config(state='disabled')
        spinbox_intensite_eclairage.config(state='disabled')


def changer_etat_chauffage(event) :
    """Active ou désactive les champs de température et de programme de chauffage
    selon que le chauffage est allumé ou éteint."""
    if combobox_etat_chauffage.get() == "Eteindre" :
        # Désactive les options de température et de programme
        spinbox_temperature.config(state="disabled")
        combobox_programme.config(state="disabled")
    else : 
        # Réactive les options de température et de programme
        spinbox_temperature.config(state="normal")
        combobox_programme.config(state="normal")

def verifier_temperature() :
    """Vérifie que la température saisie est bien dans les bornes autorisées (5°C à 30°C).
    Si ce n'est pas le cas, elle est automatiquement corrigée et un message d'avertissement est affiché."""
    if int(spinbox_temperature.get()) > 30 :
        # Température trop élevée : on la ramène à 30°C
        valeur_temperature.set(30)
        messagebox.showwarning("Alerte","La température est trop élevée ! Elle ne peut pas dépasser 30°C.")
        
    elif int(spinbox_temperature.get()) < 5 : 
        # Température trop basse : on la remonte à 5°C
        valeur_temperature.set(5)
        messagebox.showwarning("Alerte","La température est trop basse ! Elle ne peut pas être inférieure à 5°C.")

def appliquer_programme_chauffage(event) :
    """Ajuste automatiquement la température selon le programme de chauffage sélectionné
    et en fonction de l'heure actuelle."""
    # Récupère l'heure actuelle au format heure entière (0 à 23)
    heure_act = int(datetime.now().strftime('%H'))
    # Choix du programme et ajustement de la température en fonction de l'heure
    match combobox_programme.get() :
        case "Eco":
            if heure_act > 22 or heure_act < 7 : 
                valeur_temperature = 16
            else : 
                valeur_temperature = 18
        case "Hiver":
            if heure_act > 22 or heure_act < 7 : 
                valeur_temperature = 18
            else : 
                valeur_temperature = 20
        case "Ete":
            if heure_act > 22 or heure_act < 7 : 
                valeur_temperature = 26
            else : 
                valeur_temperature = 28
        case "Programmé" :
            if heure_act > 22 or heure_act < 7 : 
                valeur_temperature = 16
            else : 
                valeur_temperature = 20
        # Si aucun programme n'est sélectionné, on garde la valeur actuelle
        case _:
            valeur_temperature = spinbox_temperature.get()
    # Applique la température calculée dans la spinbox
    valeur_temperature = int(valeur_temperature)
    spinbox_temperature.delete(0,END)
    spinbox_temperature.insert(0,valeur_temperature)


# -------------------------------------------------------------
# ----------------Interface : cadres principaux----------------
# -------------------------------------------------------------

# Création de la fenêtre principale de l'application
ma_fenetre = Tk()
ma_fenetre.title("Système de domotique de la maison") # Titre affiché dans la barre de la fenêtre

# Définition de la taille de la fenêtre (largeur x hauteur en pixels)
ma_fenetre.geometry("900x650")

# Empêche le redimensionnement manuel de la fenêtre par l'utilisateur
ma_fenetre.resizable(False, False)

# Configuration du layout (grille) de la fenêtre principale
# La ligne 0 occupe tout l'espace vertical disponible
ma_fenetre.grid_rowconfigure(0, weight=1)

# Deux colonnes : colonne 0 (liste des pièces) plus étroite, colonne 1 (réglages) plus large
ma_fenetre.grid_columnconfigure(0, weight=2)
ma_fenetre.grid_columnconfigure(1, weight=5)


# ---- Cadre de gauche : liste des pièces et actions sur les pièces ----

# Création du cadre contenant la liste des pièces et les boutons Ajouter/Supprimer
cadre_pieces = Frame(ma_fenetre, 
                     bg='#222222',      # Fond sombre pour contraster avec les réglages à droite
                     width=200)         # Largeur fixe du cadre

# Configuration de la grille interne du cadre
cadre_pieces.grid_rowconfigure(0, weight=0)

# Permet à la colonne unique du cadre de s'étendre horizontalement si nécessaire
cadre_pieces.grid_columnconfigure(0, weight=1)

# ---- Cadre de droite : réglages de l'éclairage et du chauffage ----

# Cadre principal pour les réglages, placé à droite de la fenêtre
cadre_reglages = Frame(ma_fenetre, 
                      bg='#f2f2f2',     # Fond clair pour contraster avec le cadre de gauche
                      width=500)        # Largeur du cadre (plus large que la colonne des pièces)

# Sous-cadre pour les réglages liés à l'éclairage
cadre_eclairage = Frame(cadre_reglages, 
                        bg='#f2f2f2', 
                        padx=40,        # Marge intérieure à gauche et à droite
                        pady=20)        # Marge intérieure en haut et en bas

# Sous-cadre pour les réglages liés au chauffage
cadre_chauffage = Frame(cadre_reglages, 
                        bg='#f2f2f2', 
                        padx=40, 
                        pady=20)

# Placement des cadres dans la grille principale
cadre_pieces.grid(row=0,column=0,sticky="nsw")      # Colonne de gauche
cadre_reglages.grid(row=0,column=1,sticky="nsew")   # Colonne de droite
cadre_eclairage.grid(row=1, column=0, sticky="w")   # Éclairage (haut de la colonne de droite)
cadre_chauffage.grid(row=2, column=0, sticky="w")   # Chauffage (bas de la colonne de droite)


# -------------------------------------------------------------------
# -------------------Configuration du cadre de gauche----------------
# -------------------------------------------------------------------

# Variable pour afficher dynamiquement le nom de la pièce sélectionnée
label_nom_piece_selectionnee = StringVar()
label_nom_piece_selectionnee.set("Aucune pièce sélectionnée")   # Valeur par défaut

# Label affichant le nom de la pièce sélectionnée en haut du cadre
label_piece_selectionnee = Label(cadre_reglages, 
                                 textvariable=label_nom_piece_selectionnee, 
                                 font=('Arial', 24), 
                                 fg='#222222', 
                                 width=30)

# Bouton pour sauvegarder les réglages de la pièce actuelle
bouton_sauvegarder = Button(cadre_reglages, 
                            text="Valider", 
                            font=('Arial', 14, 'bold'), 
                            bg='#222222', 
                            fg='#f2f2f2', 
                            activebackground='#444444', 
                            activeforeground='#f2f2f2',
                            relief='flat',
                            padx=20, 
                            pady=10, 
                            cursor='hand2',
                            command=lambda: sauvegarder_configuration())    # Appelle la fonction de sauvegarde

# Placement du label et du bouton dans le cadre des réglages
label_piece_selectionnee.grid(row=0,column=0, pady=(20,10))
bouton_sauvegarder.grid(row=3,column=0, pady=(20,10))

# -------------------------------------------------------------------
# ---------------Liste des pièces dans le cadre de gauche------------
# -------------------------------------------------------------------

# Titre de la section "Pièces"
label_pieces = Label(cadre_pieces, 
                     text="Pièces", 
                     font=('Arial',20), 
                     bg='#222222', 
                     fg='#f2f2f2')

# Variable pour stocker la liste des pièces dans la Listbox
noms_pieces = StringVar()

# Listbox contenant les noms des pièces existantes
listebox_pieces = Listbox(cadre_pieces, 
                          listvariable=noms_pieces, 
                          font=('Arial',18), 
                          bg='#222222',
                          fg='#f2f2f2', 
                          selectbackground='#f2f2f2',   # Fond clair pour la sélection
                          selectforeground='#222222',   # Texte foncé sur sélection
                          selectmode=SINGLE,            # Une seule pièce sélectionnable à la fois
                          borderwidth=0, 
                          activestyle='none', 
                          justify='center',
                          highlightthickness=0)

# Initialise la Listbox avec les clés du dictionnaire de configuration
noms_pieces.set(list(configuration_pieces.keys()))

# Ajuste la hauteur de la Listbox au nombre de pièces
listebox_pieces.config(height=listebox_pieces.size())

# Lier la sélection de la pièce à l'affichage de sa configuration
# Quand l'utilisateur clique sur un nom de pièce dans la Listbox,
# on charge ses réglages automatiquement
listebox_pieces.bind("<<ListboxSelect>>", charger_configuration)


# -------------------------------------------------------------------
# --------------------Ajout et suppression de pièces-----------------
# -------------------------------------------------------------------

# Variable contenant le texte saisi par l'utilisateur (nom de la pièce à ajouter ou supprimer)
input_nom_piece = StringVar()

# Label d'instruction pour indiquer ce que l'utilisateur doit faire
label_ajouter_ou_supprimer = Label(cadre_pieces,
                                   text="Saisir le nom de la\npièce que vous souhaitez\najouter ou supprimer", 
                                   font=('Arial',14),
                                   bg='#222222',
                                   fg='#f2f2f2')

# Champ de saisie du nom de la pièce
saisie_nom_piece = Entry(cadre_pieces, 
                         textvariable=input_nom_piece, 
                         font=('Arial',14), 
                         bg='#f2f2f2',                  # Fond clair
                         fg='#222222',                  # Texte foncé
                         insertbackground='#222222',    # Couleur du curseur 
                         relief='flat',                 # Enlève le relief pour un aspect plus moderne
                         bd=1,                          # Ajoute une bordure fine
                         highlightthickness=1, 
                         highlightbackground='#cccccc', # Bordure gris clair
                         highlightcolor='#888888')      # Effet discret quand l'input est sélectionné

# Bouton pour ajouter une pièce à la liste
bouton_ajouter_piece = Button(cadre_pieces, text="Ajouter",
                              font=('Arial',14,'bold'), 
                              bg='#f2f2f2',
                              fg='#222222',
                              activebackground='#dddddd',
                              activeforeground='#222222',
                              relief='flat',
                              bd=0,
                              padx=10,
                              pady=5,
                              cursor='hand2',
                              width=12,
                              command=lambda: ajouter_piece())  # Appelle la fonction ajouter_piece()

# Bouton pour supprimer une pièce de la liste
bouton_supprimer_piece = Button(cadre_pieces, text="Supprimer",
                              font=('Arial',14,'bold'),
                              bg='#f2f2f2',
                              fg='#222222',
                              activebackground='#dddddd',
                              activeforeground='#222222',
                              relief='flat',
                              bd=0,
                              padx=10,
                              pady=5,
                              cursor='hand2',
                              width=12,
                              command=lambda: supprimer_piece()) # Appelle la fonction supprimer_piece()


# -------------------------------------------------------------------
# ---------Organisation de la grille dans le cadre de gauche---------
# -------------------------------------------------------------------

label_pieces.grid(row=0,column=0, pady=(40,20))
listebox_pieces.grid(row=1,column=0, pady=(0,20),sticky="ew")
label_ajouter_ou_supprimer.grid(row=2,column=0, pady=(30,0))
saisie_nom_piece.grid(row=3,column=0,padx=2,pady=10)
bouton_ajouter_piece.grid(row=4,column=0,padx=2,pady=2)
bouton_supprimer_piece.grid(row=5,column=0,padx=2,pady=2)


# -------------------------------------------------------------------
# -------------------Configuration du cadre de droite----------------
# -------------------------------------------------------------------

# Label pour la section des actions (réglages)
label_actions = Label(cadre_reglages, 
                      text="Actions", 
                      font=('Arial',20))


# -------------------------------------------------------------------
# ----------------------Paramétrage de l'éclairage-------------------
# -------------------------------------------------------------------

# Titre de la section "Éclairage"
label_eclairage = Label(cadre_eclairage, 
                        text="Eclairage", 
                        font=('Arial',18,'bold'), 
                        width=40, 
                        bg='#f2f2f2',
                        anchor='w')     # Alignement à gauche

# Variable pour stocker le statut de l'éclairage (Allumer / Éteindre)
options_eclairage = StringVar()

# Liste déroulante (Combobox) pour choisir le statut de l'éclairage
combobox_statut_eclairage = ttk.Combobox(cadre_eclairage,
                                         textvariable=options_eclairage,
                                         font=('Arial',14),
                                         width=42)

combobox_statut_eclairage['values'] = ('Allumer','Eteindre')
combobox_statut_eclairage.current(0)    # Valeur par défaut

# Label pour la couleur de l’éclairage
label_couleur_eclairage = Label(cadre_eclairage,
                                text="Couleur de l'éclairage",
                                font=('Arial',16),
                                width=40,
                                anchor='w',
                                bg='#f2f2f2')

# Variable pour stocker la couleur sélectionnée
options_couleur = StringVar()

# Liste déroulante pour choisir la couleur de la lumière
combobox_couleur_eclairage = ttk.Combobox(cadre_eclairage,
                                          textvariable=options_couleur,
                                          font=('Arial',14),
                                          width=42)

combobox_couleur_eclairage['values'] = ('Blanc',
                              'Jaune',
                              'Rouge',
                              'Vert',
                              'Bleu',
                              'Violet',
                              'Rose')
combobox_couleur_eclairage.current(0)    # Couleur par défaut

# Label pour l’intensité lumineuse
label_spinbox_intensite_eclairage = Label(cadre_eclairage, 
                                          text="Intensité lumineuse",
                                          font=('Arial',16),
                                          bg='#f2f2f2',
                                          anchor='w',
                                          width=40)

# Variable pour stocker la valeur de l’intensité lumineuse
valeur_spinbox_intensite_eclairage = StringVar()

# Spinbox (sélecteur numérique) pour choisir l’intensité entre 1 et 100
spinbox_intensite_eclairage = Spinbox(cadre_eclairage,
                                      from_=1,
                                      to=100,
                                      width=42,
                                      textvariable=valeur_spinbox_intensite_eclairage, 
                                      font=('Arial',14))

# Lier le changement de statut (Allumer/Éteindre) à l’activation/désactivation des champs associés
combobox_statut_eclairage.bind("<<ComboboxSelected>>", changer_etat_eclairage)


# -------------------------------------------------------------------
# ----------Organisation de la grille des widgets éclairage----------
# -------------------------------------------------------------------

label_eclairage.grid(row=0,column=0,pady=2)
combobox_statut_eclairage.grid(row=1,column=0,pady=2)
label_couleur_eclairage.grid(row=2, column=0,pady=2)
combobox_couleur_eclairage.grid(row=3,column=0,pady=2)
label_spinbox_intensite_eclairage.grid(row=4, column=0,pady=2)
spinbox_intensite_eclairage.grid(row=5,column=0,pady=2)



# -------------------------------------------------------------------
# -----------------------Paramétrage du chauffage--------------------
# -------------------------------------------------------------------

# Titre de la section chauffage
label_chauffage = Label(cadre_chauffage,
                        text="Chauffage :",
                        font=("Arial", 18, 'bold'),
                        width=40,
                        anchor='w')

# Options possibles pour le statut du chauffage
etats = ["Allumer", "Eteindre"]

# Liste déroulante pour choisir l'état du chauffage (allumé ou éteint)
combobox_etat_chauffage = ttk.Combobox(cadre_chauffage, 
                                       values=etats, 
                                       font=('Arial', 14),
                                       width=42)
combobox_etat_chauffage.current(0)  # Par défaut : allumé

# ---- Partie température ----

# Label pour la température de chauffage
label_temp = Label(cadre_chauffage, 
                   text="Température (en °C)", 
                   font=("Arial", 16),
                   bg='#f2f2f2', 
                   anchor='w', 
                   width=40)

# Variable qui stocke la température sélectionnée
valeur_temperature = IntVar()
valeur_temperature.set(16)  # Température par défaut

# Spinbox pour régler la température (valeurs de 5°C à 30°C)
spinbox_temperature = Spinbox(cadre_chauffage, 
                              from_=5, 
                              to=30, 
                              state="normal", 
                              textvariable=valeur_temperature, 
                              font=('Arial', 14),
                              width=42)

# ---- Partie programme ----

# Label pour la sélection du programme
label_programme = Label(cadre_chauffage, 
                        text="Programme", 
                        font=('Arial', 16),
                        bg='#f2f2f2', 
                        anchor='w', 
                        width=40)

# Liste des programmes de chauffage disponibles
choix_programme = ["Eco", "Hiver", "Ete", "Programmé", "Aucun"]

# Liste déroulante pour choisir un programme
combobox_programme = ttk.Combobox(cadre_chauffage, 
                                  values=choix_programme, 
                                  state="normal", 
                                  font=('Arial', 14),
                                  width=42)
combobox_programme.current(3)   # Par défaut : Programmé

# Lier les changements de sélection aux fonctions de mise à jour
combobox_etat_chauffage.bind("<<ComboboxSelected>>", changer_etat_chauffage)
combobox_programme.bind("<<ComboboxSelected>>", appliquer_programme_chauffage)

# -------------------------------------------------------------------
# ----------Organisation de la grille des widgets chauffage----------
# -------------------------------------------------------------------

label_chauffage.grid(row=1, column=0,pady=2)
combobox_etat_chauffage.grid(row=2, column=0,pady=2)
label_temp.grid(row=3, column=0,pady=2)
spinbox_temperature.grid(row=4, column=0,pady=2)
label_programme.grid(row=5, column=0,pady=2)
combobox_programme.grid(row=6, column=0,pady=2)



# -------------------------------------------------------------------
# --------------------Lancement de l'application---------------------
# -------------------------------------------------------------------

# Sélectionner la première pièce par défaut au démarrage
listebox_pieces.selection_set(0)
charger_configuration(None)

# Démarre la boucle principale de l'interface Tkinter
ma_fenetre.mainloop()