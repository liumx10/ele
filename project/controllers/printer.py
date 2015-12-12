# -*- coding: utf-8 -*-
from project import app
from functools  import wraps
from project.models import Relation

from flask import render_template, request, redirect
import json

import os
import apriori

@app.route('/', methods=['POST', 'GET'])
def start():
	if request.method == "POST":
		restaurant_id = request.form['restaurant_id']
		resp = app.make_response(redirect('/homepage'))
		resp.set_cookie("restaurant_id", value=str(restaurant_id))
		return resp
	return render_template('index.html')

from project.models.Relation import get_relations

@app.route("/homepage", methods=['get'])
def homepage():
	if "restaurant_id" not in request.cookies:
		return redirect('/')
	rid = request.cookies.get('restaurant_id')
	print rid
	foods = apriori.getRules(int(rid))
	return render_template('homepage.html', foods=foods)

@app.route('/count', methods=['get'])
def count():
	if 'restaurant_id' not in request.cookies:
		return redirect('/')
	rid = request.cookies.get('restaurant_id')

	data =  [{  "name": '包子',
                "y": 56.33,
                "drilldown": '包子'
            }, {
                "name": '水饺',
                "y": 24.03,
                "drilldown":  '水饺'
            }, {
                "name": '面条',
                "y": 10.38,
                "drilldown":  '面条',
            }, {
                "name": '哈哈',
                "y": 4.77,
                "drilldown": '哈哈'
            }, {
                "name": '馒头',
                "y": 0.91,
                "drilldown": '馒头'
            }, {
                "name": '其他',
                "y": 0.2,
                "drilldown": '其他'
            }]

	return render_template('count.html', data=data)

