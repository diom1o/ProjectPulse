from flask import Flask, jsonify, request
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn

@app.route('/')
def home():
    return jsonify({"message": "Welcome to our project management system!"})

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO projects (name, description) VALUES (%s, %s) RETURNING id;",
                (data['name'], data['description']))
    project_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": project_id, "status": "success"}), 201

@app.route('/projects', methods=['GET'])
def get_projects():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description FROM projects;")
    projects = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": project[0], "name": project[1], "description": project[2]} for project in projects])

@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE projects SET name = %s, description = %s WHERE id = %s;",
                (data['name'], data['description'], project_id))
    conn.commit()
    updated_rows = cur.rowcount
    cur.close()
    conn.close()
    if updated_rows == 0:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"status": "success"}), 200

@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM projects WHERE id = %s;", (project_id,))
    conn.commit()
    deleted_rows = cur.rowcount
    cur.close()
    conn.close()
    if deleted_rows == 0:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)