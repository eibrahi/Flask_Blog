from flask import Flask

app = Flask(__name__)

blogbeitraege = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
    # More blog posts can go here...
]


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
