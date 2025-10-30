from flask import Blueprint, request, jsonify
from api.models import db, User
from api.utils import APIException
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

# Endpoint de ejemplo (probablemente ya lo tenías)


@api.route('/hello', methods=['GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }
    return jsonify(response_body), 200


# ENDPOINTS DE AUTENTICACIÓN

@api.route('/signup', methods=['POST'])
def signup():
    try:
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')

        if not email or not password:
            return jsonify({"error": "Email y contraseña son requeridos"}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "El usuario ya existe"}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Usuario creado exitosamente",
            "user": new_user.serialize()
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/login', methods=['POST'])
def login():
    try:
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')

        if not email or not password:
            return jsonify({"error": "Email y contraseña son requeridos"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Credenciales inválidas"}), 401

        access_token = create_access_token(identity=user.id)

        return jsonify({
            "message": "Login exitoso",
            "access_token": access_token,
            "user": user.serialize()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/private', methods=['GET'])
@jwt_required()
def private():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({
            "message": "Acceso a ruta privada exitoso",
            "user": user.serialize()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"valid": False}), 401

        return jsonify({
            "valid": True,
            "user": user.serialize()
        }), 200

    except Exception as e:
        return jsonify({"valid": False}), 401
