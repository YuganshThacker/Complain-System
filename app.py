from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://yourdomain.com"]}})




app = Flask(__name__, static_folder='public', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

    from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__, static_folder='public', static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('public', path)

@app.route('/api/submit_complaint', methods=['POST'])
def submit_complaint():
    try:
        if 'description' not in request.form or 'department' not in request.form or 'image' not in request.files:
            return jsonify({'error': 'Missing description, department, or image'}), 400

        description = request.form['description']
        department = request.form['department']
        image = request.files['image']

        if image.filename == '':
            return jsonify({'error': 'No image selected'}), 400

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            new_complaint = Complaint(description=description, image_filename=filename, department=department)
            db.session.add(new_complaint)
            db.session.commit()

            return jsonify({'message': 'Complaint submitted successfully'}), 201

        return jsonify({'error': 'Error submitting complaint'}), 500
    except Exception as e:
        app.logger.error(f"Error submitting complaint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# ... rest of the code remains the same


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('public', path)

@app.route('/api/submit_complaint', methods=['POST'])
def submit_complaint():
    if 'description' not in request.form or 'department' not in request.form or 'image' not in request.files:
        return jsonify({'error': 'Missing description, department, or image'}), 400

    description = request.form['description']
    department = request.form['department']
    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        new_complaint = Complaint(description=description, image_filename=filename, department=department)
        db.session.add(new_complaint)
        db.session.commit()

        return jsonify({'message': 'Complaint submitted successfully'}), 201

    return jsonify({'error': 'Error submitting complaint'}), 500

@app.route('/api/complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    result = []
    for complaint in complaints:
        result.append({
            'id': complaint.id,
            'description': complaint.description,
            'image_filename': complaint.image_filename,
            'department': complaint.department,
            'status': complaint.status,
            'created_at': complaint.created_at.isoformat()
        })
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total = Complaint.query.count()
    pending = Complaint.query.filter_by(status='Pending').count()
    resolved = Complaint.query.filter_by(status='Resolved').count()

    return jsonify({
        'total': total,
        'pending': pending,
        'resolved': resolved
    })

@app.route('/api/resolve_complaint/<int:id>', methods=['PUT'])
def resolve_complaint(id):
    complaint = Complaint.query.get_or_404(id)
    complaint.status = 'Resolved'
    db.session.commit()
    return jsonify({'message': f'Complaint {id} marked as resolved'})

@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

    from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(_name_)
CORS(app)

# Configure MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "GJ27BP3993",  # Replace with your MySQL password
    "database": "college_complaints"
}

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MySQL Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Route to submit a complaint
@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    try:
        # Parse form data
        description = request.form['description']
        department = request.form['department']
        complaint_type = request.form['complaintType']
        submitted_by = request.form.get('submittedBy', 'Anonymous')
        
        # Handle file upload
        image = request.files.get('image')
        image_path = None
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO complaints (description, department, complaint_type, image_path, submitted_by)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (description, department, complaint_type, image_path, submitted_by))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Complaint submitted successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

# Route to get all complaints
@app.route('/complaints', methods=['GET'])
def get_complaints():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM complaints")
        complaints = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify(complaints), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)
    from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Mock Database (Replace with actual database implementation)
complaints = []

@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

    complaint = {
        'id': len(complaints) + 1,
        'description': data.get('description'),
        'department': data.get('department'),
        'complaint_type': data.get('complaint_type'),
        'image_path': data.get('image_path', None),
        'status': data.get('status', 'pending'),
        'submitted_by': data.get('submitted_by', 'Anonymous'),
        'created_at': datetime.now().isoformat()
    }
    complaints.append(complaint)
    return jsonify({'success': True, 'message': 'Complaint submitted successfully', 'complaint': complaint}), 201
@app.route('/complaints', methods=['GET'])
def get_complaints():
    return jsonify(complaints), 200
@app.route('/resolve-complaint/<int:complaint_id>', methods=['PUT'])
def resolve_complaint(complaint_id):
    for complaint in complaints:
        if complaint['id'] == complaint_id:
            complaint['status'] = 'resolved'
            return jsonify({'success': True, 'message': f'Complaint {complaint_id} resolved.'}), 200
    return jsonify({'success': False, 'message': 'Complaint not found.'}), 404
