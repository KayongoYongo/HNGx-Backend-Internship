from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'  # SQLite database
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    email = db.Column(db.String(255))

# Define API endpoints
@app.route('/api/people', methods=['POST'])
def create_person():
    try:
        data = request.json
        person = Person(**data)
        db.session.add(person)
        db.session.commit()
        return jsonify({"message": "Person created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Person with the same name already exists"}), 400

@app.route('/api/people/<int:user_id>', methods=['GET'])
def get_person(user_id):
    person = Person.query.get(user_id)
    if person:
        return jsonify({
            "id": person.id,
            "name": person.name,
            "age": person.age,
            "email": person.email
        }), 200
    else:
        return jsonify({"error": "Person not found"}), 404

@app.route('/api/people/<int:user_id>', methods=['PUT'])
def update_person(user_id):
    data = request.json
    person = Person.query.get(user_id)
    if person:
        person.name = data.get('name', person.name)
        person.age = data.get('age', person.age)
        person.email = data.get('email', person.email)
        db.session.commit()
        return jsonify({"message": "Person updated successfully"}), 200
    else:
        return jsonify({"error": "Person not found"}), 404

@app.route('/api/people/<int:user_id>', methods=['DELETE'])
def delete_person(user_id):
    person = Person.query.get(user_id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Person deleted successfully"}), 200
    else:
        return jsonify({"error": "Person not found"}), 404

@app.route('/api/people', methods=['GET'])
def get_person_by_name():
    name = request.args.get('name')
    if name:
        people = Person.query.filter_by(name=name).all()
        if people:
            return jsonify([{
                "id": person.id,
                "name": person.name,
                "age": person.age,
                "email": person.email
            } for person in people]), 200
        else:
            return jsonify({"error": "No matching persons found"}), 404
    else:
        return jsonify({"error": "Name parameter is required"}), 400

if __name__ == '__main__':
    with app.app_context():  # Ensure the database operations are within the Flask context
        db.create_all()  # Create the SQLite database and tables

    app.run(debug=True)