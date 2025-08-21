import threading
import queue
import time
import os, sys
import random as rd
from time import sleep 

from audio_decoder import get_message # this
from sender import * # this
from computer import computer # this
from message import message # this
from record import record_audio_and_check_frequency, record_until_end_frequency # this

from dotenv import load_dotenv
load_dotenv()

# Initialize a message queue, this stores all the messages I have to send
message_queue = queue.Queue()

running_status = threading.Event() # states if multiple threads exist currently

# Set the event to indicate that the thread should run
running_status.set()  

MAC = int(os.getenv("MAC"))
start_frequency = float(os.getenv("start_frequency"))
stop_frequency = float(os.getenv("stop_frequency"))
sender_waiting  = False
timestamp = time.time()
rand_wait_time = None

NIC = computer()

#Initialize a dummy instance of message class
message_heard = message()

recording = False  # Flag to indicate whether recording is active

print(int(os.getenv("MAC")))
def listen():
    sys.stdout.flush()
    global running_status, message_heard, timestamp, sender_waiting
    while running_status.is_set():  
        f = record_audio_and_check_frequency( duration=float(os.getenv("CS_DURATION")))
        #This is the ret value of process state
        ret = None
        if abs(f-start_frequency) <= float(os.getenv("FREQ_TOL")):
            print(f"start {start_frequency} detected")
            sender_waiting = False
            bits = record_until_end_frequency(stop_frequency)            
            message_heard = get_message(bits)
        
        elif (ret := NIC.process_state(message_heard)) is not None:
            if ret == "pop":
                if not message_queue.empty():
                    message_queue.get()
            if ret == "ack":
                print("sent ack......")
            message_heard = message()
          
        elif f+float(os.getenv("FREQ_TOL")) <= float(os.getenv("FREQ_00")) or f-float(os.getenv("FREQ_00")) >= float(os.getenv("FREQ_11")):
            print(f"channel free")
            if message_heard.message_type == None:  # this is to check if im currently in sifs time
                if not message_queue.empty():
                    if time.time() > NIC.sender_sleep_ts:
                        if not sender_waiting :
                            sender_waiting = True
                            rand_wait_time = (rd.randint(0,3) * float(os.getenv("SLOT"))) + int(os.getenv("DIFS"))
                            print("waiting for ",rand_wait_time)
                            timestamp = time.time()
                        else:
                            if (time.time() - timestamp) >= rand_wait_time:
                                NIC.send(message_queue.queue[0])
                                if message_queue.queue[0].des == 0 or message_queue.queue[0].des == MAC:
                                    message_queue.get()
                                sender_waiting = False
                    else:
                        sender_waiting = False
        else:
            print(f"cought {f}")
        sleep(0.1)    # for while loop to not go infinite remove later********

def get_input():
    global running_status, MAC
    while running_status.is_set():
        user_input = input()
        if user_input.lower() == 'exit':
            running_status.clear()
            print("Exiting...")
            break
        else:
            message_obj = message()
            print()
            print(f"<You entered: {user_input}>")
            print()
            print('<who do you want to send it to(MAC):>')
            print()
            message_obj.src = MAC
            message_obj.des = int(input())
            message_obj.message_type = "CONTENT"
            print()
            print(f"<sending to {message_obj.des}>")
            print()
            message_obj.content = user_input
            # message_obj.NAV = int(max((len(user_input)) * 5, int((24 + 10 + len(user_input)) * (float(os.getenv("PBIT_DURATION"))) * 2)))
            if message_obj.des == -1:
                message_obj.des = MAC
            print("putting")
            message_queue.put(message_obj)


if __name__ == "__main__":

    listen_thread = threading.Thread(target=listen)  # Adjust the time as needed
    input_thread = threading.Thread(target=get_input)

    # Start the listening thread
    listen_thread.start()
    # Start the input thread
    input_thread.start()

    # Wait for threads to complete
    listen_thread.join()
    input_thread.join()
    # listen()


