# -*- coding: utf-8 -*-
from project import app
from functools  import wraps
from project.models import Food as fo
from project.models.Food import get_food, get_all_food

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
	data =  get_food(rid)
	return render_template('count.html', data=data, restaurant_id=rid)

@app.route('/get_single_relation', methods=['get'])
def get_single_relation():
	if "restaurant_id" not in request.cookies:
		return redirect('/')
	rid = request.cookies.get('restaurant_id')

	fid = request.args.get('fid')
	foods = apriori.getRules(int(rid))
	single_food = None
	print fid
	for f in foods:
		if int(f['prefix_foods'][0]['id']) == int(fid) and len(f['prefix_foods']) == 1:
			single_food = f
			break
	#print single_food
	def rule_cmp(x, y):
		return x['conf'] < y['conf']
	if single_food != None and len(single_food['rules']) > 7:
		single_food['rules'] = sorted(single_food['rules'], cmp=rule_cmp)[0:6]
	
	return render_template('single_relation.html', single_food=single_food)

@app.route('/setmeal', methods=['get'])
def setmeal():
	if "restaurant_id" not in request.cookies:
		return redirect('/')
	rid = request.cookies.get('restaurant_id')

	preset = []
	allfood = get_all_food(rid)
	return render_template('setmeal.html', preset=preset, allfood=allfood)
