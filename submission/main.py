from pattern import Checker, Circle, Spectrum
import matplotlib.pyplot as plt

def main():
    checker = Checker(resolution=100, tile_size=10)
    circle = Circle(resolution=100, radius=20, position=(50, 50))
    spectrum = Spectrum(resolution=100)

    checker.draw()
    circle.draw()
    spectrum.draw()

    checker.show()
    circle.show()
    spectrum.show()

if __name__ == "__main__":
    main()
