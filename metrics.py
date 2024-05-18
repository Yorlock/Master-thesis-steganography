from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import os

class metrics_calculator:
    def __init__(self):
        self.sample_array = []
        self.stego_array = []
        self.stego_width = 0
        self.stego_height = 0
        self.stego_mode = ""
        self.hidden_message = ""
        self.algorithm = ""
        self.result_file = open("results.txt", "w")
        self.result_file.write("Name;ET;DT;MSE;PSNR;QI;SSIM;AEC;BPB;ABCPB;DM\n")
        
    
    def setup(self, algorithm, sample_image_path, sample_message_path):
        self.algorithm = algorithm
        sample = Image.open(sample_image_path, 'r')
        self.sample_array = np.array(list(sample.getdata()))
        self.sample_mode = sample.mode
        if sample.mode == 'RGBA':
            self.sample_array = np.delete(self.sample_array, 3, 1)

        stego = Image.open(os.path.join(self.algorithm.algorithm_path_dir, "stego.png"), 'r')
        msg_file = open(sample_message_path,'r')
        self.hidden_message = msg_file.read()
        msg_file.close()

        self.stego_width, self.stego_height = stego.size
        self.stego_array = np.array(list(stego.getdata()))
        self.stego_mode = stego.mode
        if stego.mode == 'RGBA':
            self.stego_array = np.delete(self.stego_array, 3, 1)


    def run(self):
        Name = type(self.algorithm).__name__

        for key, value in self.algorithm.json_content['settings'].items():
            Name += f"_{key}={value}"

        ET = self.algorithm.json_content['milli_sec_elapsed_encode']
        DT = self.algorithm.json_content['milli_sec_elapsed_decode']
        MSE = self.__MSE__()
        PSNR = self.__PSNR__()
        QI = self.__quality_index__()
        SSIM = self.__SSIM__()
        AEC = self.__average_embedding_capacity__()
        BPB = self.__bits_per_byte__()
        ABCPB = self.__average_bits_changed_per_byte__()
        
        #TODO destroy img
        destroyed_image = ""
        DM = 0 #self.__calculate_destroyed_message__(destroyed_image)

        self.result_file.write(f"{Name};{ET};{DT};{MSE};{PSNR};{QI};{SSIM};{AEC};{BPB};{ABCPB};{DM}\n")

    
    def binarize(self):
        pass


    def __MSE__(self):
        return np.mean(np.square(self.sample_array - self.stego_array))


    def __PSNR__(self):
        MSE = np.mean(np.square(self.sample_array - self.stego_array))
        if MSE == 0:
            return np.Inf
        PIXEL_MAX = 255.0
        return 20 * np.log10(PIXEL_MAX) - 10 * np.log10(MSE)  


    #max 1 when identical
    def __quality_index__(self):
        p = self.sample_array.flatten()
        q = self.stego_array.flatten()
        mean_p = p.mean()
        mean_q = q.mean()
        std_p = p.std()
        std_q = q.std()
        x = abs(p - mean_p)*abs(q - mean_q)
        y = np.mean(x)
        return (4*y*mean_p*mean_q)/((std_p**2 + std_q**2)*(mean_p**2 + mean_q**2))


    def __SSIM__(self):
        sample = self.sample_array.flatten()
        stego = self.stego_array.flatten()
        ssim_score = ssim(sample, stego)
        return ssim_score


    def __create_histograms__(self):
        fig, ax = plt.subplots()
        colors = ("red", "green", "blue")
        ax.set_xlim([0, 256])
        for channel_id, color in enumerate(colors):
            histogram, bin_edges = np.histogram(self.sample_array[:, channel_id], bins=256, range=(0, 256))
            ax.plot(bin_edges[0:-1], histogram, color=color)
        fig.savefig("sample_histogram.png")
        
        fig, ax = plt.subplots()
        colors = ("red", "green", "blue")
        ax.set_xlim([0, 256])
        for channel_id, color in enumerate(colors):
            histogram, bin_edges = np.histogram(self.stego_array[:, channel_id], bins=256, range=(0, 256))
            ax.plot(bin_edges[0:-1], histogram, color=color)
        fig.savefig("stego_histogram.png")


    def __destroy_vertical_line__(self, n=10, columns=[], seed=0):
        np.random.seed(seed)
        columns = np.unique(columns)
        if len(columns) > n:
            columns = columns[:n]

        while len(columns) < n:
            columns = list(columns)
            columns.append(np.random.randint(self.stego_width))
            columns = np.unique(columns)

        vertical_damaged_array = self.stego_array

        for column in columns:
            for i in range(self.stego_height):
                vertical_damaged_array[column + i*self.stego_width] = [0, 0, 0]

        if self.stego_mode == "RGBA":
            vertical_damaged_array = np.concatenate((vertical_damaged_array, np.ones((self.stego_height*self.stego_width,1), dtype=int)*255), axis=1)

        vertical_damaged_array = vertical_damaged_array.reshape(self.stego_height, self.stego_width, len(self.stego_mode))
        vertical_damaged_img = Image.fromarray(vertical_damaged_array.astype('uint8'), mode=self.stego_mode)
        vertical_damaged_img.save("damaged_vertical.png")


    def __destroy_horizontal_line__(self, n=10, rows=[], seed=0):
        np.random.seed(seed)
        rows = np.unique(rows)
        if len(rows) > n:
            rows = rows[:n]
            
        while len(rows) < n:
            rows = list(rows)
            rows.append(np.random.randint(self.stego_height))
            rows = np.unique(rows)

        horizontal_damaged_array = self.stego_array

        for row in rows:
            for i in range(self.stego_width):
                horizontal_damaged_array[row*self.stego_width + i] = [0, 0, 0]

        if self.stego_mode == "RGBA":
            horizontal_damaged_array = np.concatenate((horizontal_damaged_array, np.ones((self.stego_height*self.stego_width,1), dtype=int)*255), axis=1)

        horizontal_damaged_array = horizontal_damaged_array.reshape(self.stego_height, self.stego_width, len(self.stego_mode))
        horizontal_damaged_img = Image.fromarray(horizontal_damaged_array.astype('uint8'), mode=self.stego_mode)
        horizontal_damaged_img.save("damaged_horizontal.png")

    # How many bytes have changed
    def __average_embedding_capacity__(self):
        sample = self.sample_array.flatten()
        stego = self.stego_array.flatten()
        difference = sample - stego
        difference_normalized = [1 if x != 0 else 0 for x in difference]
        return sum(difference_normalized)/len(sample)

    # How much bytes have changed
    def __bits_per_byte__(self):
        sample = self.sample_array.flatten()
        stego = self.stego_array.flatten()
        difference = sample - stego
        difference_abs = [abs(x) for x in difference]
        return sum(difference_abs)/len(list(filter(lambda num: num != 0, difference_abs)))

    # How much the 0 and 1 have changed (we are not interested in the final pixel value)
    def __average_bits_changed_per_byte__(self):
        sample = self.sample_array.flatten()
        stego = self.stego_array.flatten()
        difference = np.array([int(x) ^ int(y) for x, y in zip(sample, stego)])
        difference_count = np.array([bin(x)[2:].count('1') for x in difference])
        return sum(difference_count)/len(sample)


    def __calculate_destroyed_message__(self, destroyed_image):
        pass