from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_mysqldb import MySQL
from werkzeug import secure_filename
from bcrypt import *
import MySQLdb.cursors
import re
import os


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.secrete_key = '1l0v3sh3an0r3'
#sess = session(    )

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'TenderHire'
app.config['UPLOAD_PATH'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = '.pdf'



mysql = MySQL(app)
@app.route('/Customer')
def customer():
    while True:
        User = "Customer"
        register(User)
        return redirect(url_for('register'))
    return render_template('customer.html')

@app.route('/AvailableTenders',  methods=['GET', 'POST'])
def tenders():
    cursor =  mysql.connection.cursor()
    cursor.execute("SELECT *  FROM TenderDetails")
    data = cursor.fetchall()
    return render_template('availableTenders.html', data=data)

@app.route('/')
def home():
    return render_template('index.html')

def checkFile(fileName):
    if '.' not in fileName:
        return False
    extension = fileName.rsplit('.', 1)[1]
    if extension in app.config['ALLOWED_EXTENSIONS']:
        return True
    else:
        return False

@app.route('/AvailableTenders')
def uploadFile():
    if request.method == 'POST':
        formData = request.form
        if request.files:
            File = request.files['File']
            if File.filename == "":
                print("No file name")
                redirect(url_for('contractor'))
            if checkFile(File.filename):
                fileName = secure_filename(File.filename)
                File.save(os.path.join(app.config['UPLOAD_PATH'], fileName))
                print("file saved succesfully")
                return redirect(url_for('contractor'))
            else:
                print ("extension not allowes")
                return redirect(url_for('contractors'))
            return formData

@app.route('/download') 
def downloadFile():
    path = 'uploads/vacancies.pdf'
    return send_file(path, as_attachment=True)

@app.route('/Login', methods=['GET', 'POST'])
def login():
    msg = ''
    #crete variables if the username, password are in the form and the request is post.
    if request.method == 'POST' and 'Email' in request.form and 'Password' in request.form:
        Email = request.form['Email']
        Password = request.form['Password']
        #check if the username and the password match the details in the msql table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE Email = %s and Password = %s', (Email, Password))
        #fetch the record and return the results
        account = cursor.fetchone()
        if account:
            return redirect(url_for('home'))

        else:
            msg = 'Incorect email or password'
            return redirect(url_for('login'))

    return render_template('login.html', msg='')

def logout():
    return redirect(url_for('login'))

@app.route('/signup',methods=['GET', 'POST'])
def register(User):     
    if request.method == 'POST':
        formDetails = request.form
        Email = formDetails['Email']
        Username = formDetails['Username']
        Password = formDetails['Password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO %s (Email, Username, Password) VALUES(%s, %s, %s)", (User, Email, Username, Password))
        mysql.connection.commit()
        cursor.close()
        while True:
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/contractor', methods=['GET', 'POST'])
def contractor():
    while True:
        User = "Supplier"
        return redirect(url_for('register'))

    if request.method == 'POST':
        formDetails = request.form
        Company = formDetails['Company']
        Country = formDetails['Country']
        Tender = formDetails['Name']
        Category = formDetails['Category']
        Bid = formDetails['Amount']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO TenderDetails (Company, Country, Tender, Category,Bid) VALUES(%s, %s, %s, %s, %s)', (Company, Country, Tender, Category, Bid))
        mysql.connection.commit()
        cursor.close()
    return render_template('contractor.html')

if __name__ == '__main__':
 app.run(debug=True)
