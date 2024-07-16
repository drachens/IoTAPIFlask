from flask import Blueprint, request, jsonify
from .model import db, User, Company, Location, Sensor, Sensor_Data

main_bp = Blueprint('main', __name__)

@main_bp.route('/create_admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error':'Username y password son requeridos.'}),400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error':'El username ya existe.'}),400
    new_user = User(username=data['username'], is_admin=True)
    new_user.setPassword(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'Usuario ADMIN creado exitosamente.'}),201

@main_bp.route('/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    company_id = data.get('company_id')
    location_name = data.get('location_name')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta')
    location = Location(
        company_id=company_id,
        location_name=location_name,
        location_country=location_country,
        location_city=location_city,
        location_meta=location_meta
    )
    db.session.add(location)
    db.session.commit()
    return jsonify({'message': 'Location created'}), 201

@main_bp.route('/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    company_name = data.get('company_name')
    company = Company(company_name=company_name)
    db.session.add(company)
    db.session.commit()
    return jsonify({'message': 'Company created', 'company_api_key': company.company_api_key}), 201