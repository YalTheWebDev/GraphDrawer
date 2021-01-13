from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.templating import render_template
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///graphs.db'
db = SQLAlchemy(app)


class Grapher(db.Model):
    GraphID =  db.Column(db.Integer, primary_key=True)
    GraphXValues = db.Column(db.String(200), nullable=False)
    GraphYValues = db.Column(db.String(200), nullable=False)
    GraphDate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/draw')
def draw_page():
    return render_template('draw.html')

@app.route('/about')
def about_page():
    return "Page Under Construction"

if __name__ == "__main__":
    app.run(debug=True)