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

