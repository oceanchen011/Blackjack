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

 
def authenticate_user(username, entered_password):
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result:
        stored_hash = result[0]
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
            
        if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash):
            print("Login successful")
        else:
            print("Incorrect password")
    else:
        print("Username not found")

 
authenticate_user("new_user", "secure_password")

 
cursor.close()
db.close()
