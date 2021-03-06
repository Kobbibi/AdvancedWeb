from flask import Flask,request,redirect,url_for,render_template,jsonify
from flask import request
from bson import json_util
# from flask_pymongo import MongoClient
from pymongo import MongoClient
import datetime

app = Flask(__name__)
client = MongoClient('mongodb://admin:PNFfys59212@node9139-advweb-01.app.ruk-com.cloud:27017')
mydb = client['TestDBMongo']
test = mydb['TestMongoNew']

# # Get All Staffs
@app.route('/get_all', methods=['GET', 'POST'])
def get_all():
    # New = mydb.TestMongoNew.aggregator(mydb.aggregator.TestMongoNew, mydb.DataID, ["IDcard"])
    output = test.aggregate(
        [
            {
                "$lookup":
                {
                    "from": "DataID",
                    "localField": "IDcardData",
                    "foreignField": "IDcard",
                    "as": "sum"
                }
            },
            {
                "$unwind":"$sum"
            },
            { "$project" :
              {
                "Name": "$author",
                "Status":"$sum.Status",
                "sum_name" : "sum.new",
              }
            }
        ]
    )
    # for post in mydb.TestMongoNew.find():
    #   output.append({post['author'],post['Phone']})
    return json_util.dumps(output)

# # Get Delete
@app.route('/Delete', methods=['GET', 'POST'])
def Delete():
    ID_card = request.form['Card']
    Delete = { "author" : author }
    mydb.TestMongoNew.find_one_and_delete(Delete)
    return jsonify({"status":"Delete success"})

# # Get Update
@app.route('/Update', methods=['GET', 'POST'])
def Update():
  ID_card = request.form['Card']
  author = request.form['author']
  Phone = request.form['Phone']
  Update = { "author" : author }
  newvalues = { "$set": { "Phone" : Phone  } }
  mydb.TestMongoNew.update_one(Update, newvalues)
  return jsonify({"status":"Update Success"})

@app.route('/insert', methods=['GET', 'POST'])
def insert():
  ID_card = request.form['Card']
  author = request.form['Name']
  Phone = request.form['Phone']
  Address = request.form['Address']
  Date = request.form['Date']
  Status = request.form['Status']
  Data = {"author" : author , "Phone" : Phone , "IDcard" : ID_card}
  DataNew = {"IDcardData" : ID_card , "Address" : Address , "Date" : Date , "Status" : Status}
  record_id = mydb.TestMongoNew.insert_one(Data)
  record_id = mydb.DataID.insert_one(DataNew)
  return jsonify({"status":"Create Success"})

# Web Root Hello
@app.route('/', methods=['GET', 'POST'])
def index():
  return jsonify({'ms': 'Hello Cloud DB1'})

# Run Server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
