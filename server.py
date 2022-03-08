import os
import socket
import threading
import argparse
import time
import tkinter.scrolledtext
from tkinter import *
import tkinter as tk
import tkinter.filedialog
import tkinter

# Get the args
parser = argparse.ArgumentParser(description='Chatroom Server')
parser.add_argument('host', help='Interface the server listens at')
parser.add_argument('-p', metavar='PORT', type=int, default=12000,
                    help='TCP port (default 1060)')
args = parser.parse_args()
HOST = args.host
# port = Set between 0 and 1023 Any port that is beyond 1023 to port 65535 is not defined.
# A port allows the server to know which software the client is referring to,
# different software works with different ports.
PORT = args.p
# socket - Communication between 2 devices for the purpose of transmitting information,
# communication between the server and the client
# AF_INET - So that means we get a web domain that links to Internet by name and not by IP
# SOCK_STREAM - Causes Socket to work with TCP protocol
# TCP - Provides reliable traffic and checks if all packages have arrived properly.
# If there is a problem he allows the receiving party to resend.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SOCK_DGRAM - causes the socket to work with the UDP protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Links the socket to the port
    server.bind((HOST, PORT))
    # Makes socket listen and wait for the information received to him
    # 10 - says it handles up to 10 connections at a given time,
    # 10 is the number of incoming connections waiting in line.
    server.listen(10)
except:
    # If it fails to connect to TSP you will close the program
    exit(0)
    sys.exit()
# The clients who are connected
clients = []
# Names of connected customers
nicknames = []


class Server:
    def __init__(self):
        print("server running...")
        # run gui
        gui_thread = threading.Thread(target=self.gui_run_s)
        gui_thread.start()
        self.run = True
        self.receive()

    """Displays the gui"""

    def gui_run_s(self):
        status_a = 'server'
        self.window = tk.Tk()
        n = tk.StringVar
        self.window.title(status_a)
        frame = Frame(self.window)
        frame.grid(column=0, row=1, padx=10, pady=25)
        la = Label(frame, text="list from client:", font=("Ariel", 12))
        la.pack(side=LEFT, padx=0, pady=0)
        # Messages screen, where all the messages the server received appear
        self.text_area = tkinter.scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=40, height=10,
                                                           font=("Ariel", 12))
        self.text_area.grid(column=0, row=2, pady=10, padx=5)
        # Placing cursor in the text area
        self.text_area.focus()
        # Clicking on the end of the gui will be sent to the function that ends the program
        self.window.protocol("WM_DELETE_self.window", self.stop)
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    """broadcast - Sends message to all logged in users 
        message - The message received from the customer """

    def broadcast(self, message):
        # The client wants to get the list of files where the server's file is located
        if "want show server files" in str(message):
            # Display the message on the Messages screen
            self.write(str(message))
            # Get the file location
            path = os.getcwd()
            # The list of all the files in the folder
            dirs = os.listdir(path)
            # Get the name of the client who requested the files
            s_message = (str(message).split("-"))[0]
            # Get the name of the client as it appears in the list of the server
            for i in range(len(nicknames)):
                if nicknames[i] in s_message:
                    # Sends the content to client via TCP
                    clients[i].send("_____Server File List_____\n".encode('utf-8'))
                    for file in dirs:
                        path1 = os.path.join(path, file)
                        # Checks that it really is a file and not as a folder example
                        if os.path.isfile(path1):
                            clients[i].send(file.encode())
                            clients[i].send("\n".encode('utf-8'))
                    clients[i].send("_____End Server File List_____\n".encode('utf-8'))
            # This would print all the files and directories

        # The message received by the server that contains the file name that the client wants to download,
        # the server will send the file to the client
        print(str(message))
        if "want download" in str(message):
            s_message2 = str(message).replace("b'", '')
            s_message2 = s_message2.replace("'", '')
            # Display the message on the Messages screen
            self.write(s_message2)
            # Get the name of the client who wants to download the file
            s_message = (str(message).split("-"))[0]
            # Get the name of the client as it appears in the list of the server
            for i in range(len(nicknames)):
                if nicknames[i] in s_message:
                    # Get the file name what str of the message
                    reqFile = str(message)[str(message).find("download") + 9:]
                    reqFile = reqFile.replace("'", '')
                    f = open(reqFile, "r")
                    data = f.read(1024)
                    part_client_info = str(clients[0])[str(clients[i]).find("laddr=(") + 8:]
                    laddr_client = part_client_info[:part_client_info.find(")")]
                    ip_client = part_client_info[:part_client_info.find("'")]
                    port_client = int(laddr_client[laddr_client.find(",") + 2:])
                    port_client_udp = 9090 + i
                    print(port_client_udp)
                    sock.sendto(data.encode(), (ip_client, port_client_udp))
                    while (data):
                        if (sock.sendto(data.encode(), (ip_client, port_client_udp))):
                            data = f.read(1024)
                            time.sleep(0.02)  # Give receiver a bit time to save
        # If a customer has left the chat
        if "has left the chat" in str(message):
            s_message2 = str(message).replace("b'", '')
            s_message2 = s_message2.replace("'", '')
            # Display the message on the Messages screen
            self.write(str(s_message2))
            # Get the name of the client who wants to download the file
            s_message = (s_message2.split("-"))[0]
            # Get the name of the client as it appears in the list of the server
            for i in range(len(nicknames)):
                if nicknames[i] in s_message:
                    # Delete this client from the server lists
                    clients.pop(i)
                    nicknames.pop(i)
                    break
            # Send the message to all clients connected to the server
            # Sends the updated list of customer names and also the message about the customer who has left
            for x in clients:
                x.send("&".encode('utf-8'))
                x.send(message)
                x.send("&".encode('utf-8'))
                x.send(str(nicknames).encode('utf-8'))
                x.send("&".encode('utf-8'))
        if "$" in str(message):
            # Get the name of the client who wants to download the file
            s_message = (str(message).split("$"))
            # Get the name of the client as it appears in the list of the server
            for i in range(len(nicknames)):
                if nicknames[i] in s_message[1]:
                    s_message1 = s_message[0].replace("\\n", '')
                    s_message2 = s_message1.replace("b'", '')
                    # When the file is completely downloaded
                    if "downloaded 100% out of file" in str(message):
                        # Display the message on the Messages screen
                        self.write((s_message2))
                        s_message2 = s_message2[s_message2.find("download"):]
                        clients[i].send(s_message2.encode('utf-8'))
                        clients[i].send("\n".encode('utf-8'))
                    # When the customer wants to send the message to a specific customer
                    else:
                        # Display the message on the Messages screen
                        self.write(("sent to " + nicknames[i] + " - " + s_message2))
                        clients[i].send(s_message2.encode('utf-8'))
                        clients[i].send("\n".encode('utf-8'))
        else:
            # Other types of messages, these messages are sent to all customers
            if "want show server files" not in str(message) and "want download" not in str(
                    message) and "has left the chat" not in str(message):
                s_message1 = str(message).replace("\\n", '')
                s_message2 = s_message1.replace('b"', '')
                s_message2 = s_message2.replace('"', '')
                if s_message2.find("b'") == 0:
                    s_message2 = s_message2.replace("b'", '')
                if s_message2.find("'") == len(s_message2) - 1:
                    s_message2 = s_message2.replace("'", '')
                self.write(("sent to all - " + s_message2))
                for client in clients:
                    client.send(message)

    """Write the message on the message display"""

    def write(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message + "\n")
        self.text_area.yview('end')
        self.text_area.config(state='disabled')

    """Close the program"""

    def stop(self):
        self.running = False
        self.window.destroy()
        sock.close()
        server.close()
        exit(0)
        sys.exit()

    """ handle - Manage customer connection"""

    def handle(self, client):
        while self.run:
            try:
                # recv - which returns the data in bits from the server.
                # 1024 - can be any size you want when you want to capture a large size of message at a time or small.
                message = client.recv(1024)
                self.broadcast(message)
            except:
                if client in clients:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nickname = nicknames[index]
                    nicknames.remove(nickname)
                break

    """ receive - Goes to listen all the time, and gets new customers and connects them"""

    def receive(self):
        while self.run:
            try:
                # The server is waiting for the connection request from clients,
                # creating the connection socket for the client.
                # Connected new and returns a file that refers to the same socket,
                # the new socket created not in the original listening mode is not affected by it.
                client, address = server.accept()
                print("Client connected", address)
                client.send("NICK".encode('utf-8'))  # For the user to select a nickname
                # recv - which returns the data in bits from the server.
                # 1024 - can be any size you want when you want to capture a large size of message at a time or small.
                # The client's name
                nickname = (str(client.recv(1024)).split("'"))[1]
                # Add the client to the lists
                nicknames.append(nickname)
                clients.append(client)
                # Send a message to customers
                self.broadcast(f"'{nickname}' connected to the server\n".encode('utf-8'))
                # If the client received a message from the server that contains:
                # the names of all the connected clients, the files that are in the server's folder,
                # the size of the files that are in the server's folder.
                for x in clients:
                    x.send("@".encode('utf-8'))
                    x.send(str(nicknames).encode('utf-8'))
                    x.send("@".encode('utf-8'))
                    files = []
                    # Get the file location
                    path = os.getcwd()
                    # The list of all the files in the folder
                    dirs = os.listdir(path)
                    for yx in dirs:
                        path1 = os.path.join(path, yx)
                        # Checks that it really is a file and not as a folder example
                        if os.path.isfile(path1):
                            # Add to the list the name of each file
                            files.append(yx)
                    x.send(str(files).encode('utf-8'))
                    x.send("@".encode('utf-8'))
                    files_size = []
                    for f in os.listdir(path):
                        path1 = os.path.join(path, f)
                        # Checks that it really is a file and not as a folder example
                        if os.path.isfile(path1):
                            # Add to the list the size of each file
                            files_size.append(str(os.path.getsize(path1)))
                    x.send(str(files_size).encode('utf-8'))
                    x.send("@".encode('utf-8'))
                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except:
                break


Server()
