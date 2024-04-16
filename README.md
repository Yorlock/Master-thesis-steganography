# Master-thesis-steganography

## Steganography algorithms:
- steganographyAlgorythm.py - Abstract class, all stego algorithms inherit from it.
- sample.py - Demo stego algorithm, the simplest LSB implementation.
- LSB_EOM.py - Least Significant Bit - End Of Message. A unique message is added at the end of the message to signal the end of the hidden text. A unique message can be defined by the user. You can also specify how many bits should be used in a single pixel, see parameter k.
- LSB_SOM.py - Least Significant Bit - Size Of Message. The message size is added at the beginning of the message to know how long the hidden text is. The message size occupies n bits equal to the size of the image represented in the following form: 2^n. You can also specify how many bits should be used in a single pixel, see parameter k.
- BPCS.py - Bit-Plane Complexity Segmentation steganography. The embedding operation is to replace the "complex areas" on the bit planes of the vessel image with the confidential data.