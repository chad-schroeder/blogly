"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

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
def add_user():
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
def new_user_form():
    """Form to add user."""

    return render_template('/user-add.html')


@app.route('/users/<int:user_id>')
def display_user(user_id):
    """Show user details."""

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template('/user-detail.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Edit user details form."""

    user = User.query.get_or_404(user_id)
    return render_template('/user-edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edit user details form."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url', None)

    db.session.add(user)
    db.session.commit()

    return redirect('/users', code=302)


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from database."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users', code=302)


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """New post form."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('/posts-form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts', methods=['POST'])
def add_new_post(user_id):
    """Add new post to database."""

    title = request.form.get('post_title')
    content = request.form.get('post_content')

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}', code=302)


@app.route('/posts/<int:post_id>')
def show_a_post(post_id):
    """Show an individual post"""

    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('post-details.html', post=post, user=user)


@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Show the edit post form"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts-edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handle the edit of a post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form.get('post_title')
    post.content = request.form.get('post_content')

    db.session.add(post)
    db.session.commit()
    return redirect(f'posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete individual post"""

    post = Post.query.get_or_404(post_id)
    user = post.user
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/tags')
def list_tags():
    """Show list of available tags"""

    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_indiv_tag_detail(tag_id):
    """Show detail page for individual tag"""

    tag = Tag.query.get(tag_id)
    return render_template('tag-show.html', tag=tag)


@app.route('/tags/new')
def show_new_tag_form():
    """Show the form to add a new tag"""

    return render_template('tag-form.html')


@app.route('/tags', methods=['POST'])
def process_add_tag_form():
    """Proccess the add tag form and update database"""

    name = request.form.get('tag_name')

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def show_edit_form_for_tag(tag_id):
    """Show the edit form for a tag"""

    tag = Tag.query.get(tag_id)
    return render_template('tag-edit.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def process_edit_tag_form(tag_id):
    """Process the edit tag form and update the database"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form.get('tag_name')

    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')