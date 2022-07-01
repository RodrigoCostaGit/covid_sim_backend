import pandas as pd
from flask import Flask
from flask import jsonify
from flask import request
#from dataframe import df

#weekly data of covid cases
url = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data.csv"

#initial 
df = pd.read_csv(url)


#instance of flask class
app = Flask(__name__)

## the route decorator will tell flask what url should trigger the function, and the allowed http methods
@app.route("/hello/", methods =["GET","POST"])
def welcome():
    return "hello world!"

#print(df)

@app.route("/data/")
def hello2():
    return jsonify(df.to_json(orient ='index'))

if __name__ == "__main__":
    #runs the flask aplication
    #host specifies the server we want our aplication to run
    app.run(host="0.0.0.0", port = 105)