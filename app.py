import sqlite3
import yaml
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 🚨 SAST VULNERABILITY 1: Hardcoded Secrets / Credentials
# Scanners will flag this as an exposed sensitive cryptographic key.
app.config['SECRET_KEY'] = "super-secret-admin-password-12345!"

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # 🚨 SAST VULNERABILITY 2: SQL Injection (No Parameterization)
    # Taint analysis tracks user input directly into the SQL string execution.
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query) 
    user = cursor.fetchone()
    
    return f"Welcome back, {user[0]}" if user else "Login Failed"

@app.route("/load-profile", methods=["POST"])
def load_profile():
    # 🚨 SAST VULNERABILITY 3: Insecure Deserialization / Unsafe Execution
    # yaml.load() allows arbitrary object instantiation when used without a Loader.
    user_config = request.data
    profile_data = yaml.load(user_config) 
    
    return f"Profile loaded for: {profile_data.get('name')}"

if __name__ == "__main__":
    app.run(debug=True)
