# -*- coding: utf-8 -*-
import socket, os, signal ,sys, select, time
from socerr import socerr

HOST = 'localhost'
PORTclient = 2001
PORTserveur = 2000

msgClient=""
clients={}

mySocket = socerr(socket.AF_INET, socket.SOCK_DGRAM,0)

CON=True
MSG=True
mySocket.settimeout(1)

"""
#######################################################################################################################
#Fonctions
#######################################################################################################################
"""


def sendMessage(client,flag,data=""):
    """
    Construit la trame, l'envoi, attend l'acquittement du serveur et renvoi un acquittement

    Input:  client source du message
            flag correspondant au message (message, liste, ...)
            data ajoutée en fin de trame (facultatif)
    Output: None
    """

    compt=0 #Compteur d'essai
    while compt!=20:
        """
        Construction de la trame
        """
        if data!="":
            mySocket.sendto(flag+"@1@"+data+"@$",client)

        else:
            mySocket.sendto(flag+"@1@$",client)

        #print("envoie du message, essai numero "+str(compt)+"au client "+str(client))
        compt += 1
        #print('je suis dans le while acqt')

        """
        Attente de l'acquittement
        """
        if readSocket!=[]:
            """
            Acquittement du serveur reçu
            """
            #print('readsocket pas vide')
            #print(readSocket)
            try:
                (msgServer, adress) = mySocket.recvfrom(1024)
                if msgServer.split('@')[0] == flag and msgServer.split('@')[1] == "2":
                    """
                    Si le message reçu est bien un acquittement, on renvoi un acquittement
                    """
                    mySocket.sendto(flag+"@2@"+name+"@$",client)
                    return 1
                else:
                    x = 0
                    #print(msgServer.split('@'))
            except:
                x = 0
                #☺print('erreur interne, rien recu ')

        time.sleep(1)

    if compt == 20:
        """
        Nombre maximum d'essai dépassé, on arrête d'essayer
        """
        #print('erreur de communication 1 : Server does not respond')
        return 0





def recvMessage(message, client):
    """
    Quand un message est reçu, permet d'envoyer un acquittement au serveur et d'attendre le second de sa part

    Input:  Message reçu par le Socket
            Client ayant reçu le message
    output: None
    """

    compt=0
    while compt != 20:
        """
        Tant que le nombre de test n'a pas été atteint, on envoi l'acquittement au serveur
        """
        mySocket.sendto(message.split('@')[0]+"@2@"+name+"@$",client)
        #print("envoi de l'acquittement, essai numero "+str(compt)+"au client "+str(client))
        compt += 1

        if readSocket != []:
            """
            Si il y a un message dans le Socket, et que ce message est un acquittement, alors le double acquittement
            a été reçu, on peut sortir de la fonction
            """
            #print(readSocket)
            try:
                (msgServer,address) = mySocket.recvfrom(1024)

                if msgServer.split('@')[1] == '2':

                    #print('on a recu le double acquitement c est OK')
                    return 0

                else:
                    x = 0
                    #print("erreur de communication 2 : Unexpected message")
            except:
                x = 0
                #print('erreur interne, rien recu')
        time.sleep(1)

    if compt == 20:
        """
        Nombre d'essai limite atteint
        """
        #print("erreur de communication 3 : le client n'a pas renvoye de double acquittement, le message est peu etre perdu'")
        return 1





def connexion (username):
    """
    Permet la connexion d'un nouvel utilisateur

    Input:  Username rentré par l'utilisateur
    Output: None
    """

    msgServeur = ""

    """
    Construction de la trame de connexion
    """
    msgClient = "1@1@"+username+"@$"
    """
    Envoi de la trame de connexion
    """
    mySocket.sendto(msgClient, ((HOST,PORTserveur)))


    for i in range (0,20):


        desc = [mySocket]
        read, writable, exceptional =	 select.select(desc, [], [],0.05)

        if read == []:
            """
            Si on ne reçoit rien (ie: pas d'acquittement), on renvoit le message construit précédemment
            """
            mySocket.sendto(msgClient, ((HOST,PORTserveur)))

        else:
            """
            Si on reçoit quelque chose du serveur, on vérifie que c'est bien un acquittement
            """
            msgServeur = mySocket.recv(1024)
            if msgServeur.split('@')[0] == "1" and msgServeur.split('@')[1] == "2":
                """
                On a bien reçu un acquittement du serveur -> on envoit le deuxième acquittement
                """
                #print("connecté")
                mySocket.sendto("1@2@$",((HOST,PORTserveur)))
                return 0
                break
            else:
                """
                Dans le cas où l'username est déjà utilisé, on affiche le msgServeur (Tapez un username)
                """
                print(msgServeur.split('@')[2])
                return 1
                break

"""                
#######################################################################
# A e s t h e t i c A r t
#######################################################################
"""

global name
global savedMess
global readable
global liste
liste = False
global clientsCo
clientsCo=[]




print(chr(27) + "[2J")
"""
    print("  \033[1;36;47m                                                                                        \033[0m")
    print("  \033[1;36;47m                                                                                        \033[0m")
    print("  \033[1;36;47m     ---------------------..                    ``          ----------------------`     \033[0m")
    print("  \033[1;36;47m     +oooooooooooooooooo+-`/+-                `-+-        -+oooooooooooooooooooo/`      \033[0m")
    print("  \033[1;36;47m     +oooooooooooooooo+-`  /oo+-            `-+oo-      -+oooooooooooooooooooo/`        \033[0m")
    print("  \033[1;36;47m     +oooooooooooooo+-`    /oooo+-        `-+oooo-   `-+oooooooooooooooooooo/`          \033[0m")
    print("  \033[1;36;47m     +oooooooooooo+-`      /oooooo+-    `-+oooooo-  -+oooooooooooooooooooo/.            \033[0m")
    print("  \033[1;36;47m     +oooooooooo+-`        /oooooooo+.`-+oooooooo:-+oooooooooooooooooooo/.              \033[0m")
    print("  \033[1;36;47m     +oooooooo+-`          /oooooooooo+oooooooooo-``````````:ooooooooo/.                \033[0m")
    print("  \033[1;36;47m     +oooooo+-`            /ooooooooooooooooooooo-          -ooooooo/                   \033[0m")
    print("  \033[1;36;47m     +oooo+-`              /ooooooooooooooooooooo-          -ooooo/.                    \033[0m")
    print("  \033[1;36;47m     +oo+-`                /ooooooooooooooooooooo-          -ooo/.                      \033[0m")
    print("  \033[1;36;47m     ++-`                  /ooooooooooooooooooooo-          -o/                         \033[0m")
    print("  \033[1;36;47m     -`                    -/////////////////////.          ..                          \033[0m")
    print("  \033[1;36;47m                                                                                        \033[0m")
    print("  \033[1;36;47m                                                                                        \033[0m")              
    print("  \033[1;30;47m      ___ __  __ _____     _   _  _____ _   _  _ _____ ___ ___  _   _ ___               \033[0m")
    print("  \033[1;36;47m     \033[1;30;47m|_ _|  \/  |_   _|   /_\ | ||_   _/_\ | \| |_   _|_ _/ _ \| | | | __|              \033[0m")
    print("  \033[1;36;47m      \033[1;30;47m| || |\/| | | |    / _ \| |__| |/ _ \| .` | | |  | | (_) | |_| | _|               \033[0m")
    print("  \033[1;36;47m     \033[1;30;47m|___|_|  |_| |_|   /_/ \_\____|_/_/ \_\_|\_| |_| |___\__\ \\____/|___|              \033[0m")
    print("  \033[1;36;47m                                                                                        \033[0m")
    print("  \033[1;36;47m                                                                                        \033[0m")
"""




print("")
print("")
print("")
print("          \033[35m    ____    _____   _  __          _____   ____    ___  \033[0m")
print("          \033[31m   / __ \  / ___/  | |/ /         |__  /  / __ \  |__ \ \033[0m")
print("          \033[33m  / /_/ /  \__ \   |   /           /_ <  / / / /  __/ / \033[0m")
print("          \033[36m / _, _/  ___/ /  /   |          ___/ / / /_/ /  / __/  \033[0m")
print("          \033[32m/_/ |_|  /____/  /_/|_|         /____/  \____/  /____/  \033[0m")
print("                                       ")
print("")
print("")
print("")

#####################################################################################################
# Connexion d'un client
#####################################################################################################

while CON :
    test1=True
    savedMess = ""
    while test1:
        print("\033[31mMerci de ne pas utiliser @ ou $ dans votre username\033[0m")
        name = raw_input("\033[37mUsername : \033[0m")
        test1=False
        for k in range(len(name)):
            if name[k]=='$' or name[k]=='@':
                test1=True
                break


    x = connexion(name)

    if x == 0:
        CON = False

############################################################################################################
# MENU INFO
############################################################################################################
print("\033[32mVous etes connecté dans le salon public, chattez \033[0m")
print("\033[37m   _______________________________________________________________\033[0m")
print("\033[37m  |                                                               |\033[0m")
print("\033[37m  |   \033[33mPour demander une liste:                   /l               \033[37m|\033[0m")
print("\033[37m  |   \033[36mVous pourez ensuite demander un chat prive                  \033[37m|\033[0m")
print("\033[37m  |   \033[37mDecentralise ou non                                         \033[37m|\033[0m")
print("\033[37m  |   \033[32mPour afficher les commandes disponibles    /h               \033[37m|\033[0m")
print("\033[37m  |   \033[31mPour vous déconnecter:                     /q               \033[37m|\033[0m")
print("\033[37m  |_______________________________________________________________|\033[0m")
print("")
print("")
print("")

desc1 = [mySocket,sys.stdin]
centralized = True

while True:


    """
    MODE CENTRALISE
    """

    while centralized:

        readSocket, writable, exceptional =	 select.select(desc1, [], [])

        for x in readSocket:

            if x == mySocket:
                """
                Lecture du message contenu dans le socket
                """
                #print('x appartient au socket')
                msgServer= mySocket.recv(1024)

                if msgServer.split('@')[1] == '2':
                    mySocket.sendto(msgServer.split('@')[0]+"@2@"+name+"@$",(HOST,PORTserveur))
                    break

                recvMessage(msgServer,(HOST,PORTserveur))

                if  msgServer == savedMess :
                    x = 0
                    #print("\033[31mSûrement un doublon, pas de SPAM\033[0m")





                """
                MESSAGE
                """
                if msgServer.split('@')[0]=='2' and msgServer.split('@')[1]=='1':

                    if msgServer.split('@')[2]== name:

                        #print(">>> ["+name+"] :"+msgServer.split('@')[3])
                        print("\033[1;37m>>> ["+name+"] : \033[0;37m"+msgServer.split('@')[3]+"\033[0m")
                        savedMess=msgServer

                    if msgServer.split('@')[2]!= name:

                        #print("<<< ["+msgServer.split('@')[2]+"] :"+msgServer.split('@')[3])
                        print("\033[1;35m<<< ["+msgServer.split('@')[2]+"] : \033[0;35m"+msgServer.split('@')[3]+"\033[0m")
                        savedMess=msgServer







                """
                DEMANDE DE LISTE
                """
                if msgServer.split('@')[0]=='3' and msgServer.split('@')[1]=='1':

                        print("\033[33m##### Liste des utilisateurs #####\033[0m")
                        print("")

                        for k in range(int(msgServer.split('@')[2])):
                            print("\033[33m"+msgServer.split('@')[k+3]+"\033[0m")
                            clientsCo.append(msgServer.split('@')[k+3])
                        liste=True
                        print("")
                        print("\033[33m ##### Fin de la liste ############\033[0m")





                """
                INVITATION A UNE MESSAGERIE PRIVEE
                """

                if msgServer.split('@')[0]=='4' and msgServer.split('@')[1]=='1':
                    print("\033[36m ######### Invitation a une messagerie privée ########\033[0m")
                    print("\033[37m"+msgServer.split('@')[2]+" vous a invité à une messagerie privee\033[0m")
                    print('\033[37m Entrer \033[1;32m oui \033[37m pour accepter, \033[1;31m non \033[37m pour refuser\033[0m')
                    accept = raw_input()
                    if accept == 'oui':
                        sendMessage((HOST,PORTserveur),'5',name+'@'+msgServer.split('@')[2]+'@1')
                        print('\033[36m ######## Vous etes dans le chat privéé '+msgServer.split('@')[3]+' ########\033[0m')
                    elif accept == 'non':
                        sendMessage((HOST,PORTserveur),'5',name+'@'+msgServer.split('@')[2]+'@0')
                        print("\033[36m Vous avez refusé l'invitation de "+msgServer.split('@')[2]+"\033[0m")

                    else:
                        print('\033[37m Entrez seulement \033[1;32m oui \033[37m ou \033[1;31m non \033[37m svp. Réessayez\033[0m')





                """
                REPONSE A UNE INVITATION
                """
                if msgServer.split('@')[0]=='5' and msgServer.split('@')[1]=='1':
                    if msgServer.split('@')[3]=='1':
                        print("\033[1;33m"+msgServer.split('@')[2]+" a rejoins votre chat privé\033[0m")

                    if msgServer.split('@')[3]=='0':
                       print("\033[1;33m"+msgServer.split('@')[2]+" a refusé votre invitation au chat privé\033[0m")






                """
                NOTIFICATION DE REPONSE A UN CHAT DECENTRALISE
                """
                if msgServer.split('@')[0]=='6' and msgServer.split('@')[1]=='1':

                    if msgServer.split('@')[3]=='1':
                        print("\033[1;33m"+msgServer.split('@')[2]+" a rejoins votre chat décentralisé\033[0m")



                    if msgServer.split('@')[3]=='0':
                        print("\033[1;33m"+msgServer.split('@')[2]+" a refusé votre invitation au chat décentralisé\033[0m")






                """
                DECENTRALISE DEMANDE DE LISTE AVEC ADRESSES
                """
                if msgServer.split('@')[0]=='7':

                    #print("Reception de la liste des utilisateurs et des IP")
                    #print(msgServer)
                    for k in range(int(msgServer.split('@')[5])):
                        #print(msgServer.split('@')[3*k+6])
                        clients[msgServer.split('@')[3*k+6]]=(msgServer.split('@')[3*k+7],int(msgServer.split('@')[3*k+8]))
                    clients[msgServer.split('@')[2]]=(msgServer.split('@')[3],int(msgServer.split('@')[4]))
                    #print("Fin de la liste, les clients on ete enregistres dans le dictionnaire clients")

                    print("\033[37mVous etes dans le groupe de Chat décentralisé "+"\033[1;37m"+GroupName+"\033[37m"+"\033[0m")
                    print("\033[37mTapez \033[32m/p\033[37m pour retourner au salon public\033[0m")





                """
                INVITATION A UN CHAT DECENTRALISE
                """
                if msgServer.split('@')[0]=='8':

                    print("\033[33m######### Invitation à une messagerie décentralisée  ########\033[0m")
                    print(msgServer.split('@')[2]+" vous a invité à une messagerie décentralisée")
                    print('\033[1;33mEntrer \033[1;32m oui \033[33m pour accepter, \033[1;31m non \033[33m pour refuser\033[0m')
                    accept = raw_input()
                    if accept == 'oui':
                        sendMessage((HOST,PORTserveur),'8',name+'@'+msgServer.split('@')[2]+'@1')
                        print('\033[33m######## Vous etes dans le chat prive '+msgServer.split('@')[3]+' ########\033[0m')

                    elif accept == 'non':
                        sendMessage((HOST,PORTserveur),'8',name+'@'+msgServer.split('@')[2]+'@0')
                        print("\033[33mVous avez refuse l'invitation de "+msgServer.split('@')[2]+'\033[0m')

                    else:
                        print('\033[33m Entrez seulement \033[1;32m oui \033[33m ou \033[1;31m non \033[33m svp. Réessayez\033[0m')





                """
                REPONSE A L'INVITATION DECENTRALISE
                """
                if msgServer.split('@')[0]=='9':
                    #print(msgServer)
                    try:
                        if msgServer.split('@')[8]=='1':
                            print("\033[33m"+msgServer.split('@')[5]+" a rejoins votre chat décentralisé\033[0m")
                            print('\033[32mVous passez en mode décentralisée\033[0m')
                            centralized=False


                    except:
                        x = 0
                        print("\033[31m"+msgServer.split('@')[2]+" a refusé votre invitation au chat décentralisé\033[0m")















            else:
                """
                UTILISATEUR RENTRE UN MESSAGE
                TRAITEMENT DES MENUS
                """
                #print('x appartient a input')
                msg = raw_input()
                print ("\033[A                                \033[A") #Permet d'effacer la ligne du raw input




                if msg == "/l":
                    """
                    liste
                    """
                    sendMessage((HOST,PORTserveur),"3",name)
                elif msg == "/q":
                    """
                    déconnexion
                    """
                    exit = sendMessage((HOST,PORTserveur),"0",name)

                    if exit == 1:
                        print("\033[31mT'es déconnecté, Bye Bye\033[0m")
                        sys.exit()

                elif msg == "/i":
                    """
                    invitation privée
                    """
                    if liste == False :
                        print("\033[31mVeuillez demander la liste des clients connectes avant svp\033[0m")
                    else:
                        print('\033[36m###### Demande de chat privé ######\033[0m')
                        print('')
                        print('\033[37mQui voulez-vous inviter? Séparer les noms par une virgule svp\033[0m')
                        print('')
                        people = raw_input()
                        print("\033[A                                         \033[A")
                        people = people.split(',')
                        test=1
                        for k in people:
                            if k not in clientsCo:
                                test=0
                        if test==1:
                            numb = len(people)
                            people = '@'.join(people)
                            print(people)
                            print('\033[37mQuel est le nom de votre groupe? 6 caractères max svp\033[0m')
                            GroupName = raw_input()
                            sendMessage((HOST,PORTserveur),"4",name+"@"+GroupName+"@"+str(numb)+"@"+people)
                            print('\033[37mVous etes dans le groupe de Chat '+GroupName+', Mais vous etes seul pour le moment, tapez /p pour retourner dans le chat public\033[0m')
                        else:
                            print("\033[31mN'entrez que des noms de clients valable, si besoin, redemandez une liste avec la commande /l \033[0m")




                elif msg == "/d":
                    """
                    décentralisé
                    """
                    if liste == False :
                        print("\033[31mVeuillez demander la liste des clients connectes avant svp\033[0m")
                    else:
                        print('\033[33m####### Demande de messagerie decentralisee ######\033[0m')
                        print('')
                        print('')
                        print('\033[33mQui voulez vous inviter ? Séparez les noms par une virgule\033[0m')
                        people = raw_input()
                        print("\033[A                        \033[A")
                        people = people.split(',')
                        test=1
                        for k in people:
                            if k not in clientsCo:
                                test=0
                        if test==1:
                            numb = len(people)
                            people = '@'.join(people)
                            print(people)
                            print('\033[33mQuel est le nom de votre groupe? 6 caractères max svp\033[0m')

                            GroupName = raw_input()

                            sendMessage((HOST,PORTserveur),"6",name+"@"+GroupName+"@"+str(numb)+"@"+people)
                        else:
                            print("\033[31mN'entrez que des noms de clients valable, si besoin, redemandez une liste avec la commande /l \033[0m")
                    #print('message de demande envoye, attendez la liste des IP')




                elif msg == "/p":
                    """
                    retour au public
                    """
                    sendMessage((HOST,PORTserveur),'11',name)
                    print('Vous etes dans la messagerie publique')

                elif msg == "/h":
                    '''on affiche les commandes dispo'''
                    if liste :
                        print("\033[37m   _______________________________________________________________\033[0m")
                        print("\033[37m  |                                                               |\033[0m")
                        print("\033[37m  |   \033[33mPour demander une liste:                   /l               \033[37m|\033[0m")
                        print("\033[37m  |   \033[36mPour demander une messagerie privee        /p               \033[37m|\033[0m")
                        print("\033[37m  |   \033[37mPour demander une messagerie decentralisee /d               \033[37m|\033[0m")
                        print("\033[37m  |   \033[32mPour afficher les commandes disponibles    /h               \033[37m|\033[0m")
                        print("\033[37m  |   \033[31mPour vous déconnecter:                     /q               \033[37m|\033[0m")
                        print("\033[37m  |_______________________________________________________________|\033[0m")
                        print("")
                        print("")
                    else:
                        print("\033[37m   _______________________________________________________________\033[0m")
                        print("\033[37m  |                                                               |\033[0m")
                        print("\033[37m  |   \033[33mPour demander une liste:                   /l               \033[37m|\033[0m")
                        print("\033[37m  |   \033[37mVous pourez ensuite demander un chat prive                  \033[37m|\033[0m")
                        print("\033[37m  |   \033[37mDécentralise ou non                                         \033[37m|\033[0m")
                        print("\033[37m  |   \033[32mPour afficher les commandes disponibles    /h               \033[37m|\033[0m")
                        print("\033[37m  |   \033[31mPour vous déconnecter:                     /q               \033[37m|\033[0m")
                        print("\033[37m  |_______________________________________________________________|\033[0m")
                        print("")
                        print("")

                else:
                    """
                    Message classique
                    """
                    #print("je suis dans le else")
                    sendMessage((HOST,PORTserveur),"2",name+"@"+str(msg))

    """
    Affichage du message
    """
    #•print(msgServer)
    if msgServer.split('@')[2]!=name:
        print('\033[1;31mPatientez 10 secondes SVP\033[0m')
        time.sleep(5)
        sendMessage((msgServer.split('@')[3],int(msgServer.split('@')[4])),'7',name)
        print("\033[1;31mVeuillez attendre la confirmation de réception de la liste SVP\033[0m")

    msgServer=""







    """
    MODE DENCENTRALISE
    """
    while centralized!=True:

        #print("\033[32mVous etes en mode décentralisé, vous envoyez des messages sans passer par le serveur\033[0m")
        readSocket, writable, exceptional =	 select.select(desc1, [], [])

        for x in readSocket:

            if x == mySocket:
                #print('x appartient au socket')
                msgServer = mySocket.recv(1024)
                #print(msgServer)
                try:
                    if msgServer.split('@')[1]=='2':
                        mySocket.sendto(msgServer.split('@')[0]+"@2@"+name+"@$",clients[msgServer.split('@')[2]])
                        break
                except:
                    break

                if  msgServer == savedMess :
                    recvMessage(msgServer,clients[msgServer.split('@')[2]])
                    print('surement un doublon')



                """
                MESSAGE
                """
                if msgServer.split('@')[0]=='2' and msgServer.split('@')[1]=='1':
                    recvMessage(msgServer,clients[msgServer.split('@')[2]])
                    if msgServer.split('@')[2] == name:

                        #print(">>> ["+name+"] :"+msgServer.split('@')[3])
                        print("\033[1;37m>>> \033[1;32mDCTLZ \033[1;37m["+name+"] : \033[0;37m"+msgServer.split('@')[3]+"\033[0m")
                        savedMess = msgServer

                    if msgServer.split('@')[2]!= name:

                        #print("<<< ["+msgServer.split('@')[2]+"] :"+msgServer.split('@')[3])
                        print("\033[1;35m<<< \033[1;32mDCTLZ \033[1;35m["+msgServer.split('@')[2]+"] : \033[0;35m"+msgServer.split('@')[3]+"\033[0m")
                        savedMess=msgServer





                """
                NOTIFICATION DE LA REPONSE A L'INVITATION
                """
                if msgServer.split('@')[0]=='9':
                    recvMessage(msgServer,clients[msgServer.split('@')[2]])
                    if msgServer.split('@')[3]=='1':
                        print("\033[32m"+msgServer.split('@')[2]+" a rejoins votre chat décentralisé\033[0m")

                    if msgServer.split('@')[3]=='0':
                        print("\033[31m"+msgServer.split('@')[2]+" a refuser votre invitation au chat decentralise\033[0m")




                """
                
                """
                if msgServer.split('@')[0]=='7':
                    recvMessage(msgServer,clients[msgServer.split('@')[2]])
                    #print('Un client demande la liste des IP')
                    data=name+"@"+clients[name][0]+"@"+str(clients[name][1])+"@"+str(len(clients))
                    for k in clients:

                        data=data+'@'+k+'@'+str(clients[k][0])+'@'+str(clients[k][1])
                    #print(data)
                    sendMessage(clients[msgServer.split('@')[2]],'10',data)




                """
                
                """
                if msgServer.split('@')[0]=='10':
                    recvMessage(msgServer,(msgServer.split('@')[3],int(msgServer.split('@')[4])))
                    #print(msgClient)
                    #print('liste des clients recus')
                    for k in range(int(msgServer.split('@')[5])):
                        #print(msgServer.split('@')[3*k+6])
                        clients[msgServer.split('@')[3*k+6]]=(msgServer.split('@')[3*k+7],int(msgServer.split('@')[3*k+8]))
                        #print("Fin de la liste, les clients on ete enregistres dans le dictionnaire clients")
                    print("\033[37mListe des clients recus, les clients on ete enregistres dans le dictionnaire clients\033[1;0m")
                    print("\033[37mVous pouvez commencer a ecrire dans votre chat decentralise. La \033[1;31mC\033[1;32mI\033[1;36mA\033[37m ne peut pas intercepter vos message ;)\033[0m")







            else:
                """
                UTILISATEUR RENTRE UN MESSAGE
                """
                #print('x appartient a input')
                msg = raw_input()
                print("\033[A                                 \033[A")
                if msg == '/p':
                    sendMessage((HOST,PORTserveur),'11',name)
                    print('\033[32mVous ete dans la messagerie publique\033[32m')
                    print("\033[37m   _______________________________________________________________\033[0m")
                    print("\033[37m  |                                                               |\033[0m")
                    print("\033[37m  |   \033[33mPour demander une liste:                   /l               \033[37m|\033[0m")
                    print("\033[37m  |   \033[33mVous pourez ensuite demander un chat prive                  \033[37m|\033[0m")
                    print("\033[37m  |   \033[33mDecentralise ou non                                         \033[37m|\033[0m")
                    print("\033[37m  |   \033[32mPour afficher les commandes disponibles    /h               \033[37m|\033[0m")
                    print("\033[37m  |   \033[31mPour vous déconnecter:                     /q               \033[37m|\033[0m")
                    print("\033[37m  |_______________________________________________________________|\033[0m")
                    print("")
                    print("")
                    centralized=True
                    liste= False
                    break
                elif msg == '/h':
                    print("\033[37m   _______________________________________________________________\033[0m")
                    print("\033[37m  |                                                               |\033[0m")
                    print("\033[37m  |   \033[33mVous etes dans la messagerie decentralisee                  \033[37m|\033[0m")
                    print("\033[37m  |   \033[33mvos messages ne passent plus par le serveur                 \033[37m|\033[0m")
                    print("\033[37m  |   \033[32mPour afficher les commandes disponibles    /h               \033[37m|\033[0m")
                    print("\033[37m  |   \033[31mPour revenir a la messagerie publique      /p               \033[37m|\033[0m")
                    print("\033[37m  |_______________________________________________________________|\033[0m")
                    print("")
                    print("")
                else:
                    #print("je suis dans le else")
                    for k in clients:
                        if k == name:
                            print("\033[1;37m>>> \033[1;32mDCTLZ \033[1;37m["+name+"] : \033[0;37m"+msg+"\033[0m")
                        else:
                            sendMessage(clients[k],"2",name+"@"+str(msg))
                    #print('message envoye')
