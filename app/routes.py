from flask import Blueprint, request, jsonify
from .model import db, User, Companys, Locations, Sensors, Sensor_Datas
from .extension import db
from .auth import *
from datetime import datetime


main_bp = Blueprint('main', __name__)

# Helper function to verify company API key
def verify_company_api_key(api_key):
    return Companys.query.filter_by(company_api_key=api_key).first()

# Endpoint para crear un administrador
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

# Endpoint para obtener todas las compañías
@main_bp.route('/companies', methods=['GET'])
@auth.login_required
def get_companies():
    try:
        companies = Companys.query.all()
        result = [{'company_id': company.id, 'company_name': company.company_name, 'company_api_key': company.company_api_key} for company in companies]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para crear una compañía
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
        return jsonify({'message': 'Company created', 'company_api_key': new_company.company_api_key}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoints REST estándar para Location
# Mostrar todas las ubicaciones
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

# Mostrar una ubicación
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

# Crear una ubicación
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
    company_id = company.id
    location_name = data['location_name']
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta')
    
    try:
        location = Locations(
            company_id=company_id,
            location_name=location_name,
            location_country=location_country,
            location_city=location_city,
            location_meta=location_meta
        )
        db.session.add(location)
        db.session.commit()
        return jsonify({'message': 'Location created'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Actualizar una ubicación
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

# Eliminar una ubicación
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

# Endpoints REST estándar para Sensor
# Mostrar todos los sensores
@main_bp.route('/sensors', methods=['GET'])
@auth.login_required
def get_all_sensors():
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    
    try:
        sensors = Sensors.query.filter_by(company_id=company.id).all()
        result = [{
            'sensor_id': sensor.id,
            'sensor_name': sensor.sensor_name,
            'sensor_type': sensor.sensor_type,
            'sensor_meta': sensor.sensor_meta
        } for sensor in sensors]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Mostrar un sensor
@main_bp.route('/sensors/<int:sensor_id>', methods=['GET'])
@auth.login_required
def get_sensor(sensor_id):
    """
    api_key = request.args.get('company_api_key')
    company = verify_company_api_key(api_key)
    

    if not company:
        return jsonify({'error': 'Clave API de compañía inválida.'}), 400
    """
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
    sensor_category = data.get('sensor_category')
    sensor_meta = data.get('sensor_meta')

    location = Locations.query.filter_by(company_id=company.id).first()

    
    try:
        sensor = Sensors(
            location_id=location.id,
            sensor_name=sensor_name,
            sensor_category=sensor_category,
            sensor_meta=sensor_meta
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
    
    sensor = Sensors.query.filter_by(id=sensor_id, company_id=company.id).first()
    if not sensor:
        return jsonify({'error': 'Sensor no encontrado.'}), 404
    
    data = request.get_json()
    sensor.sensor_name = data.get('sensor_name', sensor.sensor_name)
    sensor.sensor_type = data.get('sensor_type', sensor.sensor_type)
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
    
    sensor = Sensors.query.filter_by(id=sensor_id, company_id=company.id).first()
    if not sensor:
        return jsonify({'error': 'Sensor no encontrado.'}), 404
    
    try:
        db.session.delete(sensor)
        db.session.commit()
        return jsonify({'message': 'Sensor deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoint para insertar datos del sensor
@main_bp.route('/api/v1/sensor_data', methods=['POST'])
@auth.login_required
def insert_sensor_data():
    data = request.get_json()
    if not data or 'api_key' not in data or 'json_data' not in data:
        return jsonify({'error': 'api_key y json_data son requeridos.'}), 400
    
    import json
    sensor_api_key = data['api_key']
    json_data_str = data['json_data']
    corrected_json_str = json_data_str.replace("'", '"')
    json_data = json.loads(corrected_json_str)
    if len(json_data) != 2:
        raise ValueError("Se esperan exactamente dos entradas en el JSON.")
    
    data_1 = json_data[0].get('key1')
    data_2 = json_data[1].get('key2')

    sensor = Sensors.query.filter_by(sensor_api_key=sensor_api_key).first()
    if not sensor:
        return jsonify({'error': 'Clave API de sensor inválida.'}), 400
    

    sensor_data = Sensor_Datas(sensor_id=sensor.id, data_1=data_1, data_2=data_2)
    db.session.add(sensor_data)
    
    db.session.commit()
    return jsonify({'message': 'Datos del sensor insertados exitosamente.'}), 201


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
        #Convertit EPOCH a TIMESTAMP
        from_datetime = datetime.fromtimestamp(int(from_timestamp))
        to_datetime = datetime.fromtimestamp(int(to_timestamp))

        query = Sensor_Datas.query.filter(
            Sensor_Datas.sensor_id.in_(sensor_ids),
            Sensor_Datas.timestamp >= from_datetime,
            Sensor_Datas.timestamp <= to_datetime
        ).all()
        """
        query = Sensor_Data.query.filter(Sensor_Data.sensor_id.in_(sensor_ids))
        if from_timestamp:
            query = query.filter(Sensor_Data.timestamp >= int(from_timestamp))
        if to_timestamp:
            query = query.filter(Sensor_Data.timestamp <= int(to_timestamp))
        """
        sensor_data = query.all()
        result = [
            {
                'sensor_id': data.sensor_id,
                'timestamp': data.timestamp.timestamp(),
                'data': data.value
            } for data in sensor_data
        ]
        #result = [{'sensor_id': data.sensor_id, 'timestamp': data.timestamp, 'data': data.data} for data in sensor_data]
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

