from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

DATA_FILE = "blog_posts.json"


def save_posts_to_json(posts):
    """Save blog posts to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(posts, file, indent=4)


def load_posts_from_json():
    """Load blog posts from the JSON file."""
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


blog_posts = load_posts_from_json()


@app.route("/")
def index():
    """Display all blog posts on the index page."""
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Display the add-post form and create a new blog post."""
    if request.method == 'POST':
        new_author = request.form.get('author', '').strip()
        new_title = request.form.get('title', '').strip()
        new_content = request.form.get('content', '').strip()

        if not new_author or not new_title or not new_content:
            return "All fields are required", 400

        if blog_posts:
            new_id = max((post["id"] for post in blog_posts), default=0) + 1
        else:
            new_id = 1

        new_post = {
            "id": new_id,
            "author": new_author,
            "title": new_title,
            "content": new_content,
            "likes": 0
        }

        blog_posts.append(new_post)
        save_posts_to_json(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    """Delete a blog post with the specified post ID."""
    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
            break

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """Display and update a blog post with the specified post ID."""
    if request.method == "GET":
        for post in blog_posts:
            if post["id"] == post_id:
                return render_template("update.html", post=post)

    if request.method == "POST":
        for post in blog_posts:
            if post["id"] == post_id:
                post["author"] = request.form["author"]
                post["title"] = request.form["title"]
                post["content"] = request.form["content"]

                return redirect(url_for("index"))

    return "Post not found", 404


@app.route("/like/<int:post_id>", methods=["POST"])
def like(post_id):
    """Increase the like count of a blog post."""
    for post in blog_posts:
        if post["id"] == post_id:
            post["likes"] += 1
            break

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
