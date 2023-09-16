from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up before each test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Checks that template is displayed and correct info is in session"""

        with self.client:
            response = self.client.get('/')
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>score:', response.data)
            self.assertIn(b'<p>high score: 0', response.data)
            self.assertIn(b'<p>times played: 0', response.data)

    def test_valid_word(self):
        """Tests if word is valid"""

        with self.client as client:
            with client.session_transaction() as current_session:
                current_session['board'] = [["B", "A", "S", "I", "C"],
                                            ["B", "A", "S", "I", "C"],
                                            ["B", "A", "S", "I", "C"],
                                            ["B", "A", "S", "I", "C"],
                                            ["B", "A", "S", "I", "C"]]
        response = self.client.get('/check-word?word=basic')
        self.assertEqual(response.json['result'], 'ok')

        response = self.client.get('/check-word?word=bass')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Tests if word is invalid on the board"""

        self.client.get('/')
        response = self.client.get('/check-word?word=test')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_invalid_word_in_dict(self):
        """Tests if word is invalid in english"""

        self.client.get('/')
        response = self.client.get('/check-word?word=aloha')
        self.assertEqual(response.json['result'], 'not-word')



