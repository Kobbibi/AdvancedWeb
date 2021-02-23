# from flask import Flask,request,jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:EYHmqn42316@10.100.2.33:5432/CloudDB'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# db = SQLAlchemy(app)

# ma = Marshmallow(app)

# #Staff Class/Model
# class Staffs(db.Model):
#     id = db.Column(db.String(13),primary_key=True,unique=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(25))
#     phone = db.Column(db.String(10))

#     def __init__(self, id, name, email, phone):
#         self.id = id
#         self.name = name
#         self.email = email
#         self.phone = phone

# # Staff Schema
# class StaffSchema(ma.Schema):
#     class Meta:
#         fields =('id', 'name', 'email', 'phone')

# # Init Schema 
# staff_schema = StaffSchema()
# staffs_schema = StaffSchema(many=True)

# # Get All Staffs
# @app.route('/staffs', methods=['GET'])
# def get_staffs():
#     all_staffs = Staffs.query.all()
#     result = staffs_schema.dump(all_staffs)
#     return jsonify(result)

# # Get Single Staff
# @app.route('/staff/<id>', methods=['GET'])
# def get_staff(id):
#     staff = Staffs.query.get(id)
#     return staff_schema.jsonify(staff)

# # Create a Staff
# @app.route('/staff', methods=['POST'])
# def add_staff():
#     id = request.json['id']
#     name = request.json['name']
#     email = request.json['email']
#     phone = request.json['phone']

#     new_staff = Staffs(id, name, email, phone)

#     db.session.add(new_staff)
#     db.session.commit()

#     return staff_schema.jsonify(new_staff)

# # Update a Staff
# @app.route('/staff/<id>', methods=['PUT'])
# def update_staff(id):
#     staff = Staffs.query.get(id)
    
#     name = request.json['name']
#     email = request.json['email']
#     phone = request.json['phone']

#     staff.name = name
#     staff.email = email
#     staff.phone = phone

#     db.session.commit()

#     return staff_schema.jsonify(staff)

# # Delete Staff
# @app.route('/staff/<id>', methods=['DELETE'])
# def delete_staff(id):
#     staff = Staffs.query.get(id)
#     db.session.delete(staff)
#     db.session.commit()
    
#     return staff_schema.jsonify(staff)

# # Web Root Hello
# @app.route('/', methods=['GET'])
# def get():
#     return jsonify({'ms': 'Hello Cloud DB1'})

# # Run Server
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)

from flask import Flask,request,redirect,url_for,render_template
from flask import request
from bson import json_util
from flask_pymongo import MongoClient
import datetime

app = Flask(__name__)
client = MongoClient('mongodb://admin:PNFfys59212@node9139-advweb-01.app.ruk-com.cloud:11122')
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
  return redirect(url_for('get_all'))

# Run Server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
