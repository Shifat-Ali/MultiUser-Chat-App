from socket import AF_INET, socket, SOCK_STREAM 
from threading import Thread
import datetime
from connection import NewConnection

# GLOBAL costants
HOST = 'localhost'
PORT = 1967
BUFSIZ = 512
ADDR = (HOST, PORT) # my ip address

# GLOBAL variables
connections = []

SERVER = socket(family = AF_INET, type = SOCK_STREAM) # socket object 
# SOCK_STREAM is for TCP protocol
# SOCK_DGRAM is socket type for UDP 

SERVER.bind(ADDR) # binding the server object to address


# create client object that have an IP address and a name
# have dictionary of these client

def broadcast(msg, name):
    """
    send new messages to all client
    param msg: bytes["utf8"]
    param name: str
    return : none
    """
    for connection in connections:
        client = connection.client
        client.send(bytes(name, "utf8") + bytes(": ", "utf8") + msg)




def client_communication(connection):
    """
    Thread to handle messages from a particular client
    params: NewConnection
    return: none
    """
    client = connection.client
    addr = connection.addr
    name = client.recv(BUFSIZ).decode("utf8")
    connection.setName(name)
    msg = bytes(f"{name} has joined the chat!!", "utf8")
    broadcast(msg, name) #broadcast welcome message
    
    run = True
    while run:
        try:
            msg = client.recv(BUFSIZ)  
            print(name, ":", msg.decode("utf8"))
            if msg == bytes("{quit}", "utf8"):
                run = False
                print(f"[DISCONNECTED] {name} disconnected")
                client.close()
                connections.remove(connection)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "") #broadcast {quit} message
                # client.send(bytes("{quit}", "utf8"))
                break
            else:
                broadcast(msg, name)
        except Exception as e:
            print("[EXECPTION]", e)
            break


def wait_for_connection():
    """
    use: wait for new clients to connect to server and start new thread for each client
    param: none
    return: none
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept() # accepts the incoming connection and return socket object and its address
            connection = NewConnection(addr, client) # new client object
            connections.append(connection) # adding it to connections list
            print(f"[CONNECTION] {addr} connected to the server at {datetime.datetime.now()}")
            Thread(target=client_communication, args = (connection,)).start() 
        except Exception as e:
            print("[EXCEPTION]", e) 
            run = False

    print("SERVER Crashed")

if __name__ == "__main__":
    SERVER.listen() # enable server to listen for incoming connections
    print("[STARTED] Waiting for connection...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close() # terminating the server



