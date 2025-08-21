import numpy as np
import pyaudio, os
from dotenv import load_dotenv
load_dotenv()
from time import sleep

def generate_cosine_wave(frequency=700, duration=float(os.getenv("PBIT_DURATION")), volume=1 , sample_rate=44100, phase=0):
    """
    Generates a cosine wave with a specified phase shift.
    :param frequency: Frequency of the cosine wave in Hertz.
    :param duration: Duration of the sound in seconds.
    :param volume: Volume of the sound (0.0 to 1.0).
    :param sample_rate: Sampling rate in samples per second.
    :param phase: Phase shift in radians (0 to 2π).
    :return: Numpy array of samples.
    """
    # Generate time points
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate cosine wave with phase shift
    samples = volume * np.cos(2 * np.pi * frequency * t + phase)

    return samples

def play_sound(p, samples, sample_rate=44100):
    """
    Plays the given samples using PyAudio.

    :param p: PyAudio object.
    :param samples: Numpy array of samples to play.
    :param sample_rate: Sampling rate in samples per second.
    """
    # Convert to 16-bit data
    samples = (samples * 32767).astype(np.int16).tobytes()

    # Open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    output=True)

    # Play sound
    stream.write(samples)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

def play(bitstring):
    p = pyaudio.PyAudio()
    n = len(bitstring)
    combined_samples = np.array([])  # Initialize an empty array for combining samples
    a=0

    # Generate and combine the samples for each bit pair
    print("Playing sound")
    print(bitstring)
    samples = None
    play_sound(p, generate_cosine_wave(frequency=int(os.getenv("start_frequency")),duration=2))
    for i in range(0, n,2):
        a+=1
        if bitstring[i:i+2] == '00':
            print("Generating  00")
            samples = generate_cosine_wave(frequency=int(os.getenv("FREQ_00")),duration=float(os.getenv("PBIT_DURATION")))
        elif bitstring[i:i+2] == '01':
            print("Generating  01")
            samples = generate_cosine_wave(frequency=int(os.getenv("FREQ_01")),duration=float(os.getenv("PBIT_DURATION")))
        elif bitstring[i:i+2] == '10':
            print("Generating  10")
            samples = generate_cosine_wave(frequency=int(os.getenv("FREQ_10")),duration=float(os.getenv("PBIT_DURATION")))
        elif bitstring[i:i+2] == '11':
            print("Generating  11")
            samples = generate_cosine_wave(frequency=int(os.getenv("FREQ_11")),duration=float(os.getenv("PBIT_DURATION")))
        elif bitstring[i:i+2] == '0':
            print("Generating  0")
            samples = generate_cosine_wave(frequency=int(os.getenv("FREQ_0")),duration=float(os.getenv("PBIT_DURATION")))
        elif bitstring[i:i+2] == '1':
            print("Generating  1")
            samples = generate_cosine_wave(frequency=int(os.getenv("FREQ_1")),duration=float(os.getenv("PBIT_DURATION")))
        # Concatenate the current samples to the combined array
        combined_samples = np.concatenate((combined_samples, samples))
        combined_samples = np.concatenate((combined_samples, generate_cosine_wave(frequency=int(os.getenv("zero")), duration=float(os.getenv("zero_dur")))))
        # samples = generate_cosine_wave(frequency=int(os.getenv("zero")),duration=float(os.getenv("zero_dur")))
        # combined_samples = np.concatenate((combined_samples, samples))
    play_sound(p, combined_samples)
    play_sound(p, generate_cosine_wave(frequency=int(os.getenv("stop_frequency")),duration=2))
    
    p.terminate()
