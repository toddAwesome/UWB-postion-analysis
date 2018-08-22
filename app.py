import os
import time
import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from flask import Flask, render_template, request, session

__author__ = 'Todd Robbins'

app = Flask(__name__)

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
        data = pd.read_csv('csv/' + filename)
        dataType = list(data.columns.values)
        # Dimensions of the data set
        print('Data: {} rows and {} columns'.format(data.shape[0], data.shape[1]))
        if len(dataType) >= 3 and dataType[0] == 'x' and dataType[1] == 'y' and dataType[2] == 'z':
            html_graph = three_dimension_graph(data, filename)
        elif dataType[0] == 'x' and dataType[1] == 'y':
            html_graph = two_dimension_graph(data, filename)
        else:
            try:
                os.remove('csv/' + filename)
            except OSError:
                pass
    return render_template("home.html", {'graph': [html_graph]})


def two_dimension_graph(data, chartID):
    fig, ax = plt.subplots()

    ax.scatter(data['x'], data['y'], c='b', marker='o')
    ax.grid(color='lightgray', alpha=0.7)
    ax.set_title(chartID + "Scatter Plot", size=20)
    # show graph of data to save/use for reference
    return mpld3.fig_to_html(fig)


def three_dimension_graph(data, chartID):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['x'], data['y'], data['z'], c='b', marker='o')
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_zlabel('z axis')
    ax.grid(color='lightgray', alpha=0.7)
    ax.set_title(chartID + "Scatter Plot", size=20)
    return mpld3.fig_to_html(fig)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    session.clear()
    app.run(host='0.0.0.0')
