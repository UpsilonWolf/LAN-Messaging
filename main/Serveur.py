######################################################
# Copyright © 2025 - Vincent Marie et Tiki Bouglon #
######################################################

#This file is part of the “LAN Messaging Project” and is distributed under the MIT license.
#See the LICENSE file for more details.

import socket
import tkinter as tk
PORT = None

class GUI_Serveur:
    def __init__(self):
        global PORT
        self.window = tk.Tk()
        self.window.title("Port de Communication")
        self.window.geometry('250x125')
        self.window.configure(background = '#dce1e2')
        self.window.resizable(width=False, height=False)

        # Charge le dernier port depuis un fichier
        PORT = self.load_last_port()
        
        ### centrage : au-dessus ###
        self.label_nord_centrer = tk.Label(self.window,
                                           background = "#DCE1E2")
        self.label_nord_centrer.pack()
        
        ### frame contenant tous les éléments ###
        self.frame = tk.Frame(self.window, background = "#DCE1E2")
        self.frame.rowconfigure(0, weight = 1)
        self.frame.rowconfigure(1, weight = 1)
        self.frame.rowconfigure(2, weight = 1)
        self.frame.columnconfigure(0, weight = 1, uniform = "1")
        self.frame.columnconfigure(1, weight = 1, uniform = "1")
            
        
        
        self.label_port = tk.Label(self.frame,
                                   text="Veuillez entrer le port")
        self.label_port.grid(row = 0, column = 0, columnspan = 2)
        self.label_port.configure(bg='#dce1e2')

        self.entry_port = tk.Entry(self.frame)
        self.entry_port.grid(row = 1, column = 0, columnspan = 2)
        
        if PORT != None :
            self.entry_port.insert(0, str(PORT))
        
        self.bouton_fermer = tk.Button(self.frame,
                                       text="Fermer",
                                       command=self.close,
                                       fg="red")
        self.bouton_fermer.grid(row=2,column = 0, sticky = "w", pady = 10)
        
        self.bouton_envoyer = tk.Button(self.frame, text="Envoyer", command=self.port_envoyer, fg="blue")
        self.bouton_envoyer.grid(row=2,column = 1, sticky = "e")

        
        self.frame.pack(anchor = "n")
        
        self.window.mainloop()

    def port_envoyer(self):
        global PORT
        
        ### récupération ###
        temp_port = self.entry_port.get()
        
        ### tests pour voir si le port est valide ###
        try :
            temp_port = int(temp_port)
        except :
            tk.messagebox.showerror("Erreur : Port du serveur",
                                    "Le port doit être un nombre !!!")
        else:
            if temp_port < 1025 or temp_port > 65535:
                tk.messagebox.showerror("Erreur : Port du serveur",
                                        "Le port doit être entre 1025 et 65535 !!!")
            ### stockage du port si il est valide ###
            else:
                PORT = temp_port
                self.save_last_port(PORT)
                self.window.destroy()
        

    def close(self):
        global PORT
        PORT = None  # Définit PORT comme None avant de fermer
        self.window.destroy()  # Ferme la fenêtre

    def load_last_port(self):
        """Charge le dernier port utilisé depuis un fichier."""
        try:
            with open("dernier_port.txt", "r") as fichier_port:
                derniere_ligne = fichier_port.read().strip()
                return int(derniere_ligne)
        except :
            
            return None  # Retourne None si le fichier n'existe pas ou contient une valeur invalide

    def save_last_port(self, port):
        """Enregistre le dernier port utilisé dans un fichier."""
        with open("dernier_port.txt", "w") as fichier_port:
            fichier_port.write(str(port))





def lancer(adresse):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(adresse)
        sock.listen()
        print(f"Serveur démarré sur {adresse[0]}:{adresse[1]}.")
        
        
        compteur_messages = 0
        liste_messages = {}
        liste_messages_prive = {}
        while True:  # Boucle infinie pour accepter plusieurs connexions
            
            print("En attente de connexion...")
            nc_client, adresse_client = sock.accept()
             
            
            # Communication avec le client
            try:
                nc_client.settimeout(1)
                # Réception du message du client
                type_connexion = nc_client.recv(7).decode()
                
                nc_client.settimeout(None)
                if not type_connexion:
                    nc_client.close()
                    print("connexion fermée par le client")
                print(type_connexion)
                
                ### première connexion serveur-client ###
                if type_connexion == "premier":
                    pseudo = nc_client.recv(32).decode("utf-8")
                    print(f"Client connecté depuis : {adresse_client[0]}:{adresse_client[1]}")
                    print(f"{pseudo} a rejoint le chat !")
                    liste_messages[compteur_messages] = (("New",f"{pseudo} a rejoint le chat !"))
                    nc_client.send(bytes(str(liste_messages[compteur_messages]), encoding="utf-8"))  # Répond au client
                    compteur_messages += 1
                
                ### réception d'un message ###
                elif type_connexion == "message":
                    #réception pseudo
                    pseudo = nc_client.recv(32).decode("utf-8") #qui envoie ?
                    nc_client.send(b"recu")
                    message = nc_client.recv(1024).decode("utf-8") #qu'envoie-t-il ?
                    nc_client.send(b"recu")
                    heure = nc_client.recv(1024).decode("utf-8") #à quelle heure ?
                    if message:
                        nc_client.send(b"recu")
                        chat = nc_client.recv(32).decode("utf-8")#où l'envoie-t-il ?
                    
                    if not message:
                        print("Un message corrompu a été reçu")
                    elif chat == "general":
                        liste_messages[compteur_messages] = (("Msg",pseudo,message,heure))
                        print(f"Message reçu : {message} - Depuis : {adresse_client[0]} à {heure}")
                        print(liste_messages)
                        compteur_messages += 1
                    else:
                        
                            
                        
                        
                        taille1 = liste_messages_prive[chat][pseudo]["nb"] 
                        liste_messages_prive[chat][pseudo]["nb"] = taille1 + 1
                        taille2 = liste_messages_prive[pseudo][chat]["nb"] 
                        liste_messages_prive[pseudo][chat]["nb"] = taille2 + 1
                        
                        liste_messages_prive[chat][pseudo][taille1] = [pseudo, message, heure]
                        liste_messages_prive[pseudo][chat][taille2] = [pseudo, message, heure]
                        
                        
                        
                    
                ### demande du client de récupérer les messages ###
                elif type_connexion == "ecouter":
                    #quel chat ?
                    le_chat = nc_client.recv(32).decode()
                    nc_client.send(b"recu")
                    
                    #id du dernier message du client
                    if le_chat == "general":
                        compteur_message_client = compteur_messages - int(nc_client.recv(1024).decode())
                    else:
                        le_pseudo = nc_client.recv(32).decode()
                        nc_client.send(b"recu")
                        
                        if le_chat not in liste_messages_prive.keys():
                            liste_messages_prive[le_chat] = {}
                        if le_pseudo not in liste_messages_prive.keys():
                            liste_messages_prive[le_pseudo] = {}
                        if le_chat not in liste_messages_prive[le_pseudo].keys():
                            liste_messages_prive[le_pseudo][le_chat] = {"nb":0}
                        if le_pseudo not in liste_messages_prive[le_chat].keys():
                            liste_messages_prive[le_chat][le_pseudo] = {"nb":0}
                            
                        compteur_message_client = liste_messages_prive[le_pseudo][le_chat]["nb"] - int(nc_client.recv(1024).decode())
                        
                    #id du dernier message sur le serveur
                    nc_client.send(bytes(str(compteur_message_client), encoding = "utf-8"))
                    #envoi des messages manquants
                    print(compteur_message_client,compteur_messages)
                    if le_chat == "general":
                        for i in range(compteur_messages - compteur_message_client, compteur_messages):
                            print(i)
                            print(liste_messages[i])
                            nc_client.recv(4) #ici le client envoie "recu"
                            nc_client.sendall(bytes(str(liste_messages[i][0]), encoding="utf-8")) #type msg
                            nc_client.recv(4) #ici le client envoie "recu"
                            nc_client.sendall(bytes(str(liste_messages[i][1]), encoding="utf-8")) #pseudo
                            if liste_messages[i][0] == "Msg":
                                nc_client.recv(4)
                                nc_client.sendall(bytes(liste_messages[i][2], encoding="utf-8")) #message
                                nc_client.recv(4)
                                nc_client.sendall(bytes(liste_messages[i][3], encoding="utf-8")) #heure
                    else:
                        for i in range(liste_messages_prive[le_pseudo][le_chat]["nb"] - compteur_message_client, liste_messages_prive[le_pseudo][le_chat]["nb"]):
                            print("test")
                            print(i)
                            print(liste_messages_prive[le_pseudo][le_chat])
                            print("att c là")
                            nc_client.recv(4) #ici le client envoie "recu"
                            nc_client.sendall(b"Msp") #les mp sont forcément des messages
                            nc_client.recv(4) #ici le client envoie "recu"
                            print(liste_messages_prive[le_pseudo][le_chat][i][0],liste_messages_prive[le_pseudo][le_chat][i][1],liste_messages_prive[le_pseudo][le_chat][i][2])
                            nc_client.sendall(bytes(str(liste_messages_prive[le_pseudo][le_chat][i][0]), encoding="utf-8")) #pseudo
                            nc_client.recv(4) #ici le client envoie "recu"
                            nc_client.sendall(bytes(str(liste_messages_prive[le_pseudo][le_chat][i][1]), encoding="utf-8")) #chat
                            nc_client.recv(4) #ici le client envoie "recu"
                            nc_client.sendall(bytes(str(liste_messages_prive[le_pseudo][le_chat][i][2]), encoding="utf-8")) #heure
                                
                ### le client quitte la messagerie ###
                elif type_connexion == "quitter":
                    nc_client.send(b"recu")
                    pseudo = nc_client.recv(32).decode("utf-8")
                    print(f"{pseudo} a quitté le chat !")
                    liste_messages[compteur_messages] = (("Bye",f"{pseudo} a quitté le chat !"))
                    nc_client.send(bytes(str(liste_messages[compteur_messages]), encoding="utf-8"))  # Répond au client
                    compteur_messages += 1

                    
                
            except Exception as e:
                print(f"Erreur de communication : {e}")
                
            
            finally:
                nc_client.close()  # Ferme la connexion avec le client



# Lance l'interface graphique pour obtenir le port
GUI_Serveur()

# Configuration du serveur après avoir obtenu le port
mon_ip = socket.gethostbyname(socket.gethostname())
Adresse = (mon_ip, PORT)

# Instancie et lance le serveur
if PORT != None:
    lancer(Adresse)
