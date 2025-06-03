import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

def test_database_connection():
    """Test database connection and display detailed information"""
    print("🔍 Testing database connection...")
    print("-" * 50)
    
    # Display configuration (without sensitive data)
    print(f"Server: {os.getenv('DB_SERVER', 'localhost')}")
    print(f"Database: {os.getenv('DB_NAME', 'Students')}")
    print(f"Driver: {os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')}")
    print(f"Authentication: {'Windows Authentication' if os.getenv('DB_TRUSTED_CONNECTION', 'yes').lower() == 'yes' else 'SQL Server Authentication'}")
    print("-" * 50)
    
    try:
        # Get connection string
        conn_str = get_connection_string()
        
        # Test connection
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Get database information
        cursor.execute("SELECT DB_NAME();")
        db_name = cursor.fetchone()[0]
        
        cursor.execute("SELECT @@VERSION;")
        sql_version = cursor.fetchone()[0].split('\n')[0]
        
        cursor.execute("SELECT GETDATE();")
        current_time = cursor.fetchone()[0]
        
        # Test if our table exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'dbo' 
            AND TABLE_NAME = 'Students_data'
        """)
        table_exists = cursor.fetchone()[0] > 0
        
        # Get table info if it exists
        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM dbo.Students_data;")
            record_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        # Display success information
        print("✅ DATABASE CONNECTION SUCCESSFUL!")
        print(f"📊 Connected to: {db_name}")
        print(f"🖥️  SQL Server: {sql_version}")
        print(f"⏰ Server time: {current_time}")
        print(f"📋 Students_data table: {'✅ EXISTS' if table_exists else '❌ NOT FOUND'}")
        
        if table_exists:
            print(f"📈 Records in table: {record_count}")
            
            if record_count > 0:
                # Show sample data
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute("SELECT TOP 3 name, class, roll_no, subject FROM dbo.Students_data ORDER BY id DESC;")
                recent_records = cursor.fetchall()
                cursor.close()
                conn.close()
                
                print("\n🔍 Recent records:")
                for record in recent_records:
                    print(f"   - {record[0]} | Class: {record[1]} | Roll: {record[2]} | Subject: {record[3]}")
        else:
            print("\n⚠️  To create the Students_data table, run this SQL:")
            print("""
            CREATE TABLE dbo.Students_data (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(100) NOT NULL,
                class NVARCHAR(50) NOT NULL,
                roll_no INT NOT NULL,
                subject NVARCHAR(100) NOT NULL,
                created_at DATETIME DEFAULT GETDATE()
            );
            """)
        
        return True
        
    except Exception as e:
        print("❌ DATABASE CONNECTION FAILED!")
        print(f"Error: {str(e)}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Ensure SQL Server is running")
        print("2. Check server name and database name")
        print("3. Verify ODBC Driver 17 is installed")
        print("4. Check Windows Authentication permissions")
        print("5. Ensure the 'Students' database exists")
        
        return False

if __name__ == "__main__":
    test_database_connection()