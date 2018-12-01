"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route('/')
def homepage():
    """Homepage."""

    return redirect('/users', code=302)


@app.route('/users')
def show_users():
    """Display a list of users."""

    users = User.query.all()
    return render_template('/user-listing.html', users=users)


@app.route('/users', methods=['POST'])
def add_user_to_database():
    """Add user to database."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url', None)

    user = User(
        first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users', code=302)


@app.route('/users/new')
def add_user_form():
    """Form to add user."""

    return render_template('/user-add.html')


@app.route('/users/<int:user_id>')
def display_user(user_id):
    """Show user details."""

    user = User.query.get(user_id)
    return render_template('/user-detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Edit user details form."""

    user = User.query.get(user_id)
    return render_template('/user-edit.html', user=user)