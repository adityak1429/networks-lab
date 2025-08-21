import os
from message import message
from sender import *
from dotenv import load_dotenv
import time
from time import sleep

load_dotenv()

class computer:
    def __init__(self):
        #There are 3 possible states base, sender, reciever
        self.mac = int(os.getenv("MAC"))
        self.state = "BASE"
        #If you are in base the following 2 will be None
        #If you are a reciever, then waitingfor_mac will have sender MAC
        self.waitingfor_mac = None
        #If you are a sender, then sendingto_mac will have reciever MAC
        self.sendingto_mac = None
        self.current_pipeline = None
        self.sender_sleep_ts = 0 # this is timestamp after which sender is allowed to send
        self.ts = 0

    def process_state(self, message_heard):
        ret = None
        if message_heard.message_type == "RTS":
            if message_heard.des == self.mac:
                self.state = "RECIEVER"
                self.waitingfor_mac = message_heard.src
                self.sendingto_mac = None
                # sleep(int(os.getenv("SIFS")))
                if time.time() - self.ts > int(os.getenv("SIFS"))  :
                    send_cts(message_heard)
                    self.ts = time.time()

            else:
                print("NAV ...", int(os.getenv("NAV")))
                self.sender_sleep_ts = time.time() + int(os.getenv("NAV"))
                
        elif message_heard.message_type == "CTS":
            if message_heard.des == self.mac:
                self.state = "CTS_REC"
                # sleep(int(os.getenv("SIFS")))
                if time.time() - self.ts > int(os.getenv("SIFS"))  :
                    print("[SENT]: ", self.current_pipeline.content, self.current_pipeline.des, time.time())
                    send_content(self.current_pipeline)
                    self.ts = time.time()
            else:
                print("NAV ...", int(os.getenv("NAV")))
                self.sender_sleep_ts = time.time() + int(os.getenv("NAV"))
        
        elif message_heard.message_type == "CONTENT":
            if message_heard.des == self.mac:
                self.state = "CON_REC"
                print("[RECVD]: ",message_heard.content, message_heard.src, time.time())
                send_ack(message_heard)
                ret = "ack"
            #This is a broadcast
            elif message_heard.des == 0:
                print("[RECVD]: ",message_heard.content, message_heard.src, time.time())
                self.state = "CON_REC"
                ret = "ack"
            else:
                pass

        elif message_heard.message_type == "ACK":
            if message_heard.des == self.mac:
                self.state = "BASE"
                self.current_pipeline = None
                self.waitingfor_mac = None
                self.sendingto_mac = None
                ret = "pop"
            else:
                pass # do nothing

        
        return ret
    
    def send(self,message_obj):
        """
        Depending on state send current message in pipeline(simulate this by a global variable of currently sending message)
        """
        self.current_pipeline = message_obj
        if message_obj.des == 0:
            print("[SENT]: ", message_obj.content, message_obj.des, time.time())
            send_content(message_obj)
        elif message_obj.src == message_obj.des:
            print("[SENT]: ", message_obj.content, -1, time.time())
            send_content(message_obj)
        else:
            send_rts(message_obj)
        

