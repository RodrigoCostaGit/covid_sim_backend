import pandas as pd
from flask import Flask, jsonify, make_response,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
from functools import wraps
import datetime
import os 
from dotenv import load_dotenv

load_dotenv()


#weekly data of covid cases
url = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv"

#loads the csv to df
df = pd.read_csv(url)


#instance of flask class
app = Flask(__name__)

 
app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
# app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////database.db"
# app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////projeto final 2022\covid_sim_backend\database.db"
if os.environ.get("id")=="heroku":
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("database_uri")
if os.environ.get("id")=="dev":
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("database_uri")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

 
db = SQLAlchemy(app)

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.Integer)
   name = db.Column(db.String(50))
   password = db.Column(db.String(50))
   admin = db.Column(db.Boolean)

#loads Users to table
db.create_all()

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'token' in request.headers:
        token = request.headers['token']

      if not token:
        return jsonify({'message': 'a valid token is missing'})

      try:
        data = jwt.decode(token, app.config["SECRET_KEY"],algorithms=["HS256"])
        current_user = Users.query.filter_by(public_id=data['public_id']).first()
      except:
        return jsonify({'message': 'token is invalid'})


      return f(current_user, *args, **kwargs)
   return decorator



@app.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
 
   user = Users.query.filter_by(name=auth.username).first()  
   if check_password_hash(user.password, auth.password):
    #    token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
       token = jwt.encode({'public_id' : user.public_id}, app.config['SECRET_KEY'], "HS256")

       return jsonify({'token' : token})
 
   return make_response('could not verify',  401, {'Authentication': '"login required"'})


## the route decorator will tell flask what url should trigger the function, and the allowed http methods

@app.route("/", methods =["GET","POST"])
def welcome():
    return "hello tiago!"

#print(df)

@app.route("/data/",methods =["GET","POST"])
@token_required
def hello2(key):
    return jsonify(df.to_json(orient ='index'))


#preciso do site do tiago para testar isto,
# Authentication decorator



if __name__ == "__main__":
    #runs the flask aplication
    #host specifies the server we want our aplication to run
    app.run()