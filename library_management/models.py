from library_management import db

books = db.Table('books',
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id')),
    db.Column('member_id', db.Integer, db.ForeignKey('member.member_id'))
)

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(4), nullable=False)
    isbn = db.Column(db.String(150), nullable=False)
    publisher = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"ID: {self.book_id}, Title: {self.title}"

class Member(db.Model):
    __tablename__ = 'member'
    member_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    books = db.relationship("Book", secondary=books, lazy='subquery')
    
    def __repr__(self):
        return f"ID: {self.member_id}, Name: {self.name}, Books: {self.books}"
