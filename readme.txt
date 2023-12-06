# CS3201 bulletin board system 
## Introduction
This repository is created for `City University HK` course `CS3201 - Computer Networks` programming assignment <br />
All credit goes to: Poon Nok Tung, Claire


## Getting Started
1. install python
```
2. Start the project
```
$ python server.py
$ python client.py
```
3. type in IP address: localhost and port : 16011

## File Description
| File      | Usage                                                                        |
| --------- | ---------------------------------------------------------------------------- |
| client.py | Handle the client connection and the chatroom UI                             |
| server.py | Server hosting, handle all the client connection and broadcasting of message |

## Logic Flow
### Join bulletin board 
User will be prompted to type in the correct IP and port and a socket will be created with a try catch. <br />
Error message will prompt if server can't reach for whatever reason. <br />
After the connection made, user will be prompted to enter command 1-4 <br />
command "1":input string (can input more than one string, until the user input "&" , the loop will end and the user will receive response "ok" from server)
command "2":post file (C:\Users\Claire\Desktop\CS3201\demodemo\client.py)
command "3":get string 
command "4":exit (user will need to reconnect the socket again)



