from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

blog_posts = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
    # More blog posts can go here...
]
@app.route("/")
def index():
    # code to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # fill this in the next step
        new_author = request.form.get('author', '')
        new_title = request.form.get('title', '')
        new_content = request.form.get('content', '')

        if blog_posts:
            new_id = max(post['id'] for post in blog_posts) + 1
        else:
            new_id = 1

        new_post = {
            "id": new_id,
            "author": new_author,
            "title": new_title,
            "content": new_content
        }
        blog_posts.append(new_post)

        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    if request.method == 'GET':
        for post in blog_posts:
            if post['id'] == post_id:
                return render_template('update.html', post=post)

    if request.method == 'POST':
        for post in blog_posts:
            if post['id'] == post_id:
                post['title'] = request.form['title']
                post['content'] = request.form['content']
                return redirect(url_for('index'))

    return "Post not found", 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
