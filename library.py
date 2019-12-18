import os

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask import redirect


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "library.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    def __repr__(self):
        return self.title + " " + self.author

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

@app.route("/update_title", methods=["POST"])
def update_title():
    new_title = request.form.get("newtitle")
    old_title = request.form.get("oldtitle")
    book = Book.query.filter_by(title=old_title).first()
    book.title = new_title
    db.session.commit()
    return redirect("/home")

@app.route("/update_author", methods=["POST"])
def update_author():
    new_author = request.form.get("newauthor")
    old_title = request.form.get("title")
    book = Book.query.filter_by(title=old_title).first()
    book.author = new_author
    db.session.commit()
    return redirect("/home")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/home")

@app.route("/home", methods=["GET", "POST"])
def home():
    # if request.form:
    if request.form.get("title") and request.form.get("author"):
        book = Book(title=request.form.get("title"), author=request.form.get("author"))
        db.session.add(book)
        db.session.commit()
        print(request.form)
    books = Book.query.all()
    return render_template("home.html", books=books)

@app.route('/customers', methods=["GET"])
def costumers():
    return render_template("customers.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        login = User.query.filter_by(username=user, password=passw).first()
        if login is not None:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        register = User(username=user, password=passw)
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/')
def welcome():
    return render_template('welcome.html')

if __name__ == "__main__":
    app.run(debug=True)