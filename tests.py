import pytest
from app import app, db, User, Post, Like
import warnings
from sqlalchemy.exc import SAWarning

warnings.filterwarnings("ignore", category=SAWarning)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'\xd7\x91\xd7\xa8\xd7\x95\xd7\x9b\xd7\x99\xd7\x9d \xd7\x94\xd7\x91\xd7\x90\xd7\x99\xd7\x9d' in response.data  # "ברוכים הבאים" in Hebrew

def test_create_user(client):
    response = client.post('/', data={'user_name': 'Test User'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test User' in response.data

def test_create_post(client):
    with app.app_context():
        # First, create a user
        client.post('/', data={'user_name': 'Test User'}, follow_redirects=True)
        
        # Now, create a post
        user = User.query.filter_by(name='Test User').first()
        response = client.post(f'/feed/{user.id}', data={'content': 'Test post content'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Test post content' in response.data

def test_feed_page(client):
    with app.app_context():
        # Create a user and a post
        client.post('/', data={'user_name': 'Test User'}, follow_redirects=True)
        user = User.query.filter_by(name='Test User').first()
        client.post(f'/feed/{user.id}', data={'content': 'Test post content'}, follow_redirects=True)

        # Check the feed page
        response = client.get(f'/feed/{user.id}')
        assert response.status_code == 200
        assert b'Test User' in response.data
        assert b'Test post content' in response.data

def test_like_post(client):
    with app.app_context():
        # Create a user and a post
        client.post('/', data={'user_name': 'Test User'}, follow_redirects=True)
        user = User.query.filter_by(name='Test User').first()
        client.post(f'/feed/{user.id}', data={'content': 'Test post content'}, follow_redirects=True)
        post = Post.query.filter_by(content='Test post content').first()

        # Like the post
        response = client.post(f'/like/{user.id}/{post.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['likes'] == 1
        assert data['action'] == 'liked'

        # Unlike the post
        response = client.post(f'/like/{user.id}/{post.id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['likes'] == 0
        assert data['action'] == 'unliked'