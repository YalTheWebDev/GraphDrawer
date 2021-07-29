import io
from flask import Flask, request, Response
import sqlite3
from sqlite3 import Error
from datetime import datetime
from flask.templating import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/draw', methods=['POST', 'GET'])
def draw_page():
    def create_figure():
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        # Handling different graph types (incomplete)
        xs = range(int(request.form['GraphXValues']))
        compression = int(request.form['DataCompression'])
        compressionAmount = [1000 if compression == 0 else 1000 // (compression * 10)]
        if request.form['GraphYValues'] == 'sin(x)':
            ys = [np.sin(x) for x in xs]
            axis.plot(xs, ys)
        elif 'x' in request.form['GraphYValues'] and '^2' not in request.form['GraphYValues'] and '^3' not in request.form['GraphYValues'] and 'sin' not in request.form['GraphYValues'] and 'cos' not in request.form['GraphYValues'] and 'tan' not in request.form['GraphYValues'] and request.form['GraphYValues'] != '1/x' and request.form['GraphYValues'] != '2^x' and 'x^4' not in request.form['GraphYValues']:
            if '+' in request.form['GraphYValues']:
                values = request.form['GraphYValues'].split('+')
                values = [value.split('x') for value in values]
                values = [values[0][0], values[1][0]]
                print(values)
                ys = [x * values[0] + values[1][0] for x in xs]
                axis.plot(xs, ys)
        elif request.form['GraphYValues'] == 'x^2+2x+24':
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount)
            ys = [x**2+(2*x)+24 for x in xs]
            print(ys)
            axis.plot(xs, ys)
        elif 'x^3' in request.form['GraphYValues'] and 'x^4' not in request.form['GraphYValues'] and 'x^5' not in request.form['GraphYValues'] and 'x^6' not in request.form['GraphYValues'] and 'x^7' not in request.form['GraphYValues']:
            values = request.form['GraphYValues'].split('+')
            values = [value.split('x') for value in values]
            print(values)
            values = [values[0][0], int(values[1][0]), int(values[2][0]), int(values[3][0])]
            print(values)
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            ys = [x**3 + (values[1] * x**2) + (values[2] * x) + values[3] for x in xs]
            axis.plot(xs, ys)
        elif request.form['GraphYValues'] == 'cos(x)':
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            ys = [np.cos(x) for x in xs]
            axis.plot(xs, ys)
        elif request.form['GraphYValues'] == 'tan(x)':
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            ys = [np.tan(x) for x in xs]
            axis.plot(xs, ys)
        elif request.form['GraphYValues'] == '1/x':
            xs = np.linspace(0, int(request.form['GraphXValues']), compressionAmount[0])
            xs = list(xs)
            xs.remove(0)
            ys = [1/x for x in xs]
            axis.plot(xs, ys)
            print(xs, ys)
        elif request.form['GraphYValues'] == '2^x':
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            ys = [2 ** x for x in xs]
            axis.plot(xs, ys)
        elif 'x^4' in request.form['GraphYValues'] and 'x^5' not in request.form['GraphYValues'] and 'x^6' not in request.form['GraphYValues'] and 'x^7' not in request.form['GraphYValues']:
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            values = request.form['GraphYValues'].split('+')
            values = [value.split('x') for value in values]
            print(values)
            ys = [int(values[0][0]) * x**4 + int(values[1][0]) * x**3 + int(values[2][0]) * x**2 + int(values[3][0]) * x + int(values[4][0]) for x in xs]
            axis.plot(xs, ys)
        elif 'x^5' in request.form['GraphYValues'] and 'x^6' not in request.form['GraphYValues'] and 'x^7' not in request.form['GraphYValues']:
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            values = request.form['GraphYValues'].split('+')
            values = [value.split('x') for value in values]
            print(values)
            ys = [int(values[0][0]) * x**5 for x in xs]
            axis.plot(xs, ys)
        elif 'x^6' in request.form['GraphYValues'] and 'x^7' not in request.form['GraphYValues']:
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            values = request.form['GraphYValues'].split('+')
            values = [value.split('x') for value in values]
            print(values)
            ys = [int(values[0][0]) * x**6 + int(values[1][0]) * x**5 + int(values[2][0]) * x**4 + int(values[3][0]) * x**3 + int(values[4][0]) * x**2 + int(values[5][0]) * x + int(values[6][0]) for x in xs]
            axis.plot(xs, ys)
        elif 'x^7' in request.form['GraphYValues']:
            xs = np.linspace(-int(request.form['GraphXValues']), int(request.form['GraphXValues']), compressionAmount[0])
            values = request.form['GraphYValues'].split('+')
            values = [value.split('x') for value in values]
            print(values)
            ys = [int(values[0][0]), int(values[1][0]), int(values[2][0]), int(values[3][0]), int(values[4][0]), int(values[5][0]), int(values[6][0]), int(values[7][0])]
            axis.plot(xs, ys)
        return fig
    
    if request.method == 'POST':
        try:
            fig = create_figure()
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            image = Response(output.getvalue(), mimetype='image/png')
            try:
                connection = sqlite3.connect('graph.db')
                cursor = connection.cursor()
                connection.commit()
            except Error:
                print('Error Connecting To/Modyfing Database.')
            return image
        except:
            return render_template('graph_error.html')
    else:
        return render_template('draw.html')

@app.route('/about')
def about_page():
    return "Page Under Construction"

if __name__ == "__main__":
    app.run(debug=True)
