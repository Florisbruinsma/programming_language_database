from flask import render_template, request, redirect, url_for
from app import app
import requests
import json
import certifi
import urllib3
import os
import math
import random
# TODO
# make a database check where I merge everything with the same name
# in advanced search be able to sleect and or or for any of the fields
# when you change random style, stay on same page
# index link like index/page_number/column_number/ascending/descending
#   column number can also be id for standard sort
PAGINATION_SIZE = 3
ROWS_PER_PAGE = 5
PRIME_COLOR = "#{:06x}".format(random.randint(0, 0xFFFFFF))#"#555555"
SEC_COLOR = "#{:06x}".format(random.randint(0, 0xFFFFFF))#"#398AA4"

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where(),
    timeout=urllib3.Timeout(connect=2.0, read=2.0),#max time for connection is 2 sec and for read is 2 sec
    retries=urllib3.Retry(3, redirect=False)#retry maximum of 3 times to get the data, and disable being redirected
    )
API_LINK = 'https://localhost:44386/api/programmingLanguages'

def seed_database():
    file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'programmingLanguage.json')
    with open(file_dir) as json_file:
        seed_data = json.load(json_file)
        for seed in seed_data:
            requests.post(url = API_LINK, json = seed,  verify=False)

def pagination(table_data, page):
    page_amount = 0
    rows = len(table_data)
    total_pages = math.ceil(rows/ROWS_PER_PAGE)
    pages = [1]
    if(page > total_pages):
        print("page to far")
        # TODO update the page in the href?
        page = total_pages
    if(page < 1):
        page = 1
    if(page == 1):
        page_number = 1
        while(page_number <= total_pages and page_amount < PAGINATION_SIZE):
            pages.append(page_number)
            page_number += 1
            page_amount += 1
    elif(page == total_pages):
        page_number = total_pages - PAGINATION_SIZE + 1
        if(page_number<1):
            page_number = 1
        while(page_number <= total_pages and page_amount < PAGINATION_SIZE):
            pages.append(page_number)
            page_number += 1
            page_amount += 1
    else:
        pages.extend([page-1,page,page+1])
    pages.append(total_pages)
    table_data = table_data[(page-1)*ROWS_PER_PAGE:(page)*ROWS_PER_PAGE]
    return table_data, pages

@app.route('/')
@app.route('/index/<page>')
@app.route('/index/<page>/<query>')
@app.route('/index/<page>/<query>/<column_name>')
@app.route('/index/<page>/<query>/<column_name>/<sorting_order>/')#main page, show the database and actions you can take
def index(page = 1, query = '*', column_name = 'id', sorting_order = "ASC"):
    table_data = requests.get(API_LINK + "/GetByAll/" + query , verify=False).json()
    if(table_data == []):
        seed_database()
        table_data = requests.get(API_LINK, verify=False).json()
    table_data, pages = pagination(table_data, int(page))
    return render_template('index.html',query = query, title='Home', table_data = table_data, pages = pages, prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

@app.route("/add", methods=["GET", "POST"])#post the form to the api
def add():
    responce = None
    if request.method == 'POST':
        data = {
            'name' : request.form['name'],
            'application' : request.form['application'],
            'framework' : request.form['framework'],
            'compatible' : request.form['compatible'],
        }
        responce = requests.post(url = API_LINK, json = data,  verify=False).reason
    return render_template('add.html', title='Add', post_info=responce)

@app.route("/delete", methods=["GET", "POST"])#post the delete statement to the api
def delete():
    if request.method == 'POST':
        id = request.form['delete_id']
        requests.delete(url = API_LINK + "/" + id , verify=False)
    table_data = requests.get(API_LINK, verify=False).json()
    return render_template('delete.html', title='Delete', table_data = table_data, prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

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

@app.route('/edit/post/', methods=["GET", "POST"])#TODO merge with above by usin /<id>
def edit_form_post():
    data = {
    'id': request.form['id'],
    'name' : request.form['name'],
    'application' : request.form['application'],
    'framework' : request.form['framework'],
    'compatible' : request.form['compatible'],
    }
    responce = requests.put(url = API_LINK + "/" + data["id"], json = data,  verify=False).reason
    return render_template('edit_form.html', title='Edit', table_data = data ,post_info=responce)

@app.route('/style', methods=["GET", "POST"])
def style():
    if request.method == 'POST':
        global PRIME_COLOR
        global SEC_COLOR
        PRIME_COLOR = request.form['prime_color']
        SEC_COLOR = request.form['sec_color']
    return render_template('style.html', title='Edit', prime_color = PRIME_COLOR, sec_color = SEC_COLOR)

@app.route('/style_rand')
def style_rand():
    global PRIME_COLOR
    global SEC_COLOR
    PRIME_COLOR = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    SEC_COLOR = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return redirect(url_for('index', page=1))

@app.route('/search', methods=["GET", "POST"])
@app.route('/search/<page>', methods=["GET", "POST"])
def search(page = 1):
    if request.method == 'POST':
        query = request.form['search_query']#TODO make sure that this cannot be empty
    if(query == ""):
        query = "*"
    return redirect(url_for('index', query=query, page = page))
    # return render_template('advanced_search.html', title='Search')

@app.route('/advanced_search')
def advanced_search():
    return render_template('advanced_search.html', title='Search')

@app.route('/advanced_search/post', methods=["GET", "POST"])
def advanced_search_post():
    return render_template('advanced_search.html', title='Search')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)