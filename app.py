import json
import pandas as pd
from flask import Flask, jsonify, make_response,request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
from functools import wraps
import datetime
import os 
from seir_model import pred_run


#weekly data of covid cases
url = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv"

#loads the csv to df
df = pd.read_csv(url)

#daily data covid
url2 = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/dados_diarios.csv"

#loads the csv to df2
df2 = pd.read_csv(url2)

#instance of flask class
app = Flask(__name__)

#vaccine data with 2nd shot data
url3 = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/vacinas.csv"
#loads the csv to df3
df3 = pd.read_csv(url3)

#vaccine data with 1nd shot data
url4 = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/vacinas_detalhe.csv"
df4 = pd.read_csv(url4)


 
app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
# app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////database.db"
# app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////projeto final 2022\covid_sim_backend\database.db"
if os.environ.get("enviro")=="production":
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("database_uri")
else:
    from dotenv import load_dotenv
    load_dotenv()
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
def hello2():
    # return jsonify(df.to_json(orient ='index'))
    return df.to_json(orient="index")


@app.route("/prediction", methods =["GET"])
def pred():
  return json.dumps(pred_run().tolist())


@app.route("/internados",methods =["GET"])
@token_required
def internados(key):
  return df[["data","internados","internados_uci","obitos"]].to_json(orient="index")

@app.route("/casos_diarios",methods =["GET"])
@token_required
def diarios(key):
  return df2[["data","confirmados_novos"]].to_json(orient="index")



@app.route("/get_obitos",methods =["GET"])
@token_required
def obitos(key):
  return df2[["data","obitos","obitos_novos"]].to_json(orient="index")




if __name__ == "__main__":
    #runs the flask aplication
    #host specifies the server we want our aplication to run
    app.run()
