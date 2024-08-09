import mysql.connector
import bcrypt

# Establishing the connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="test",
    password="Test!",
    auth_plugin='mysql_native_password',
    database="blackjack"
)

cursor = db.cursor()

# Function to create the users table if it doesn't exist
def create_users_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    db.commit()

# Function to register a user
def register_user(username, password, email):
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Prepare the SQL query to insert the new user
    sql = "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)"
    val = (username, hashed_password, email)
    
    try:
        cursor.execute(sql, val)
        db.commit()
        print("User registered successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

# Create the users table
create_users_table()

# Example usage
register_user("new_user", "secure_password", "user@example.com")

# Close the database connection
cursor.close()
db.close()
