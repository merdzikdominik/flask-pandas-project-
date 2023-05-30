from flask import Flask, render_template, session, redirect, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.secret_key = '678396938698796995179695008948'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    if 'username' in session:
        username = session.get('username')
        return render_template('dashboard.html', user=username)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return render_template('registrationError.html')

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username
        return redirect('/')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = user.username
            return redirect('/')

        return render_template('loginError.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out!")

    return redirect('/')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
