import socket
import threading
import time
import tkinter.scrolledtext
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter
import argparse
import os
# HOST = '10.9.0.255'  # ipconfig ifconfig
# PORT = 9090
import select


class Client:
    def __init__(self):
        self.run_udp = False
        print("client running...")
        # List of clients' names connected to the server
        self.nicknames = []
        # The list of files that appears in the server folder
        self.files = []
        # File sizes that appears in the server folder
        self.files_size = []
        self.host = ''
        # client username
        self.nickname = ''
        self.running = True
        self.close_run = True
        self.filename = ''
        self.continue_download = True
        self.continue_download_count = 0
        # socket - Communication between 2 devices for the purpose of transmitting information,
        # communication between the server and the client
        # AF_INET - So that means we get a web domain that links to Internet by name and not by IP
        # SOCK_STREAM - Causes Socket to work with TCP protocol
        # TCP - Provides reliable traffic and checks if all packages have arrived properly.
        # If there is a problem he allows the receiving party to resend.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creates socket server, socket login
        # SOCK_DGRAM - causes the socket to work with the UDP protocol
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.con_udp = True
        # run gui
        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()

    """Displays the gui"""

    def gui_loop(self):
        status_a = 'client'
        self.window = tk.Tk()
        n = tk.StringVar
        self.window.title(status_a)
        frame = Frame(self.window)
        frame.grid(column=0, row=1, padx=10, pady=25)
        la = Label(frame, text="name:", font=("Ariel", 12))
        la.pack(side=LEFT, padx=0, pady=0)
        # Write down your username to log in
        box_text = Text(frame, height=1, width=10)
        box_text.pack(side=LEFT, padx=5, pady=0)
        la_address = Label(frame, text="address:", font=("Ariel", 12))
        la_address.pack(side=LEFT, padx=0, pady=0)
        # Write down the ip address you connect to
        box_text_address = Text(frame, height=1, width=10)
        box_text_address.pack(side=LEFT, padx=5, pady=0)
        # Clicking will cause all the files in the server's folder to be received
        self.serverFileButton = tk.Button(self.window, text="Show server files", command=self.send_file)
        self.serverFileButton.grid(column=0, row=2)
        # Messages screen, where all the messages the client received appear
        self.text_area = tkinter.scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=40, height=10,
                                                           font=("Ariel", 12))
        self.text_area.grid(column=0, row=3, pady=10, padx=5)
        self.text_area.focus()
        frame_area = Frame(self.window)
        frame_area.grid(column=0, row=5, padx=10, pady=10)
        to_message = Label(frame_area, text="To:", font=("Ariel", 12))
        to_message.pack(side=LEFT, padx=5, pady=5)
        # The list of the names of all the clients connected to the server
        nick_message = ["All"]
        for x in self.nicknames:
            nick_message.append(x)
        # Select the name to which the message will be sent
        self.combo_box = ttk.Combobox(frame_area, width=3, textvariable=n)
        self.combo_box['values'] = nick_message
        self.combo_box.pack(side=LEFT, padx=5, pady=5)
        self.combo_box.current(0)
        message_la = Label(frame_area, text="message", font=("Ariel", 12), background='lightgray', foreground="white")
        message_la.pack(side=LEFT, padx=5, pady=5)
        # Record the message sent to the client you selected
        self.input_area = Text(frame_area, height=2, width=40)
        self.input_area.pack(side=LEFT, padx=5, pady=5)
        # Clicking on it will send the message to the selected name
        self.send_button = Button(frame_area, text="send", command=self.write)
        self.send_button.pack(side=LEFT)
        frame_file = Frame(self.window)
        frame_file.grid(column=0, row=6, padx=25, pady=10)
        whichFile = Label(frame_file, text="Choose file to download:", font=("Ariel", 8))
        whichFile.pack(side=LEFT, padx=0, pady=0)
        # Select the file to download from the list that appears in the server folder
        self.box_file = ttk.Combobox(frame_file, width=30)
        self.box_file['values'] = self.files
        self.box_file.pack(side=LEFT)
        if len(self.files) > 0:
            self.box_file.current(0)
        new_name_file = Label(frame_file, text="save file as:", font=("Ariel", 8))
        new_name_file.pack(side=LEFT, padx=0, pady=0)
        # Write down the name of the new file of the downloaded file
        self.new_name_file = Text(frame_file, height=1, width=10)
        self.new_name_file.pack(side=LEFT, padx=5, pady=0)
        # Clicking on it will download the file from the server and save it in the client's folder with the selected name
        self.download_file = tk.Button(frame_file, text="Download file",
                                       command=self.download_file_f)
        self.download_file.pack(side=LEFT, padx=5, pady=0)
        self.style = ttk.Style(self.window)
        self.style.layout('text.Horizontal.TProgressbar',
                          [('Horizontal.Progressbar.trough',
                            {'children': [('Horizontal.Progressbar.pbar',
                                           {'side': 'left', 'sticky': 'ns'})],
                             'sticky': 'nswe'}),
                           ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')
        # Will show the percentage of the download, the amount of size dropped from the full amount of the file in percent
        self.progress_bar = ttk.Progressbar(self.window, style='text.Horizontal.TProgressbar', length=200,
                                            maximum=100, value=0)
        self.progress_bar.grid(column=0, row=7, pady=10, padx=5)

        """Will display the list of users connected to the server in the display of the messages"""

        def online_list_f():
            self.text_area.config(state='normal')
            # Prints on the display of the messages
            self.text_area.insert('end', "____online list____\n")
            for i in range(len(self.nicknames)):
                if i != 0 and i != len(self.nicknames) - 1:
                    self.text_area.insert('end', self.nicknames[i])
                    self.text_area.insert('end', ",")
            # Prints the names of the customers on the display of the messages
            if len(self.nicknames) > 0:
                self.text_area.insert('end', self.nicknames[len(self.nicknames) - 1])
            self.text_area.insert('end', "\n")
            self.text_area.insert('end', "____end list____\n")
            self.text_area.yview('end')
            self.text_area.config(state='disabled')

        """client login or logout to server"""

        def client_login_or_logout_to_server():
            # The client disconnects from the server
            if self.nickname != '':
                message = f"{self.nickname}- has left the chat."  # ('1.0','end') get all text
                # Will send a message via tcp to the server that this client has left,
                # this message will also be sent to all clients connected to the server
                self.sock.send(message.encode('utf-8'))
                print('\nQuit...')
                # Closing the socket, closing the communication between 2 devices for the purpose
                # of transmitting information, communication between the server and the client
                self.sock.close()
                # Stop the program
                os._exit(0)
            # The client login to the server
            try:
                # Save the name the client entered in this variable
                self.nickname = box_text.get("1.0", 'end-1c')
                self.running = True
                # Save the ip address the client entered in this variable
                self.host = box_text_address.get("1.0", 'end-1c')
                # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Establishes a connection with the server
                self.sock.connect((self.host, PORT))
                # So that it is not possible to change what is listed there, the name
                box_text.configure(state='normal')
                box_text.insert('end', '')
                box_text.configure(state='disabled')
                # So that it is not possible to change what is listed there, the ip
                box_text_address.configure(state='normal')
                box_text_address.insert('end', '')
                box_text_address.configure(state='disabled')
                # Change what is listed in the button from login to logout
                self.slogan.config(text="Logout")
                # connected to server - TCP
                receive_thread = threading.Thread(target=self.receive)
                receive_thread.start()
            except:
                # Failed to connect to server, displays message on message screen
                self.text_area.config(state='normal')
                self.text_area.insert('end', "Failed to connect\n")
                self.text_area.yview('end')
                self.text_area.config(state='disabled')

        # By clicking on it the client login or logout to server
        self.slogan = Button(frame, text="Login", command=client_login_or_logout_to_server)
        self.slogan.pack(side=LEFT)
        # By clicking on it, the list of names connected to the server appears on the message screen
        online_list = Button(frame, text="online_list", command=online_list_f)
        online_list.pack(side=LEFT)
        self.gui_done = True
        # Clicking on the end of the gui will be sent to the function that ends the program
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.protocol("WM_DELETE_self.window", self.stop)
        self.window.mainloop()

    #
    # def write_nick_name(self):
    #     message = self.input_nickname.get('1.0', 'end')
    #     self.nickname = message.encode('utf-8')
    #     self.input_nickname.delete('1.0', 'end')

    """TCP - Sends a request to the server that 
    the client wants to see the files in the server folder for Show server files"""

    def send_file(self):
        message = f"{self.nickname}- want show server files"  # ('1.0','end') get all text
        self.sock.send(message.encode('utf-8'))

    """Updates the download percentage of the file"""

    def update_progress_bar(self, percentage):
        self.progress_bar.config(value=percentage)
        self.style.configure('text.Horizontal.TProgressbar', text='{:g} %'.format(percentage))

    """Downloads the file we received from the server through udp and returns the hack"""

    def download_file_f(self):
        print(len(self.files))
        if len(self.files) > 0:
            # If the client has not yet started downloading the file and wants to download it
            print(self.download_file.cget('text'))
            if "Download file" in self.download_file.cget('text'):
                # The download button can not be pressed again
                self.download_file.configure(state=DISABLED)
                # Get the file name in whose name the downloaded file will be saved
                new_name_file_d = (str(self.new_name_file.get('1.0', 'end'))).split('.')
                # The name of the file being downloaded
                file_name = (str(self.box_file.get())).split('.')
                # Tests that he file name in whose name the downloaded file will be saved is correct
                if len(new_name_file_d) == 1:
                    window1 = tk.Tk()
                    window1.eval('tk::PlaceWindow . center')
                    window1.title("error")
                    ttk.Label(window1,
                              text="The file name should be as follows: File name. File type (same type of original file) ",
                              font=("Times New Roman", 12)).grid(column=0, row=15, padx=5, pady=5)
                    return

                elif new_name_file_d[1].find(file_name[1]) == -1:
                    window1 = tk.Tk()
                    window1.eval('tk::PlaceWindow . center')
                    window1.title("error in type file")
                    ttk.Label(window1, text="The file type after the dot should be the same as in the original file ",
                              font=("Times New Roman", 12)).grid(column=0, row=15, padx=5, pady=5)
                    return

                self.filename = str(self.box_file.get())
                # Send to the server the name of the file that the client wants to download,
                # so that it can transfer the file to it via udp
                message = f"{self.nickname}- want download {self.filename}"  # ('1.0','end') get all text
                self.sock.send(message.encode('utf-8'))
            else:
                # If the customer clicks on Proceed, that means the customer wants to continue with the download
                message = f"User {self.nickname} confirm proceeding. ${str(self.nickname)}"  # ('1.0','end') get all text
                # Send to server that the client wants to continue with the download
                self.sock.send(message.encode('utf-8'))
                self.continue_download = True
                # Rename the button
                self.download_file.config(text="Download file")
                self.download_file.configure(state=DISABLED)

    """Send to the server the message that the client wants to send to everyone or one client,
     so that the server will send it to the relevant clients or client that the client wants to send."""

    def write(self):
        if self.nickname != '':
            if "All" not in str(self.combo_box.get()):
                message = f"{self.nickname}: {self.input_area.get('1.0', 'end')} ${str(self.combo_box.get())}"  # ('1.0','end') get all text
            else:
                message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"  # ('1.0','end') get all text
            self.sock.send(message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    """Close the program"""
    def stop(self):
        self.close_run = False
        self.window.destroy()
        self.sock.close()
        os._exit(0)
        exit(0)
        sys.exit()

    """UDP context - to download the file from server"""
    def receive_udp(self):
        while self.running:
            try:
                if not self.close_run:
                    break
                if self.continue_download:
                    data, adder = self.sock_udp.recvfrom(1024)
                    timeout = 5
                    if data:
                        if self.con_udp:
                            self.text_area.config(state='normal')
                            self.text_area.insert('end', "Got a download connection\n")
                            self.text_area.yview('end')
                            self.text_area.config(state='disabled')
                            self.con_udp = False
                        file_name = data.strip()
                        size_file_d = 1000
                        for t in range(len(self.files)):
                            if self.files[t] in self.filename:
                                size_file_d = int(self.files_size[t])
                        new_file_name = str(self.new_name_file.get('1.0', 'end'))
                        new_file_name = new_file_name.replace('\n', '')
                        f = open(new_file_name, 'ab')
                        if self.continue_download_count == 1:
                            f.write(data)
                        while self.continue_download:
                            ready = select.select([self.sock_udp], [], [], timeout)
                            if ready[0]:
                                path = os.getcwd()
                                size_new_file = os.path.getsize(path + "/" + new_file_name)
                                pre = size_new_file / (size_file_d / 100)
                                pre = float("{:.2f}".format(pre))
                                self.update_progress_bar(pre)
                                if size_file_d / 2 < size_new_file and self.continue_download_count == 0:
                                    pre = size_new_file / (size_file_d / 100)
                                    self.continue_download = False
                                    self.continue_download_count = 1
                                    pre = float("{:.2f}".format(pre))
                                    self.download_file.configure(state=NORMAL)
                                    self.download_file.config(text="Proceed")
                                    f.close()
                                    with open(new_file_name, 'rb') as f:
                                        hh = f.read()[-8:]
                                    hh = str(hh)
                                    if hh.find('b') == 0:
                                        hh = hh[2:]
                                        hh = hh[:-1]
                                    message = f"User {self.nickname} downloaded {pre}% out of file. Last byte is: {hh} ${str(self.nickname)}"  # ('1.0','end') get all text
                                    self.sock.send(message.encode('utf-8'))
                                else:
                                    data, adder = self.sock_udp.recvfrom(1024)
                                    f.write(data)
                                    size_new_file = os.path.getsize(path + "/" + new_file_name)
                                    pre = size_new_file / (size_file_d / 100)
                                    pre = float("{:.2f}".format(pre))
                                    self.update_progress_bar(pre)
                            else:
                                print("Finish downloaded")
                                # ddd
                                self.update_progress_bar(100)
                                message = f"User {self.nickname} downloaded 100% out of file. ${str(self.nickname)}"  # ('1.0','end') get all text
                                self.sock.send(message.encode('utf-8'))
                                start = time.time()
                                while time.time() < start + 5:
                                    pass
                                self.download_file.configure(state=NORMAL)
                                self.new_name_file.delete('1.0', 'end')
                                self.download_file.config(text="Download file")
                                self.update_progress_bar(0)
                                self.con_udp = True
                                self.sock_udp.close()
                                f.close()
                                break

            except ConnectionAbortedError:
                break
            except:
                print("error_udp")
                self.sock_udp.close()
                break

    """TCP context - for receiving messages from the server"""

    def receive(self):
        while self.running:
            try:
                if not self.close_run:
                    break
                # recv - which returns the data in bits from the server.
                # 1024 - can be any size you want when you want to capture a large size of message at a time or small.
                # decode - converts the bits to a string of text
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    # If the gui ran
                    if self.gui_done:
                        # If the client received a message from the server that contains:
                        # client login message
                        # the names of all the connected clients, the files that are in the server's folder,
                        # the size of the files that are in the server's folder.
                        # or If the client received a message from the server: the names of all the connected clients
                        if "[" in message:
                            # Separate the types of message
                            message_x = message.split("@")
                            # or get only the names of all the connected clients
                            message_t = message.split("&")
                            if len(message_t) > 1:
                                # The message that contains the names of all the connected clients
                                message_nicknames = message_t[1]
                                # Display on the notifications screen the client logout message
                                self.text_area.config(state='normal')
                                self.text_area.insert('end', message_t[0])
                                self.text_area.yview('end')
                                self.text_area.config(state='disabled')
                                # Get the names of connected clients
                                x = message_nicknames.split("[")
                                x = x[1].split("]")
                                x.pop(len(x) - 1)
                                self.nicknames = []
                                self.nicknames.append("All")
                                x = x[0].split("'")
                                if ',' in x[1]:
                                    x = x[1].split(",")
                                for i in x:
                                    if ("," not in i) and len(i) > 0:
                                        self.nicknames.append(i)
                                self.combo_box['values'] = self.nicknames
                                # Links the socket to the port
                                print(self.run_udp)
                                if not self.run_udp:
                                    for i in range(len(self.nicknames)):
                                        print(self.nicknames[i])
                                        if self.nickname in self.nicknames[i]:
                                            print(self.host)
                                            if self.host != '':
                                                port_client_udp = 9090 + i
                                                self.sock_udp.bind((self.host, port_client_udp))
                                                self.run_udp = True
                                                # connected to server - UDP
                                                receive_thread = threading.Thread(target=self.receive_udp)
                                                receive_thread.start()
                            # If all the message containing the information has been received
                            if len(message_x) == 5:
                                # The message that contains the names of all the connected clients
                                message_nicknames = message_x[1]
                                # The message that contains the files that are in the server's folder
                                message_files = message_x[2]
                                # The message that contains the size of the files that are in the server's folder
                                message_files_size = message_x[3]
                                # Display on the notifications screen the client login message
                                self.text_area.config(state='normal')
                                self.text_area.insert('end', message_x[0])
                                self.text_area.yview('end')
                                self.text_area.config(state='disabled')
                                # Get the names of connected clients
                                x = message_nicknames.split("[")
                                x = x[1].split("]")
                                x.pop(len(x) - 1)
                                self.nicknames = []
                                self.nicknames.append("All")
                                x = x[0].split("'")
                                if ',' in x[1]:
                                    x = x[1].split(",")
                                for i in x:
                                    if ("," not in i) and len(i) > 0:
                                        self.nicknames.append(i)
                                x = message_files.split("[")
                                x = x[1].split("]")
                                x.pop(len(x) - 1)
                                # Get the files from str
                                self.files = []
                                x = x[0].split("'")
                                if ',' in x[1]:
                                    x = x[1].split(",")
                                for i in x:
                                    if ("," not in i) and len(i) > 0:
                                        self.files.append(i)
                                x = message_files_size.split("[")
                                x = x[1].split("]")
                                x.pop(len(x) - 1)
                                # Get the size of files from str
                                self.files_size = []
                                x = x[0].split("'")
                                if ',' in x[1]:
                                    x = x[1].split(",")
                                for i in x:
                                    if ("," not in i) and len(i) > 0:
                                        self.files_size.append(i)
                                self.combo_box['values'] = self.nicknames
                                self.box_file['values'] = self.files
                                if len(self.files) > 0:
                                    self.box_file.current(0)
                                    # Links the socket to the port
                                    print(self.run_udp)
                                    if not self.run_udp:
                                        for i in range(len(self.nicknames)):
                                            print(self.nicknames[i])
                                            if self.nickname in self.nicknames[i]:
                                                print(i)
                                                print(self.host)
                                                if self.host != '':
                                                    port_client_udp = 9089 + i
                                                    print(port_client_udp)
                                                    self.sock_udp.bind((self.host, port_client_udp))
                                                    self.run_udp = True
                                                    # connected to server - UDP
                                                    receive_thread = threading.Thread(target=self.receive_udp)
                                                    receive_thread.start()
                        else:
                            # Display the message on the screen
                            message = message.replace("@", '')
                            message = message.replace("&", '')
                            self.text_area.config(state='normal')
                            self.text_area.insert('end', message)
                            self.text_area.yview('end')
                            self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("error")
                self.sock.close()
                break


# Get the args
parser = argparse.ArgumentParser(description='Chatroom Server')
parser.add_argument('-p', metavar='PORT', type=int, default=12000,
                    help='TCP port (default 1040)')
args = parser.parse_args()
# port = Set between 0 and 1023 Any port that is beyond 1023 to port 65535 is not defined.
# A port allows the server to know which software the client is referring to,
# different software works with different ports.
PORT = args.p
client = Client()
