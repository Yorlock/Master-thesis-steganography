# Master-thesis-steganography

## Steganography algorithms:
- steganographyAlgorythm.py - Abstract class, all stego algorithms inherit from it.
- sample.py - Demo stego algorithm, the simplest LSB implementation.
- LSB_EOM.py - Least Significant Bit - End Of Message. A unique message is added at the end of the message to signal the end of the hidden text.
- LSB_SOM.py - Least Significant Bit - Size Of Message. The message size is added at the beginning of the message to know how long the hidden text is. The message size occupies n bits equal to the size of the image represented in the following form: 2^n.