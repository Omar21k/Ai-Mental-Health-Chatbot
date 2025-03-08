import sqlite3 as sq
from datetime import datetime as dt 
from werkzeug.security import generate_password_hash, check_password_hash

#creates the database/ checks if there is one 
def create_database(): 
    con = sq.connect("conversations.db") 
    cur = con.cursor() 
    #Creates a table for the usernames
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    #If the messages table doesn't exist this makes one  
    cur.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            user_messages TEXT NOT NULL, 
            gpt_response  TEXT NOT NULL 
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''') 

    con.commit()
    con.close() 

#This will work to insert user conversations
def logger(user_id, user_messages, gpt_response): 
    con = sq.connect("conversations.db") 
    cur = con.cursor() 

    date = dt.now().strftime("%Y-%m-%d %H:%M:%S") #sets the date of the message to when it was sent
    cur.execute("INSERT INTO conversations (user_id, date, user_messages, gpt_response) VALUES (?,?,?,?)", 
                   (user_id, date, user_messages, gpt_response)) #inserts the user id, date, user messages, and gpt response into the database
    #line 26-28 sets a group of messages (question + bot response) into the database with their time 
    con.commit()
    con.close()  

#This will retrieve a set of messages 
def grabber(user_id): 
    con = sq.connect("conversations.db")
    cur = con.cursor()
    
    cur.execute("SELECT date, user_messages, gpt_response FROM conversations WHERE user_id = ? ORDER BY date DESC", (user_id))
    chats = cur.fetchall()
    
    con.close() 
    history = "\n".join([f"{date}: {conversation}" for date, conversation in chats])
    return history

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
        return user[0]  # Return user_id if authentication is successful
    return None
    