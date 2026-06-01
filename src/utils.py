import numpy as np
import cv2

def text_to_binary(text, eof_marker):
    """Convert text + EOF marker to binary string."""
    text += eof_marker
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary_str):
    """Convert binary string to text."""
    chars = []
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def get_dft(img):
    """Apply Discrete Fourier Transform."""
    # Convert image to float32 and apply DFT
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    return dft

def get_idft(dft):
    """Apply Inverse Discrete Fourier Transform."""
    # Convert back to spatial domain
    idft = cv2.idft(dft, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)
    return idft