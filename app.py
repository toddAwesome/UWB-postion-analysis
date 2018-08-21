import os
import time
import urllib
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

from flask import Flask, render_template, request, session

__author__ = 'Todd Robbins'

app = Flask(__name__)
nameFile = ""

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# https://www.youtube.com/watch?v=bxFaa_FNdL4
@app.route('/')
def index():
    return render_template("index.html")


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
        time.sleep(1)  # what for files to upload
    for filename in os.listdir('csv/'):
        data_analyzer('csv/' + filename)
    return render_template("complete.html")


def data_analyzer(filename):
    data = pd.read_csv(filename)
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
    plt.plot(x=data['x'], y=data['y'])
    img = io.BytesIO()
    plt.savefig(img, format='png')  # save figure to the buffer
    img.seek(0)  # rewind your buffer
    plot_data = urllib.quote(base64.b64encode(img.read()).decode())

    # show graph of data to save/use for reference
    return render_template("GraphTwoDimensions.html", plot_url=plot_data)


@app.route('/3DPositionAnalysis', methods=['GET', 'POST'])
def three_dimension_graph(data, chartID):
    return render_template("GraphThreeDimensions.html")


if __name__ == '__main__':
    session.clear()
    app.run(debug=True)
# app.run(host='0.0.0.0', port=8080)
