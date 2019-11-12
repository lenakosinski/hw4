from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'

class DogForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    breed = StringField('Breed:', validators=[DataRequired()])
    color = StringField('Color:', validators=[DataRequired()])
    age = StringField('Age:', validators=[DataRequired()])


@app.route('/')
def index():
    return render_template('index.html', pageTitle='Dogs of Iowa City')

@app.route('/add', methods=['GET', 'POST'])
def add_dog():
    form = DogForm()
    if form.validate_on_submit():
        return "This {0} year-old {1} {2} is named {3}".format(form.age.data,form.color.data,form.breed.data,form.name.data)


    return render_template('add_dog.html', form=form, pageTitle='Add A New Dog')

if __name__ == '__main__':
    app.run(debug=True)
