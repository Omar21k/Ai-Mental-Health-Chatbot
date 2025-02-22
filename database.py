import sqlite3 as sq
from datetime import datetime as dt 

def create_database(): 
    con = sq.connect("conversations.db") 
    cur = con.cursor() 
    table = '''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date TEXT NOT NULL,
            messages TEXT NOT NULL
        )
    '''
    cur.execute(table) #If the table doesn't exist this makes one  
    con.commit()
    con.close()