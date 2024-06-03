from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///job_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), default="Applied")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/applications', methods=['POST'])
def add_application():
    data = request.json
    new_application = JobApplication(title=data['title'], company=data['company'], status=data.get('status', "Applied"))
    db.session.add(new_application)
    db.session.commit()
    return jsonify({'message': 'Job application added'}), 201

@app.route('/applications', methods=['GET'])
def get_applications():
    applications = JobApplication.query.all()
    return jsonify([{'id': app.id, 'title': app.title, 'company': app.company, 'status': app.status} for app in applications])

@app.route('/applications/<int:id>', methods=['PUT'])
def update_application(id):
    data = request.json
    application = JobApplication.query.get_or_404(id)
    application.title = data.get('title', application.title)
    application.company = data.get('company', application.company)
    application.status = data.get('status', application.status)
    db.session.commit()
    return jsonify({'message': 'Job application updated'})

@app.route('/applications/<int:id>', methods=['DELETE'])
def delete_application(id):
    application = JobApplication.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    return jsonify({'message': 'Job application deleted'})

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = User.query.get_or_404(id)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({'message': 'User updated'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)