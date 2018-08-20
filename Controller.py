import html
import pandas as pd
from tkinter.filedialog import askopenfile
import matplotlib.pyplot as plt
import numpy as np
import os
from mpl_toolkits.mplot3d import Axes3D

# read in file
fileCSV = dict(defaultextension='.csv', filetypes=[('CSV file', '*.csv'), ('All files', '*.*')])
file = askopenfile(title='Choose a file', **fileCSV)
data = pd.read_csv(file.name)

# remove name for new .csv file we create
name, ext = os.path.splitext(file.name)

# rows
numRows = data.shape[0]

# columns
numColumns = data.shape[1]

# how many points per leg
criticalPoints = 0

# number of position records per leg
legChunks = 0

# list of ground truths for each direction
turningPointXs = []
turningPointYs = []
turningPointZs = []

# number of legs
LegDirection = []

# Dimensions of the data set
print('Dataset: {} rows and {} columns'.format(data.shape[0], data.shape[1]))
if numColumns == 2:
    print("two dimensions")

    criticalPoints = int(input("How many turning points are there? NOTE: include starting and ending point."))

    chunkSize = int(numRows / (criticalPoints - 1))  # where to place each leg flag

    for i in range(0, criticalPoints):
        turningPointXs.append(int(input("Enter x position")))
        if turningPointXs[i] == turningPointXs[i - 1]:
            LegDirection.append("vertical")
            turningPointXs.remove(i)
        turningPointYs.append(int(input("Enter y position")))
        if turningPointYs[i] == turningPointYs[i - 1]:
            LegDirection.append("horizontal")
            turningPointYs.remove(i)
        else:
            LegDirection.append("angle")
    for direction in LegDirection:
        print(direction)

    data.to_csv(name + "-results.csv", sep=',')
    # two dimensional plot
    plt.scatter(x=data['x'], y=data['y'])
    plt.show()  # show graph of data to save/use for reference
else:
    print("three dimensions")

    # three dimensional plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['x'], data['y'], data['z'], c='b', marker='o')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    plt.show()
