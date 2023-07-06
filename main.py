from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

import db_management as dbm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __repr__(self):
        return f'Your Username : {self.name}'

# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        print('The pass :', user.password)
        # Find user by email entered.
        the_user = dbm.search_user(email)
        if int(the_user[1]) > 0:
            print("Good username")
            # user = User.query.filter_by(email=email).first()
            # Check stored password hash against entered password hashed.
            the_password = dbm.check_password(email)
            print(f"in /login : {the_password[0][0][0]}")
            if int(the_password[1]) > 0:
                if check_password_hash(the_password[0][0][0], password):
                    # if the_password[0][0][0] == password:
                    login_user(user)
                    print("Good password and user : ", user.name)
                    return redirect(url_for('secrets', name=user.name))

    return render_template("login.html")


@app.route('/secrets', methods=["GET", "POST"])
# @login_required
def secrets():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        save = dbm.add_user(name, email, password)
        if save:
            user = User.query.filter_by(email=email).first()
            login_user(user)
            print(user)
            print("Information saved 'secret'")
            information = "You have to login now !"
            return render_template("login.html", information=information)
        else:
            return "Information not saved 'secret'"
    else:
        name = request.args.get('name')
        # print(email)
        return render_template("secrets.html", name=name)


@app.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', filename="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
