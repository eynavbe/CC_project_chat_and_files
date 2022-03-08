# CC_project_chat_and_files
- A primitive instant messaging system (Chat) based on communication over TCP.
- In addition the system transfers files over UDP.
## How to run:
### Running order:
1. Run server:
  - Open cmd that will be redirected to the folder where the files are located.
  - Impressions:
    “Python server.py <address ip>”
    address ip - an address found using:
    ipconfig -> Wi-Fi- IPv4 Address
2. Client run:
  - Open cmd that will be redirected to the folder where the files are located.
  - Impressions:
    “Python client.py”
After running, two gui screens open:
  - server
  - client (If you run "run client" several times, several client screens will open
  Representing multiple customers).
  
## Project presentation:
### File folder:
You can see that the client.py, server.py files are from different folders, the reason for this importance when a client wants to download a file is to download it from the server folder.
  <img width="804" alt="files_folder_1" src="https://user-images.githubusercontent.com/93534494/157260698-df6eb6d0-e4b5-4bb7-a385-6a71580d3743.png">

  ### To run the program:
Running server:
- Open cmd that will be redirected to the folder where the files are located.
- Impressions:
“Python server.py <address ip>”
address ip - an address found using:
ipconfig -> Wi-Fi- IPv4 Address
Client run:
- Open cmd that will be redirected to the folder where the files are located.
- Impressions:
“Python client.py”
  
  <img width="909" alt="run_cmd_2" src="https://user-images.githubusercontent.com/93534494/157260944-94df4e0a-ebbb-4829-8666-590970ad514b.png">

 After running server.py in cmd:
- A gui file opens that displays a message screen that the server receives from the client.
- On the server's screen, you receive messages on the screen according to the customers, ie messages about the client's login, the client's disconnection, sending a message to a specific customer, sending a message to all the clients, the client downloaded a file from the server.
 - It is important to run the server file in front of the client because only then will the client be able to connect to the server.
  
  <img width="908" alt="run_cmd_server_3" src="https://user-images.githubusercontent.com/93534494/157261116-e996e581-361c-4586-86be-2ad681da0764.png">

  After running client.py in cmd:
Opens the customer's gui.
  <img width="917" alt="run_cmd_client_4" src="https://user-images.githubusercontent.com/93534494/157261220-6c769828-84ac-4370-800d-fb45a01aea47.png">
  
 ### Register as a new customer:
- In the window that opens for us at the top, it is possible to enter the name of the client and the IP address of the server.
- If an incorrect IP address is entered, a message will appear on the screen.
- Clicking the "Login" button connects to the server (if the IP is correct)
  
  <img width="939" alt="5" src="https://user-images.githubusercontent.com/93534494/157261402-859bddff-6da4-42b1-a7a2-6b446475ec0e.png">

  After clicking login to connect to the server:
- After clicking the "Login" button, a connection to the server was made
- The "Login" button changes to the "Logout" button that allows the client to log out of the server.
- The message received on both the server and all connected clients:
  <name> connected to the server
    
  <img width="942" alt="6" src="https://user-images.githubusercontent.com/93534494/157261532-2b635c2a-22d7-43ca-81c3-f3562c1ec29d.png">

 ###File names that the client can download:
You can see that these are the files that are in the server's folder
    <img width="946" alt="7" src="https://user-images.githubusercontent.com/93534494/157261667-4aa08482-f3e3-4b59-b57d-fbcf0013462c.png">

  
  ### The names of the clients that the client can send a message to:
The clients connected to the server are just Leah the name we connected to so the client can only send to her or everyone.
  
<img width="844" alt="8" src="https://user-images.githubusercontent.com/93534494/157261767-30d2ccc8-df38-4839-a7c0-5fc12c3c8228.png">

    ### Connecting another client to the server:
- To connect another client to the server, open another cmd that will be routed to the folder where the files are located.
Impressions:
“Python client.py”
    
  <img width="847" alt="9" src="https://user-images.githubusercontent.com/93534494/157261889-bfb038fb-1b74-485d-9b16-856930e4a0fa.png">
 
    ### The additional customer's gui opens
- In the window that opens at the top, enter the name of the client and the IP address of the server.
- If an incorrect IP address is entered, a message will appear on the screen.
- Clicking the "Login" button connects to the server (if the IP is correct)
    
    <img width="958" alt="10" src="https://user-images.githubusercontent.com/93534494/157262026-1fb80606-6765-4990-88df-1ab355ab8696.png">

    ### After clicking on login another customer is added that customers can send messages to:
- After clicking the "Login" button, a connection to the server was made
- The "Login" button changes to the "Logout" button that allows the client to log out of the server.
- The message received on both the server and all connected clients:
  <name> connected to the serve
- The names of the clients that the client can send a message have been updated and the new client has been added, ie the clients that are connected to the server are Leah, Shlomo and therefore the client can only send to Leah or Shlomo or to everyone.
    
    <img width="960" alt="11" src="https://user-images.githubusercontent.com/93534494/157262163-a77f9f6c-4883-4346-b627-a7c0b9352852.png">

    ### Send a message to a specific customer:
- Next to the "To" on the client screen, there is an option to select who is sending the message.
Selecting "All" will send the message to everyone - this is the default.
Selecting a specific customer will send a message to the selected customer.
- By clicking "send" the message will be sent to the selected customer or to all customers.
    
    <img width="960" alt="12" src="https://user-images.githubusercontent.com/93534494/157262311-710894f2-f744-4b18-b000-36f77d14c17c.png">

    ### After sending send to send a message:
- As soon as the message is sent, the server receives an update and the message appears to him and to whom it was sent.
- All messages are sent using TCP protocol.
- The message received by the client:
<name>: <message>
- The message received on the server:
send to <name> - <message>
- And the message box is emptied in favor of sending a new message.
  
  <img width="960" alt="13" src="https://user-images.githubusercontent.com/93534494/157262514-9c8fa971-318b-4d45-99e9-6edfd9dae5f2.png">
  
  - Send a message from the other customer to a specific customer:
    
    <img width="960" alt="14" src="https://user-images.githubusercontent.com/93534494/157262525-5af09ec1-75d1-418a-8b19-df4c43056bc7.png">

    - After sending on the send:
  
  <img width="960" alt="15" src="https://user-images.githubusercontent.com/93534494/157262621-401e5be2-2eec-4de4-b326-651f69c61e55.png">

   ### Send a message to all customers:
- Next to the "To" on the client screen, there is an option to select who is sending the message.
- Selecting "All" will send the message to everyone by clicking on "send" will send the message to all customers.
    
    <img width="958" alt="16" src="https://user-images.githubusercontent.com/93534494/157262648-d44385b8-c3a6-4b10-a622-5cecd049b2e1.png">

   ### After sending send to send the messages to all customers:
- As soon as the message is sent, the server receives an update and the message appears to him and that it is sent to everyone.
- All messages are sent using TCP protocol.
- The message received to each client:
<name>: <message>
- The message received on the server:
send to <name> - <message>
- And the message box is emptied in favor of sending a new message.
    
    <img width="956" alt="17" src="https://user-images.githubusercontent.com/93534494/157262918-5215c879-a139-4508-bf15-bd6e4d74e9c9.png">

   ###Receiving the customer list:
By clicking on the "online_list" button, the list of clients connected to the server will appear on the screen.
  
  <img width="960" alt="18" src="https://user-images.githubusercontent.com/93534494/157263086-ffc4f07c-8ec1-41fc-8791-09fc6aaf5ead.png">

  ### List of files that appear on the server:
Clicking on "show server file" at the top of the screen will show the client all the files on the server.
  
  <img width="960" alt="19" src="https://user-images.githubusercontent.com/93534494/157263108-d37642b2-c677-41e3-969b-5078f06af5c7.png">
  
  
  ### Customer logout:
Customers connected to server:
  
  <img width="959" alt="20" src="https://user-images.githubusercontent.com/93534494/157263356-1f25b479-6ea1-4e56-af00-3b14c8e15785.png">

  
 #### Disconnection from the server:
- By clicking on the "Logout" button, the client disconnects from the server and the client window will close, in addition, it will send a message to all participants that - - the client has disconnected from the server, etc. The message that it has disconnected will also be sent to the server.
- The message received on both the server and all connected clients:
  <name> has left the chat
  
  <img width="955" alt="21" src="https://user-images.githubusercontent.com/93534494/157263367-728e10bf-b2e1-41a1-b052-28f70ace9fdf.png">

  #### Updated customer list to be notified:
    
    <img width="856" alt="22" src="https://user-images.githubusercontent.com/93534494/157263470-9e81fa18-7675-4a72-aa75-e93fdd376756.png">

  ### Files:
- File download:
- As soon as a client connects to the server, a list of files appears at the bottom of the screen that he can choose to download. The file list is the list in the server folder.
- After the customer selects the file to download, he must register in which name he wants to save the file.
- The name should be in the following format: <name>. <File type>
 If the client did not enter the file type, an error pane will pop up and an explanation of the required format.
If the customer entered the wrong file type another window will pop up explaining the problem.
- After selecting the file and choosing a new name for the file, click on "Download".
Once clicked the client sends a request to the server to receive the file using TCP.
The server accepts the request and sends the file using the UDP protocol.
The download stops at a certain point.
Once clicked "Download" the button will change to "Proceed".


- The messages that appear on the client:
got a download connection
user <name> downloaded __% out on file. last byte is: __
- The messages that appear on the server:
<name> - want to download <file name>
send to <name> - user <name> downloaded __% out on file. last byte is: __


- "Proceed" will continue to download the file from where it left off.
Shortly after the download is complete, a new file can be downloaded from the list again.


- The messages that appear in the client after clicking proceed:
user <name> confirm procssding
downloaded 100% out of file.
- The messages that appear on the server:
send to <name> - user <name> confirm proceeding.
user <name> downloaded 100% out of file.
  
    
### Messages that appear on the screen on the server:
- Customer login notifications
- Disengagement of a customer,
- Sending a message to a specific customer,
- Send a message to all customers
- The client wants to download a file from the server
- The client downloaded a certain percentage of a file from the server or the entire file.


### Messages that appear on the client screen:
- Connected or not connected to the server.
- The clients that connected to the server after the current client.
- The messages sent to the customer.
- Client disconnected from server.
- List of connected customers.
- List of existing files on the server.
- The file that the client wants to download, download the file
From the server.    
    
    
## video run: 

https://user-images.githubusercontent.com/93534494/157265335-adbd2334-af65-44ba-bdda-559c5f1a0e19.mp4
  
  #### download the file:

https://user-images.githubusercontent.com/93534494/157265445-8b876ba2-4414-4e37-9934-5d2b4004b222.mp4


