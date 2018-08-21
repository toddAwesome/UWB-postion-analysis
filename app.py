import os
import time

import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from flask import Flask, render_template, request, session
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

__author__ = 'Todd Robbins'

app = Flask(__name__)
nameFile = ""

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods=['GET', 'POST'])
def upload():
    target = os.path.join(APP_ROOT, 'csv/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "".join([target, filename])
        print(destination)
        print(filename)
        file.save(destination)
    while not os.path.exists('csv/' + filename):
        time.sleep(1)  # what for files to upload
    for filename in os.listdir('csv/'):
        data_analyzer('csv/' + filename)
    return render_template("complete.html")


def data_analyzer(filename):
    data = pd.read_csv(filename)
    print(data)
    dataType = list(data.columns.values)
    chartID = filename[4:]
    # Dimensions of the data set
    print('Data: {} rows and {} columns'.format(data.shape[0], data.shape[1]))
    if len(dataType) >= 3 and dataType[0] == 'x' and dataType[1] == 'y' and dataType[2] == 'z':
        three_dimension_graph(data, chartID)
    elif dataType[0] == 'x' and dataType[1] == 'y':
        two_dimension_graph(data, chartID)
    else:
        try:
            os.remove('csv/' + filename)
        except OSError:
            pass


@app.route('/2DPositionAnalysis', methods=['GET', 'POST'])
def two_dimension_graph(data, chartID):
    fig, ax = plt.subplots()
    color = 15
    size = 2

    ax.scatter(data['x'], data['y'], c=color, s=500 * size, alpha=0.3)
    ax.grid(color='lightgray', alpha=0.7)
    ax.set_title(chartID + "Scatter Plot", size=20)

    # show graph of data to save/use for reference
    mpld3.show()


@app.route('/3DPositionAnalysis', methods=['GET', 'POST'])
def three_dimension_graph(data, chartID):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['x'], data['y'], data['z'], c='b', marker='o')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    mpld3.show()

    while not os.path.exists('templates/scatterXYZ.html'):
        time.sleep(1)  # what for files to upload


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    session.clear()
    app.run(host='0.0.0.0', port=8080)
