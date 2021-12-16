from werkzeug.wrappers import response
from library_management import create_app, db
import unittest

app = create_app()
app.config['SECRET_KEY'] = 'test_key'
app.app_context().push()

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()
    
    def test_home_page(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Library Management' in response.data)
    
    def test_books_page(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Books' in response.data)
    
    def test_members_page(self):
        tester = app.test_client(self)
        response = tester.get('/members', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Members' in response.data)
    
    def test_transactions_page(self):
        tester = app.test_client(self)
        response = tester.get('/transactions', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Transactions' in response.data)
    
    def test_reports_page(self):
        tester = app.test_client(self)
        response = tester.get('/reports', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Reports' in response.data)
    
    def test_register_member(self):
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

if __name__ == '__main__':
    unittest.main()