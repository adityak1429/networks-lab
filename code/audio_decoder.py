import os
from correction import find_errors
from message import message

def get_message(bits):
    bits_messagetype = {
        0 : "RTS" ,
        1 : "CTS" ,
        2 : "CONTENT",
        3 : "ACK"
    }

    # bits=find_errors(bits,error_support=3)

    print("bits",bits)
    if not bits:  # i.e if message is beyond correction
        return message()
    if len(bits) < 6:  # i.e if message is beyond correction
        return message()   
    # bits = bits[:len(bits)-len(str(os.getenv("GENERATOR")))+1]

    print("data", bits)
    
    # initialize obj
    message_object = message()
    message_object.message_type = bits_messagetype[int(bits[:2],2)]
    
    message_object.src = int(bits[2:4],2)
    
    message_object.des = int(bits[4:6],2)
    
    message_object.content = bits[6:]
 
    return message_object
