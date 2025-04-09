from flask import Blueprint, request, jsonify
from .model import db, User, Companys, Locations, Sensors, Sensor_Datas
from .extension import db
from .auth import *
from datetime import datetime
import json


main_bp = Blueprint('main', __name__)

# Helper function to verify company API key
def verify_company_api_key(api_key):
    return Companys.query.filter_by(company_api_key=api_key).first()

#--------------------------------
# Endopoints para ADMIN y COMPANY
#--------------------------------

@main_bp.route('/create_admin', methods=['POST'])
def create_admin():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username y password son requeridos.'}), 400
    
    username = data['username']
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'El username ya existe.'}), 400
    
    try:
        new_user = User(username=username, is_admin=True)
        new_user.setPassword(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuario ADMIN creado exitosamente.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/companies', methods=['GET'])
@auth.login_required
def get_companies():
    try:
        companies = Companys.query.all()
        result = [{
            'company_id': company.id, 
            'company_name': company.company_name, 
            'company_api_key': company.company_api_key
            } for company in companies]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/companies', methods=['POST'])
@auth.login_required
def create_company():
    data = request.get_json()
    if not data or 'company_name' not in data:
        return jsonify({'error': 'company_name es requerido.'}), 400
    
    company_name = data['company_name']
    try:
        new_company = Companys(company_name=company_name)
        db.session.add(new_company)
        db.session.commit()
        return jsonify({
            'message': 'Company created', 
            'company_api_key': new_company.company_api_key
            }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


#--------------------------------
# Endpoints para Locations
#--------------------------------

@main_bp.route('/locations', methods=['GET'])
@auth.login_required
def get_all_locations():
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400

    try:
        locations = Locations.query.filter_by(company_id=company.id).all()
        result = [{
            'location_id': location.id,
            'location_name': location.location_name,
            'location_country': location.location_country,
            'location_city': location.location_city,
            'location_meta': location.location_meta
        } for location in locations]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/locations/<int:location_id>', methods=['GET'])
@auth.login_required
def get_location(location_id):
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    location = Locations.query.filter_by(id=location_id, company_id=company.id).first()
    if not location:
        return jsonify({'error': 'Ubicación no encontrada.'}), 404
    
    result = {
        'location_id': location.id,
        'location_name': location.location_name,
        'location_country': location.location_country,
        'location_city': location.location_city,
        'location_meta': location.location_meta
    }
    return jsonify(result), 200

@main_bp.route('/locations', methods=['POST'])
@auth.login_required
def create_location():
    data = request.get_json()
    api_key = data.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    if 'location_name' not in data:
        return jsonify({'error': 'location_name es requerido.'}), 400
        
    try:
        location = Locations(
            company_id=company.id,
            location_name=data['location_name'],
            location_country=data.get('location_country',''),
            location_city=data.get('location_city',''),
            location_meta=data.get('location_meta','')
        )
        db.session.add(location)
        db.session.commit()
        return jsonify({'message': 'Location created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/locations/<int:location_id>', methods=['PUT'])
@auth.login_required
def update_location(location_id):
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    location = Locations.query.filter_by(id=location_id, company_id=company.id).first()
    if not location:
        return jsonify({'error': 'Ubicación no encontrada.'}), 404
    
    data = request.get_json()
    location.location_name = data.get('location_name', location.location_name)
    location.location_country = data.get('location_country', location.location_country)
    location.location_city = data.get('location_city', location.location_city)
    location.location_meta = data.get('location_meta', location.location_meta)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Location updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main_bp.route('/locations/<int:location_id>', methods=['DELETE'])
@auth.login_required
def delete_location(location_id):
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    location = Locations.query.filter_by(id=location_id, company_id=company.id).first()
    if not location:
        return jsonify({'error': 'Ubicación no encontrada.'}), 404
    
    try:
        db.session.delete(location)
        db.session.commit()
        return jsonify({'message': 'Location deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


#------------------------------------
# Endpoints para Sensors
#------------------------------------

@main_bp.route('/sensors', methods=['GET'])
@auth.login_required
def get_all_sensors():
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    try:
        sensors = Sensors.query.join(Locations).filter(Locations.company_id == company.id).all()
        result = [{
            'sensor_id': sensor.id,
            'sensor_name': sensor.sensor_name,
            'sensor_category': sensor.sensor_category,            
            'sensor_meta': sensor.sensor_meta,
            'sensor_api_key': sensor.sensor_api_key
        } for sensor in sensors]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Mostrar un sensor
@main_bp.route('/sensors/<int:sensor_id>', methods=['GET'])
@auth.login_required
def get_sensor(sensor_id):
    sensor = Sensors.query.filter_by(id=sensor_id).first()
    if not sensor:
        return jsonify({'error': 'Sensor no encontrado.'}), 404
    
    result = {
        'sensor_id': sensor.id,
        'sensor_name': sensor.sensor_name,
        'sensor_category': sensor.sensor_category,
        'sensor_meta': sensor.sensor_meta,
        'sensor_api_key': sensor.sensor_api_key
    }
    return jsonify(result), 200

# Crear un sensor
@main_bp.route('/sensors', methods=['POST'])
@auth.login_required
def create_sensor():
    data = request.get_json()
    api_key = data.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    if 'sensor_name' not in data:
        return jsonify({'error': 'sensor_name es requerido.'}), 400
    
    sensor_name = data['sensor_name']
    sensor_category = data.get('sensor_category','')
    sensor_meta = data.get('sensor_meta','')

    # Se busca una ubicación para asociar el sensor (se asume que la compañía tiene al menos una)
    location = Locations.query.filter_by(company_id=company.id).first()

    if not location:
        return jsonify({'error': 'No hay ubicaciones registradas para la compañía.'}), 400
    
    try:
        sensor = Sensors(
            sensor_name = sensor_name,
            sensor_category = sensor_category,
            sensor_meta = sensor_meta,
            location_id = location.id
        )
        db.session.add(sensor)
        db.session.commit()
        return jsonify({'message': 'Sensor created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Actualizar un sensor
@main_bp.route('/sensors/<int:sensor_id>', methods=['PUT'])
@auth.login_required
def update_sensor(sensor_id):
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400

    # Se realiza el join para confirmar la pertenencia del sensor a la compañía.
    sensor = Sensors.query.join(Locations).filter(
        Sensors.id == sensor_id,
        Locations.company_id == company.id
    ).first()
    
    if not sensor:
        return jsonify({'error': 'Sensor no encontrado.'}), 404
    
    data = request.get_json()
    sensor.sensor_name = data.get('sensor_name', sensor.sensor_name)
    sensor.sensor_category = data.get('sensor_category', sensor.sensor_category)
    sensor.sensor_meta = data.get('sensor_meta', sensor.sensor_meta)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Sensor updated'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Eliminar un sensor
@main_bp.route('/sensors/<int:sensor_id>', methods=['DELETE'])
@auth.login_required
def delete_sensor(sensor_id):
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    sensor = Sensors.query.join(Locations).filter(
        Sensors.id == sensor_id,
        Locations.company_id == company.id
    ).first()

    if not sensor:
        return jsonify({'error': 'Sensor no encontrado.'}), 404
    
    try:
        db.session.delete(sensor)
        db.session.commit()
        return jsonify({'message': 'Sensor deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


#----------------------------------------
# Endpoints para Sensor_Data
#----------------------------------------

@main_bp.route('/api/v1/sensor_data', methods=['POST'])
@auth.login_required
def insert_sensor_data():
    data = request.get_json()
    if not data or 'api_key' not in data or 'json_data' not in data:
        return jsonify({'error': 'api_key y json_data son requeridos.'}), 400
    

    sensor_api_key = data['api_key']
    json_data_str = data['json_data']

    if not isinstance(json_data_str, list) or len(json_data_str) != 2:
        return jsonify({'error': 'Se esperan exactamente dos entradas en el json_data.'}), 400

    # Se asume que las dos entradas tienen claves 'key1' y 'key2' respectivamente.
    data_1 = json_data_str[0].get('key1')
    data_2 = json_data_str[1].get('key2')

    sensor = Sensors.query.filter_by(sensor_api_key=sensor_api_key).first()
    if not sensor:
        return jsonify({'error': 'Clave API de sensor inválida.'}), 400
    

    sensor_data = Sensor_Datas(sensor_id=sensor.id, data_1=data_1, data_2=data_2)

    try:
        sensor_data = Sensor_Datas(data_1=data_1, data_2=data_2, sensor_id=sensor.id)
        db.session.add(sensor_data)
        db.session.commit()
        return jsonify({'message': 'Datos del sensor insertados exitosamente.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Endpoint para consultar datos del sensor
@main_bp.route('/api/v1/sensor_data', methods=['GET'])
@auth.login_required
def get_sensor_data():
    company_api_key = request.headers.get('company_api_key') or request.args.get('company_api_key')
    from_timestamp = request.args.get('from')
    to_timestamp = request.args.get('to')
    sensor_ids = request.args.getlist('sensor_id')
    
    if not company_api_key or not from_timestamp or not to_timestamp or not sensor_ids:
        return jsonify({'error': 'Missing required parameters'}), 400
        
    company = verify_company_api_key(company_api_key)

    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    try:
        from_datetime = datetime.fromtimestamp(int(from_timestamp))
        to_datetime = datetime.fromtimestamp(int(to_timestamp))
        # Convertir sensor_ids a enteros
        sensor_ids_int = [int(sid) for sid in sensor_ids]

        sensor_data_list = Sensor_Datas.query.filter(
            Sensor_Datas.sensor_id.in_(sensor_ids_int),
            Sensor_Datas.timestamp >= from_datetime,
            Sensor_Datas.timestamp <= to_datetime
        ).all()

        result = [{
            'sensor_id': data.sensor_id,
            'timestamp': int(data.timestamp.timestamp()),
            'data': {
                'data_1': data.data_1,
                'data_2': data.data_2
            }
        } for data in sensor_data_list]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

