from flask import Flask, request, render_template_string
import pyodbc

app = Flask(__name__)


conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"  #here type the name of your server
    "DATABASE=Students;" #here type the name of your database
    "Trusted_Connection=yes;" #if you are not using windows for connection then turn thid off and also add "USERNAME=NAME;" "PASSWORD=YOUR PASSWORD;"
)

#this is to confirm that the connection is okay
try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connected to the database!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)

#you can edit the html as per your needs

form_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Form</title>
</head>
<body>
    <h2>Enter Student Details</h2>
    <form method="POST">
        Name: <input type="text" name="name"><br><br>
        Class: <input type="text" name="class"><br><br>
        Roll No: <input type="number" name="roll_no"><br><br>
        Subject: <input type="text" name="subject"><br><br>
        <input type="submit" value="Submit">
    </form>
    {% if message %}
    <p style="color: green;">{{ message }}</p>
    {% endif %}
</body>
</html>
'''
# this part gets data from the website and upload it into the database

@app.route('/', methods=['GET', 'POST'])
def form():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        class_ = request.form['class']
        roll_no = request.form['roll_no']
        subject = request.form['subject']

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            #INSERT INTO {dbo.Students_data} here you can remove "dbo." if you are encountering an error
            cursor.execute("INSERT INTO dbo.Students_data (name, class, roll_no, subject) VALUES (?, ?, ?, ?)",
                           name, class_, roll_no, subject)
            conn.commit()
            cursor.close()
            conn.close()
            message = 'Data submitted successfully!'
        except Exception as e:
            message = f'Error: {str(e)}'

    return render_template_string(form_html, message=message)

if __name__ == '__main__':
    app.run(debug=True)
    # you can use "app.run(host='0.0.0.0', port=5000, debug=True)" instead of "app.run(debug=True)" if you want to run the website locally on any device connected to your wifi or whatever network
