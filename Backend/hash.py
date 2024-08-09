import mysql.connector
import bcrypt

 
db = mysql.connector.connect(
    host="localhost",
    user="test",
    password="test",
    auth_plugin='mysql_native_password',
    database="blackjack"
)

cursor = db.cursor()

 
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

 
def register_user(username, password, email):
     
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
     
    sql = "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)"
    val = (username, hashed_password, email)
    
    try:
        cursor.execute(sql, val)
        db.commit()
        print("User registered successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()

 
create_users_table()

 
register_user("new_user", "secure_password", "user@example.com")

 
cursor.close()
db.close()
