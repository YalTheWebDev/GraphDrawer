import io
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.templating import render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///graphs.db'
db = SQLAlchemy(app)


class Grapher(db.Model):
    GraphID =  db.Column(db.Integer, primary_key=True)
    GraphXValues = db.Column(db.String(200), nullable=False)
    GraphYValues = db.Column(db.String(200), nullable=False)
    GraphURI = db.Column(db.String(20), nullable=False)
    GraphDate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/draw', methods=['POST', 'GET'])
def draw_page():
    def create_figure():
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        xs = range(int(request.form['GraphXValues']))
        ys = [np.sin(x) for x in xs]
        axis.plot(xs, ys)
        return fig
    
    if request.method == 'POST':
        fig = create_figure()
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    else:
        return render_template('draw.html')

@app.route('/about')
def about_page():
    return "Page Under Construction"

if __name__ == "__main__":
    app.run(debug=True)
