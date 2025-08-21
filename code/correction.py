import os
from dotenv import load_dotenv
load_dotenv()

"""
export find_errors, crc_encode
"""

generator = str(os.getenv("GENERATOR"))

def xor(dividend, divisor):
    """
    returns bitwise XOR of two binary strings
    """
    result = []
    for i in range(1, len(divisor)):
        if dividend[i] == divisor[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def mod2div(dividend, divisor):
    """
    returns remainder between 2 arguments
    """
    # Number of bits to be XORed at a time
    pick = len(divisor)
    # Slicing the dividend to get the portion that matches the length of the divisor
    tmp = dividend[0:pick]
    while pick < len(dividend):
        if tmp[0] == '1':
            # Replace the dividend by the result of XOR and pull down the next bit
            tmp = xor(tmp, divisor) + dividend[pick]
        else:
            # If the first bit is '0', we XOR with '0...0' (equivalent to just appending the next bit)
            tmp = xor(tmp, '0' * len(divisor)) + dividend[pick]
        # Increment pick to move the window forward
        pick += 1
    
    # For the last n bits, we need to XOR with the divisor
    if tmp[0] == '1':
        tmp = xor(tmp, divisor)
    else:
        tmp = xor(tmp, '0' * len(divisor))
    
    return tmp

def crc_encode(data):
    """
    returns the codeword after appending the CRC remainder
    """
    global generator
    # Append zeros to the data string, length of generator minus 1
    appended_data = data + '0' * (len(generator) - 1)
    # Perform division and get the CRC remainder
    remainder = mod2div(appended_data, generator)
    # The final CRC is the remainder of the division
    crc = remainder
    return data + crc

def crc_judge(codeword):
    """
    returns True if codeword is valid, False otherwise
    """
    global generator
    remainder = mod2div(codeword, generator)
    return remainder == '0' * (len(generator) - 1)

def flip(code_word, index):
    """
    flips the bit at index in code_word
    """
    code_word = list(code_word)
    code_word[index] = '1' if code_word[index] == '0' else '0'
    return ''.join(code_word)

def find_errors(code_word, error_support = 3):
    """
    tries to find error indices if error is present
    returns corrected codeword if found else None
    """
    global generator
    word = code_word
    print("codeword: ",code_word)
    for i in range((len(word)+1) ** error_support):
        for x in range(error_support):
            index_to_flip = int((i / (len(word)+1)**x) % (len(word) + 1))-1
            if  index_to_flip >=  0:
                word = flip(word, index_to_flip)

        if crc_judge(word):
            return word
        
        for x in range(error_support):
            index_to_flip = int((i / (len(word)+1)**x) % (len(word) + 1))-1
            if  index_to_flip >= 0:
                word = flip(word, index_to_flip)

    return None
