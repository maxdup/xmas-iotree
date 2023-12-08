from utils import IOArgParser, JSONFileRead, JSONFileWrite

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import argparse


def plot(coords):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    zs = [c[2] for c in coords]

    ax.scatter(xs, ys, zs, c='r', marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


if __name__ == '__main__':
    args = IOArgParser(
        'Visualize coordinate file',
        'coordinates.json',
        'The filename for you coordinates',
    )

    coords = JSONFileRead(args.input_coords)
    plot(coords)
