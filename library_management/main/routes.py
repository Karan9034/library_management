from requests import get
from flask import Blueprint, render_template, request
from library_management import db

main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    res = get('https://frappe.io/api/method/frappe-library?title=Harry+Potter')
    if res.status_code != 200:
        return render_template('error.html')
    books = res.json()['message']
    return render_template('home.html', books=books)
