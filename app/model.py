from flask import Flask, request, jsonify
from .extension import *
from .config import *
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
import secrets


auth = HTTPBasicAuth()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def setPassword(self, password):
        self.password_hash=generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.password_hash,password)
    
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    company_api_key = db.Column(db.String(32), nullable=False)
    #Define una relación de uno a muchos entre Company y Locations
    locations = db.relationship('Location',backref='company',lazy=True)
    
    def __init__(self, company_name):
        self.company_name = company_name
        self.company_api_key = secrets.token_hex(16) #Genera clave API de 32 caracteres

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'),nullable=False)
    location_name = db.Column(db.String(120), nullable=False)
    location_country = db.Column(db.String(120), nullable=False)
    location_city = db.Column(db.String(120), nullable=False)
    location_meta = db.Column(db.String(255))
    company = db.relationship('Company', backref=db.backref('locations',lazy=True))
    sensors = db.relationship('Sensor',backref='location',lazy=True)

    def __init__(self, location_name, location_country, location_city, location_meta):
        self.location_name = location_name
        self.location_country = location_country
        self.location_city = location_city
        self.location_meta = location_meta

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    sensor_name = db.Column(db.String(80), nullable=False)
    sensor_category = db.Column(db.String(80), nullable=False)
    sensor_meta = db.Column(db.String(255))
    sensor_api_key = db.Column(db.String(32), nullable=False)
    location = db.relationship('Location',backref=db.backref('sensors', lazy=True))
    sensor_datas = db.relationship('Sensor_data', backref='sensor',lazy=True)

    def __init__(self,sensor_name, sensor_category, sensor_meta):
        self.sensor_name = sensor_name
        self.sensor_category = sensor_category
        self.sensor_meta = sensor_meta
        self.sensor_api_key = secrets.token_hex(16)

class Sensor_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    data_1 = db.Column(db.Integer, nullable=False)
    data_2 = db.Column(db.Integer, nullable=False)
    sensor = db.relationship('Sensor', backref=db.backref('sensor_datas', lazy=True))

    def __init__(self, data_1, data_2):
        self.data_1 = data_1
        self.data_2 = data_2
    