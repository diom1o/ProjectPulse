from flask import Flask, jsonify, request, after_this_request
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import logging
from functools import wraps

load_dotenv()

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")

try:
    conn_pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                   host=DB_HOST,
                                                   dbname=DB_NAME,
                                                   user=DB_USER,
                                                   password=DB_PASS,
                                                   port=DB_PORT)
    if conn_pool:
        logging.info("Connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    logging.error("Error while connecting to PostgreSQL", error)
    exit(1)

def get_db_connection():
    return conn_pool.getconn()

def put_db_connection(conn):
    conn_pool.putconn(conn)

def log_route(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Incoming request: {request.method} {request.path}")
        response = func(*args, **kwargs)
        @after_this_request
        def log_response(response):
            logging.info(f"Response status: {response.status}")
            return response
        return response
    return wrapper

@app.route('/')
@log_route
def home():
    return jsonify({"message": "Welcome to our project management system!"})

@app.route('/projects', methods=['POST'])
@log_route
def add_project():
    data = request.json
    if not data.get('name') or not data.get('description'):
        return jsonify({"error": "Missing name or description"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO projects (name, description) VALUES (%s, %s) RETURNING id;",
                    (data['name'], data['description']))
        project_id = cur.fetchone()[0]
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        cur.close()
        put_db_connection(conn)
    
    return jsonify({"id": project_id, "status": "success"}), 201

@app.route('/projects', methods=['GET'])
@log_route
def get_projects():
    conn = get_db_connection()
    projects = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM projects;")
        projects = cur.fetchall()
    except Exception as e:
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        cur.close()
        put_db_connection(conn)

    return jsonify([{"id": project[0], "name": project[1], "description": project[2]} for project in projects])

@app.route('/projects/<int:project_id>', methods=['PUT', 'DELETE'])
@log_route
def update_or_delete_project(project_id):
    data = request.json if request.method == 'PUT' else None
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        if request.method == 'PUT':
            if not data.get('name') or not data.get('description'):
                return jsonify({"error": "Missing name or description"}), 400
            
            cur.execute("UPDATE projects SET name = %s, description = %s WHERE id = %s;",
                        (data['name'], data['description'], project_id))
        elif request.method == 'DELETE':
            cur.execute("DELETE FROM projects WHERE id = %s;", (project_id,))
        
        affected_rows = cur.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    finally:
        cur.close()
        put_db_connection(conn)
    
    if affected_rows == 0:
        return jsonify({"error": "Project not found"}), 404
    
    status_message = "Updated successfully" if request.method == 'PUT' else "Deleted successfully"
    return jsonify({"status": status_message}), 200

if __name__ == '__main__':
    app.run(debug=True)