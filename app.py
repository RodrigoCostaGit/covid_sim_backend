import json
import pandas as pd
from flask import Flask, jsonify, make_response,request
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
from functools import wraps
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

#user class where authorized users of the API will be stored.
class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.Integer)
   name = db.Column(db.String(50))
   password = db.Column(db.String(50))
   admin = db.Column(db.Boolean)

#loads Users to table
db.create_all()


# this function will authenticate the token that was given in the login function
## if the header is valid, i will try to decode the token using the secret key saved in the env file
## it will then search the db for a valid public id, if it doesnt find any, it will throa
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


## this function will check if the username is in the database, if it is, it will then compare the given passwork
## with the hashed password stored in the database, if it succeeds, with will give out a unique token based on the user unique
# id, to be used for authentication
## if it fails, it will throw out a error message.
@app.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return make_response('could not verify', 401, {'Authentication': 'login required"'})   
   user = Users.query.filter_by(name=auth.username).first()  
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id}, app.config['SECRET_KEY'], "HS256")
       return jsonify({'token' : token})
   return make_response('could not verify',  401, {'Authentication': '"login required"'})


## the route decorator will tell flask what url should trigger the function, and the allowed http methods

@app.route("/", methods =["GET","POST"])
def welcome():
    return "Send a mail to rodrigoafonsocostawork@gmail.com to request acess to this api"


#returns all the raw data from the weekly dataset
@app.route("/data/",methods =["GET","POST"])
@token_required
def hello2():
    # return jsonify(df.to_json(orient ='index'))
    return df.to_json(orient="index")

#returns a json with a list of the predictions of the sir model.
@app.route("/prediction", methods =["GET"])
def pred():
  return json.dumps(pred_run().tolist())

#returns a json with the date, number of people hospitalized, number of people in intensive care, and deaths
@app.route("/internados",methods =["GET"])
@token_required
def internados(key):
  return df[["data","internados","internados_uci","obitos"]].to_json(orient="index")

#returns a json with the date, and the number of new covid cases daily
@app.route("/casos_diarios",methods =["GET"])
@token_required
def diarios(key):
  cols = df2.columns.difference(["data"])
  # d = (df2.groupby('data')[cols]
  #       .apply(lambda x: x.to_dict('r'))
  #       .reset_index(name='info')
  #       .to_json(orient='records'))
  return df2[["data","confirmados_novos"]].to_json(orient="index")

# @app.route("/vacinados",methods =["GET"])
# @token_required
# def vacinados(key):
#   cols = df2.columns.difference(["data"])
#   return df2[["data","confirmados_novos"]].to_json(orient="index")

@app.route("/get_obitos",methods =["GET"])
@token_required
def diarios(key):
  return df2[["data","obitos","obitos_novos"]].to_json(orient="index")




if __name__ == "__main__":
    #runs the flask aplication
    #host specifies the server we want our aplication to run
    app.run()

