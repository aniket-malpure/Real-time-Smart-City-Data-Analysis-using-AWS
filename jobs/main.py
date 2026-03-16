import os
import confluent_kafka import SerialzingProducer
import simplejson as json
from datetime import datetime
import random

GAINESVILLE_COORDINATES = {
    "latitute": 29.6516,
    "longitude": -82.3248
}
ORLANDO_COORDINATES = {
    "latitute": 28.5383,
    "longitude": -81.3792
}

# Calculate the movement increments
LATITUDE_INCREMENT = (ORLANDO_COORDINATES['latitude'] - GAINESVILLE_COORDINATES['latitute']) / 100
LONGITUDE_INCREMENT = (ORLANDO_COORDINATES['longitude'] - GAINESVILLE_COORDINATES['longitude']) / 100

# Environment variables for configuration
KAFKA_BOOTSTRAP_SERVICES = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC', 'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC', 'gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC', 'traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC', 'weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC', 'emergency_data')

random.seed(42)

start_time = datetime.now()
start_location = GAINESVILLE_COORDINATES.copy()

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60)) # Update Frequency
    return start_time

def generate_gps_data(device_id, timestamp, vehicle_type='private'):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'speed': random.uniform(0, 40),
        'direction': 'South-East',
        'vehicleType': vehicle_type 
    }

def generate_traffic_camera_data(device_id, timestamp, location, camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'cameraId': camera_id,
        'location': location, 
        'timestamp': timestamp,
        'snapshot': 'Base64EncodedString' # In real world enter the url where you'll get the pictures
    }

def generate_weather_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'location': location, 
        'timestamp': timestamp,
        'temperature': random.uniform(-5, 35),
        'weatherCondition': random.chouce(['Sunny', 'Cloudy', 'Rain', 'Super Hot']),
        'precipitation': random.uniform(0, 25),
        'windspeed': random.uniform(0, 100),
        'humidity': random.randint(0, 100),
        'airQualityIndex': random.uniform(10, 300)
    }

def generate_emergency_incident_data(device_id, timestamp, location):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident', 'Fire', 'Medical', 'Police', 'None']),
        'location': location, 
        'timestamp': timestamp,
        'status': random.choice(['Active', 'Resolved']),
        'description': 'Descriptiom of the incident'
    }

def simulate_vehicle_movement():
    global start_location

    # Move towards Orlando
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT

    # Add some randomness to simulate actual road travel
    start_location['latitude'] += random.uniform('0.0005, 0005')
    start_location['longitude'] += random.uniform('0.0005, 0005')

    return start_location

def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()

    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitutde'], location['longitude']),
        'speed': random.uniform(10, 40),
        'direction': 'South-East',
        'make': 'BMW',
        'model': 'M2',
        'year': 2025,
        'fueltype': 'Hybrid'
    }

def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def produce_data_to_kafka(producer, topic, data):
    producer.produce(
        topic,
        key=str(data['id']),
        value=json.dumps(data, default=json_serializer).encode('utf-8')
        on_delivery=delivery_report
    )

    producer.flush()

def simulate_journey(producer, device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id, vehicle_data['timestamp'])
        traffic_camera_data = generate_traffic_camera_data(device_id, vehicle_data['timestamp'], vehicle_data['location'], 'Camera123')
        weather_data = generate_weather_data(device_id, vehicle_data['timestamp'], vehicle_data['location'])
        emergency_incident_data = generate_emergency_incident_data(device_id, vehicle_data['timestamp'], vehicle_data['location'])

        if (vehicle_data['location'][0] <= ORLANDO_COORDINATES['latitude']
            and vehicle_data['location'][1] >= ORLANDO_COORDINATES['longitude']):
            print('Vehicle has reached Orlando, Simluation ending...')
            break

        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_incident_data)

        time.sleep(5)

if __name__=='main':
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVICES,
        'error_cb': lambda err: print(f'Kafka error: {err}')
    }
    producer = SerialzingProducer(producer_config)

    try:
        simulate_journey(producer, 'Vehicle123')

    except KeyboardInterrupt:
        print('Simulation ended by the user')

    except Exception as e:
        print(f'Enexpected error occured: {e}')