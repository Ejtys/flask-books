from flask import Flask, render_template

from models.bookModel import Book

app = Flask(__name__)


@app.route("/")
def home():
    return 'Hello, world!!!'

@app.route("/books/<int:start>-<int:limit>")
def book_list(start=None, limit=None):
    books =  Book.all(limit=limit, offset=start-1)

    return render_template('booklist.html', books = books)
    


if __name__ == "__main__":
    app.run(debug=True)