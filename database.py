import sqlite3 as sq
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash

def create_database(): 
    con = sq.connect("conversations.db") 
    cur = con.cursor('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL, 
            password  TEXT NOT NULL
        )
    ''') 
    cur.excute()
    table = '''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            user_messages TEXT NOT NULL, 
            gpt_response  TEXT NOT NULL
        )
    '''
    cur.execute(table)  
    con.commit()
    con.close()



def logger(user_id, user_message, gpt_response): 
    con = sq.connect("conversations.db") 
    cur = con.cursor() 

    date = dt.now().strftime("%Y-%m-%d %H:%M:%S") #sets the date of the message to when it was sent
    cur.execute("INSERT INTO conversations (user_id, date, user_message, gpt_response) VALUES (?,?,?,?)", 
                   (user_id, date, user_message, gpt_response)) #inserts the user id, date, user messages, and gpt response into the database
    con.commit()
    con.close()  

def grabber(user_id): 
    try:
        con = sqlite3.connect("conversations.db")  
        cur = conn.cursor()
        
        cur.execute("""
            SELECT user_message, bot_response
            FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp ASC
            LIMIT 10  -- You can adjust the limit based on memory constraints
        """, (user_id,))
        
        conversation = cur.fetchall()
        con.close()
        
        # Format the results into a list of dictionaries
        return [{"user_message": row[0], "bot_response": row[1]} for row in conversation]
    
    except Exception as e:
        print(f"Database Error: {e}")
        return []

def register(username, password): 
    con = sq.connect("conversations.db")
    cur = con.cursor() 
    #Registers the user into our new users table 
    try:
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return {"success": True, "message": "User registered successfully"}
    finally:
        conn.close() 

def verify(username, password): 
    con = sq.connect("conversations.db")
    cur = con.cursor() 

    cursor.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        return user[0]  
    return None
    