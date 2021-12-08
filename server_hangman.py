import socket
import random

#Pregatirea serverului

serverName = '127.0.0.1'
serverPort = 1515
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(2)
print("Serverul TCP asculta pe adresa ", serverSocket.getsockname())


# Pregatirea jocului

sesiuneHangman = False
joc_cuvTinta = ""
joc_incercari = 0
joc_litereGhicite = []
listaTinta = []
primaLitera = ''
ultimaLitera = ''

# Functia pentru alegerea unui cuvant din hangwords.txt

def AlegereCuvant():
  hangwords = open("hangwords.txt")
  linii = hangwords.readlines()
  cuvinte = []
  W = len(linii)
  for i in range(W):
      cuvinte.append(linii[i].strip('\n'))
      # Se scote \n (caracterul de newline) din fiecare cuvant
  K = random.randrange(1, W, 1) # Alegere la intamplare
  x1 = cuvinte[K-1]
  x2 = x1.upper() # Cuvantul este transformat in UPPERCASE automat
  return x2

# Functia pentru afisarea jocului

def statusJoc(litereGhicite, cuvant, incercari):
  secret = "_"*len(cuvant) 
  secretlista = list(secret)
  for lt in litereGhicite:
    for poz,lit in enumerate(cuvant):
      if(lit == lt):
          secretlista[poz] = lt
  hangw = "HANGMAN"
  hangwl = list(hangw)
  hangStatus=[]
  for x in range(incercari):
    hangStatus.append(hangwl[x])
  rasp = "[ " + ' '.join(secretlista) + " ] " + "[" + ''.join(hangStatus) + "]"
  return rasp

# Functia pentru verificarea daca jucatorul a castigat

def castigareJoc(litereGhicite, cuvant, incercari):
  secret = "-"*len(cuvant) 
  secretlista = list(secret)
  for lt in litereGhicite:
    for poz,lit in enumerate(cuvant):
      if(lit == lt):
          secretlista[poz] = lt
  secret2 = ''.join(secretlista)
  if '-' in secret2:
    return False
  else:
    return True

# Inceputul programului

while 1:
  connSocket, clientAddress = serverSocket.accept()
  print("Accesat de catre ", clientAddress)
  while 1:
    mesajNormal = connSocket.recv(1024)
    mesajPrimit = mesajNormal.decode()
    print("Serverul a primit: " + mesajPrimit)
    # Inceperea jocului
    if mesajPrimit == "START" and sesiuneHangman == False:
      sesiuneHangman = True
      joc_incercari = 0
      joc_litereGhicite = []
      joc_cuvTinta = AlegereCuvant()
      listaTinta = list(joc_cuvTinta)
      primaLitera = listaTinta[0]
      ultimaLitera = listaTinta[len(joc_cuvTinta)-1]
      joc_litereGhicite.append(primaLitera)
      joc_litereGhicite.append(ultimaLitera)

      connSocket.send(statusJoc(joc_litereGhicite, joc_cuvTinta, joc_incercari).encode())
      print("Jocul a inceput! Cuvantul tinta este " + joc_cuvTinta)
    # Daca mesajul este o litera iar jocul a inceput
    elif len(mesajPrimit) == 1 and sesiuneHangman == True:
      # Daca litera se afla in cuvant atunci se introduce in lista literelor ghicite. Este permisa repetarea literelor corecte.
      if mesajPrimit in joc_cuvTinta: 
        joc_litereGhicite.append(mesajPrimit)
        # Daca conditia de castig este indeplinita, jocul se incheie.
        if castigareJoc(joc_litereGhicite, joc_cuvTinta, joc_incercari) == True:
          connSocket.send((statusJoc(joc_litereGhicite, joc_cuvTinta, joc_incercari) + "\nFelicitari! Ai castigat!\nJocul s-a sfarsit! Poti incepe un nou joc cu 'START'.").encode())
          sesiuneHangman = False
          print("Jocul s-a sfarsit! Clientul a castigat!")
        else:
          connSocket.send(statusJoc(joc_litereGhicite, joc_cuvTinta, joc_incercari).encode())
      # Daca jucatorul greseste litera atunci pierde o incercare.
      elif joc_incercari<7:
        joc_incercari+=1
        # Jocul se sfarseste daca jucatorul a folosit toate incercarile
        if joc_incercari == 7:
          connSocket.send((statusJoc(joc_litereGhicite, joc_cuvTinta, joc_incercari) + "\nAi pierdut! Jocul s-a sfarsit!\nPoti incepe un nou joc cu 'START'.").encode())
          sesiuneHangman = False
          print("Jocul s-a sfarsit! Clientul a pierdut!")
        # Daca nu a folosit toate incercarile, jocul continua
        else:
          connSocket.send(statusJoc(joc_litereGhicite, joc_cuvTinta, joc_incercari).encode())
      else:
        connSocket.send((statusJoc(joc_litereGhicite, joc_cuvTinta, joc_incercari) + "\nAi pierdut! Jocul s-a sfarsit!\nPoti incepe un nou joc cu 'START'.").encode())
        sesiuneHangman = False
        print("Jocul s-a sfarsit! Clientul a pierdut!")
    # Daca mesajul nu este o litera sau "START"
    else:
      connSocket.send(("Mesaj necunoscut! Mai incearca!").encode())
  connSocket.close()