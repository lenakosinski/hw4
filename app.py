from flask import Flask
from flask import render_template, redirect, flash, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
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
    dogId = IntegerField('Dog ID:')
    name = StringField('Name:', validators=[DataRequired()])
    breed = StringField('Breed:', validators=[DataRequired()])
    color = StringField('Color:', validators=[DataRequired()])
    age = IntegerField('Age:', validators=[DataRequired()])


@app.route('/')
def index():
    all_dogs = kosinski_dogsapp.query.all()
    return render_template('index.html', dogs=all_dogs, pageTitle='Dogs of Iowa City')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = kosinski_dogsapp.query.filter(or_(kosinski_dogsapp.name.like(search))).all()
        return render_template('index.html', dogs=results, pageTitle='Dogs of Iowa City', legend="Search Results")
    else:
        return redirect('/')


@app.route('/add_dog', methods=['GET', 'POST'])
def add_dog():
    form = DogForm()
    if form.validate_on_submit():
        dog = kosinski_dogsapp(name=form.name.data, breed=form.breed.data, color=form.color.data, age=form.age.data)
        db.session.add(dog)
        db.session.commit()
        return redirect ('/')

    return render_template('add_dog.html', form=form, pageTitle='Add A New Dog')

@app.route('/dog/<int:dogId>/delete', methods=['GET','POST'])
def delete_dog(dogId):
    if request.method == 'POST':
        dog = kosinski_dogsapp.query.get_or_404(dogId)
        db.session.delete(dog)
        db.session.commit()
        flash('Dog was deleted!')
        return redirect("/")

    else:
        return redirect("/")

@app.route('/dog/<int:dogId>', methods=['GET','POST'])
def get_dog(dogId):
    dog = kosinski_dogsapp.query.get_or_404(dogId)
    return render_template('dog.html', form=dog, pageTitle='Dog Details', legend="Dog Details")

@app.route('/dog/<int:dogId>/update', methods=['GET','POST'])
def update_dog(dogId):
    dog = kosinski_dogsapp.query.get_or_404(dogId)
    form = DogForm()

    if form.validate_on_submit():
        dog.name = form.name.data
        dog.breed = form.breed.data
        dog.color = form.color.data
        dog.age = form.age.data
        db.session.commit()
        return redirect(url_for('get_dog', dogId=dog.dogId))
    form.dogId.data = dog.dogId
    form.name.data = dog.name
    form.breed.data = dog.breed
    form.color.data = dog.color
    form.age.data = dog.age
    return render_template('update_dog.html', form=form, pageTitle='Update Dog', legend="Update a Dog")

if __name__ == '__main__':
    app.run(debug=True)
