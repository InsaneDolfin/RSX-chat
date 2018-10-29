# -*- coding: utf-8 -*-

import socket

import select, time
from socerr import socerr
PORT=2000
clients={}
salon={}
mySocket=socerr(socket.AF_INET,socket.SOCK_DGRAM,0)
mySocket.bind(("localhost",PORT))
inputs=[mySocket]
mySocket.settimeout(1)
global lastname


print(chr(27) + "[2J")
print("")
print("")
print("")
print("          \033[35m   _____                                   \033[0m")
print("          \033[31m  / ___/  ___    _____ _   __  ___    _____\033[0m")
print("          \033[33m  \__ \  / _ \  / ___/| | / / / _ \  / ___/\033[0m")
print("          \033[36m ___/ / /  __/ / /    | |/ / /  __/ / /    \033[0m")
print("          \033[32m/____/  \___/ /_/     |___/  \___/ /_/     \033[0m")
print("                                       ")
print("")
print("")
print("")    


################################################################
#Fonctions
################################################################

def connexion(message,address):
    """
    Permet d'accepter ou de refuser la connexion d'un nouveau client
    
    Input:  message reçu par le serveur
            address du client ayant envoyé le message
    Output: None
    """
    

    if message[2] in clients:
        """
        Si l'username saisi est déjà dans la liste des clients connecté, renvoyer une erreur
        """
        mySocket.sendto("1@3@username already in use@$",address)
    else:  
        """
        Si l'username peut être utilisé, on l'ajoute dans le dictionnaire de clients et on associe le client au salon Public.
        On envoit alors un acquittement
        """
        clients[message[2]]=address
        salon[message[2]]='public'
        mySocket.sendto("1@2@$",clients[message[2]])
        
        print("\033[1;37m##### Message de Connexion #####\033[0")        
        print("")
        print("\033[37mUne nouvelle connection a ete enregistrée, attente de validation . . .\033[0m")
        print("")        
        
        #2eme confirmation
        for i in range (0,20):
            """
            On test 20 fois si le deuxième acquittement n'a pas été reçu
            """
            desc = [mySocket]
            readable, writable, exceptional =	 select.select(desc, [], [],0.05)
        
            if readable == []:
                #On renvoit l'acquittement
                mySocket.sendto("1@2@$",clients[message[2]])
            else:
                #On regarde l'acquittement, si il est bon, on print connecté
                msgClient = mySocket.recv(1024)
                if msgClient.split('@')[0] == "1" and msgClient.split('@')[1] == "2":
                    print("\033[1;32mConnecté\033[0m")
                    print("")
                    break
                    
def sendMessage(client,flag,data=""):
    """
    Permet l'envoi d'un message, la vérification de l'acquittement, et l'envoi du deuxième acquittement
    
    Input:  client à qui envoyé le message
            flag de la trame a envoyer
            data (facultatif) a ajouter en pied de trame
    Output: None
    """
    
    
    compt=0
    print("\033[1;37m##### Envoi d'une trame #####\033[0m")
    print("")
    
    while compt!=20:
        
        if data!="":
            mySocket.sendto(flag+"@1@"+data+"@$",client)
            
        else:
            mySocket.sendto(flag+"@1@$",client)
        
        print("\033[37mEnvoie du message, essai numero "+str(compt)+" au client "+str(client)+"\033[0m")    
        compt += 1
        #print('je suis dans le while acqt')
        
        if readable!=[]:
            """
            l'acquittement a été reçu
            """
            try:
                (msgClient, adress) = mySocket.recvfrom(1024)
                if msgClient.split('@')[0] == flag and msgClient.split('@')[1] == "2":
                    #C'est bien un acquittement
                    print("")
                    print("\033[1;32mMessage Envoyé\033[0m")
                    mySocket.sendto(flag+"@2@$",client)
                    return 1
                else:
                    print("\033[31mErreur de communication 2: Unexpected message\033[0m")
                    print(msgClient.split('@'))
            except:
                    print("\033[31mErreur interne, rien reçu\033[0m")
        
        
    if compt==20:
        
        print("\033[31mErreur de communication 1: Server does'nt respond\033[0m")
        return 0
        
    
def recvMessage(message,client):
    """
    Permet de recevoir un message d'un client, d'envoyer un acquittement et d'attendre la réception du deuxième
    
    Input:  message reçu
            client qui a envoyé le message
    Output: None
    """
    
    
    print("\033[1;37m##### Réception d'une trame #####\033[0m")
    print("")
    compt=0
    while compt!=20:
        
        mySocket.sendto(message.split('@')[0]+"@2@"+message.split('@')[2]+"@$",client)
        print("\033[35mEnvoi de l'acquittement, essai numero "+str(compt)+" au client "+str(client)+"\033[1;0m")    
        compt += 1
     
        if readable!=[]:
            """
            l'acquittement a été envoyé, et le deuxième à potentiellement été reçu
            """
            try:
                (msgServer,address) = mySocket.recvfrom(1024)
        
                if msgServer.split('@')[1]=='2':
                
                    print("\033[32mDeuxième acquittement reçu\033[0m")
                    return 0
            
                else:
                
                    print("\033[31mErreur de communication 2: Unexpected message\033[0m")
            except:
                print('\033[31mErreur interne, Nothing received\033[0m')

        
    if compt==20:
        
        print("\033[31mErreur de communication 3: le client n'a pas renvoye de double acquittement\033[0m")
        return 1
    
####################################################################
#Code Serveur
#################################################################### 
global readable

while True:
    
    
    readable,w,x=select.select(inputs,[],[])
    for sock in readable:
        if sock not in inputs:
            inputs.append(sock)
        (message,address)=mySocket.recvfrom(1024)
        #print(message)
        
        
        
        
        if message.split('@')[0]== "1":
            
            print("\033[1;32m########## Demande de connexion ##########\033[0m")
            print("")
            connexion(message.split('@'),address)
            print(clients)
            print("")
            print("\033[1;32m########## Fin de la demande de connexion ##########\033[0m")
            print("")            
            break
        
        
        
        else:
            if message.split('@')[1]=='2':
                mySocket.sendto(message.split('@')[0]+"@2@$",clients[message.split('@')[2]])
                break
            if message.split('@')[0]=="2":
                print("\033[1;35m########## Réception d'un message Chat ##########\033[0m")
                print("")                
                acq=recvMessage(message,clients[message.split('@')[2]])
                for k in clients:
                    if salon[k]==salon[message.split('@')[2]]:
                        print("\033[35m########## Retranssmistion du message à l'utilisateur "+str(k)+" ##########\033[0m")
                        sendMessage(clients[k],'2',message.split('@')[2]+'@'+message.split('@')[3])
                print("")
                print("\033[1;35m########## Fin du traitement du message ##########\033[0m")
                print("")                
                break
            
            
            
            if message.split('@')[0]=="3":
                print("\033[1;33m########## Demande de liste ##########\033[0m")
                print("")
                acq=recvMessage(message,clients[message.split('@')[2]])
                data=str(len(clients))
                print("\033[33m########## Construction du message liste ##########\033[0m")
                print("")                
                for k in clients:
                    data=data+"@"+str(k)
                print(data)
                sendMessage(clients[message.split('@')[2]],"3",data)
                print("")
                print("\033[1;33m########## Fin du traitement de la Liste ##########\033[0m")
                print("")                
                break
            
            
            
            if message.split('@')[0]=='0':
                print("\033[1;31m########## Déconnexion ##########\033[0m")
                print("")
                acq=recvMessage(message,clients[message.split('@')[2]])
                clients.pop(message.split('@')[2])
                print("")
                print("\033[1;31m########## Fin du traitement de Déconnexion ##########\033[0m")
                print("")                
                break
            
            
            
            if message.split('@')[0]=='4':
                print("\033[1;36m########## Invitation à un salon privé ##########\033[0m")
                print("")
                acq=recvMessage(message,clients[message.split('@')[2]])
                salon[message.split('@')[2]]=message.split('@')[3]
                print("\033[1;36m########## Demande de la part de "+message.split('@')[2]+ "##########\033[0m")
                #print("\033[36m    Invités:\033[0m")                
                for k in range(int(message.split('@')[4])):
                    sendMessage(clients[message.split('@')[k+5]],"4",message.split('@')[2]+'@'+message.split('@')[3])
                    #print("\033[37m"+clients[message.split('@')[k+5]]+"\033[0m")
                print("")
                print("\033[1;36m########## Fin de l'invitation à un salon privé ##########\033[0m")
                print("")
                break
            
            
            
            
            if message.split('@')[0]=='5':
                print("\033[1;36m########## Réponse à un salon privé ##########\033[0m")
                print("")
                acq=recvMessage(message,clients[message.split('@')[2]])
                if message.split('@')[4]=='1':
                    salon[message.split('@')[2]]=salon[message.split('@')[3]]
                    print("\033[1;37Clients qui ont acceptés l'invitation\033[0m")
                    print("")
                    for k in clients:
                        if salon[k]==salon[message.split('@')[3]]:
                            sendMessage(clients[k],'5',message.split('@')[2]+'@1')
                            print("\033[37"+message.split('@')[2]+"\033[0m")
                            print("")
                else:
                    for k in clients:
                        if salon[k]==salon[message.split('@')[3]]:
                            sendMessage(clients[k],'5',message.split('@')[2]+'@0')
                break
            
            
            
            if message.split('@')[0]=='6':
                print("\033[1;32m########## Demande de messagerie décentralisée ###########\033[0m")
                print("")
                acq=recvMessage(message,clients[message.split('@')[2]])
                salon[message.split('@')[2]]=message.split('@')[3]
                data=message.split('@')[2]+'@'+clients[message.split('@')[2]][0]+'@'+str(clients[message.split('@')[2]][1])+'@'+message.split('@')[4]
                lastname=message.split('@')[2]
                print("\033[1;37mLes invités sont: \033[0m")
                for k in range(int(message.split('@')[4])):
                    
                    data=data+'@'+message.split('@')[k+5]+'@'+str(clients[message.split('@')[k+5]][0])+'@'+str(clients[message.split('@')[k+5]][1])
                
                    print("\033[32m"+message.split('@')[k+5]+"\033[0m")
                print("")
                sendMessage(clients[message.split('@')[2]],'7',data)
                
                for k in range(int(message.split('@')[4])):
                    sendMessage(clients[message.split('@')[k+5]],'8',message.split('@')[2]+'@'+message.split('@')[3])
                print("\033[1;32m########## Fin de la demande de messagerie décentralisée ###########\033[0m")                
                print("")
                break 
            
            
            
            
            if message.split('@')[0]=='8':
                acq=recvMessage(message,clients[message.split('@')[2]])
                if message.split('@')[4]=='1':
                    salon[message.split('@')[2]]=salon[message.split('@')[3]]
                    for k in clients:
                        if salon[k]==salon[message.split('@')[3]]:
                            sendMessage(clients[k],'9',lastname+'@'+clients[lastname][0]+'@'+str(clients[lastname][1])+'@'+message.split('@')[2]+'@'+clients[message.split('@')[2]][0]+'@'+str(clients[message.split('@')[2]][1])+'@1')
                     
                else:
                    for k in clients:
                        if salon[k]==salon[message.split('@')[3]]:
                                sendMessage(clients[k],'9',message.split('@')[2]+'@0')
                break
                
            
            
            if message.split('@')[0]=='11':
                print("\033[1;32m########## Retour en salon Public ###########\033[0m")
                print("")
                print("\033[32mProceeding . . .\033[0m")
                acq=recvMessage(message,clients[message.split('@')[2]])
                salon[message.split('@')[2]]='public'
                print("\033[1;32m########## Fin de retour en salon Public ###########\033[0m")
                print("")
                break
                
                    
                    
                
    
   