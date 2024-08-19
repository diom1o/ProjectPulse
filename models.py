from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///projectpulse_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)

class Project(database.Model):
    project_id = database.Column(database.Integer, primary_key=True)
    project_name = database.Column(database.String(120), nullable=False)
    project_description = database.Column(database.Text, nullable=True)
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    associated_tasks = database.relationship('Task', backref='associated_project', lazy=True)
    
    def __repr__(self):
        return f'<Project {self.project_name}>'

class Task(database.Model):
    task_id = database.Column(database.Integer, primary_key=True)
    task_title = database.Column(database.String(120), nullable=False)
    task_description = database.Column(database.Text, nullable=True)
    task_status = database.Column(database.String(50), nullable=False, default="pending")
    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    linked_project_id = database.Column(database.Integer, database.ForeignKey('project.project_id'), nullable=False)
    task_metrics = database.relationship('Metric', backref='linked_task', lazy=True)
    
    def __repr__(self):
        return f'<Task {self.task_title}>'

class Metric(database.Model):
    metric_id = database.Column(database.Integer, primary_key=True)
    metric_name = database.Column(database.String(120), nullable=False)
    metric_value = database.Column(database.Float, nullable=False)
    recording_time = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    associated_task_id = database.Column(database.Integer, database.ForeignKey('task.task_id'), nullable=False)
    
    def __repr__(self):
        return f'<Metric {self.metric_name}: {self.metric_value}>'

@app.before_first_request
def create_database_tables():
    database.create_all()

if __name__ == '__main__':
    app.run(debug=True)