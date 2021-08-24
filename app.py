#coding: utf-8
from flask import Flask, request, make_response
import requests
import os
app = Flask(__name__, static_folder='.')
host=os.environ['DB_HOST']
sql = 'CREATE TABLE IF NOT EXISTS nametbl ( firstname CHAR(50), lastname CHAR(50) NOT NULL PRIMARY KEY)' 
print(sql)
url = "http://%s" % (host)
payload = {'sql':sql}
result = requests.post(url, data=payload)
print(result)
@app.route('/')
def index():
    html = '<html><body>'
    html = html + 'First name search system.'
    html = html + '<form action="/search" method="post">'
    html = html + '<div>'
    html = html + '<label for="lastname">Enter Last name: </label>'
    html = html + '<input type="text" name="lastname">'
    html = html + '</div>'
    html = html + '<div class="form-example">'
    html = html + '<input type="submit" value="Search">'
    html = html + '</div>'
    html = html + '</form>'
    html = html + '<a href="/register">Register new name</a>'
    html = html + '</body></html>'
    return(html)
@app.route('/register')
def register():
    html = '<html><body>'
    html = html + '<form action="/regdb" method="post">'
    html = html + '<div>'
    html = html + '<label for="lastname">Enter Last name: </label>'
    html = html + '<input type="text" name="lastname">'
    html = html + '</div>'
    html = html + '<div>'
    html = html + '<label for="firstname">Enter First name: </label>'
    html = html + '<input type="text" name="firstname">'
    html = html + '</div>'
    html = html + '<div>'
    html = html + '<input type="submit" value="Register">'
    html = html + '</div>'
    html = html + '</form>'
    html = html + '</body></html>'
    return(html)
@app.route('/search', methods=['POST'])
def search():
    lastname = request.form['lastname']
    if lastname == "":
        html = '<html><body>'
        html = html + 'Invalid imput.<br>'
        html = html + '<a href="/">return</a>'
        html = html + '</body></html>'
        return(html)
    host=os.environ['DB_HOST']
    sql = 'SELECT firstname FROM nametbl WHERE lastname = "%s"' %(lastname) 
    print(sql)
    url = "http://%s" % (host)
    payload = {'sql':sql}
    result = requests.post(url, data=payload)
    print(result)
    return(result.text)
@app.route('/regdb', methods=['POST'])
def regdb():
    lastname = request.form['lastname']
    firstname = request.form['firstname']
    if lastname == "" or firstname == "":
        html = '<html><body>'
        html = html + 'Invalid imput.<br>'
        html = html + '<a href="/">return</a>'
        html = html + '</body></html>'
        return(html)
    host=os.environ['DB_HOST']
    sql = 'INSERT INTO nametbl (firstname,lastname) VALUES("%s", "%s") ON DUPLICATE KEY UPDATE firstname = "%s"' %(firstname, lastname, firstname) 
    print(sql)
    url = "http://%s" % (host)
    payload = {'sql':sql}
    result = requests.post(url, data=payload)
    print(result)
    html = '<html><body>'
    html = html + '%s, %s has been registerd!!<br>' %(firstname, lastname)
    html = html + '<a href="/">return</a>'
    html = html + '</body></html>'
    return(html)
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=8081) 
