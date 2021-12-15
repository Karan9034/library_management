from datetime import datetime
from flask import Blueprint, url_for, redirect, render_template, request, flash
from library_management import db
from library_management.models import Book, Member, Transaction
from library_management.transactions.forms import ReturnForm

transactions = Blueprint("transactions", __name__)

@transactions.route('/transactions')
def all_transactions():
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.order_by(Transaction.closed, Transaction.issued_on.desc()).paginate(page=page, per_page=20)
    return render_template("transactions.html", title="Transactions", transactions=transactions, data=transactions.items)


@transactions.route('/transactions/close/<int:id>', methods=['GET', 'POST'])
def return_book(id):
    return_form = ReturnForm()
    transaction = Transaction.query.get_or_404(id)
    if request.method == 'POST' and return_form.validate_on_submit():
        amount = return_form.amount.data
        transaction.amount_paid = amount
        transaction.closed = True
        book = Book.query.get(transaction.book.book_id)
        book.quantity += 1
        book.rented -= 1
        db.session.commit()
        flash('Transaction Closed', 'success')
        return redirect(url_for('transactions.all_transactions'))
    return render_template('return.html', title="Return", return_form=return_form, transaction=transaction, time=datetime.utcnow())

@transactions.route('/transactions/search')
def search():
    query = request.args.get('search')
    members_by_name = Member.query.filter(Member.name.contains(query)).all()
    members_by_email = Member.query.filter(Member.email.contains(query)).all()
    members = members_by_name + members_by_email
    members = set(members)
    members = list(members)
    members = sorted(members, key=lambda x: x.member_id, reverse=False)
    data = []
    for member in members:
        for trans in member.transactions:
            data.append(trans)
    data = sorted(data, key=lambda x: x.issued_on, reverse=True)
    data = sorted(data, key=lambda x: x.closed, reverse=False)
    return render_template('transactions.html', title=f"Search {query}", data=data)