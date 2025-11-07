######################################################
# Copyright © 2025 - Vincent Marie et Tiki Bouglon #
######################################################

#This file is part of the “LAN Messaging Project” and is distributed under the MIT license.
#See the LICENSE file for more details.

import tkinter as tk
import tkinter.messagebox
import tkinter.font
import Technique.Client as client
import colorsys
import random
import functools #pour envoyer des arguments avec les commandes de bouton tkinter




class GUI_nouvelle_connexion:
    def __init__(self):
        ### création de la GUI tkinter ###
        self.gui = tk.Tk()
        self.gui.title("Se connecter à un serveur")
        self.gui.minsize(width=400, height=150)
        self.gui.resizable(width=False, height=False)
        self.gui.configure(bg="#f4f4f4")  # Fond clair et moderne

        # Frame principale
        self.frame = tk.Frame(self.gui, bg="#f4f4f4", padx=10, pady=10)
        self.frame.grid(row=0, column=0, sticky="news")

        # Éléments de l'interface
        self.IP_label = tk.Label(self.frame, text="Adresse IP :", font=('Arial', 12), bg="#f4f4f4")
        self.IP_entree = tk.Entry(self.frame, font=('Arial', 14))
        
        self.Port_label = tk.Label(self.frame, text="Port :", font=('Arial', 12), bg="#f4f4f4")
        self.Port_entree = tk.Entry(self.frame, font=('Arial', 14))
        
        self.Pseudo_label = tk.Label(self.frame, text="Pseudo :", font=('Arial', 12), bg="#f4f4f4")
        self.Pseudo_entree = tk.Entry(self.frame, font=('Arial', 14))

        self.envoi_donnees = tk.Button(self.frame, text="Se connecter", font=('Arial', 12), bg="#008CBA", fg="white", padx=10, pady=5, command=self.recuperer_infos)

        # Placement des éléments
        self.IP_label.grid(row=0, column=0, sticky="w", pady=5)
        self.IP_entree.grid(row=0, column=1, pady=5, padx=5)
        
        self.Port_label.grid(row=1, column=0, sticky="w", pady=5)
        self.Port_entree.grid(row=1, column=1, pady=5, padx=5)
        
        self.Pseudo_label.grid(row=2, column=0, sticky="w", pady=5)
        self.Pseudo_entree.grid(row=2, column=1, pady=5, padx=5)
        
        self.envoi_donnees.grid(row=3, column=1, pady=10)
     
        self.frame.pack(fill = "x")
        self.charger_infos_enregistrees()
        
            
            
            

    
    def charger_infos_enregistrees(self):
        nombre_lignes_max = 10
        lignes = []
        try:
            with open('infos.txt', 'r') as file:
                fichier_vide = True
                for line in file:
                    fichier_vide = False
                    lignes.append(line)
            
            
        except:
            creer_fichier =  open("infos.txt", "x")
            creer_fichier.close()
        else:
            if not fichier_vide:
                self.newframe = tk.Frame(self.gui)
                self.newframe.columnconfigure(0, weight = 1)
                self.newframe.columnconfigure(1, weight = 1)
                self.newframe.columnconfigure(2, weight = 1)
                self.newframe.columnconfigure(3, weight = 1)
                self.newframe.rowconfigure(0,weight = 2)
                self.labeltitre = tk.Label(self.newframe,
                                           text = "Anciennes connexions...")
                self.labeltitre.grid(row = 0, column = 0, columnspan = 4)
                
                self.newframe.rowconfigure(1,weight = 1)
                
                self.labeliptitre = tk.Label(self.newframe,
                                        text = "IP :")
                self.labeliptitre.grid(column = 0, row = 1)
                self.labelporttitre = tk.Label(self.newframe,
                                          text = "Port :")
                self.labelporttitre.grid(column = 1, row = 1)
                self.labelpseudotitre = tk.Label(self.newframe,
                                            text = "Pseudo :")
                self.labelpseudotitre.grid(column = 2, row = 1)
                    
                y = 2
                for l in lignes:
                    if nombre_lignes_max == 0:
                        break
                    nombre_lignes_max -= 1
                    elements = l.split()
                    self.newframe.rowconfigure(y, weight = 1)
                    
                    self.labelip = tk.Label(self.newframe,
                                            text = elements[0])
                    self.labelip.grid(column = 0, row = y)
                    self.labelport = tk.Label(self.newframe,
                                              text = elements[1])
                    self.labelport.grid(column = 1, row = y)
                    self.labelpseudo = tk.Label(self.newframe,
                                                text = elements[2])
                    self.labelpseudo.grid(column = 2, row = y)
                    
                    self.bouton_login = tk.Button(self.newframe,
                                                  text = "connexion rapide",
                                                  command = functools.partial(self.recuperer_infos_rapide,
                                                                              elements))
                    self.bouton_login.grid(column = 3, row = y)
                    y += 1
                
                self.newframe.pack(fill = "x")
        
        """for wid in self.frame.winfo_children():
            print(wid.grid_info())
              
        print("Total lines:", line_count)
        self.IP_entree.insert(0, str(INFOS[0]))
        self.Port_entree.insert(0, str(INFOS[1]))
        self.Pseudo_entree.insert(0, str(INFOS[2]))
        """
        
    def recuperer_infos(self):
        info = {}
        try:
            info["IP"] = self.IP_entree.get()
            info["Port"] = int(self.Port_entree.get())
            info["Pseudo"] = bytes(self.Pseudo_entree.get(),encoding = "UTF-8")
            assert len(info["Pseudo"].split()) == 1, "pas d'espace dans le pseudo !!!"
            if len(info["Pseudo"]) >= 32:
                raise MemoryError()
            
        except AssertionError:
            tk.messagebox.showinfo(title = "Erreur", message = "Il ne faut pas d'espace dans le pseudo !!!")
        except MemoryError:
            tk.messagebox.showinfo(title = "Erreur", message = "Le pseudo doit faire maximum 31 de long !!!")
        except:
            tk.messagebox.showinfo(title = "Erreur", message = "Vous avez entrez des données non-conformes !!!\nPort doit être convertible en int\nPseudo doit être convertible en bytes")
        else:
            self.connexion = client.se_co(info["IP"],info["Port"],info["Pseudo"])
            self.connexion.nouvelle_connexion()
            print(self.connexion.estCo())
            if self.connexion.estCo():
                self.gui.destroy()
                self.garder_infos(info)
                GUI_messagerie(info,self.connexion)
            else:
                tk.messagebox.showinfo(title = "Erreur", message = "Adresse IP ou Port incorrect !!!")
        
    def recuperer_infos_rapide(self,elem):
        ip = elem[0]
        port = int(elem[1])
        pseudo = bytes(elem[2],encoding = "UTF-8")
        assert len(pseudo.split()) == 1, "pas d'espace dans le pseudo !!!"
        self.connexion = client.se_co(ip,port,pseudo)
        self.connexion.nouvelle_connexion()
        if self.connexion.estCo() == True:
            self.gui.destroy()
            GUI_messagerie({"IP":ip,"Port":port,"Pseudo":pseudo},self.connexion)
        else:
            tk.messagebox.showinfo(title = "Échec de connexion", message = "La connexion n'a pas pu être établie !!!\n L'adresse IP et/ou le port demandés n'existent pas où sont éteints")
    
    def garder_infos(self,info):
        a_enregistrer = info["IP"]
        a_enregistrer += f" {str(info['Port'])}"
        a_enregistrer += f" {info['Pseudo'].decode()}"
        print(a_enregistrer)
        a_enregistrer = [a_enregistrer]
        with open('infos.txt', "r") as fichier_infos:
            contenu = fichier_infos.read()
        
        print(contenu)
        contenu = contenu.split("\n")
        print(contenu)
        for ligne in contenu:
            a_enregistrer.append(ligne)
        while len(a_enregistrer) > 10 :
            a_enregistrer.pop()
        for ligne in range(len(a_enregistrer)-1):
            a_enregistrer[ligne] += "\n"
        with open('infos.txt', "w") as fichier_infos:
            fichier_infos.writelines(a_enregistrer)


class GUI_messagerie:
    def __init__(self,info,connexion):
        self.info = info
        self.connexion = connexion
        
        self.gui = tk.Tk()
        self.name = info["Pseudo"].decode("utf-8")
        self.gui.title(f"Messagerie : connecté au serveur {info['IP']}")
        #self.gui.resizable(width=False, height=False)
        self.gui.configure(bg="#202225")
        self.gui.geometry("900x550") #810x570
        self.photo = tk.PhotoImage(file="Logo/bouton_denvoi.png")
        self.photo_theme_jour = tk.PhotoImage(file="Logo/icone_theme_jour.png")
        self.photo_theme_nuit = tk.PhotoImage(file="Logo/icone_theme_nuit.png")
        self.photo_scroll = tk.PhotoImage(file="Logo/icone_autoscroll.png")
        self.photo_scroll_2 = tk.PhotoImage(file="Logo/icone_autoscroll_2.png")
        self.photo_disco = tk.PhotoImage(file="Logo/icone_discoball.png")
        
        self.topBar = tk.Frame(self.gui, bg="#FFFFFF", height=20)
        self.topBar.pack(fill="x")

        self.buttontheme = tk.Button(self.topBar, image=self.photo_theme_nuit, bg="#FFFFFF", font="Helvetica 8", bd=0, padx=2, pady=1,  command = self.toggleTheme)
        self.buttontheme.pack(side="left", padx=0, pady=0)
        self.buttontheme.bind("<Enter>", self.on_enter)
        self.buttontheme.bind("<Leave>", self.on_leave)
        self.theme = "nuit" #quel thème ?
        
        self.buttonscroll = tk.Button(self.topBar, image=self.photo_scroll, bg="#FFFFFF", font="Helvetica 8", bd=0, padx=2, pady=1, command = self.toggleAutoscroll)
        self.buttonscroll.pack(side="left", padx=0, pady=0)
        self.buttonscroll.bind("<Enter>", self.on_enter)
        self.buttonscroll.bind("<Leave>", self.on_leave)
        
        self.buttondisco = tk.Button(self.topBar, image=self.photo_disco, bg="#FFFFFF", font="Helvetica 8", bd=0, padx=2, pady=1, command = functools.partial(self.toggleDisco, True))
        self.buttondisco.pack(side="left", padx=0, pady=0)
        self.buttondisco.bind("<Enter>", self.on_enter)
        self.buttondisco.bind("<Leave>", self.on_leave)
        self.disco = False #le mode disco est-il activé ?
        
        # En-tête du pseudo
        self.labelHead = tk.Label(self.gui, text=self.name, bg="#2f3136", fg="#EAECEE",
                                  font="Helvetica 13 bold", pady=11)
        
        
        self.labelHead.pack(fill="x")

        # Ligne de séparation
        self.line2 = tk.Label(self.gui, bg="#202225", width=440)
        self.line2.place(relwidth=1, rely=0.12, relheight=0.012)

        # Ajouter une colonne à gauche sous le labelHead
        self.leftColumn = tk.Frame(self.gui, bg="#2f3136")  # Largeur de la colonne (ajustable)
        self.leftColumn.pack(side="left", fill="y", padx=6, pady=5)
        self.leftColumn.columnconfigure(0, minsize = 80)
        self.leftColumn.rowconfigure(0, weight = 1)
        self.leftColumn.rowconfigure(1, weight = 1)
        self.leftColumn.rowconfigure(2, weight = 1, minsize = 400)
        
        # Exemple de contenu dans la colonne
        self.leftLabel1 = tk.Button(self.leftColumn, text="Général", bg="#40444b", font="Helvetica 10",fg="#FFFFFF",
                                   command = functools.partial(self.changer_chat, "general"))
        self.leftLabel1.grid(row = 0, sticky = "news")

        self.leftLabel2 = tk.Button(self.leftColumn, text="Message", bg="#40444b", font="Helvetica 10",fg="#FFFFFF",
                                   command = functools.partial(self.changer_chat, "prive"))
        self.leftLabel2.grid(row = 1, sticky = "news")

        # Zone des messages avec barre de défilement
        self.frame_messages = tk.Frame(self.gui, bg="#17202A")
        self.frame_messages.pack(expand=True, fill="x", padx=4, pady=4)


        self.textCons = tk.Text(self.frame_messages, bg="#40444b", fg="#EAECEE",
                                font="Helvetica 14", padx=6, pady=4, height=13, width=40, wrap="word")
        self.textCons.pack(side="left", fill="both", expand=True)
        self.nombre_ligne = 1.0
        self.font_14 = tkinter.font.Font(family = "Nakula", size = 14)
        self.font_13_bold = tkinter.font.Font( family = "Andika", size = 13,weight="bold", slant="italic")
        self.textCons.tag_configure("tag_join", font=self.font_13_bold, foreground= "#90cc87")
        self.textCons.tag_configure("tag_quit", font=self.font_13_bold, foreground= "#d48c8c")
        self.textCons.tag_configure("tag_message", font=self.font_14)
        self.textCons.config(spacing1=10)
        
        self.scrollbar = tk.Scrollbar(self.frame_messages, command=self.textCons.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.autoscroll = False
        self.textCons.config(yscrollcommand=self.scrollbar.set)

        # Label du bas plus large
        self.frameBottom = tk.Frame(self.gui, bg="#2f3136")
        self.frameBottom.pack(fill="x", padx=5, pady=5)
        self.frameBottom.rowconfigure(0, minsize = 1)
        # Zone de saisie à gauche
        self.entryMsg = tk.Entry(self.frameBottom, bg="#36393e", fg="#EAECEE",
                                 font="Helvetica 13", width=84)
        self.entryMsg.pack(side = "left", pady=4 ,padx=4)
        self.entryMsg.bind("<Return>", self.entrée)
        self.entryMsg.focus()

        # Bouton d'envoi à droite
        self.buttonMsg = tk.Button(self.frameBottom, image=self.photo, bg="#5E646E",
                                   command=self.envoyer)
        self.buttonMsg.pack(pady=4, anchor = "center")
        
        
        
        self.chat = "general"
        
        self.gui.protocol("WM_DELETE_WINDOW", self.fermer_fenetre)
        ### lancer l'actualisation permanente ###
        self.lancer_actualisation()

    def fermer_fenetre(self):
        self.connexion.quitter()
        self.gui.destroy()
            
    def toggleTheme(self):
        
        self.disco = None
        # Choisir la nouvelle couleur de fond et de texte en fonction du thème actuel
        if self.theme == "nuit":
            self.theme = "jour"
            new_bg = "#ABB2B9" # Thème clair
            new_fg = "#000000"
            top_bar_bg = "#ABB2B9" # Couleur claire pour la barre du haut
            bottom_bar_bg = "#E6E6E6" # Couleur claire pour la barre du bas
            left_column_bg = "#E6E6E6" # Couleur claire pour la colonne de gauche
            text_area_bg = "#EBEBEB" # Couleur claire pour la zone de messages
            entry_bg = "#ffffff" # Couleur claire pour la zone de saisie
            label_color = "#F2F2F2"
            line = "#ABB2B9"
            bouttonMsg = "#EBEBEB"
            image = self.photo_theme_jour
        else:
            self.theme = "nuit"
            new_bg = "#202225" # Thème sombre
            new_fg = "#EAECEE"
            top_bar_bg = "#FFFFFF" # Couleur claire pour la barre du haut en thème sombre (pour le contraste)
            bottom_bar_bg = "#2f3136" # Couleur plus claire pour la barre du bas en thème sombre
            left_column_bg = "#2f3136" # Couleur sombre pour la colonne de gauche
            text_area_bg = "#40444b" # Couleur sombre pour la zone de messages
            entry_bg = "#36393e" # Couleur sombre pour la zone de saisie 
            label_color = "#40444b"
            line = "#202225"
            bouttonMsg = "#6D7480"
            image = self.photo_theme_nuit
            
        # Appliquer les nouvelles couleurs aux différents éléments de l'interface
        self.gui.configure(bg=new_bg)
        self.labelHead.configure(bg=bottom_bar_bg, fg=new_fg)
        self.line2.configure(bg=line) # On utilise la couleur de la barre du haut pour la ligne
        self.leftColumn.configure(bg=left_column_bg)
        self.leftLabel1.configure(bg=label_color, fg=new_fg)
        self.leftLabel2.configure(bg=label_color, fg=new_fg)
        self.frame_messages.configure(bg=new_bg)
        self.textCons.configure(bg=text_area_bg, fg=new_fg)
        self.frameBottom.configure(bg=bottom_bar_bg)
        self.entryMsg.configure(bg=entry_bg, fg=new_fg)
        self.buttonMsg.configure(bg=bouttonMsg)
        self.buttontheme.configure(image = image)
        self.buttontheme.photo = image
            
    def toggleAutoscroll(self):
        """ active ou désactive la fonctionnalité AutoScroll
        cette fonctionnalité permet que dès qu'un message est reçu ou envoyé,
        la fenêtre des messages défile vers le bas"""
        self.autoscroll = not self.autoscroll
        if self.autoscroll:
            self.buttonscroll.configure(image = self.photo_scroll_2)
            self.buttonscroll.photo = self.photo_scroll_2
        else:
            self.buttonscroll.configure(image = self.photo_scroll)
            self.buttonscroll.photo = self.photo_scroll
        
    def toggleDisco(self, change = False):
        if change:
            self.disco = not self.disco
        if self.disco == True:
            hue = random.uniform(0.0,1.0)
            self.gui.configure(bg =  convertir_hsv_hex(hue, 1, 0.8))
            self.labelHead.configure(bg= convertir_hsv_hex(hue, 1, 0.9), fg= convertir_hsv_hex(hue, 0.5, 1))
            self.line2.configure(bg= convertir_hsv_hex(hue, 1, 0.8)) 
            self.leftColumn.configure(bg= convertir_hsv_hex(hue, 1, 0.9))
            self.leftLabel1.configure(bg= convertir_hsv_hex(hue, 1, 1), fg= convertir_hsv_hex(hue, 0.5, 0.9))
            self.leftLabel2.configure(bg= convertir_hsv_hex(hue, 1, 1), fg= convertir_hsv_hex(hue, 0.5, 0.9))
            self.frame_messages.configure(bg= convertir_hsv_hex(hue, 0.9, 1))
            self.textCons.configure(bg= convertir_hsv_hex(hue, 0.9, 1), fg= convertir_hsv_hex(hue, 0.4, 0.9))
            self.frameBottom.configure(bg= convertir_hsv_hex(hue, 1, 0.9))
            self.entryMsg.configure(bg= convertir_hsv_hex(hue, 0.9, 1), fg= convertir_hsv_hex(hue, 0.4, 0.9))
            self.buttonMsg.configure(bg= convertir_hsv_hex(hue, 0.8, 1))
            self.gui.after(300, self.toggleDisco)
        elif self.disco == False:
            if self.theme == "nuit": #permet de remettre l'ancien thème (sans ça le thème change quand on désactive disco)
                self.theme = "jour"
            else:
                self.theme = "nuit"
            self.toggleTheme() #remet l'ancien thème
            self.disco = None
        else: #résout un bug où le thème était changé deux fois
            self.disco == False
        
        
    def on_enter(self, event):
        widget = event.widget
        current_bg = widget["bg"]
        if current_bg == "#ABB2B9":
            widget.config(bg="#99A3A4")
        elif current_bg == "#f0f0f0": # Pour le thème clair
            widget.config(bg="#d9d9d9")
        elif current_bg == "#FFFFFF": # Pour le thème sombre (barre claire)
            widget.config(bg="#e6e6e6")

    def on_leave(self, event):
        widget = event.widget
        current_bg = widget["bg"]
        if current_bg == "#99A3A4":
            widget.config(bg="#ABB2B9")
        elif current_bg == "#d9d9d9":
            widget.config(bg="#f0f0f0")
        elif current_bg == "#e6e6e6":
            widget.config(bg="#FFFFFF")
    
    def changer_chat(self, quel_chat):
        self.peut_update = False
        if quel_chat == "general":
            if self.chat != "general":
                self.chat = "general"
                self.labelHead["text"] = self.name
                self.textCons.config(state="normal")
                self.textCons.delete('1.0', tk.END)
                self.textCons.config(state="disabled")
                self.connexion.resetIdMsg(quel_chat)
                self.lancer_actualisation()
        else:
            self.chat_demande = tk.Toplevel(self.gui)
            self.chat_demande.protocol("WM_DELETE_WINDOW", self.chat_mp)
            self.chat_demande.grab_set() #empêche un input quelquonque sur la messagerie tant qu'un pseudo n'est pas renseigné
            self.chat_demande_entree = tk.Entry(self.chat_demande)
            self.chat_demande_entree.focus()
            self.chat_demande_entree.pack()
            self.chat_demande_envoi = tk.Button(self.chat_demande,command = self.chat_mp, text = "Démarrer une\ndiscussion")
            self.chat_demande_envoi.pack()
            self.connexion.resetIdMsg(quel_chat)
            self.chat_demande.mainloop()
        
            
    def chat_mp(self):
        self.chat = self.chat_demande_entree.get()
        if len(self.chat) < 32 and len(self.chat) > 0:
            self.chat_demande.destroy()
            self.labelHead["text"] = f"{self.name} → {self.chat}"
            self.textCons.config(state="normal")
            self.textCons.delete('1.0', tk.END)
            self.textCons.config(state="disabled")
            self.lancer_actualisation()
        elif len(self.chat) == 0 :
            tk.messagebox.showinfo(title = "Erreur", message = "Veuillez entrer un pseudo !!!")
        else :
            tk.messagebox.showinfo(title = "Erreur", message = "Le pseudo entré a trop de caractères !!!\n(max 31)")
            
    
    
    def entrée(self, event):
        self.envoyer()
    
    def recevoir(self):
        """fonction qui reçoit les messages
        le message est stocké dans la variable messages"""
        if self.peut_update == True:
            messages = self.connexion.ecouter(self.chat)
            if len(messages) > 0:
                for message in messages: 
                    self.textCons.config(state="normal")
                    
                    ### traitement du message ###
                    if message[0] == "New":
                        self.textCons.insert("end", f"{message[1]}\n")
                        self.textCons.tag_add("tag_join", self.nombre_ligne, f"{self.nombre_ligne} lineend") 
                    elif message[0] == "Bye":
                        self.textCons.insert("end", f"{message[1]}\n")
                        self.textCons.tag_add("tag_quit", self.nombre_ligne, f"{self.nombre_ligne} lineend")
                    elif message[0] == "Msg":
                        self.textCons.insert("end", f"{message[1]}: {message[2]}\t\t\t\t\t\t\t\t{message[3]}\n")         
                        self.textCons.tag_add("tag_message", self.nombre_ligne, f"{self.nombre_ligne} lineend")
                    elif message[0] == "Msp":
                        self.textCons.insert("end", f"{message[1]}: {message[2]}\t\t\t\t\t\t\t\t{message[3]}\n")
                    
                    self.nombre_ligne += 1
                    self.textCons.config(state="disabled")
                    
                    if self.autoscroll:
                        self.textCons.see("end")
                        
            if self.chat != "general":
                self.nombre_ligne = 1.0
            
            
            self.gui.after(1000, self.recevoir)
        
    def lancer_actualisation(self):
        """fonction qui lance la fonction recevoir
        à ne pas modifier"""
        self.peut_update = True
        self.recevoir()
        self.gui.mainloop()
        
    def envoyer(self):
        message = self.entryMsg.get()
        if not message == False: #empêcher l'envoi de messages vides
            self.connexion.envoyer_message(message, self.chat)
            self.entryMsg.delete(0, tk.END)


def convertir_hsv_hex(hue,sat,val):
    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    r, g, b = hex(int(r * 255)), hex(int(g * 255)), hex(int(b * 255))

    finalrgb = "#"
    for rgb in (r,g,b):
        if len(rgb) == 3:
            finalrgb += "0"
        for ind,val in enumerate(rgb):
            if ind > 1:
                finalrgb += str(val)
    return finalrgb

a = GUI_nouvelle_connexion()
a.gui.mainloop()