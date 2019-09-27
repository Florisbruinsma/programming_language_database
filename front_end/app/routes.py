from flask import render_template, request
from app import app
import requests
import json
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
API_LINK = 'https://localhost:44351/api/programminglanguages'

@app.route('/')
@app.route('/index')#main page, show the database and actions you can take
def index():
    table_json = requests.get(API_LINK, verify=False)
    return render_template('index.html', title='Home', table_data = table_json.json())

@app.route('/add')#form to add to database
def add():
    return render_template('add.html', title='Add')

@app.route("/add/post", methods=["GET", "POST"])#post the form to the api
def add_post():
    data = {
        'name' : request.form['name'],
        'application' : request.form['application'],
        'framework' : request.form['framework'],
        'compatible' : request.form['compatible'],
    }
    responce = requests.post(url = API_LINK, json = data,  verify=False)
    return render_template('add.html', title='Post', post_info=responce.reason)#TODO add some text at botum of page to show succes or failure

@app.route('/delete')
def delete():
    table_json = requests.get(API_LINK, verify=False)
    return render_template('delete.html', title='Delete', table_data = table_json.json())

@app.route("/delete/post", methods=["GET", "POST"])#post the delete statement to the api
def delete_post():
    id = request.form['delete_id']

    responce = requests.delete(url = API_LINK + "/" + id , verify=False)
    print(responce)
    table_json = requests.get(API_LINK, verify=False)
    return render_template('delete.html', title='Post', table_data = table_json.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)