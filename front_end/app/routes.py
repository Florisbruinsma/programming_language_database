from flask import render_template
from app import app
import requests
import json

test_json = '''
{
	"programmingLanguage": [{
		"name": "JavaScript",
		"application": "backend",
		"framework": [
			"Angular",
			"ReactJs",
			"React Native"
		],
		"compatible": [
			"HTML",
			"Java"
		]
	}, {
		"name": "PHP",
		"application": "fullstack",
		"framework": [
			"Symphony"
		],
		"compatible": [
			"HTML"
		]
	}]
}
'''
# todo
# generate request get link
# convert json to table
def get_json():
    params = {
    'api_key': '{API_KEY}',
    }
    r = requests.get(
        'http://ip.jsontest.com/',
        params=params)
    return json.loads(r.text)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Floris'}
    get_json()
    return render_template('index.html', title='Home', user=user, table_data = json.loads(test_json))

@app.route('/add')#get the form
def add():
    return render_template('add.html', title='Add item')

@app.route('/delete')
def delete():
    user = {'username': 'Floris'}
    return render_template('index.html', title='Home', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)