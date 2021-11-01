from flask import Flask
from flask import render_template, redirect, url_for, request

from database import Database

from routes.api import api


from datetime import datetime

from pytz import timezone,utc

import requests

app = Flask(__name__)

app.register_blueprint(api)


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
def index():
    entries = requests.get('https://protected-spire-82809.herokuapp.com/entries').json()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        utc = datetime.now(timezone('UTC'))
        p = utc.astimezone(timezone('US/Pacific'))
        data = {
            'title': request.form['title'],
            'post': request.form['post'],
            'time': p.strftime(' %I:%M %p'),

            'date': p.strftime('%Y-%m-%d')
        }
        # Database.insert_record(data)
        requests.post('https://protected-spire-82809.herokuapp.com/post', data=data)
        return redirect(url_for('index'))

    return render_template('add_entry.html')


@app.route('/clear')
def delete_entries():
    # Database.delete_all_records()
    requests.delete('https://protected-spire-82809.herokuapp.com/delete')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True)
