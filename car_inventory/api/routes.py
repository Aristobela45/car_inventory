from flask import Blueprint, request, jsonify
from car_inventory.helpers import token_required
from car_inventory.models import db, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
@token_required
def getdata():
    return {'some': 'value'}



@api.route('/cars', methods = ["POST"])
@token_required
def create_car(our_user):
    
    car_price = request.json['car_price']
    car_mileage = request.json['car_mileage']
    car_mph = request.json['car_mph']
    car_make = request.json['car_make']
    car_color = request.json['car_color']
    car_year = request.json['car_year']
    car_engine = request.json['car_engine']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    car = Car(car_price, car_mileage, car_mph, car_make, car_color, car_year, car_engine, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

#Retrieve(READ) 
@api.route('/car', methods = ['GET'])
@token_required
def get_car(our_user):
    owner = our_user.token
    Car = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(Car)

    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(our_user, id):    
    if id:
        Car = Car.query.get(id)
        response = car_schema.dump(Car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Id equired'}), 401


@api.route('/cars/<id>', methods = ['PUT'])
@token_required
def update_car(our_user, id): 
    Car = Car.query.get(id)   
    Car.car_mileage = request.json['car_mileage']
    Car.car_mph = request.json['car_mph']
    Car.car_make = request.json['car_make']
    Car.car_color = request.json['car_color']
    Car.car_year = request.json['car_year']
    Car.car_engine = request.json['car_engine']
    Car.user_token = our_user.token  

    db.session.commit()

    response = car_schema.dump(Car)

    return jsonify(response)


@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_cars(our_user, id):
    Car = Car.query.get(id)
    db.session.delete(Car)
    db.session.commit()

    response = car_schema.dump(Car)
    return jsonify(response) 