import os.path
import json
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import resize

# In this exercise task you will implement an image generator. Generator objects in python are defined as having a next function.
# This next function returns the next generated object. In our case it returns the input of a neural network each time it gets called.
# This input consists of a batch of images and its corresponding labels.
class ImageGenerator:
    def __init__(self, file_path, label_path, batch_size, image_size, rotation=False, mirroring=False, shuffle=False):
        # Define all members of your generator class object as global members here.
        # These need to include:
        # the batch size
        # the image size
        # flags for different augmentations and whether the data should be shuffled for each epoch
        # Also depending on the size of your data-set you can consider loading all images into memory here already.
        # The labels are stored in json format and can be directly loaded as dictionary.
        # Note that the file names correspond to the dicts of the label dictionary.
        self.file_path = file_path
        self.label_path = label_path
        self.batch_size = batch_size
        self.image_size = image_size
        self.rotation = rotation
        self.mirroring = mirroring
        self.shuffle = shuffle

        #load json data    
        with open(self.label_path, 'r') as file:
            self.label_data = json.load(file)

        #list for all data files
        self.files = []
        for file in os.listdir(self.file_path):
            self.files.append(file)

        self.epoch = 0
        self.image_index = 0 # position inside the dataset

        #run shuffle if flag true
        if self.shuffle:
            np.random.shuffle(self.files)


        self.class_dict = {0: 'airplane', 1: 'automobile', 2: 'bird', 3: 'cat', 4: 'deer', 5: 'dog', 6: 'frog',
                           7: 'horse', 8: 'ship', 9: 'truck'}

    def next(self):
        # This function creates a batch of images and corresponding labels and returns them.
        # In this context a "batch" of images just means a bunch, say 10 images that are forwarded at once.
        # Note that your amount of total data might not be divisible without remainder with the batch_size.
        # Think about how to handle such cases
        #TODO: implement next method
        #if 1st epoch finishes:    
        if self.image_index >= len(self.files):
            self.epoch += 1
            self.image_index = 0
            if self.shuffle:
                np.random.shuffle(self.files)

        batch = self.files[self.image_index:self.image_index + self.batch_size] #create batches
        # to adjust last batch    
        if len(batch) < self.batch_size:
            remaining_images = self.batch_size - len(batch)
            batch += self.files[:remaining_images]
        images = [] # image array
        labels = [] # label array
        for file in batch:
            img_path = os.path.join(self.file_path,file)
            img = np.load(img_path)
            img_edit = resize(img,(self.image_size[0],self.image_size[1],self.image_size[2]))
            f = file.split('.')[0]
            json_label = self.label_data[f]
            labels.append(json_label)
            if self.rotation or self.mirroring:
                img_edit = self.augment(img_edit)
            images.append(img_edit)    
                
        self.image_index = self.image_index + self.batch_size

        images = np.array(images)  
        labels = np.array(labels)
        return images, labels

    def augment(self,img):
        # this function takes a single image as an input and performs a random transformation
        # (mirroring and/or rotation) on it and outputs the transformed image
        #TODO: implement augmentation function
        if self.rotation:
            rotation = np.random.choice([1,2,3])
            img = np.rot90(img, k=rotation)
        if self.mirroring:
            input_test = np.random.choice([0,1])
            if input_test == 1:
                img = np.fliplr(img)
        return img

    def current_epoch(self):
        current_epoch = self.epoch
        return current_epoch

    def class_name(self, x):
        # This function returns the class name for a specific input
        #TODO: implement class name function
        image_label = self.class_dict[x]
        return image_label
    def show(self):
        # In order to verify that the generator creates batches as required, this functions calls next to get a
        # batch of images and labels and visualizes it.
        #TODO: implement show method
        images, labels = self.next()

        # plt.figure(figsize=(50, 50))
        columns = 3
        for i, image in enumerate(images):
            plt.subplot(len(images) // columns + 1, columns, i+1)
            plt.imshow(image)
            plt.title(self.class_name(labels[i]))
        plt.show()
