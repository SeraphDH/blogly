"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, user, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Blahblah"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """Shows home page"""
    return render_template('/home.html')

@app.route('/users')
def users():
    """show all users"""
    users_list = user.query.order_by(user.last_name, user.first_name).all()
    return render_template('users.html', users=users_list)

@app.route('/users/new', methods = ["GET"])
def get_new_users():
    """Get user form"""
    return render_template('new_user.html')

@app.route('/users/new', methods = ["POST"])
def add_new_user():
    """Add new user"""
    new_user = user(
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        image_url = request.form["image_url"] or None
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show user info"""
    user_info = user.query.get_or_404(user_id)
    return render_template('show_user_info.html', user=user_info)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def edit_user_info(user_id):
    """Edit profile"""
    user_to_edit = user.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user_to_edit)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit(user_id):
    """Submit changes to user info"""
    user_to_edit = user.query.get_or_404(user_id)
    user_to_edit.first_name = request.form["first_name"]
    user_to_edit.last_name = request.form["last_name"]
    user_to_edit.image_url = request.form["image_url"] or None
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user info"""
    user_to_delete = user.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def get_new_post_form(user_id):
    """Show form to add a post for that user."""
    user_info = user.query.get_or_404(user_id)
    return render_template('new_post.html', user_info=user_info)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    user_info = user.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user=user_info)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    post = Post.query.get_or_404(post_id)
    return render_template('show_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def get_edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

# app.run(debug=True)