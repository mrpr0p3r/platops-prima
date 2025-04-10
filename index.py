from flask import Flask, jsonify, request
from model.people import People
from base import Session, engine, Base
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

with app.app_context():
    Base.metadata.create_all(engine)
    session = Session()
    try:
        # Check if the table is empty
        if session.query(People).count() == 0:
            session.add_all([
                People(name='Alice', age=30),
                People(name='Bob', age=25),
                People(name='Charlie', age=35)
            ])
            session.commit()
    finally:
        session.close()


@app.route("/users")
def users():
    session = Session()
    try:
        people = session.query(People).all()
        return jsonify([{'name': p.name, 'age': p.age} for p in people]), 200
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Database operation failed'}), 500

    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()

@app.route("/user", methods=['POST'])
def add_user():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    if 'name' not in request.json or 'age' not in request.json:
        return jsonify({'error': 'Missing name or age'}), 400
    if not isinstance(request.json['name'], str) or not isinstance(request.json['age'], int):
        return jsonify({'error': 'Invalid name or age type'}), 400
    session = Session()
    try:
        user = People(name=request.json['name'], age=request.json['age'])
        session.add(user)
        session.commit()
        return '', 204
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Failed to create user'}), 500
    except ValueError as e:
        return jsonify({'error': 'Invalid data format'}), 400
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'User already exists'}), 400
    finally:
        session.close()
@app.errorhandler(HTTPException)
def handle_exception(e):
    logger.error(f"HTTP error: {str(e)}")
    return jsonify({
        "error": e.name,
        "message": e.description
    }), e.code
@app.errorhandler(Exception)
def handle_general_exception(e):
    logger.critical(f"Unexpected error: {str(e)}")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred."
    }), 500