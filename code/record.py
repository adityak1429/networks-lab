import pyaudio, sys, os
import numpy as np
from scipy.fft import fft, fftfreq
from physical import get_frequency
from contextlib import redirect_stderr
from physical import majority_vote

def record_audio_and_check_frequency( duration, threshold = 25, rate=44100):
    """
    Records audio for a given duration and checks if the target frequency is present.
    
    :param target_frequency: The frequency to check for (in Hz).
    :param duration: Duration of the audio recording in seconds (default 2 seconds).
    :param threshold: Amplitude threshold to detect the frequency (default 0.05).
    :param rate: The sample rate (default 44100 Hz).
    :return: True if the target frequency is present, otherwise False.
    """
    # Create a null device for suppressing output
    p = pyaudio.PyAudio()
    # Set the parameters for recording
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16  # 16-bit depth
    channels = 1  # Mono audio
    
    # Open the stream
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print(f"Analyzing for ",end="")
    
    # Record audio
    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk,exception_on_overflow=False)
        frames.append(np.frombuffer(data, dtype=np.int16))
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print(f"{duration} seconds...",end="")
    
    # Convert frames to a single numpy array
    audio_data = np.concatenate(frames)
    freq = get_frequency(audio_data)

    return freq
    
import time
num_chunks = int(os.getenv("NUM_CHUNKS"))
def record_until_end_frequency(end_frequency, rate=44100, chunk_duration=float(os.getenv("PBIT_DURATION"))/num_chunks):
    """
    Continuously records audio and stops when the end frequency is detected.
    
    :param end_frequency: The frequency to detect to stop the recording (in Hz).
    :param threshold: Amplitude threshold to detect the frequency (default 0.05).
    :param rate: The sample rate (default 44100 Hz).
    :param chunk_duration: The duration of each recording chunk (default 1 second).
    :return: List of audio frames (each frame is a byte string).
    """

    p = pyaudio.PyAudio()
    # Set the parameters for recording
    chunk = int(rate * chunk_duration)  # Convert chunk duration to samples
    format = pyaudio.paInt16  # 16-bit depth
    channels = 1  # Mono audio
    
    # Open the stream
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    
    print("Recording... (Press Ctrl+C to stop manually)")
    
    ret = [] 
    count = 1
    tic = time.time()
    t=0
    freqs = []  
    while True:
        # Record a chunk of audio
        toc = time.time()
        data = stream.read(chunk)
        tic = time.time()
        freq = get_frequency(np.frombuffer(data, dtype=np.int16))

        # if abs(freq-int(os.getenv("zero")))<int(os.getenv("FREQ_TOL")):
        #     continue

        freqs.append(freq)
        if count<num_chunks:
            count+=1
        else:
            count = 0
            inference = majority_vote(freqs)

            print(f"detected: {inference} ")
            
            if inference == "STOP" :
                print(f'****************{end_frequency} detected stopping now')
                break
            elif inference != "NONE" and inference != "STOP":
                ret.append(inference)
            freqs.clear()
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print(''.join(ret))
    return ''.join(ret)  # Return the list of freqs
