from app import app, db, Users
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import uuid
import sqlite3
request = Flask.request_class



def signup_user(password,name): 
   #data = request.get_json() 
   hashed_password = generate_password_hash(password, method='sha256')
   new_user = Users(public_id=str(uuid.uuid4()), name=name, password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
#    return jsonify({'message': 'registered successfully'})
   print("user added")




def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except:
        print("dunno")

    return conn
