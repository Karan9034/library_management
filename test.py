from library_management import create_app, db
import unittest

app = create_app()
app.config['SECRET_KEY'] = 'test_key'
app.app_context().push()
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.drop_all()
db.create_all()

class AppTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_01_home_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Library Management' in response.data)
    
    def test_02_books_page(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Books' in response.data)

    def test_03_members_page(self):
        tester = app.test_client(self)
        response = tester.get('/members', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Members' in response.data)
    
    def test_04_reports_page(self):
        tester = app.test_client(self)
        response = tester.get('/reports', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Reports' in response.data)
    
    def test_05_transactions_page(self):
        tester = app.test_client(self)
        response = tester.get('/transactions', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Transactions' in response.data)
    
    def test_06_books_import(self):
        tester = app.test_client(self)
        response = tester.post(
            '/books/import',
            data={
                'number': 10,
                'quantity': 5,
                'title': '',
                'authors': '',
                'isbn': '',
                'publisher': ''
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'10 out of 10 books have been imported' , response.data)
    
    def test_07_books_import_repeated(self):
        tester = app.test_client(self)
        response = tester.post(
            '/books/import',
            data={
                'number': 10,
                'quantity': 5,
                'title': '',
                'authors': '',
                'isbn': '',
                'publisher': ''
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'10 books were repeated' , response.data)

    def test_08_books_import_repeated_missing(self):
        tester = app.test_client(self)
        response = tester.post(
            '/books/import',
            data={
                'number': 20,
                'quantity': 5,
                'title': 'Harry Potter',
                'authors': '',
                'isbn': '',
                'publisher': ''
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'2 books were repeated' , response.data)
        self.assertIn(b'10 out of 20 books have been imported.\n10 books were missing' , response.data)
    
    def test_09_member_register(self):
        tester = app.test_client(self)
        response = tester.post(
            '/members/register',
            data={
                'name': 'testuser',
                'email': 'test@user.com'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Member Registered with ID' , response.data)

    def test_10_member_register_exists(self):
        tester = app.test_client(self)
        response = tester.post(
            '/members/register',
            data={
                'name': 'testuser',
                'email': 'test@user.com'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Member already exists' , response.data)

    def test_11_member_register_invalid(self):
        tester = app.test_client(self)
        response = tester.post(
            '/members/register',
            data={
                'name': 'testuser',
                'email': 'testemail'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)
    
    def test_12_member_update(self):
        tester = app.test_client(self)
        response = tester.post(
            '/member/1/edit',
            data={
                'name': 'testuser1',
                'email': 'test@email.com'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The member details have been updated!', response.data)
    
    def test_13_member_update_invalid(self):
        tester = app.test_client(self)
        response = tester.post(
            '/member/1/edit',
            data={
                'name': 'testuser1',
                'email': 'testem.com'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)
    
    def test_14_book_issue_invalid_email(self):
        tester = app.test_client(self)
        response = tester.post(
            '/book/1/issue',
            data={
                'email': 'test@emai.com',
                'book_id': 1,
                'charges': 20
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No member registered with the email test@emai.com. Register Now!', response.data)
    
    def test_15_book_issue_invalid_book(self):
        tester = app.test_client(self)
        response = tester.post(
            '/book/1/issue',
            data={
                'email': 'test@email.com',
                'book_id': 2000,
                'charges': 20
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No book available with the id 2000', response.data)
    
    def test_16_book_issue(self):
        tester = app.test_client(self)
        response = tester.post(
            '/book/1/issue',
            data={
                'email': 'test@email.com',
                'book_id': 1,
                'charges': 20
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Issued Successfully', response.data)
        response = tester.post(
            '/book/1/issue',
            data={
                'email': 'test@email.com',
                'book_id': 1,
                'charges': 20
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Issued Successfully', response.data)

    def test_17_books_update_invalid(self):
        tester = app.test_client(self)
        response = tester.post(
            '/book/1/edit',
            data={
                'quantity': 1,
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Quantity for book with id 1 should be more than or equal to 2' , response.data)
    
    def test_18_books_update(self):
        tester = app.test_client(self)
        response = tester.post(
            '/book/1/edit',
            data={
                'quantity': 2,
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The book quantity has been updated!' , response.data)
    
    def test_19_book_issue_unavailable(self):
        tester = app.test_client(self)
        response = tester.post(
            '/book/1/issue',
            data={
                'email': 'test@email.com',
                'book_id': 1,
                'charges': 20
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book currently not available to rent', response.data)
    
    def test_20_book_issue_failed(self):
        tester = app.test_client(self)
        response = tester.post(
            '/book/1/issue',
            data={
                'email': 'test@email.com',
                'book_id': 2,
                'charges': 480
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Outstanding debt exceeds INR 500', response.data)

    def test_21_transaction_book_return(self):
        tester = app.test_client(self)
        response = tester.post(
            '/transactions/close/1',
            data={
                'amount': 20
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transaction Closed', response.data)
        response = tester.post(
            '/transactions/close/2',
            data={
                'amount': 20
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Transaction Closed', response.data)
    
    def test_22_verify_reports_page(self):
        tester = app.test_client(self)
        response = tester.get('/reports')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Harry Poter', response.data)
        self.assertIn(b'test@email.cm', response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()