import unittest
from unittest.mock import patch, MagicMock
import bcrypt
from login import authenticate_user

class TestLoginFunctions(unittest.TestCase):

    @patch('login.cursor')
    def test_authenticate_user_success(self, mock_cursor):
        print("\nRunning test_authenticate_user_success")
        mock_cursor.fetchone.return_value = [b'$2b$12$somehashedpassword']
        with patch('bcrypt.checkpw', return_value=True):
            with patch('builtins.print') as mock_print:
                authenticate_user('test_user', 'password123')
                mock_cursor.execute.assert_called_once_with(
                    "SELECT password_hash FROM users WHERE username = %s", 
                    ('test_user',)
                )
                mock_print.assert_called_once_with("Login successful")

    @patch('login.cursor')
    def test_authenticate_user_wrong_password(self, mock_cursor):
        print("\nRunning test_authenticate_user_wrong_password")
        mock_cursor.fetchone.return_value = [b'$2b$12$somehashedpassword']
        with patch('bcrypt.checkpw', return_value=False):
            authenticate_user('test_user', 'wrongpassword')
            with patch('builtins.print') as mock_print:
                authenticate_user('test_user', 'wrongpassword')
                mock_print.assert_called_once_with("Incorrect password")

    @patch('login.cursor')
    def test_authenticate_user_username_not_found(self, mock_cursor):
        
        mock_cursor.fetchone.return_value = None
        print("testing unkown user")
        authenticate_user('unknown_user', 'password123')
        with patch('builtins.print') as mock_print:
            
            authenticate_user('unknown_user', 'password123')
            mock_print.assert_called_once_with("Username not found")

if __name__ == '__main__':
    unittest.main()
