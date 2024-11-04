from flask import Flask, render_template, request, redirect
import mysql.connector
from flask_bcrypt import Bcrypt
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
bcrypt = Bcrypt(app)

# Configure MySQL connection
db = mysql.connector.connect(
    host="cse335-fall-2024.c924km8o85q2.us-east-1.rds.amazonaws.com",
    user="v0igir01",
    password="2c3e13850d",
    database="student_v0igir01_db"
)

cursor = db.cursor()


# Home page
@app.route('/')
def index():
    cursor.execute(
        "SELECT ID, MovieName, Rating, Runtime, Genre, Metascore, Plot, Directors, Stars, Votes, Gross, Link FROM Movies"
    )
    movies = cursor.fetchall()
    return render_template('home.html', movies=movies)


# Search functionality
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    if query:
        cursor.execute(
            """
            SELECT ID, MovieName, Rating, Runtime, Genre, Metascore, Plot, Directors, Stars, Votes, Gross, Link 
            FROM Movies 
            WHERE MovieName LIKE %s OR Directors LIKE %s OR Stars LIKE %s
            """,
            (f'%{query}%', f'%{query}%', f'%{query}%')
        )
        movies = cursor.fetchall()
        return render_template('home.html', movies=movies, search_query=query)
    else:
        return redirect('/')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
