from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import time
import matplotlib.pyplot as plt
import io
import base64

__author__ = 'Todd Robbins'

app = Flask(__name__)
nameFile = ""

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# https://www.youtube.com/watch?v=bxFaa_FNdL4
@app.route('/')
def index():
    return render_template("upload.html")


@app.route('/', methods=['POST'])
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
        time.sleep(1)
    for filename in os.listdir('csv/'):
        data = pd.read_csv('csv/' + filename)
        dataType = list(data.columns.values)
        # Dimensions of the data set
        # print('Dataset: {} rows and {} columns'.format(data.shape[0], data.shape[1]))
        if len(dataType) == 2 and dataType[0] == 'x' and dataType[1] == 'y':
            nameFile = 'csv/' + filename
            return redirect(url_for('two_dimension_graph'))
        elif len(dataType) == 3 and dataType[0] == 'x' and dataType[1] == 'y' and dataType[2] == 'z':
            return redirect(url_for('three_dimension_graph'))
        else:
            try:
                os.remove('csv/' + filename)
            except OSError:
                pass
    return render_template("complete.html")


@app.route('/2DPositionAnalysis')
def two_dimension_graph():
    #  data = pd.read_csv('csv/')
    #  return data
    return render_template("index.html")


@app.route('/3DPositionAnalysis')
def three_dimension_graph():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
