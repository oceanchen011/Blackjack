from flask import Flask, session, redirect, url_for, request, make_response,jsonify
import os
import hashlib, bcrypt
import mysql.connector
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'   

 
db = mysql.connector.connect(
    host="localhost",
    user="test",
    password="test",
    auth_plugin='mysql_native_password',
    database="blackjack"
)

cursor = db.cursor()

 
def generate_token():
    return hashlib.sha256(os.urandom(60)).hexdigest()

 
def store_session(user_id):
    session_id = str(uuid.uuid4())   
    expires_at = datetime.now() + timedelta(days=1)   
    
     
    sql = "INSERT INTO user_sessions (user_id, session_id, expires_at) VALUES (%s, %s, %s)"
    val = (user_id, session_id, expires_at)
    cursor.execute(sql, val)
    db.commit()
    
    return session_id

 
def validate_session(session_id):
    sql = "SELECT user_id FROM user_sessions WHERE session_id = %s AND expires_at > NOW()"
    cursor.execute(sql, (session_id,))
    result = cursor.fetchone()
    
    if result:
        return result[0]   
    else:
        return None   

 
def delete_session(session_id):
    sql = "DELETE FROM user_sessions WHERE session_id = %s"
    cursor.execute(sql, (session_id,))
    db.commit()

def authenticate_user(username, password):
    print(username)
    print(password)
    sql = "SELECT id, password_hash FROM users WHERE username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    
    if not result:
        return None, "Username not found"
    
    user_id, stored_hash = result
    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return None, "Incorrect password"
    
    return user_id,username, None

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    print(f"Username: {username}, Password: {password}")   

    user_id, username, error = authenticate_user(username, password)

    if error:
         
        return jsonify({"success": False, "message": error}), 401
    
    if request.form.get('remember_me'):
        token = generate_token()
        tokens[user_id] = token   
        
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('remember_token', token, max_age=30*24*60*60, httponly=True)   
        return resp
    
     
    session_id = store_session(user_id)
    session['session_id'] = session_id
    session['username'] = username   

    return redirect(url_for('dashboard'))

 
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'session_id' in session:
        user_id = validate_session(session['session_id'])
        if user_id:
            username = session.get('username')   
            return f'Logged in as {username}'
    
    remember_token = request.cookies.get('remember_token')
    if remember_token:
        for user_id, token in tokens.items():
            if token == remember_token:
                session_id = store_session(user_id)
                session['session_id'] = session_id
                session['username'] = get_username_from_db(user_id)   
                return f'Logged in as {session["username"]}'
    
    return 'You are not logged in!'

 
@app.route('/logout')
def logout():
    if 'session_id' in session:
        delete_session(session['session_id'])
        session.pop('session_id', None)
    
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('remember_token')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
