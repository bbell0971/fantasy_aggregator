from flask import Flask
import pymongo
import csv
import json
import pandas as pd
import sys, getopt, pprint
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["fantasy_aggregator"]
        g.db = mydb

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        print('Closing')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    users = db['users']
    users.insert_one({ "name": "John", "address": "Highway 37" })
    process_players(db)
    sources = db['sources']
    sources.insert_many([{"id":"daily_roto", "url":"http://www.dailyroto.com"}, {"id":"awesemo", "url":"http://www.awesemo.com"} ,{"id":"rg","url":"http://www.rotogrinders.com"}, {"id":"saber_sim", "url":"http://www.sabersim.com"}, {"id":"basketball_monster", "url":"http://www.basketballmonster.com"}, {"id":"labs", "url":"http://www.fantasylabs.com"}, {"id":"rw", "url":"http://www.rotowire.com"}, {"id":"NA","url":"http://www.establishtherun.com"},{"id":"ftn","url":"http://www.establishtherun.com"},{"id":"dk","url":"http://www.establishtherun.com"}])


def process_players(db):
    csvfile = open("/home/branden/Projects/fantasy-aggregator/playernames.csv", 'r')
    reader = csv.DictReader( csvfile )
    db["players"].drop()
    header= ["awesemo","labs","saber_sim","rw","daily_roto","basketball_monster","rg","ftn","dk"]
    count = 0
    for each in reader:
        count = count + 1
        row={}
        for field in header:
            row[field]=each[field]
        row["id"]= count
        db.players.insert(row)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')