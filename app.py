from flask import Flask, render_template

from models.bookModel import Book

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('base.html')

@app.route("/books/<int:page>-<int:limit>")
def book_list(page=None, limit=None):
    books =  Book.all(limit=limit, offset=page*limit-limit)

    return render_template('book-list.html', books = books, p=page, l=limit)
    


if __name__ == "__main__":
    app.run(debug=True)