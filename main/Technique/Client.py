######################################################
# Copyright © 2025 - Vincent Marie et Tiki Bouglon #
######################################################

#Ce fichier fait partie de "Projet Messagerie LAN" et est distribué sous la licence MIT.
#Consultez le fichier LICENSE pour plus de détails.

import socket #les sockets (prises en français) permettent à deux machines de communiquer entre elles
import datetime as dt
#on ouvre une instance de socket de manière à ce qu'elle ferme dans tous les cas
#si on utilisait juste "socket.close()" à la fin du programme l'instruction...
#pourrait ne pas se lancer si une erreur ou un renvoi a lieu dans le programme


class se_co:
    def __init__(self,IP,Port,Pseudo):
        assert isinstance(IP,str)
        assert isinstance(Port,int)
        assert isinstance(Pseudo,bytes)
        self.id_dernier_message = {"general" : 0}
        
        ### stockage des informations ###
        self.adresse = (IP,Port)
        self.pseudo = Pseudo
        
    def nouvelle_connexion(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_cl:
            ### connexion au serveur ###
            try:
                sock_cl.settimeout(5)
                sock_cl.connect(self.adresse) #l'adresse IP est celle d'une des machines de la salle 223
                sock_cl.settimeout(None)
            except:
                self.connecte = False
                sock_cl.settimeout(None)
            else:
                sock_cl.sendall(b"premier") #informe le serveur que nous venons de nous co
                sock_cl.sendall(self.pseudo) #envoi du pseudo (le serveur attend un message du client à ce moment précis)
                
                sock_cl.settimeout(1)
                try :
                    sock_cl.recv(1024).decode() #attente d'un message du serveur, qui sera imprimé
                except socket.timeout:
                    self.connecte = False
                except :
                    self.connecte = False
                    print("autre erreur")
                else:
                    self.connecte = True
                finally:
                    sock_cl.settimeout(None)
                

    def resetIdMsg(self,quel_chat):
        ### reset de "id_dernier_message" pr toutes les vals sauf "general" ###
        for pseudo_chat in self.id_dernier_message.keys():
            if pseudo_chat != quel_chat:
                self.id_dernier_message[pseudo_chat] = 0
            
    def estCo(self):
        return self.connecte
    
    
    def ecouter(self, chat):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ecoute:
            ### connexion au serveur ###
            ecoute.connect(self.adresse) #l'adresse IP est celle d'une des machines de la salle 223
            ecoute.sendall(b"ecouter") #informe le serveur que nous venons de nous co
            
            ### envoi du type de chat ###
            ecoute.sendall(bytes(str(chat),encoding = "utf-8"))
            ecoute.recv(4) #ici le serveur renvoie "recu"
            if chat != "general":
                ecoute.sendall(self.pseudo)
                ecoute.recv(4) #ici le serveur renvoie "recu"
                
            if chat not in self.id_dernier_message.keys():
                self.id_dernier_message[chat] = 0
            ecoute.sendall(bytes(str(self.id_dernier_message[chat]), encoding = "utf-8"))
            
            ecoute.settimeout(1)
            try :
                nombre_messages = int(ecoute.recv(2).decode()) #nb messages à récup
                messages = []
            except socket.timeout:
                self.connecte = False
            except :
                self.connecte = False
                print("autre erreur")
            else:
                for message in range(nombre_messages):
                    ecoute.sendall(b"recu")
                    info_msg = [ecoute.recv(1024).decode()]
                    ecoute.sendall(b"recu")
                    info_msg.append(ecoute.recv(1024).decode())
                    if info_msg[0] in ["Msg","Msp"]:
                        ecoute.sendall(b"recu")
                        info_msg.append(ecoute.recv(1024).decode()) #message
                        ecoute.sendall(b"recu")
                        info_msg.append(ecoute.recv(1024).decode()) #heure
                    messages.append(info_msg)
                    self.id_dernier_message[chat] += 1
                self.connecte = True
            finally:
                ecoute.settimeout(None)
            return messages

                
    
    def envoyer_message(self,message, chat):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as envoyer:
            ### connexion au serveur ###
            envoyer.connect(self.adresse) #l'adresse IP est celle d'une des machines de la salle 223
            envoyer.sendall(b"message") #informe le serveur que nous venons de nous co
            envoyer.settimeout(1)
            try :
                envoyer.sendall(self.pseudo)
                envoyer.recv(4) #Le serveur devrait envoyer "recu" ici
                envoyer.sendall(bytes(message, encoding = "utf-8"))
                envoyer.recv(4) #Le serveur devrait envoyer "recu" ici
                current_time = dt.datetime.now().strftime("%H:%M") #heure d'envoi
                envoyer.sendall(bytes(current_time, encoding = "utf-8"))
                
            except socket.timeout:
                print("erreur de connexion trop longue")
            except :
                print("autre erreur")
            else:
                envoyer.recv(4) #Le serveur devrait envoyer "recu" ici
                envoyer.sendall(bytes(chat, encoding = "utf-8"))
                self.connecte = True
            finally:
                envoyer.settimeout(None)
    
    def quitter(self):
        self.connecte = False
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as quitter:
            ### quitter ###
            quitter.connect(self.adresse) #l'adresse IP est celle d'une des machines de la salle 223
            quitter.sendall(b"quitter") #informe le serveur que nous venons de nous co
            quitter.settimeout(1)
            quitter.recv(4)
            quitter.sendall(self.pseudo)
            quitter.settimeout(None)
        