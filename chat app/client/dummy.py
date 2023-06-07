from client import Client
import time
from threading import Thread


c1 = Client('Ted')
c2 = Client('shifat')

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
        
c1.send_message('hello')
time.sleep(5)
c2.send_message("what's up")
time.sleep(5)
c1.send_message("nothing much, bruhh")
time.sleep(5)
c2.send_message("Boring...")
time.sleep(5)

c1.disconnect()
c2.send_message("you gone already?? ok bye!!")
time.sleep(5)
c2.disconnect()