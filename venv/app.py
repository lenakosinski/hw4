from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'



@app.route('/')
def index():
    return render_template('index.html', pageTitle='Dogs of Iowa City')


if __name__ == '__main__':
    app.run(debug=True)
