from curses import flash
import pandas as pd
from flask import Flask
from flask import jsonify
from flask import request
#from dataframe import df
request = Flask.request_class

#weekly data of covid cases
url = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv"

#initial 
df = pd.read_csv(url)


#instance of flask class
app = Flask(__name__)

## the route decorator will tell flask what url should trigger the function, and the allowed http methods
@app.route("/", methods =["GET","POST"])
def welcome():
    return "hello tiago!"

#print(df)

@app.route("/data/")
def hello2():
    return jsonify(df.to_json(orient ='index'))


#preciso do site do tiago para testar isto,
@app.before_request()
def authenticate(*args, **kwargs):
    if request.args.get("id") != 11223344:
        return "you dont have access"


if __name__ == "__main__":
    #runs the flask aplication
    #host specifies the server we want our aplication to run
    app.run()