from requests import get
from flask import Blueprint, render_template, request, redirect, flash, url_for
from library_management import db
from library_management.models import Book
from library_management.books.forms import ImportForm

books = Blueprint("books", __name__)


@books.route('/books')
def all_books():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.book_id.desc()).paginate(page=page, per_page=20)
    return render_template("books.html", title="Books", books=books)

@books.route('/books/import', methods=['GET','POST'])
def import_books():
    import_form = ImportForm()
    if request.method=='POST' and import_form.validate_on_submit():
        title = import_form.title.data
        authors = import_form.authors.data
        isbn = import_form.isbn.data
        publisher = import_form.publisher.data
        number = import_form.number.data
        quantity = import_form.quantity.data
        
        page = 1
        number_of_books_imported = 0
        repeated_books = 0
        while number_of_books_imported != number:
            print(page)
            res = get(f"https://frappe.io/api/method/frappe-library?page={page}&publisher={publisher}&authors={authors}&title={title}&isbn={isbn}")
            data = res.json()
            if not data['message']:
                break
            for book in data['message']:
                temp = Book.query.filter_by(book_id=book['bookID']).first()
                if temp:
                    repeated_books += 1
                    continue
                temp = Book(book_id=book['bookID'], title=book['title'], authors=book['authors'], rating=book['average_rating'], isbn=book['isbn'], publisher=book['publisher'], quantity=quantity)
                db.session.add(temp)
                db.session.commit()
                number_of_books_imported += 1
                if number_of_books_imported == number:
                    break
            page += 1
        msg = f"{number_of_books_imported} out of {number} books have been imported.\n"
        msg_type = 'success'
        if number_of_books_imported != number:
            msgType = 'warning'
            msg += f"{number-number_of_books_imported} books were missing"
        print(msg)
        print(repeated_books)
        flash(msg, msg_type)
        return redirect(url_for('main.home'))
    return render_template('import_books.html', title="Import Books", import_form=import_form)