from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

piece_actuelle = None

# Dictionnaire pour stocker les configurations des pièces
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

def changer_etat_eclairage(event):
    """Fonction qui permet le réglage de la couleur et de l'intensité de l'éclairage si l'éclairage est allumé"""
    if combobox_statut_eclairage.get() == "Allumer":
        combobox_couleur_eclairage.config(state= "normal")
        spinbox_intensite_eclairage.config(state='normal')
    else :
        combobox_couleur_eclairage.config(state='disabled')
        spinbox_intensite_eclairage.config(state='disabled')

def ajouter_piece():
    """Fonction qui permet d'ajouter une pièce à la liste des pièces"""
    nom_piece = input_nom_piece.get().strip()
    if nom_piece and nom_piece not in configuration_pieces:
        # Ajouter la pièce à la liste
        listebox_pieces.insert(END, nom_piece)
        listebox_pieces.config(height=listebox_pieces.size())
        
        # Ajouter une configuration par défaut pour la pièce
        configuration_pieces[nom_piece] = {
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
        
        # Réinitialiser le champ de saisie
        input_nom_piece.set("")
    elif nom_piece in configuration_pieces:
        messagebox.showerror("Erreur","Cette pièce existe déjà !")
    else:
        messagebox.showerror("Erreur","Veuillez entrer un nom de pièce valide.")

def supprimer_piece():
    """Fonction qui permet de supprimer une pièce à la liste des pièces"""
    nom_piece = input_nom_piece.get().strip() 

    if listebox_pieces.size() <= 1:
        messagebox.showwarning("Alerte", "Vous ne pouvez pas supprimer la dernière pièce.")
        return
    
    try:
        index = listebox_pieces.get(0, END).index(input_nom_piece.get())
        listebox_pieces.delete(index)
        listebox_pieces.config(height=listebox_pieces.size())
        input_nom_piece.set("")
        
        if nom_piece in configuration_pieces:
            del configuration_pieces[nom_piece]

        # Réinitialiser l'affichage si la pièce supprimée était sélectionnée
        listebox_pieces.selection_set(0)
        charger_configuration(None)
    except:
        messagebox.showerror("Erreur","La pièce que vous essayez de supprimer n'existe pas !")
        input_nom_piece.set("")

def charger_configuration(event):
    selection = listebox_pieces.curselection()
    if not selection:
        return

    piece_selectionnee = listebox_pieces.get(selection[0])
    global piece_actuelle
    piece_actuelle = piece_selectionnee
    label_nom_piece_selectionnee.set(f"Réglage de la pièce {piece_actuelle}")

    if piece_selectionnee in configuration_pieces:
        config = configuration_pieces[piece_selectionnee]
        eclairage = config['eclairage']
        chauffage = config['chauffage']
        combobox_statut_eclairage.set(eclairage['statut'])
        combobox_couleur_eclairage.set(eclairage['couleur'])
        valeur_spinbox_intensite_eclairage.set(eclairage['intensite'])
        etat_chauffage.set(chauffage['etat'])
        valeur_temperature.set(chauffage['temperature'])
        combobox_programme.set(chauffage['programme'])
        changer_etat_eclairage(None)
        changer_etat_chauffage(None)

    else:
        messagebox.showerror("Erreur","La configuration de cette pièce est introuvable.")

def sauvegarder_configuration():
    if piece_actuelle and piece_actuelle in configuration_pieces:
        verifier_temperature()
        config = configuration_pieces[piece_actuelle]

        # Sauvegarde de l'éclairage
        config['eclairage'] = {
            'statut': combobox_statut_eclairage.get(),
            'couleur': combobox_couleur_eclairage.get(),
            'intensite': int(valeur_spinbox_intensite_eclairage.get())
        }

        # Sauvegarde du chauffage
        config['chauffage'] = {
            'etat': etat_chauffage.get(),
            'temperature': int(spinbox_temperature.get()),
            'programme': combobox_programme.get()
        }
       
        messagebox.showinfo("Sauvegarde réussie",f"Configuration de la pièce « {piece_actuelle} »\nsauvegardée avec succès.")
    else:
        messagebox.showerror("Erreur","Aucune pièce sélectionnée.")

def changer_etat_chauffage(event) :
    """Fonction pour allumer et éteindre le chauffage."""
    etat = etat_chauffage.get()
    if etat == "Eteindre" :
        spinbox_temperature.config(state="disabled")
        combobox_programme.config(state="disabled")
    else : 
        spinbox_temperature.config(state="normal")
        combobox_programme.config(state="normal")

def verifier_temperature() :
    """Fonction pour modifier le chauffage"""
    if int(spinbox_temperature.get()) > 30 :
        valeur_temperature.set(30)
        messagebox.showwarning("Alerte","La température est trop élevée ! Elle ne peut pas dépasser 30°C.")
        
    elif int(spinbox_temperature.get()) < 5 : 
        valeur_temperature.set(5)
        messagebox.showwarning("Alerte","La température est trop basse ! Elle ne peut pas être inférieure à 5°C.")

def appliquer_programme_chauffage(event) :
    """#Fonction pour programme économique, hiver, été, programé ou aucun"""
    heure_act = int(datetime.now().strftime('%H'))
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
        #Concerne si le choix du programme est aucun et que l'utilisateur veut choisir manuellement la température
        case _:
            valeur_temperature = spinbox_temperature.get()

    spinbox_temperature.config(values=valeur_temperature)


ma_fenetre = Tk()
ma_fenetre.title("Système de domotique de la maison")
ma_fenetre.geometry("900x600")

ma_fenetre.grid_rowconfigure(0, weight=1)
ma_fenetre.grid_columnconfigure(0, weight=2)
ma_fenetre.grid_columnconfigure(1, weight=5)
# Création du cadre ou se trouvent tous les paramétrages de l'éclairage

cadre_pieces = Frame(ma_fenetre, bg='#222222', width=200)
cadre_pieces.grid_rowconfigure(0, weight=0)
cadre_pieces.grid_columnconfigure(0, weight=1)

cadre_actions = Frame(ma_fenetre, bg='#f2f2f2', width=500) 
cadre_eclairage = Frame(cadre_actions)
cadre_chauffage = Frame(cadre_actions)

cadre_pieces.grid(row=0,column=0,sticky="nsw")
cadre_actions.grid(row=0,column=1,sticky="nsew")
cadre_eclairage.grid(row=1, column=0)
cadre_chauffage.grid(row=2, column=0)


# Configuration de la zone de séléction des pièces
label_nom_piece_selectionnee = StringVar()
label_nom_piece_selectionnee.set("Aucune pièce sélectionnée")
label_piece_selectionnee = Label(cadre_actions, textvariable=label_nom_piece_selectionnee, font=('Arial', 24), fg='#222222', width=30)
bouton_sauvegarder = Button(cadre_actions, text="Valider", font=('Arial', 14), command=lambda: sauvegarder_configuration())

label_piece_selectionnee.grid(row=0,column=0, pady=(20,10))
bouton_sauvegarder.grid(row=3,column=0, pady=(20,10))


label_pieces = Label(cadre_pieces, text="Pièces", font=('Arial',20), bg='#222222', fg='#f2f2f2')
noms_pieces = StringVar()
listebox_pieces = Listbox(cadre_pieces, listvariable=noms_pieces, font=('Arial',18), 
                          bg='#222222',fg='#f2f2f2', selectbackground='#f2f2f2',selectforeground='#222222',
                          selectmode=SINGLE, borderwidth=0, activestyle='none', justify='center',
                          highlightthickness=0)
noms_pieces.set(list(configuration_pieces.keys()))
listebox_pieces.config(height=listebox_pieces.size())

# Lier la sélection de la pièce à l'affichage de sa configuration
listebox_pieces.bind("<<ListboxSelect>>", charger_configuration)



input_nom_piece = StringVar()
label_ajouter_ou_supprimer = Label(cadre_pieces, text="Saisir le nom de la\npièce que vous souhaitez\najouter ou supprimer", 
                                   font=('Arial',14), bg='#222222', fg='#f2f2f2')
saisie_nom_piece = Entry(cadre_pieces, textvariable=input_nom_piece,font=('Arial',14), bg='#f2f2f2')
bouton_ajouter_piece = Button(cadre_pieces, text="Ajouter",
                              font=('Arial',14), command=lambda: ajouter_piece(),
                              bg='#f2f2f2',fg='#222222',width=10)

bouton_supprimer_piece = Button(cadre_pieces, text="Supprimer",
                              font=('Arial',14), command=lambda: supprimer_piece(),
                              bg='#f2f2f2',fg='#222222', width=10)

# Organisation de la grille de la zone de séléction des pièces

label_pieces.grid(row=0,column=0, pady=(40,20))
listebox_pieces.grid(row=1,column=0, pady=(0,20),sticky="ew")
label_ajouter_ou_supprimer.grid(row=2,column=0, pady=(30,0))
saisie_nom_piece.grid(row=3,column=0,padx=2,pady=10)
bouton_ajouter_piece.grid(row=4,column=0,padx=2,pady=2)
bouton_supprimer_piece.grid(row=5,column=0,padx=2,pady=2)


# Configuration de la zone d'actions
label_actions = Label(cadre_actions, text="Actions", font=('Arial',20))
# Séléction du statut de l'éclairage : Allumer ou Eteindre
label_eclairage = Label(cadre_eclairage, text="Eclairage", font=('Arial',20), anchor='w')

options_eclairage = StringVar()
combobox_statut_eclairage = ttk.Combobox(cadre_eclairage,textvariable=options_eclairage,font=('Arial',14))
combobox_statut_eclairage['values'] = ('Allumer','Eteindre')
combobox_statut_eclairage.current(0)

# Séléction de la couleur de l'éclairage
label_couleur_eclairage = Label(cadre_eclairage, text="Couleur de l'éclairage",
                                font=('Arial',16))
options_couleur = StringVar()
combobox_couleur_eclairage = ttk.Combobox(cadre_eclairage,textvariable=options_couleur,font=('Arial',14))
combobox_couleur_eclairage['values'] = ('Blanc',
                              'Jaune',
                              'Rouge',
                              'Vert',
                              'Bleu',
                              'Violet',
                              'Rose')
combobox_couleur_eclairage.current(0)

# Séléction de l'intensité de l'éclairage
label_spinbox_intensite_eclairage = Label(cadre_eclairage, text="Intensité lumineuse",
                                font=('Arial',16))
valeur_spinbox_intensite_eclairage = StringVar()
spinbox_intensite_eclairage = Spinbox(cadre_eclairage, from_=1, to=100, textvariable=valeur_spinbox_intensite_eclairage, font=('Arial',14))

combobox_statut_eclairage.bind("<<ComboboxSelected>>", changer_etat_eclairage)

# Affichage des différents éléments
label_eclairage.grid(row=0,column=0,pady=2)
combobox_statut_eclairage.grid(row=1,column=0,pady=2)
label_couleur_eclairage.grid(row=2, column=0,pady=2)
combobox_couleur_eclairage.grid(row=3,column=0,pady=2)
label_spinbox_intensite_eclairage.grid(row=4, column=0,pady=2)
spinbox_intensite_eclairage.grid(row=5,column=0,pady=2)

###partie qui décide de l'allumage
prez_chauffage = Label(cadre_chauffage, text="Chauffage :", font=("Arial", 20))

#définition des choix présents dans la liste box.
etats = ["Allumer", "Eteindre"]
etat_chauffage = ttk.Combobox(cadre_chauffage, values=etats, font=('Arial', 14))
etat_chauffage.current(0)

###Partie qui décide de la température
prez_temp = Label(cadre_chauffage, text="Température (en °C)", font=("Arial", 16))

valeur_temperature = IntVar()
valeur_temperature.set(16)
spinbox_temperature = Spinbox(cadre_chauffage, from_=5, to=30, state="normal", textvariable=valeur_temperature, font=('Arial', 14))

###Partie qui décide du programme
prez_programme = Label(cadre_chauffage, text="Programme", font=('Arial', 16))

choix_programme = ["Eco", "Hiver", "Ete", "Programmé", "Aucun"]
combobox_programme = ttk.Combobox(cadre_chauffage, values=choix_programme, state="normal", font=('Arial', 14))
combobox_programme.current(3)

etat_chauffage.bind("<<ComboboxSelected>>", changer_etat_chauffage)
combobox_programme.bind("<<ComboboxSelected>>", appliquer_programme_chauffage)

#placement des widgets
prez_chauffage.grid(row=1, column=0,pady=2)
etat_chauffage.grid(row=2, column=0,pady=2)
prez_temp.grid(row=3, column=0,pady=2)
spinbox_temperature.grid(row=4, column=0,pady=2)
prez_programme.grid(row=5, column=0,pady=2)
combobox_programme.grid(row=6, column=0,pady=2)


# Sélectionner la première pièce par défaut
listebox_pieces.selection_set(0)
charger_configuration(None)


ma_fenetre.mainloop()