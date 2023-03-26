from flask import Flask, render_template, request, redirect, url_for

from models.bookModel import Book

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('base.html')

@app.route("/books/<int:page>-<int:limit>")
def book_list(page=None, limit=None):
    books =  Book.all(limit=limit, offset=page*limit-limit)

    return render_template('book-list.html', books = books, p=page, l=limit)

@app.route("/books/delete/", methods=['POST'])
def delete_book():
    id = request.form.get("book_id")
    book = Book.from_id(id)
    print(book.__repr__())
    book.delete()

    p = request.form.get("page")
    l = request.form.get("limit")
    return redirect(url_for('book_list', page = p, limit = l))

if __name__ == "__main__":
    app.run(debug=True)