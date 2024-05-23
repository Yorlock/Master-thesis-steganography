from PIL import Image
import numpy as np
import json
from time import time

from algorithms.steganographyAlgorithm import steganographyAlgorithm
import util

class chain_LSB(steganographyAlgorithm):
    def __init__(self, k=0, end_msg="$t3g0"):
        self.msg_extension = ".txt"
        self.stego_extension = ".png"
        self.is_success = False
        self.k = k
        self.error_msg = ""
        self.end_msg = end_msg
        self.timeout = 10
        self.json_content = {"algorithm":"chain_LSB", "settings": {"k":self.k, "end_msg":self.end_msg}}

    @property
    def is_success(self):
        return self._is_success
    
    @is_success.setter
    def is_success(self, value):
        self._is_success = value

    @property
    def error_msg(self):
        return self._error_msg
    
    @error_msg.setter
    def error_msg(self, value):
        self._error_msg = value

    @property
    def msg_extension(self):
        return self._msg_extension
    
    @msg_extension.setter
    def msg_extension(self, value):
        self._msg_extension = value

    @property
    def stego_extension(self):
        return self._stego_extension
    
    @stego_extension.setter
    def stego_extension(self, value):
        self._stego_extension = value

    @property
    def stego_img_path(self):
        return self._stego_img_path
    
    @stego_img_path.setter
    def stego_img_path(self, value):
        self._stego_img_path = value

    @property
    def destination_path(self):
        return self._destination_path
    
    @destination_path.setter
    def destination_path(self, value):
        self._destination_path = value

    @property
    def algorithm_path_dir(self):
        return self._algorithm_path_dir
    
    @algorithm_path_dir.setter
    def algorithm_path_dir(self, value):
        self._algorithm_path_dir = value

    @property
    def metadata_path(self):
        return self._metadata_path
    
    @metadata_path.setter
    def metadata_path(self, value):
        self._metadata_path = value

    @property
    def json_content(self):
        return self._json_content
    
    @json_content.setter
    def json_content(self, value):
        self._json_content = value

    def reset_params(self):
        self.is_success = False
        self.error_msg = ""

    def encode(self, img_path, msg_path):
        self.algorithm_path_dir = util.get_algorithm_path_dir(self)
        self.stego_img_path = util.get_encode_path(self)
        self.destination_path = util.get_decode_path(self)
        self.metadata_path = util.get_metadata_path(self)
    
        img = Image.open(img_path, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        msg_file = open(msg_path,'r')
        message = msg_file.read()
        msg_file.close()

        start_time = time()

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4
        total_pixels = array.size//n
        
        pointer_length = int(np.ceil(np.log2(total_pixels*3)))
        default_length = int(np.power(2, pointer_length/2) - 1)
        if self.k == 0:
            self.k = default_length
       
        if self.k > len(array):
            self.k = default_length
            self.error_msg += f"The value of parameter k has been changed to {default_length}."

        message += self.end_msg
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_bits = len(b_message)
        req_chunks = int(np.ceil(req_bits/self.k)) #chunks required for msg
        possible_chunks = int(np.floor(((total_pixels*3) - pointer_length)/(pointer_length + self.k))) #possible chunks in image

        if req_chunks > possible_chunks:
            self.is_success = False
            self.error_msg = "ERROR: Need larger file size or larger k."
            return

        array = self.__hide_text__(pointer_length, b_message, req_chunks, possible_chunks, array)
        
        end_time = time()
        milli_sec_elapsed =  int(round((end_time - start_time) * 1000))
        self.json_content["milli_sec_elapsed_encode"] =  milli_sec_elapsed

        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(self.stego_img_path)
        self.is_success = True

    def decode(self, pipe=None, save_to_txt=True):
        if not self.is_success:
            self.error_msg = "Encode failed"
            return

        self.reset_params()
        img = Image.open(self.stego_img_path, 'r')
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB':
            n = 3
        elif img.mode == 'RGBA':
            n = 4
        total_pixels = array.size//n

        pointer_length = int(np.ceil(np.log2(total_pixels*3)))
        b_k = ""
        hidden_bits = ""
        counter = 0
            
        start_time = time()

        for p in range(total_pixels):
            if counter >= pointer_length:
                    break
            for q in range(0, 3):
                b_k += str(array[p][q] %2)
                counter += 1
                if counter >= pointer_length:
                    break
        k = int(b_k, 2)
        p = pointer_length // 3
        q = pointer_length % 3
        while True:                     
            b_next_chunk_position=""
            for i in range(pointer_length):
                b_next_chunk_position += str(array[((p*3)+q+i)//3][(q+i)%3]%2)
            next_chunk_position = int(b_next_chunk_position, 2)
            for i in range(k):
                hidden_bits += str(array[((p*3)+i+q+pointer_length)//3][(q+i+pointer_length)%3]%2)
            p, q = self.__p_and_q_from_chunk__(next_chunk_position)
            if next_chunk_position == 0:
                break

        while len(hidden_bits) % 8 != 0:
            hidden_bits = hidden_bits[:-1]

        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
        
        message = ""        
        for i in range(len(hidden_bits)):
            if message[-len(self.end_msg):] == self.end_msg:
                break
            else:
                message += chr(int(hidden_bits[i], 2))

        if self.end_msg not in message:
            self.is_success = False
            self.error_msg = "No Hidden Message Found\n"
            return

        end_time = time()
        milli_sec_elapsed =  int(round((end_time - start_time) * 1000))
        self.json_content["milli_sec_elapsed_decode"] = milli_sec_elapsed

        message = message[:-len(self.end_msg)]

        with open(self.metadata_path, "w") as f:
            json.dump(self.json_content, f)

        if save_to_txt:
            destination_file = open(self.destination_path, "w")
            destination_file.write(message)
            destination_file.close()

        if pipe is not None:
            pipe.send(message)
            pipe.close()

        self.is_success = True
        return message

    def __hide_text__(self, pointer_length, b_message, req_chunks, possible_chunks, array):
        messages_chunks = self.__split_string_into_substrings__(b_message, self.k)
        chunks_list = range(1, possible_chunks)
        chunks_list_positions = [pointer_length + (el * (pointer_length+self.k)) for el in chunks_list]
        chosen_chunks = np.random.choice(chunks_list_positions, req_chunks-1, replace=False)
        chosen_chunks = [pointer_length] + list(chosen_chunks) + [0]
        counter = 0
        b_k = str(bin(self.k)[2:]).rjust(pointer_length,'0')
        for el in b_k:
            if int(el) == 0:
                array[counter//3][counter%3] = self.__set_to_0__(int(array[counter//3][counter%3]))
            else:
                array[counter//3][counter%3] = self.__set_to_1__(int(array[counter//3][counter%3]))
            counter += 1
        for id, messages_chunk in enumerate(messages_chunks):
            p, q = self.__p_and_q_from_chunk__(chosen_chunks[id])
            next_chunk_position = chosen_chunks[id+1]
            counter = 0
            for el in str(bin(next_chunk_position)[2:]).rjust(pointer_length,'0'):
                if int(el) == 0:
                    array[((p*3)+counter+q)//3][(q+counter)%3] = self.__set_to_0__(int(array[((p*3)+counter+q)//3][(q+counter)%3]))
                else:
                    array[((p*3)+counter+q)//3][(q+counter)%3] = self.__set_to_1__(int(array[((p*3)+counter+q)//3][(q+counter)%3]))
                counter += 1
            for el in messages_chunk:
                if int(el) == 0:
                    array[((p*3)+counter+q)//3][(q+counter)%3] = self.__set_to_0__(int(array[((p*3)+counter+q)//3][(q+counter)%3]))
                else:
                    array[((p*3)+counter+q)//3][(q+counter)%3] = self.__set_to_1__(int(array[((p*3)+counter+q)//3][(q+counter)%3]))
                counter += 1
        return array

    def __set_to_0__(self, num):
        if num % 2 == 0:
            return num
        else:
            return num-1
    
    def __set_to_1__(self, num):
        if num % 2 == 1:
            return num
        else:
            return num+1
    
    def __split_string_into_substrings__(self, string, k):
        substrings = [string[i:i+k] for i in range(0, len(string), k)]
        return substrings
    
    def __p_and_q_from_chunk__(self, chunk):
        p = chunk // 3
        q = chunk % 3
        return p, q
