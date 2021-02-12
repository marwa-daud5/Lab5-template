from flask import Flask, render_template,request

import sqlite3

app = Flask('app')

## Table Schema
## username[text]| password [text]| first_name [text] | last_name [text]| email [text]
## --------------| ---------------|-------------------|-----------------|--------------|
## user1         | password1.     | Lucas             | Chaufournier.   | luccas@gmail.com |

@app.route('/')
def home():
  # Render the homepage 
  return render_template("index.html")

@app.route('/login',methods=['GET', 'POST'])
def login():
  user_message = ""
  conn = sqlite3.connect("example.db")
  c = conn.cursor()

  c.execute("SELECT username, password FROM users WHERE username = ? and password = ?", (request.form["username"], request.form["password"]))

  results = c.fetchone();

  if results is None:
     user_message = "You don't have an account"
  
  else:
    user_message = "Welcome " + request.form["username"]

  conn.close()
  

  # Modify this to select the username and password from the database and compare against what the user entered. Return the loggedin.html page with a custom error message if it doesnt match otherwise dispaly "Welcome <<USERNAME>>"

  #Render the loggedin template.
  return render_template('loggedin.html',message=user_message)

@app.route('/register',methods=['GET', 'POST'])
def register():
 
  
  
  if request.method == 'POST':
    ## Modify this to connect to the database and insert a new users with fields from the form. Return the registered.html page to show success._
    user_message = ""
    conn = sqlite3.connect("example.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (request.form["username"], request.form["password"], request.form["firstname"],request.form["lastname"], request.form["email"]))
  

    c.execute("SELECT username, email FROM users WHERE username = ?, email = ?", (request.form["username"], request.form["email"]))

    results = c.fetchall()
    for result in results:
      print(result)

    if len(results) == 1:
      conn.commit()
      conn.close()
      user_message = "User " + request.form["username"] + " registered"
      return render_template('registered.html', message=user_message)
  
    else:
      user_message = request.form["username"] + " already has an account!"
      conn.close()
      return render_template('registered.html',message=user_message)
 
    

    ## Otherwise return register page on get request
  return render_template('register.html')

app.run(host='0.0.0.0', port=8080)