import numpy as np
import matplotlib.pyplot as plt

class Checker:
    def __init__(self, resolution, tile_size):
        self.resolution = resolution
        self.tile_size = tile_size
        self.output = None

    def draw(self):
        if self.resolution % (2 * self.tile_size) != 0:
            raise ValueError("Resolution must be divisible by 2 * tile size.")

        black_tile = np.zeros((self.tile_size, self.tile_size), dtype=int)
        white_tile = np.ones((self.tile_size, self.tile_size), dtype=int)
        
        first_row = np.tile(np.hstack((black_tile, white_tile)), (1, self.resolution // (2 * self.tile_size)))
        second_row = np.tile(np.hstack((white_tile, black_tile)), (1, self.resolution // (2 * self.tile_size)))
        
        board = np.vstack((first_row, second_row) * (self.resolution // (2 * self.tile_size)))

        self.output = board
        return self.output.copy()
    
    def show(self):
        plt.imshow(self.output, cmap='gray')
        plt.show()

class Circle:
    def __init__(self,resolution,radius,position):
        self.resolution = resolution
        self.radius = radius
        self.position = position
        self.output = None
    def draw(self):
        x = np.arange(self.resolution)
        y = np.arange(self.resolution)

        xv,yv = np.meshgrid(x,y)

        circle_map = (xv-self.position[0]) **2 + (yv-self.position[1]) **2 <= self.radius **2

        self.output = np.zeros((self.resolution,self.resolution),dtype=int)
        self.output[circle_map] = 1

        return self.output.copy()
    
    def show(self):
        plt.imshow(self.output, cmap='gray')
        plt.show()

class Spectrum:
    def __init__(self,resolution):
        self.resolution = resolution
        self.output = None
    def draw(self):
        resolution = self.resolution

        pixel_array = np.linspace(0, 1, resolution)
        spectrum_pixel_x, spectrum_pixel_y = np.meshgrid(pixel_array, pixel_array)
        
        self.output = np.stack((spectrum_pixel_x, spectrum_pixel_y, 1-spectrum_pixel_x), axis=2)

        return self.output.copy()
    
    def show(self):
        plt.imshow(self.output)
        plt.show()
