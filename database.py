import sqlite3 as sq
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash

def create_database(): 
    con = sq.connect("conversations.db") 
    cur = con.cursor() 
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL, 
            password  TEXT NOT NULL
        )
    ''')
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

def grabber(username): 
    try:
        con = sq.connect("conversations.db")  
        cur = con.cursor()
        
        cur.execute("""
            SELECT user_message, gpt_response
            FROM conversations
            WHERE user_id = (SELECT user_id FROM users WHERE username = ?)
            ORDER BY date DESC
            LIMIT 15 
        """, (username,)) #Used limit 15 cause might be a lot of text 
        
        conversation = cur.fetchall()
        con.close()
        
        history = "\n".join([f"User: {user_msg}\nBot: {bot_resp}" for user_msg, bot_resp in conversation])
        return history
    
    except Exception as e:
        print(f"Database Error: {e}")
        return []

def register(username, password): 
    con = sq.connect("conversations.db")
    cur = con.cursor() 
    #Registers the user into our new users table 
    try:
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        con.commit()
        return {"success": True, "message": "User registered successfully"} 
    except sq.IntegrityError:
        return False
    finally:
        con.close() 

def verify(username, password): 
    con = sq.connect("conversations.db")
    cur = con.cursor() 
    
    try:
        cur.execute("SELECT user_id, password FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
     
    
        if user and check_password_hash(user[1], password):
            return user[0]  
        return None 
    finally: 
        con.close()
    