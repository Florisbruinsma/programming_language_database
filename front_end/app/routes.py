from flask import render_template, request, redirect, url_for
from app import app
import requests
import json
import certifi
import urllib3
import os
import math
import random

PAGINATION_SIZE = 3
ROWS_PER_PAGE = 3
PRIME_COLOR = "#{:06x}".format(random.randint(0, 0xFFFFFF))#"#555555"
SEC_COLOR = "#{:06x}".format(random.randint(0, 0xFFFFFF))#"#398AA4"

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=2.0, read=2.0),#max time for connection is 2 sec and for read is 2 sec
    retries=urllib3.Retry(3, redirect=False)#retry maximum of 3 times to get the data, and disable being redirected
    )
API_LINK = 'https://localhost:44351/api/programminglanguages'

def seed_database():
    file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'programmingLanguage.json')
    with open(file_dir) as json_file:
        seed_data = json.load(json_file)
        for seed in seed_data:
            requests.post(url = API_LINK, json = seed,  verify=False)

def pagination(table_data, page):
    rows = len(table_data)
    total_pages = math.ceil(rows/ROWS_PER_PAGE)
    pages = [1]
    if(page > total_pages):
        print("page to far")
        # TODO update the page in the href?
        page = total_pages
    if(page == 1):
        pages.extend([1,2,3,total_pages])
    elif(page == total_pages):
        pages.extend([total_pages-2,total_pages-1,total_pages,total_pages])
    else:
        pages.extend([page-1,page,page+1,total_pages])
    table_data = table_data[(page-1)*ROWS_PER_PAGE:(page)*ROWS_PER_PAGE]
    return table_data, pages

@app.route('/')
def start():
    return redirect(url_for('index', page=1))

@app.route('/index/<page>')#main page, show the database and actions you can take
def index(page):
    table_data = requests.get(API_LINK, verify=False).json()
    if(table_data == []):
        seed_database()
        table_data = requests.get(API_LINK, verify=False).json()
    table_data, pages = pagination(table_data, int(page))
    return render_template('index.html', title='Home', table_data = table_data, pages = pages, prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

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
    return render_template('add.html', title='Post', post_info=responce.reason)

@app.route('/delete')
def delete():
    table_data = requests.get(API_LINK, verify=False).json()
    return render_template('delete.html', title='Delete', table_data = table_data, prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

@app.route("/delete/post", methods=["GET", "POST"])#post the delete statement to the api
def delete_post():
    id = request.form['delete_id']

    responce = requests.delete(url = API_LINK + "/" + id , verify=False)
    print(responce)#TODO place this responce somewhere on screen
    table_data = requests.get(API_LINK, verify=False).json()
    return render_template('delete.html', title='Post', table_data = table_data, prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

@app.route('/edit')
def edit():
    table_data = requests.get(API_LINK, verify=False).json()
    return render_template('edit.html', title='Edit', table_data = table_data, prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

@app.route('/edit/form', methods=["GET", "POST"])
def edit_form():
    # give table data to autofill
    id = request.form['edit_id']
    table_data = requests.get(API_LINK + "/" + id, verify=False).json()
    return render_template('edit_form.html', title='Edit', table_data = table_data)

@app.route('/edit/post', methods=["GET", "POST"])
def edit_form_post():
    data = {
    'id': int(request.form['id']),
    'name' : request.form['name'],
    'application' : request.form['application'],
    'framework' : request.form['framework'],
    'compatible' : request.form['compatible'],
    }
    responce = requests.put(url = API_LINK + "/" + str(data["id"]), json = data,  verify=False)
    return render_template('edit_form.html', title='Edit', table_data = data ,post_info=responce.reason)

@app.route('/style')
def style():
    return render_template('style.html', title='Edit', prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

@app.route('/style/post', methods=["GET", "POST"])
def style_post():
    global PRIME_COLOR
    global SEC_COLOR
    PRIME_COLOR = request.form['prime_color']
    SEC_COLOR = request.form['sec_color']
    return render_template('style.html', title='Edit', prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

@app.route('/advanced_search')
def advanced_search():
    return render_template('advanced_search.html', title='Search')

@app.route('/advanced_search/post', methods=["GET", "POST"])
def advanced_search_post():
    return render_template('advanced_search.html', title='Search')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)