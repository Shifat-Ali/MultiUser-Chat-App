from client import Client
import time
from threading import Thread

print("enter your name: ")
name = input()
c1 = Client(name)

def update_message():
    msgs = []
    run =True
    while run:
        time.sleep(0.1)
        new_messages = c1.get_messages()
        msgs.extend(new_messages)
        for msg in new_messages:
            print(msg)
            if msg == "{quit}":
                run = False
                break

Thread(target=update_message).start()

while True: 
    msgs = []
    msg = input()
    if msg == "quit":
        c1.disconnect()
        break
    c1.send_message(msg)
