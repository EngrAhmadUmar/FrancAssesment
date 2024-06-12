from flask import Flask, render_template, jsonify, Response, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    posts = []
    
    # Read users from users.json
    with open('./users.json', 'r') as f:
        users_data = json.load(f)
        users = list(users_data.keys())
    
    # If a username is provided, get their posts
    if username:
        with open('./posts.json', 'r') as f:
            posts_data = json.load(f)
            posts = posts_data.get(username, [])
            
            # Sort posts by time in descending order (most recent first)
            posts.sort(key=lambda x: datetime.strptime(x['time'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
            
    return render_template('index.html', username=username, posts=posts, users=users)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1')
