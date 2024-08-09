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

# Function to authenticate a user
def authenticate_user(username, entered_password):
    # Fetch the stored password hash for the given username
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result:
        stored_hash = result[0]
        # Compare the entered password with the stored hash
        if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8')):
            print("Login successful")
        else:
            print("Incorrect password")
    else:
        print("Username not found")

# Example usage
authenticate_user("new_user", "secure_password")

# Close the database connection
cursor.close()
db.close()
