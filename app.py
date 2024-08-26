from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_paginate import Pagination, get_page_parameter
from flask_migrate import Migrate
from markdown import markdown
import bleach
from bleach_allowlist import markdown_tags, markdown_attrs
import re
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ContentProcessor:
    @staticmethod
    def process_content(raw_content):
        # Convert markdown to HTML
        html_content = markdown(raw_content, extensions=['extra'])
        
        # Sanitize the HTML
        allowed_tags = markdown_tags + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']
        allowed_attrs = markdown_attrs.copy()
        allowed_attrs['a'] = ['href', 'target', 'rel']
        cleaned_html = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs)
        
        return cleaned_html

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raw_content = db.Column(db.Text, nullable=False)
    rendered_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def render_content(self):
        self.rendered_content = ContentProcessor.process_content(self.raw_content)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.render_content()

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user = User.query.filter_by(name=user_name).first()
        if not user:
            user = User(name=user_name)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('feed', user_id=user.id))
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/feed/<int:user_id>', methods=['GET', 'POST'])
def feed(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        content = request.form['content']
        post = Post(raw_content=content, author=user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('feed', user_id=user.id))
    
    page = request.args.get('page', type=int, default=1)
    per_page = 10  # Number of posts per page
    posts_pagination = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'html': render_template('_posts.html', posts=posts_pagination.items, user=user),
            'has_next': posts_pagination.has_next
        })
    
    return render_template('feed.html', user=user, posts=posts_pagination.items, page=page, has_next=posts_pagination.has_next)

@app.route('/like/<int:user_id>/<int:post_id>', methods=['POST'])
def like_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(user_id=user.id, post_id=post.id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        action = 'unliked'
    else:
        new_like = Like(user_id=user.id, post_id=post.id)
        db.session.add(new_like)
        action = 'liked'
    
    db.session.commit()
    return jsonify({'likes': len(post.likes), 'action': action})

@app.route('/comment/<int:user_id>/<int:post_id>', methods=['POST'])
def add_comment(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    comment = Comment(content=content, author=user, post=post)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('feed', user_id=user.id))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts_count = Post.query.filter_by(user_id=user.id).count()
    comments_count = Comment.query.filter_by(user_id=user.id).count()
    likes_given = Like.query.filter_by(user_id=user.id).count()
    likes_received = sum(len(post.likes) for post in user.posts)
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts_count=posts_count, 
                           comments_count=comments_count, likes_given=likes_given, 
                           likes_received=likes_received, posts=posts)

@app.cli.command("update-rendered-content")
def update_rendered_content():
    with app.app_context():
        posts = Post.query.all()
        for post in posts:
            post.render_content()
        db.session.commit()
    print("All posts have been updated.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)