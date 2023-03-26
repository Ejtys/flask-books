from flask import Flask, render_template, request, redirect, url_for

from models.bookModel import Book

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('base.html/')

@app.route("/books/<int:page>-<int:limit>/")
def book_list(page=None, limit=None):
    books =  Book.all(limit=limit, offset=page*limit-limit)
    categories = Book.all_categories()

    return render_template('book-list.html', books = books, p=page, l=limit, genders = categories)

@app.route("/books/delete/", methods=['POST'])
def delete_book():
    id = request.form.get("book_id")
    book = Book.from_id(id)
    book.delete()

    p = request.form.get("page")
    l = request.form.get("limit")
    return redirect(url_for('book_list', page = p, limit = l))

@app.route("/books/add/", methods=['POST'])
def add_book():
    title = request.form.get("title")
    price = request.form.get("price")
    gender = request.form.get("gender")
    description = request.form.get("description")
    if title and price and gender and description  and Book.is_title_unique(title):
        book = Book(title,  float(price) * 100, description, gender)


    p = request.form.get("page")
    l = request.form.get("limit")
    return redirect(url_for('book_list', page = p, limit = l))

@app.route("/books/update/", methods=['POST'])
def update_book():
    id = request.form.get("book_id")
    title = request.form.get("title")
    price = request.form.get("price")
    gender = request.form.get("gender")
    description = request.form.get("description")
    book = Book.from_id(id)
    if book and (Book.is_title_unique(title) or title == book.title):
        book.title = title
        book.price_cents = int(float(price) * 100)
        book.category = gender
        book.description = description
        book.save()

    p = request.form.get("page")
    l = request.form.get("limit")
    return redirect(url_for('book_list', page = p, limit = l))

if __name__ == "__main__":
    app.run(debug=True)