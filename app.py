import os
from flask import Flask, request, render_template_string
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Flask configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Database connection string using environment variables
def get_connection_string():
    """Build database connection string from environment variables"""
    driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    server = os.getenv('DB_SERVER', 'localhost')
    database = os.getenv('DB_NAME', 'Students')
    trusted_connection = os.getenv('DB_TRUSTED_CONNECTION', 'yes')
    
    conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
    
    if trusted_connection.lower() == 'yes':
        conn_str += "Trusted_Connection=yes;"
    else:
        username = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        if username and password:
            conn_str += f"UID={username};PWD={password};"
        else:
            raise ValueError("DB_USERNAME and DB_PASSWORD must be set when not using trusted connection")
    
    return conn_str

# Get connection string
conn_str = get_connection_string()

# Test database connection on startup
def test_connection():
    """Test database connection and print status"""
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT DB_NAME();")
        db_name = cursor.fetchone()[0]
        print(f"✅ Connected to database: {db_name}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

# Test connection on startup
test_connection()

# HTML form template
form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h2 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input[type="text"]:focus, input[type="number"]:focus {
            border-color: #4CAF50;
            outline: none;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .message {
            padding: 10px;
            margin: 20px 0;
            border-radius: 5px;
            text-align: center;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Enter Student Details</h2>
        <form method="POST">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="class">Class:</label>
                <input type="text" id="class" name="class" required>
            </div>
            
            <div class="form-group">
                <label for="roll_no">Roll No:</label>
                <input type="number" id="roll_no" name="roll_no" min="1" required>
            </div>
            
            <div class="form-group">
                <label for="subject">Subject:</label>
                <input type="text" id="subject" name="subject" required>
            </div>
            
            <input type="submit" value="Submit Student Data">
        </form>
        
        {% if message %}
            <div class="message {{ message_type }}">
                {{ message }}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

def validate_form_data(name, class_, roll_no, subject):
    """Validate form input data"""
    errors = []
    
    if not name or not name.strip():
        errors.append("Name is required")
    elif len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long")
    
    if not class_ or not class_.strip():
        errors.append("Class is required")
    
    if not roll_no:
        errors.append("Roll number is required")
    else:
        try:
            roll_no_int = int(roll_no)
            if roll_no_int <= 0:
                errors.append("Roll number must be a positive number")
        except ValueError:
            errors.append("Roll number must be a valid number")
    
    if not subject or not subject.strip():
        errors.append("Subject is required")
    
    return errors

@app.route('/', methods=['GET', 'POST'])
def form():
    message = ''
    message_type = ''
    app_name = os.getenv('APP_NAME', 'Student Form Application')
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        class_ = request.form.get('class', '').strip()
        roll_no = request.form.get('roll_no', '')
        subject = request.form.get('subject', '').strip()
        
        # Validate form data
        validation_errors = validate_form_data(name, class_, roll_no, subject)
        
        if validation_errors:
            message = '; '.join(validation_errors)
            message_type = 'error'
        else:
            try:
                # Connect to database and insert data
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                
                # Use parameterized query to prevent SQL injection
                cursor.execute(
                    "INSERT INTO dbo.Students_data (name, class, roll_no, subject) VALUES (?, ?, ?, ?)",
                    name, class_, int(roll_no), subject
                )
                
                conn.commit()
                cursor.close()
                conn.close()
                
                message = f'Student data for {name} submitted successfully!'
                message_type = 'success'
                
            except Exception as e:
                message = f'Database error: {str(e)}'
                message_type = 'error'
                print(f"Database error: {e}")  # Log error for debugging

    return render_template_string(
        form_html, 
        message=message, 
        message_type=message_type,
        app_name=app_name
    )

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        conn = pyodbc.connect(conn_str)
        conn.close()
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}, 500

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting {os.getenv('APP_NAME', 'Student Form Application')}")
    print(f"Server: http://{host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)