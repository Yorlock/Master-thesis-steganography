# Master-thesis-steganography

## Steganography algorithms:
- steganographyAlgorythm - Abstract class, all stego algorithms inherit from it.
- sample - Demo stego algorithm, the simplest LSB implementation.
- LSB_EOM - Least Significant Bit - End Of Message. A unique message is added at the end of the message to signal the end of the hidden text. A unique message can be defined by the user. You can also specify how many bits should be used in a single pixel, see parameter k.
- LSB_SOM - Least Significant Bit - Size Of Message. The message size is added at the beginning of the message to know how long the hidden text is. The message size occupies n bits equal to the size of the image represented in the following form: 2^n. You can also specify how many bits should be used in a single pixel, see parameter k.
- chain_LSB - chain Least Significant Bit. The message is divided into chunks. Each chunk contains a hidden part of the message and a pointer to the next chunk. The chunks are placed randomly.
- LSB_PF - Least Significant Bit - Password-Filtered. The algorithm is an implementation of the article. The final implementation has been modified. Added end of message text to determine where a hidden message ends. The XOR operation for block = 0 cannot be performed because the wrong bit is written; In this case, we encode as a regular LSB. Mentioned article: The Islam, M. R., Tanni, T. R., Parvin, S., Sultana, M. J., & Siddiqa, A. (2021). A modified LSB image steganography method using filtering algorithm and stream of password. Information Security Journal: A Global Perspective, 30(6), 359–370. https://doi.org/10.1080/19393555.2020.1854902
- LSB_SINE - Least Significant Bit - Sine. The algorithm is an implementation of the article. The final implementation has been modified. Added end of message text to determine where a hidden message ends. The implementation logic of the algorithm has been changed, but the general idea has been kept. Mentioned article: Mahdi, S. A., & Maisa’a, A. K. (2021). An improved method for combine (LSB and MSB) based on color image RGB. Engineering and Technology Journal, 39(01), 231-242. https://doi.org/10.30684/etj.v39i1B.1574
- PVD_8D - Pixel Value Differencing - 8 Directional. The algorithm is an implementation of the article. Mentioned article Swain, G. (2018). Digital image steganography using eight-directional PVD against RS analysis and PDH analysis. Advances in multimedia, 2018. https://doi.org/10.1155/2018/4847098
- QVD_8D - Quotient Value Differencing - 8 Directional. The algorithm is an implementation of the article: Swain, G. (2019). Very high capacity image steganography technique using quotient value differencing and LSB substitution. Arabian Journal for Science and Engineering, 44(4), 2995-3004. https://doi.org/10.1007/s13369-018-3372-2
- n_RMBR - n-Right most Bit Replacement. The algorithm is an implementation of the article: Sahu, A. K., & Swain, G. (2019). A novel n-rightmost bit replacement image steganography technique. 3D Research, 10, 1-18. https://doi.org/10.1007/s13319-018-0211-x
- BF - Bit flipping. The algorithm is an implementation of the article: Sahu, A. K., Swain, G., & Babu, E. S. (2018). Digital image steganography using bit flipping. Cybernetics and Information Technologies, 18(1), 69-80. https://doi.org/10.2478/cait-2018-0006
- BPCS - Bit-Plane Complexity Segmentation steganography. The embedding operation is to replace the "complex areas" on the bit planes of the vessel image with the confidential data.