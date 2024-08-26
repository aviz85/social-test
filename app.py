from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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
        post = Post(content=content, author=user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('feed', user_id=user.id))
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('feed.html', user=user, posts=posts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)