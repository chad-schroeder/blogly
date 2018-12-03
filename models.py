"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True)

    posts = db.relationship("Post", backref="user")

    def __repr__(self):
        """Show info for user."""

        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>"


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    post_tags = db.relationship('PostTag', backref="post")

    def __repr__(self):
        """Show info for user."""

        return f"<Post id={self.id}, Post title={self.title}, content={self.content}, created at={self.created_at} user_id={self.user_id}>"


class Tag(db.Model):
    """Posts tags."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    post_tags = db.relationship("PostTag", backref="tag")

    def __repr__(self):
        """Show tag."""

        return f"<Tag id={self.id}, name={self.name}>"


class PostTag(db.Model):
    """Posts tags (joins a Post and a Tag)."""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        """Show PostTag."""

        return f"<PostTag post_id={self.post_id}, tag_id={self.tag_id}>"