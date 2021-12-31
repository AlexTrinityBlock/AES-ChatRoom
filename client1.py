import socket
import threading
from tkinter import *
from tkinter import messagebox

PORT = 5050
FONT_FORMAT = "utf-8"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

class GUI:
	serverIP="127.0.0.1"
	
	def __init__(self):
		self.Window = Tk()
		self.Window.withdraw()
		self.loginPage()
		self.Window.mainloop()
		
	def socketConnect(self,serverIP):
		try:
			print("Connect to server",serverIP)
			client.connect((serverIP, PORT))
		except Exception as e:
			print(e)
			messagebox.showwarning("Student 1100336",e)
			exit()

	def loginPage(self):
		self.login = Tk()
		self.login.title("AES Secret Chat room")
		##Input User name
		self.login.resizable(width = False,
							height = False)
		self.login.configure(width = 400,
							height = 400)
		self.pls = Label(self.login,
					text = "AES Secret Chat room",
					justify = CENTER,
					font = "lucida 14 bold")
		self.pls.place(relheight = 0.15,
					relx = 0.2,
					rely = 0.05)
		self.labelName = Label(self.login,
							text = "Name: ",
							font = "lucida 12")
		self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.15)
		self.entryName = Entry(self.login,
							font = "lucida 12",
							bg = "#000000",
							fg = "#00e622",
							)				
		self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
		##Input Server IP
		self.labelIP = Label(self.login,
							text = "Server IP",
							font = "lucida 12")
		self.labelIP.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.35)
		self.entryIP = Entry(self.login,
							font = "lucida 12",
							bg = "#000000",
							fg = "#00e622",
							)				
		self.entryIP.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.4)
		##Input Secret IP
		self.labelSecret = Label(self.login,
							text = "Secret",
							font = "lucida 12")
		self.labelSecret.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.55)
		self.entrySecret = Entry(self.login,
							font = "lucida 12",
							bg = "#000000",
							fg = "#00e622",
							)				
		self.entrySecret.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.6)

		#Btn					
		self.continueBtn = Button(self.login,
						text = "Enter",
						font = "lucida 12 bold",
						command = lambda: [self.socketConnect(self.entryIP.get()),self.goAhead(self.entryName.get())]
						)
		self.continueBtn.place(relx = 0.4,rely = 0.8)

	def goAhead(self, name):
		self.login.destroy()
		self.chatPage(name)
		rcv = threading.Thread(target=self.receiveMessageAction)
		rcv.start()

	# The chat page
	def chatPage(self,name):
		self.name = name
		self.Window.deiconify()
		self.Window.title("AES Chat Room")
		self.Window.resizable(width = False,
							height = False)
		self.Window.configure(width = 470,
							height = 600,
							bg = "#000000")
		self.labelHead = Label(self.Window,
							bg = "#000000",
							fg = "#00e622",
							text = self.name ,
							font = "lucida 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		

		#Cipher text
		self.cipherText = Text(self.Window,
							width = 20,
							height = 0.5,
							bg = "#000000",
							fg = "#00e622",
							font = "lucida 14",
							padx = 5,
							pady = 1)
		self.cipherText.place(relheight = 0.3,
							relwidth = 1,
							rely = 0.08)
		self.cipherText.config(state = DISABLED)

		self.labelBottom = Label(self.Window,
								bg = "#ABB2B9",
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		#Decode text
		self.decodeText = Text(self.Window,
							width = 20,
							height = 0.5,
							bg = "#000000",
							fg = "#00e622",
							font = "lucida 14",
							padx = 5,
							pady = 0)
		self.decodeText.place(relheight = 0.3,
							relwidth = 1,
							rely = 0.4)
		self.decodeText.config(state = DISABLED)

		#Input Message box

		self.messageInputBox = Entry(self.labelBottom,
							bg = "#000000",
							fg = "#00e622",
							font = "lucida 13")
		
		self.messageInputBox.place(relwidth = 0.74,
							relheight = 0.06,
							rely = 0.001,
							relx = 0.011)
		
		self.messageInputBox.focus()
		
		# Btn of send message
		self.buttonMsg = Button(self.labelBottom,
								text = "Pass message",
								font = "lucida 10 bold",
								width = 20,
								bg = "#ABB2B9",
								command = lambda : self.sendMessageAction(self.messageInputBox.get()))
		
		self.buttonMsg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.22)
		
		self.cipherText.config(cursor = "arrow")
		
		scrollbar = Scrollbar(self.cipherText)
		scrollbar.place(relheight = 1,
						relx = 0.974)
		
		scrollbar.config(command = self.cipherText.yview)
	
	#Send message action
	def sendMessageAction(self, msg):
		self.cipherText.config(state = DISABLED)
		self.msg=msg
		self.messageInputBox.delete(0, END)
		snd= threading.Thread(target = self.sendMessage)
		snd.start()

	def receiveMessageAction(self):
		while True:
			try:
				message = client.recv(1024).decode(FONT_FORMAT)
				
				# if the messages from the server is NAME send the client's name
				if message == 'NAME':
					client.send(self.name.encode(FONT_FORMAT))
				else:
					# insert messages to text box
					self.cipherText.config(state = NORMAL)
					self.cipherText.insert(END,
										message+"\n\n")
					
					self.cipherText.config(state = DISABLED)
					self.cipherText.see(END)
			except:
				# an error will be printed on the command line or console if there's an error
				print("An error occured!")
				client.close()
				break

	def sendMessage(self):
		self.cipherText.config(state=DISABLED)
		while True:
			message = (f"{self.name}: {self.msg}")
			client.send(message.encode(FONT_FORMAT))
			break

mainObject = GUI()
