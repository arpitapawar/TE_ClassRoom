from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] ='Arp123@'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'web'
mysql = MySQL(app)


@app.route('/')
def logi():
    return render_template('login.html')

@app.route('/',methods=['POST','GET'])
def form():
    name = request.form['n']
    username=request.form['u']
    password=request.form['p']
    if username == " " or password == "" or name== "":
        return "All fields required"
    else:
        cur = mysql.connection.cursor()
        data = cur.execute("Select *from login where username='" + username + "' and password='" + password + "' and name= '" + name + "'")
        print(data)
        if data == 0:
            return "Username or password is wrong"
        else:
            mysql.connection.commit()
            cur.execute("Select user from login where username= ' " + username +" ' ")
            data2 = cur.fetchone()
            print(data2)
            if (data2):
                return render_template('classes.html')
            else:
                return render_template('students.html')
            return render_template('classes.html')

@app.route('/second')
def classes():
    if request.method=='GET':
        cur = mysql.connection.cursor()
        query = "Select *from Class"
        cur.execute(query)
        aclass=cur.fetchall()
        mysql.connection.commit()
        cur.close()
    return render_template('classes.html',aclass=aclass)

@app.route('/third',methods=['GET', 'POST'])
def create():
    if request.method=='POST':
        userDetails = request.form
        class1 = userDetails['class']
        sub = userDetails['subject']
        r = userDetails['room']
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO Class(Class,Subject,Room) VALUES(%s, %s,%s)",
            (class1, sub, r,))
        mysql.connection.commit()
        cur.close()
        return render_template('classes.html')
    return render_template('create.html')

@app.route('/fourth',methods=['GET', 'POST'])
def add_s():
    if request.method == 'POST':
        userDetails = request.form
        room = userDetails['room']
        cur = mysql.connection.cursor()
        cur.execute("Select *from class where Room='" + room + "'")
        data=cur.fetchall()
        print(data)
        return render_template('add_stu.html', data=data)
    return render_template('add.html')

@app.route('/fifth',methods=['GET', 'POST'])
def add_to_class():
    if request.method == 'POST':
        class1 = userDetails['class']
        sub = userDetails['subject']
        r = userDetails['room']
        add = request.form['add_students']
        cur = mysql.connection.cursor()
        cur.execute ("Select *from Class where Room='" + room + "'")
        data1 = cur.fetchall()
        print(data1)
        mysql.connection.commit()
        cur.close()
        return render_template('add_to_class.html', data1=data1)
    return render_template('add_to_class.html')

app.run(debug=True)
