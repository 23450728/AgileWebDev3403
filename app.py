
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__, template_folder='Templates', static_folder='Static')
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'hard to guess string'

connect = sqlite3.connect('database.db') 

connect.execute( 
    'CREATE TABLE IF NOT EXISTS USER (username TEXT, password TEXT, email TEXT)') 

connect.execute(
    'CREATE TABLE IF NOT EXISTS POST (title TEXT, description TEXT)'
)

@app.route('/')
@app.route('/Main')
def main():
    #
    #connect = sqlite3.connect('database.db')
    #cursor = connect.cursor()
    #cursor.execute('SELECT * FROM POST')
    #data=cursor.fetchall()
    #return render_template('Main.html', data=data)
    return render_template('Main.html')

@app.route('/login')
def login_page():
   return render_template('login.html')


@app.route('/Create Post', methods=['GET','POST'])
def Create_post():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        with sqlite3.connect("database.db") as POST: 
            cursor = POST.cursor() 
            cursor.execute("INSERT INTO POST (title,description) VALUES (?,?)", (title, description)) 
            POST.commit()
    return render_template('Create Post.html')


@app.route('/Profile')
def profile():
    return render_template('Profile.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        with sqlite3.connect("database.db") as users: 
            cursor = users.cursor() 
            cursor.execute("INSERT INTO USER (username,password,email) VALUES (?,?,?)", (username, password, email)) 
            users.commit()
    return render_template('signup.html')

@app.route('/Forgot Password')
def forgotPassword():
    return render_template('Forgot Password.html')