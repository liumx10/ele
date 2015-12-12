#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app, db

from flask.ext.script import Server, Shell, Manager, prompt_bool
from project.models import Food

import random
import getdata

manager = Manager(app)
manager.debug = True
manager.add_command("runserver", Server('0.0.0.0',port=8008, threaded=True))
print "reload"

@manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()
@manager.command
def createall():
    db.create_all()

@manager.command
def init():
    "Add food count to db"
    shops = getdata.get_shop()
    for shop in shops['hits']['hits']:
        rid = shop['_id']
        print rid
        foods = {}
        orders = getdata.get_order(rid)
        for order in orders['hits']['hits']:
            #print order
            groups = order['_source']['detail']['group']
            for group in groups:
                for f in group:
                    key = f['id']
                    if foods.has_key(key):
                        foods[key]['count'] += f['quantity']
                    else:
                        foods[key] = {'fid': f['id'], 'count': f['quantity'], 'name': f['name'] }
        #print foods
        for key in foods: 
         #   print foods[key]
            f = Food(rid, foods[key]['fid'], foods[key]['name'], foods[key]['count'])
            db.session.add(f)
            db.session.commit()


if __name__ == "__main__":
    manager.run()
