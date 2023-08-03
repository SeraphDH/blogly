import unittest
from app import app, db
from models import user

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['TESTING'] = True

class FlaskTests(unittest.TestCase):

    def setUp(self):
        """Set up the test client and create a test database."""
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        """Test home page route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shows home page', response.data)

    def test_users(self):
        """Test users route."""
        # Add some test users to the database for testing
        test_user1 = user(first_name='John', last_name='Doe')
        test_user2 = user(first_name='Jane', last_name='Smith')
        with app.app_context():
            db.session.add_all([test_user1, test_user2])
            db.session.commit()

        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John', response.data)
        self.assertIn(b'Jane', response.data)

    def test_add_new_user(self):
        """Test add_new_user route."""
        response = self.client.post('/users/new', data={
            'first_name': 'New',
            'last_name': 'User',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New User', response.data)

    def test_delete_user(self):
        """Test delete_user route."""
        # Add a test user to the database for testing deletion
        test_user = user(first_name='Delete', last_name='Me')
        with app.app_context():
            db.session.add(test_user)
            db.session.commit()

        response = self.client.post(f'/users/{test_user.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Delete Me', response.data)


if __name__ == '__main__':
    unittest.main()
