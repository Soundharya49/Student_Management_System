from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from extensions import mongo
from bson.objectid import ObjectId
import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == current_app.config['ADMIN_USER'] and password == current_app.config['ADMIN_PASS']:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        
        # Store tokens in MongoDB (upsert to ensure one valid set per admin)
        mongo.db.tokens.update_one(
            {'username': username},
            {'$set': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'created_at': datetime.datetime.utcnow()
            }},
            upsert=True
        )
        
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@api_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    students_collection = mongo.db.students
    students = []
    for student in students_collection.find():
        student['_id'] = str(student['_id'])
        students.append(student)
    return jsonify(students), 200

@api_bp.route('/students', methods=['POST'])
@jwt_required()
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No input data provided"}), 400
    
    # Simple validation
    required_fields = ['name', 'email', 'course']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"Missing field: {field}"}), 400

    students_collection = mongo.db.students
    result = students_collection.insert_one(data)
    
    return jsonify({"msg": "Student added", "id": str(result.inserted_id)}), 201

@api_bp.route('/students/<id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    data = request.get_json()
    students_collection = mongo.db.students
    
    try:
        oid = ObjectId(id)
    except:
        return jsonify({"msg": "Invalid ID format"}), 400

    result = students_collection.update_one({'_id': oid}, {'$set': data})
    
    if result.matched_count == 0:
        return jsonify({"msg": "Student not found"}), 404
        
    return jsonify({"msg": "Student updated"}), 200

@api_bp.route('/students/<id>', methods=['DELETE'])
@jwt_required()
def delete_student(id):
    students_collection = mongo.db.students
    try:
        oid = ObjectId(id)
    except:
        return jsonify({"msg": "Invalid ID format"}), 400
        
    result = students_collection.delete_one({'_id': oid})
    
    if result.deleted_count == 0:
        return jsonify({"msg": "Student not found"}), 404
        
    return jsonify({"msg": "Student deleted"}), 200
