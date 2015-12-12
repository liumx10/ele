# -*- coding: utf-8 -*-
from project import app
from functools  import wraps
from project.models import Food as fo
from project.models.Food import get_food, get_all_food

from flask import render_template, request, redirect
import json
import requests

import os
import apriori, getdata

@app.route('/', methods=['POST', 'GET'])
def start():
	if request.method == "POST":
		restaurant_id = request.form['restaurant_id']
		r = requests.get('http://115.159.159.158:9200/hackathon/restaurant/_search?q=_id:'+str(restaurant_id))
		res = json.loads(r.text)
		if res['hits']['total'] == 0:
			return render_template('index.html')
		resp = app.make_response(redirect('/count'))
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

	preset = request.args.get('preset')
	preset_food = []
	if preset is not None:
		preset = preset.split(',')
		for p in preset:
			preset_food.append(int(p))
	allfood = get_all_food(rid)
	return render_template('setmeal.html', preset=preset_food, allfood=allfood)

@app.route('/get_orders', methods=['POST'])
def get_orders():
	if "restaurant_id" not in request.cookies:
		return json.dumps({'status': 1})

	rid = request.cookies.get('restaurant_id')
	params = request.get_json()
	ipset = params.get('ipset').split(',')
	sets = []
	for i in ipset:
		sets.append(int(i))
	res = getdata.get_order_by_foods_and_restaurant(int(rid), set(sets))
	return json.dumps(res)
