import socket

# Pregatirea serverului

serverName = '127.0.0.1'
serverPort = 1515

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))  
print("Puteti incepe jocul folosind 'START' sau 'start'.")
print("Mesajele sunt transformate in UPPERCASE automatic!\n")

while 1:

  modmessage = input("Trimite: ")
  message = modmessage.upper()
  if message == "EXIT":
    break
  clientSocket.sendto(message.encode(), (serverName, serverPort))
  mesajPrimit = clientSocket.recv(1024)
  print(mesajPrimit.decode())

clientSocket.close()