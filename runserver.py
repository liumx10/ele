#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app, db

from flask.ext.script import Server, Shell, Manager, prompt_bool
from project.models import Relation, Word, Heat

import random

manager = Manager(app)

manager.add_command("runserver", Server('0.0.0.0',port=8008, threaded=True))


@manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()
        
if __name__ == "__main__":
    manager.run()
