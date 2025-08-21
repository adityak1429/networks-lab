from correction import crc_encode, find_errors, flip
import numpy as np
import os
from play import play
from dotenv import load_dotenv
load_dotenv()

"""
export send_data, decode_audio_data
"""

generator = str(os.getenv("GENERATOR"))

def get_frequency(data, sample_rate=44100):
    """Get the dominant frequency of a block of audio data."""
    # Apply FFT to get frequency content
    fft_result = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(len(data), 1 / sample_rate)
    
    # Get the index of the peak in the FFT result (dominant frequency)
    peak_index = np.argmax(np.abs(fft_result))
    peak_frequency = freqs[peak_index]
    
    return peak_frequency

def send_data(data):
    # Send data to the receiver

    # data = crc_encode(data)

    play(data)

mp = {0:"", 1:"00", 2:"01", 3:"10", 4:"11", 5:"STOP", 6:"NONE", 7:"0", 8:"1"}

freq_00 = int(os.getenv("FREQ_00"))

freq_01 = int(os.getenv("FREQ_01"))

freq_10 = int(os.getenv("FREQ_10"))

freq_11 = int(os.getenv("FREQ_11"))

freq_0 = int(os.getenv("FREQ_0"))

freq_1 = int(os.getenv("FREQ_1"))

freq_tol = int(os.getenv("FREQ_TOL"))

freq_start = int(os.getenv("start_frequency"))

freq_stop = int(os.getenv("stop_frequency"))

def majority_vote(freqs):
    global mp, freq_00,freq_01,freq_10,freq_11,freq_tol,freq_start,freq_stop
    arr = [0]*9
    for freq in freqs: 
        if abs(freq - freq_00)<freq_tol:
            arr[1]+=1
        elif abs(freq - freq_01)<freq_tol:
            arr[2]+=1
        elif abs(freq - freq_10)<freq_tol:
            arr[3]+=1
        elif abs(freq - freq_11)<freq_tol:
            arr[4]+=1
        elif abs(freq - freq_stop)<freq_tol:
            arr[5]+=1
        elif abs(freq - freq_start)<freq_tol:
            arr[0]+=1
        elif abs(freq - freq_0)<freq_tol:
            arr[7]+=1
        elif abs(freq - freq_1)<freq_tol:
            arr[8]+=1
        else:
            arr[6]+=1
    
    k = mp[np.argmax(arr)]
    if max(arr)<5:
        print("took none bro check this")
    
    if k=="NONE" or k=="":
        print("see here none came")
        
    return k


