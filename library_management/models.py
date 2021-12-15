from enum import unique
from library_management import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(4), nullable=False)
    isbn = db.Column(db.String(150), nullable=False)
    publisher = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    rented = db.Column(db.Integer, nullable=False, default=0)
    transactions = db.relationship('Transaction', backref='book', lazy=True)

    def __repr__(self):
        return f"ID: {self.book_id}, Title: {self.title}"

class Member(db.Model):
    __tablename__ = 'member'
    member_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    transactions = db.relationship('Transaction', backref='member', lazy=True)

    def __repr__(self):
        return f"ID: {self.member_id}, Name: {self.name}, Books: {self.transactions}"

class Transaction(db.Model):
    __tablename__='transaction'
    transaction_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.member_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    issued_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dues_per_week = db.Column(db.Integer, nullable=False, default=0)
    amount_paid = db.Column(db.Integer, nullable=False, default=0)
    closed = db.Column(db.Boolean, nullable=False, default=False)