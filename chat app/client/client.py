from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

class Client:
    """
    for communication with server
    """
    HOST = 'localhost'
    PORT = 1967
    ADDR = (HOST, PORT)
    BUFSIZE = 512
    run = True

    def __init__(self, name):
        self.client_socket = socket(family = AF_INET, type = SOCK_STREAM)
        self.client_socket.connect(self.ADDR) 
        self.messages = []
        recieve_thread = Thread(target=self.recieve_messages)
        recieve_thread.start()
        self.send_message(name)
        self.lock = Lock() # lock this thread so that any other thread couldnt acces its data
    
    def recieve_messages(self):
        """
        recieve messages from server
        param :
        return: none
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZE).decode()
                
                #make sure memory access is safe
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION] 3", e)
                break

    def send_message(self,msg):
        """
        send messages to server
        param msg: str
        return: none
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == bytes("{quit}", "utf8"):
            self.client_socket.close()


    def get_messages(self):
        """
        returns a list of str messages
        return: list[str]
        """
        messages_copy = self.messages[:]

        # make sure memory is safe to acces
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy
    
    def disconnect(self):
        self.send_message("{quit}")
    



