# Student Form Application

A simple Flask web application that allows users to submit student information through a web form and stores the data in a SQL Server database.

## Features

- Clean web interface for entering student details
- Real-time form submission with success/error feedback
- SQL Server database integration
- Input validation and parameterized queries for security

## Prerequisites

Before running this application, make sure you have:

- Python 3.7 or any big version
- SQL Server 
- ODBC Driver 17 for SQL Server(SSMS)

## Installation

1. **Clone the repository**
   ```bash
   yet to be added
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. **Create the database**
   - Open SQL Server Management Studio (SSMS)
   - Create a new database named `Students`

2. **Create the table**
   ```sql
   USE Students;
   
   CREATE TABLE dbo.Students_data (
       id INT IDENTITY(1,1) PRIMARY KEY,
       name NVARCHAR(100) NOT NULL,
       class NVARCHAR(50) NOT NULL,
       roll_no INT NOT NULL,
       subject NVARCHAR(100) NOT NULL,
       created_at DATETIME DEFAULT GETDATE()
   );
   ```

## Configuration

1. **Environment Variables (Recommended)**
   - Copy `.env.example` to `.env`
   - Update the database connection details in `.env`:
   ```
   DB_SERVER=localhost
   DB_NAME=Students
   DB_TRUSTED_CONNECTION=yes
   ```

2. **Direct Configuration (Alternative)**
   - If not using environment variables, update the connection string in `app.py`:
   ```python
   conn_str = (
       "DRIVER={ODBC Driver 17 for SQL Server};"
       "SERVER=your_server_name;"
       "DATABASE=Students;"
       "Trusted_Connection=yes;"
   )
   ```

## Running the Application

1. **Test database connection**
   ```bash
   python connection.py
   ```
   You should see: `✅ Connected to database: Students`

2. **Start the Flask application**
   ```bash
   python app.py
   ```

3. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Fill out the student form and submit

## Usage

The application provides a simple form with the following fields:
- **Name**: Student's full name
- **Class**: Student's class/grade
- **Roll No**: Student's roll number (numeric)
- **Subject**: Subject name

After submission, the data is stored in the SQL Server database and a success message is displayed.

## File Structure

```
student-form-app/
│
├── app.py              # Main Flask application
├── connection.py       # Database connection test
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure SQL Server is running
   - Verify server name and database name
   - Check if ODBC Driver 17 is installed

2. **ODBC Driver Not Found**
   - Download and install [Microsoft ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

3. **Permission Denied**
   - Ensure your Windows user has access to SQL Server
   - Or configure SQL Server authentication with username/password

### Network Access

To allow access from other devices on your network:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## Security Considerations

- Input validation is implemented through parameterized queries
- For production deployment:
  - Set `debug=False`
  - Use HTTPS
  - Implement proper authentication
  - Add CSRF protection
  - Use environment variables for all sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Search existing issues on GitHub
3. Create a new issue with detailed information about your problem

## Future Enhancements

- [ ] Add data validation on the frontend
- [ ] Implement student data viewing/editing functionality
- [ ] Add search and filter capabilities
- [ ] Export data to CSV/Excel
- [ ] Add user authentication
- [ ] Implement RESTful API endpoints