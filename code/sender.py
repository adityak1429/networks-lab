from message import message
from physical import send_data

def send_message(message_object):
    messagetype_bits = {
    "RTS" : "00" ,
    "CTS" : "01",
    "CONTENT" : "10",
    "ACK" : "11"
    }
    bitstring = ""
    bitstring += str(messagetype_bits[message_object.message_type]).zfill(2)
    bitstring += bin(message_object.src)[2:4].zfill(2)
    bitstring += bin(message_object.des)[2:4].zfill(2)
    bitstring += str(message_object.content)

    send_data(bitstring)

def send_cts(message_heard):
    """
    message_heard is RTS here
    """
    message_object = message()
    message_object.message_type = "CTS"
    message_object.src = message_heard.des
    message_object.des = message_heard.src
    message_object.content = str(message_heard.NAV)
    
    send_message(message_object)

def send_rts(message_heard):
    
    message_object = message()
    message_object.message_type = "RTS"
    message_object.src = message_heard.src
    message_object.des = message_heard.des
    message_object.content = str(bin(message_heard.NAV)[2:])

    send_message(message_object)

def send_content(message):
    send_message(message)

def send_ack(message_heard):
    message_object = message()
    message_object.message_type = "ACK"
    message_object.src = message_heard.des
    message_object.des = message_heard.src
    message_object.content = ""

    send_message(message_object)