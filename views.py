from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('metrics', lazy=True))

@app.before_first_request
def create_tables():
    db.create_all()

def add_and_commit(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def delete_and_commit(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.json
    try:
        new_project = Project(name=data['name'], description=data.get('description'))
        add_and_commit(new_project)
        return jsonify({'message': 'Project created successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    try:
        project = Project.query.get_or_404(id)
        return jsonify({'id': project.id, 'name': project.name, 'description': project.description}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/projects/<int:id>', methods=['PUT'])
def update_project(id):
    try:
        project = get_object(Project, id)
        update_project_attributes(project, request.json)
        db.session.commit()
        return jsonify({'message': 'Project updated successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_object(model, id):
    return model.query.get_or_404(id)

def update_project_attributes(project, data):
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    try:
        project = get_object(Project, id)
        delete_and_commit(project)
        return jsonify({'message': 'Project deleted successfully.'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    try:
        new_task = Task(name=data['name'], status=data['status'], project_id=data['project_id'])
        add_and_commit(new_task)
        return jsonify({'message': 'Task created successfully.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    try:
        task = get_object(Task, id)
        return jsonify({'id': task.id, 'name': task.name, 'status': task.status, 'project_id': task.project_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        task = get_object(Task, id)
        update_task_attributes(task, request.json)
        db.session.commit()
        return jsonify({'message': 'Task updated successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_task_attributes(task, data):
    task.name = data.get('name', task.name)
    task.status = data.get('status', task.status)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        task = get_object(Task, id)
        delete_and_commit(task)
        return jsonify({'message': 'Task deleted successfully.'}), 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)