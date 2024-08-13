import unittest
from unittest.mock import patch, MagicMock
import bcrypt
import mysql.connector
from hash import create_users_table, register_user

class TestHashFunctions(unittest.TestCase):

    @patch('hash.cursor')
    @patch('hash.db')
    def test_create_users_table(self, mock_db, mock_cursor):
        create_users_table()
        expected_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
        mock_cursor.execute.assert_called_once_with(expected_sql)
        mock_db.commit.assert_called_once()

    @patch('hash.cursor')
    @patch('hash.db')
    @patch('bcrypt.gensalt')
    @patch('bcrypt.hashpw')
    def test_register_user(self, mock_hashpw, mock_gensalt, mock_db, mock_cursor):
        mock_gensalt.return_value = b'$2b$12$5pdPLDNf2vkz/PznZCYUt.'

        mock_hashpw.return_value = b'some_hashed_password'

        register_user('test_user', 'password123', 'test@example.com')

        mock_hashpw.assert_called_once_with(b'password123', mock_gensalt.return_value)
        
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
            ('test_user', mock_hashpw.return_value, 'test@example.com')
        )
        mock_db.commit.assert_called_once()

    @patch('hash.cursor')
    def test_register_user_duplicate_error(self, mock_cursor):
        mock_cursor.execute.side_effect = mysql.connector.Error("Duplicate entry")
        with patch('hash.db.rollback') as mock_rollback:
            register_user('test_user', 'password123', 'test@example.com')
            mock_rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
