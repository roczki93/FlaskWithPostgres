#!flask/bin/python
from flask import Flask, render_template
from flask import jsonify, request, abort
#import flask_restless
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://myuser:mypass@192.168.177.183:5432/mydatabase1'
app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
app.debug = True
db = SQLAlchemy(app)

class User_information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    city = db.Column(db.String(50))
    street = db.Column(db.String(50))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    
    def __init__(self, first_name, last_name, email, gender, city, street, latitude, longitude):
	self.first_name = first_name
	self.last_name = last_name
	self.email = email
	self.gender = gender
	self.city = city
	self.street = street
	self.latitude = latitude
	self.longitude = longitude
	
    def __repr__(self):
	return '<user_information %r>' % self.id
    @property
    def serialize(self):
	return {
	    'id'	:self.id,
	    'first_name':self.first_name,
	    'last_name'	:self.last_name,
	    'email'	:self.email,
	    'gender'	:self.gender,
	    'street'	:self.street,
	    'latitude'	:self.latitude,
	    'longitude'	:self.longitude
	}
    @property
    def serialize_many2many(self):
	return [ item.serialize for item in self.many2many]
	
@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/v1/userinfo', methods=['POST'])
def post_userinfo():
    user_info = User_information(request.form['first_name'],request.form['last_name'], request.form['email'], request.form['gender'], request.form['city'], request.form['street'], request.form['latitude'], request.form['longitude'])
    #print request.form['first_name']
    
    #print list(request.form.keys())[0]
    
    db.session.add(user_info)
    db.session.commit()
    #return "%r" % user_info.id
    return "OK"
    
@app.route('/api/v1/userinfo/', methods=['GET'])
def get_userinfo():
    #my_userinfo = User_information.query.limit(10).offset(0).all()
    #oneItem = User_information.query.filter_by(first_name="Lukasz").first()
    #print oneItem
    #onverted = list(jsonify({'user_info': User_information.query.all()}))
    
    return jsonify([i.serialize for i in User_information.query.order_by('-id').limit(10).all()])

@app.route('/api/v1/userinfo/<string:key>')
def get_userinfo_by(key):
    return jsonify([i.serialize for i in User_information.query.filter_by(first_name=key)])
    
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int("80"))
