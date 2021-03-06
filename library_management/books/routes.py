from requests import get
from flask import Blueprint, render_template, request, redirect, flash, url_for
from library_management import db
from library_management.models import Book, Member, Transaction
from library_management.books.forms import EditForm, ImportForm, IssueForm

books = Blueprint("books", __name__)


@books.route('/books')
def all_books():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.book_id.asc()).paginate(page=page, per_page=20)
    return render_template("books.html", title="Books", books=books, data=books.items)

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
            res = get(f"https://frappe.io/api/method/frappe-library?page={page}&publisher={publisher}&authors={authors}&title={title}&isbn={isbn}")
            data = res.json()
            if not data['message']:
                break
            for book in data['message']:
                temp = Book.query.filter_by(book_id=book['bookID']).first()
                if temp:
                    repeated_books += 1
                    # number_of_books_imported += 1
                    # temp.quantity += quantity
                    # db.session.commit()
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
            msg_type = 'warning'
            msg += f"{number-number_of_books_imported} books were missing"
        if repeated_books > 0:
            flash(f'{repeated_books} books were repeated.', 'info')
        flash(msg, msg_type)
        return redirect(url_for('books.all_books'))
    return render_template('import_books.html', title="Import Books", import_form=import_form)


@books.route('/book/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get_or_404(id)
    edit_form = EditForm()
    if request.method == 'POST' and edit_form.validate_on_submit():
        if book.rented > edit_form.quantity.data:
            flash(f'Quantity for book with id {book.book_id} should be more than or equal to {book.rented}', 'warning')
            return redirect(url_for('books.all_books'))
        book.quantity = edit_form.quantity.data
        db.session.commit()
        flash('The book quantity has been updated!', 'success')
        return redirect(url_for('books.all_books'))
    elif request.method == 'GET':
        edit_form.quantity.data = book.quantity
    return render_template('edit_book.html', title=f'Book {book.book_id}', edit_form=edit_form)


@books.route('/books/search', methods=['POST'])
def search():
    query = request.form.get('search')
    books_by_name = Book.query.filter(Book.title.contains(query)).all()
    books_by_author = Book.query.filter(Book.authors.contains(query)).all()
    books = books_by_name + books_by_author
    books = set(books)
    books = list(books)
    books = sorted(books, key=lambda x: x.book_id, reverse=False)
    return render_template('books.html', title=f"Search {query}", data=books)


@books.route('/book/<int:id>/issue', methods=['GET', 'POST'])
def issue_book(id):
    issue_form = IssueForm()
    if request.method == 'POST' and issue_form.validate_on_submit():
        email = issue_form.email.data
        book_id = issue_form.book_id.data
        charges = issue_form.charges.data
        member = Member.query.filter_by(email=email).first()
        if not member:
            flash(f'No member registered with the email {email}. Register Now!', 'danger')
            return redirect(url_for('members.register_member'))
        book = Book.query.get(book_id)
        if not book:
            flash(f'No book available with the id {book_id}.', 'danger')
            return redirect(url_for('books.all_books'))
        if member.outstanding_dues + charges > 500:
            flash('Outstanding debt exceeds INR 500', 'warning')
            return redirect(url_for('transactions.all_transactions'))
        if book.quantity - book.rented < 1:
            flash('Book currently not available to rent', 'warning')
            return redirect(url_for('books.all_books'))
        trans = Transaction(book_id=book.book_id, member_id=member.member_id, charges=charges)
        book.rented += 1
        book.no_of_times_rented += 1
        member.outstanding_dues += charges
        member.rented += 1
        db.session.add(trans)
        db.session.commit()
        flash('Book Issued Successfully', 'success')
        return redirect(url_for('transactions.all_transactions'))
    return render_template('issue.html', issue_form=issue_form, title='Issue Book', id=id)