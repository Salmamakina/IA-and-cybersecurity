from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS, cross_origin
import os
import mysql.connector
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler


# Create the Flask app
app = Flask(__name__, static_folder='cyber-guard', static_url_path='//cyber-guard')
CORS(app)  # Enable CORS for all routes


# Load the scaler and model
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="beylessenne",
    database="cyberguard"
)
cursor = db.cursor()

# Define a route for serving the Angular app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')

def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')




# Signup
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), email VARCHAR(255), password VARCHAR(255), role ENUM('admin', 'analyst'))")

@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    data = request.json
    print('Received data:', data)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    # Store the user information in the database
    cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)", (username, email, password, role))
    db.commit()
    return jsonify({'message': 'User registered successfully'})



# login
@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    print(email)
    # Query the database to check if the email and password are valid
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        user_dict = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'password': user[3],
            'role': user[4]
        }
        
        return jsonify({'role': user_dict['role']}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401



# Password-recovery
@app.route('/password-recovery', methods=['POST'])
def password_recovery():
    data = request.json
    email = data.get('email')
    print(email)
    # Query the database to retrieve the password for the given email
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result:
        password = result[0]
        print(password)
        # Return the password as part of the response
        return jsonify({'message': f'Your password is: {password}'}), 200
    else:
        return jsonify({'error': 'Email not found'}), 404





# Contact
cursor.execute("CREATE TABLE IF NOT EXISTS contact (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), message TEXT)")

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    print(message)
    # Store the contact message in the database
    cursor.execute("INSERT INTO contact (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
    db.commit()
    return jsonify({'message': 'Contact message received successfully'})



# feedback
cursor.execute("CREATE TABLE IF NOT EXISTS feedback (id INT AUTO_INCREMENT PRIMARY KEY, message TEXT)")

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    message = data.get('message')
    print(message)
    # Store the feedback message in the database
    cursor.execute("INSERT INTO feedback (message) VALUES (%s)", (message,))
    db.commit()
    return jsonify({'message': 'Feedback received successfully'})



@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    print("Received JSON data:", data)  # Debug statement

    try:
        features = np.array(data['features']).reshape(1, -1)
        print("Reshaped features:", features)  # Debug statement

        # Ensure scaler is a StandardScaler object
        if not hasattr(scaler, 'transform'):
            raise ValueError('Scaler object is not a valid transformer.')

        features_scaled = scaler.transform(features)
        print("Scaled features:", features_scaled)  # Debug statement

        rf_probs = rf_model.predict_proba(features_scaled)
        rf_prediction = rf_model.predict(features_scaled)[0]

        response = {
            'RandomForest': int(rf_prediction),
            'Probabilities': rf_probs.tolist()
        }
        print(response)
        return jsonify(response)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 400
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
