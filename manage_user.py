import sqlite3
import re
from datetime import date


DB = "crm.db"
TODAY = date.today()

# connect to our database and insert a new user
def insert_user(user_name, user_mail, user_phone, db=DB, entry_date=TODAY):
    """Create a new user into the users table
    :param user_name:
    :param user_mail:
    :param user_phone:
    :param db:
    :param today:
    :return: user_name, user_mail, user_phone, date
    """
    db_connection = None
    
    try:
        db_connection = sqlite3.connect(db)
        cursor = db_connection.cursor()
     
        print("[*] DB Connection Successful!")
        
        sql = '''INSERT INTO crm(entry_date, user_name, user_mail, user_phone)
              VALUES(?,?,?,?)'''
        
        cursor.execute(sql, (entry_date, user_name, user_mail, user_phone))
        db_connection.commit()
        print("[*] User Inserted!")
        db_connection.close()
        
        return entry_date, user_name, user_mail, user_phone
    
    except ConnectionError as e:
        print(f"[!] DB connection aborted! Error:{e}")
        return f"[!] DB connection aborted! Error:{e}"
    
# extract all users from the users table
def retrieve_all_users(db=DB):
    """Retrieve all users from the users table
    :param db:
    :return: users
    """
    db_connection = None
    
    try:
        db_connection = sqlite3.connect(db)
        cursor = db_connection.cursor()
        
        print("[*] DB Connection Successful!")
        
        sql = '''SELECT rowid, entry_date, user_name, user_mail, user_phone FROM crm'''
            
        cursor.execute(sql)
        users = cursor.fetchall()
        db_connection.commit()
        print("[*] Users Retrieved!")
        db_connection.close()
        
        print(users)
        return users
    
    except ConnectionError as e:
        print(f"[!] DB connection aborted! Error:{e}")
        return f"[!] DB connection aborted! Error:{e}"
    
# extract a specific user from the users table
def retrieve_user(user_name, db=DB):
    """Retrieve one users from the users table
    :param user_name:
    :param db:
    :return: user data
    """
    db_connection = None
    
    try:
        db_connection = sqlite3.connect(db)
        cursor = db_connection.cursor()
        
        print("[*] DB Connection Successful!")
        
        sql = '''SELECT rowid, entry_date, user_name, user_mail, user_phone 
                 FROM crm 
                 WHERE user_name = ?'''
            
        cursor.execute(sql, (user_name,))
        user = cursor.fetchall()
        db_connection.commit()
        db_connection.close()
        
        if user != []:
            print("[*] User Retrieved!")
            user = user
        else:
            print(f"[!] User {user_name} not found")
            user = [f"[!] User {user_name} not found"]
    
        print(user)
        return user
    
    except ConnectionError as e:
        print(f"[!] DB connection aborted! Error:{e}")
        return f"[!] DB connection aborted! Error:{e}"
    
# check formal correctness of user email
def mail_check(email):
    """Check if the email has a valid format
    """
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    
    if (re.search(regex, email)):
        return True
    else:
        return False

# call the functions
if __name__ == '__main__':
    insert_user("dummy_user", "dummy@dummy.com", "1234567890")
    retrieve_all_users()
    retrieve_user("carlo")
