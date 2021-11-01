from flask import Blueprint,request

from database import Database
from datetime import datetime

from pytz import timezone,utc

import json

api=Blueprint('api', __name__,template_folder='templates')

@api.route('/entries')

def get_all_entries():
	entries=Database.get_records()
	for entry in entries:
		entry['_id']=str(entry['_id'])
	return json.dumps(entries)


@api.route('/delete', methods=['DELETE'])

def delete_all_entries():
	Database.delete_all_records()
	return 'Record successfully deleted!'


@api.route('/post',methods=['POST'])

def add_entry():
	utc = datetime.now(timezone('UTC'))
	p = utc.astimezone(timezone('US/Pacific'))
	doc={
	'title':request.form['title'],
	'post':request.form['post'],
	'time':  p.strftime(' %I:%M %p') ,
	'date':p.strftime('%Y-%m-%d')
	}

	Database.insert_record(doc)
	return 'Record successfully added'