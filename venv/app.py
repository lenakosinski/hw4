from flask import Flask
from flask import render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class kosinski_dogsapp(db.Model):
    dogId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    breed = db.Column(db.String(255))
    color = db.Column(db.String(255))
    age = db.Column(db.Integer)

    def __repr__(self):
        return "id: {0} | name: {1} | breed: {2} | color: {3} | age: {4}".format(self.dogId, self.name, self.breed, self.color, self.age)

class DogForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    breed = StringField('Breed:', validators=[DataRequired()])
    color = StringField('Color:', validators=[DataRequired()])
    age = StringField('Age:', validators=[DataRequired()])


@app.route('/')
def index():
    all_dogs = kosinski_dogsapp.query.all()
    return render_template('index.html', dogs=all_dogs, pagetitle='Dogs of Iowa City')

@app.route('/add_dog', methods=['GET', 'POST'])
def add_dog():
    form = DogForm()
    if form.validate_on_submit():
        dog = kosinski_dogsapp(name=form.name.data, breed=form.breed.data, color=form.color.data, age=form.age.data)
        db.session.add(dog)
        db.session.commit()
        return redirect ('/')

    return render_template('add_dog.html', form=form, pageTitle='Add A New Dog')

@app.route('/delete_dog/<int:dogId>', methods=['GET','POST'])
def delete_dog(dogId):
    if request.method == 'POST':
        obj = kosinski_dogsapp.query.filter_by(dogId=dogId).first()
        db.session.delete(obj)
        db.session.commit()
        flash('Dog was deleted!')
        return redirect("/")

    else:
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
