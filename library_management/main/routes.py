from flask import Blueprint, render_template
from library_management.models import Book, Member

main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/reports')
def reports():
    books = Book.query.order_by(Book.no_of_times_rented.desc()).all()
    members = Member.query.order_by(Member.total_paid.desc()).all()
    return render_template('reports.html', title="Reports", members=members[:5], books=books[:5])