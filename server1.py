import socket
import threading

SERVER_PORT = 5050
SERVER_IP = "127.0.0.1"
SERVER_LISTEN_ADDRESS = (SERVER_IP, SERVER_PORT)
SOCKET_ENCODE = "utf-8"

clientList:list=[]
numberOfClient=0
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
	server.bind(SERVER_LISTEN_ADDRESS)
except Exception as e:
	print("[Server]Scoket error")
	print(e)
	exit()

def buildConnections():
	print("[Server]Server side listen port:" , SERVER_PORT)
	server.listen()
	print("[Server]Waiting for any client")
	try:
		while True:
			global numberOfClient

			conn, addr = server.accept()
			conn.send("NAME".encode(SOCKET_ENCODE))
			name = conn.recv(4096).decode(SOCKET_ENCODE)

			clientList.append({"name":name,"connect_object":conn})
			print(f"Name is :{name}")
			broadcasToClient(f"Client{name} join".encode(SOCKET_ENCODE))

			numberOfClient+=1

			conn.send('Connection successful!'.encode(SOCKET_ENCODE))
			
			thread = threading.Thread(target = connectHandler,args = (conn, addr))
			thread.start()
			
			print(f"active connections {numberOfClient}")
	except Exception as e:
		print("Server stop")
		print(e)
		server.close()
		exit()
	except KeyboardInterrupt:
		print("\nServer stop by Ctrl+c")
		print("Server stop,try to close socket")
		server.close()
		exit()

def connectHandler(conn, addr):
	print(f"new connection {addr}")
	connected = True
	while connected:
		message = conn.recv(1024)
		broadcasToClient(message)
	print("[Server]1 Client leave")
	conn.close()

def broadcasToClient(message):
	global numberOfClient
	for clientMsg in clientList:
		try:
			clientMsg["connect_object"].send(message)
		except Exception as e:
			print("[Server]1 Client leave")
			clientList.remove(clientMsg)
			numberOfClient-=1

try:
	buildConnections()
except Exception as e:
	print("[Server]Scoket error")
	print(e)
	server.close()
	exit()