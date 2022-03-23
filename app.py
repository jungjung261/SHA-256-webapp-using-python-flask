from flask import Flask,render_template,request,redirect,url_for,jsonify
import os
import time
from sha256 import SHA256
from Salt import Salt
from flask_sqlalchemy import SQLAlchemy


PEOPLE_FOLDER = os.path.join('static')
app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Create db model
class Pass(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    plain = db.Column(db.Text)
    hash = db.Column(db.Text)
    hashsalt = db.Column(db.Text)
    salt = db.Column(db.LargeBinary)
    
    

@app.route("/")
def index():
    return render_template("index.html", reload = time.time())

@app.route("/hash")
def hash():
    plain = request.args.get('texttohash','')
    hashcode = SHA256()
    hashcode.update(plain.encode('ascii'))
    hashgen = hashcode.hexdigest()
    saltvalue = salting()
    hashsalt = SHA256()
    hashsalt.update((plain).encode('ascii')+saltvalue)
    hashwithsaltgen = hashsalt.hexdigest()
    storehash = Pass(plain=plain,hash=hashgen,hashsalt=hashwithsaltgen,salt=saltvalue)
    try:
        db.session.add(storehash)
        db.session.commit()
    except:
        UnsuccessException = "There was a problem storing text."
    return jsonify({
        "hash"        : hashgen,
        "hashsalt":hashwithsaltgen
    })

#Salt generate
def salting():
    salt = Salt()
    saltValue = salt.getsalt()
    return saltValue

@app.route("/decode")
def decode():
    response = 'False'
    plain = request.args.get('texttotest','')
    hashtext = request.args.get('hashtotest','')
    testhash = SHA256()
    testhash.update(plain.encode('ascii'))
    testgen = testhash.hexdigest()
    if(testgen == hashtext):
        response = "True"
    return jsonify({
        "response"        :  response,
        "hashcode" : testgen
    })
    
@app.route("/decodesalt")
def decodesalt():
    response = 'False'
    plain = request.args.get('texttotest','')
    hashtext = request.args.get('hashtotest','')
    
    records = db.session.query(Pass.salt).all()
    records_remove_comma = [i for i, in records]
    for salt in records_remove_comma:
        testhash = SHA256()
        testhash.update(plain.encode('ascii')+salt)
        testgen = testhash.hexdigest()
        if(testgen==hashtext):
            response = "True"
        
    return jsonify({
        "response"        :  response
    })