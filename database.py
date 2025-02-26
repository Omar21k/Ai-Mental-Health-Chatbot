import sqlite3 as sq
from datetime import datetime as dt 

#creates the database/ checks if there is one 
def create_database(): 
    con = sq.connect("conversations.db") 
    cur = con.cursor() 
    table = '''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date TEXT NOT NULL,
            user_messages TEXT NOT NULL, 
            bot_messages TEXT NOT NULL
        )
    '''
    cur.execute(table) #If the table doesn't exist this makes one  
    con.commit()
    con.close() 

#This will work to insert user conversations
def logger(user_id, user_messages, bot_messages): 
    con = sq.connect("conversations.db") 
    cur = con.cursor() 

    date = dt.now().strftime("%Y-%m-%d %H:%M:%S") #sets the date of the message to when it was sent
    cursor.execute("INSERT INTO conversations (user_id, date, user_messages, bot_messages) VALUES (?,?,?,?)", 
                   (user_id, date, user_messages, bot_messages)) 
    #line 26-28 sets a group of messages (question + bot response) into the database with their time 
    con.commit()
    con.close()  

#This will retrieve a set of messages 
def grabber(user_id): 
    con = sq.connect("conversations.db")
    cur = con.cursor()
    
    cur.execute("SELECT date, conversation FROM conversations WHERE user_id = ? ORDER BY date DESC", (user_id))
    chats = cur.fetchall()
    
    con.close()
    return chats