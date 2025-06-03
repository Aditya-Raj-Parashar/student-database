import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  # Or just 'localhost' if no instance name
    "DATABASE=Students;"
    "Trusted_Connection=yes;"
)



try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT DB_NAME();")
    db_name = cursor.fetchone()[0]
    print(f"✅ Connected to database: {db_name}")
    conn.close()
except Exception as e:
    print("❌ Error:", e)
