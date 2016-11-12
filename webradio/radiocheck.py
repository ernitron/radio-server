#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import os
import subprocess
from termcolor import colored

from peewee import *

# Global
global db
database = 'database.db'
db = SqliteDatabase(database)

class Radio(Model):
    radio = TextField()
    genre = TextField()
    url = TextField()
    exist = IntegerField()

    class Meta:
        database = db # This model uses the "database.db"

def getradios():
    l = Radio.select().where(Radio.exist == 0)
    return l

def delradio(id):
    #q = Radio.delete().where(Radio.id == id)
    #q.execute()
    update = Radio.update(exist=0).where(Radio.id == id)
    update.execute()

def updradio(id):
    #q = Radio.delete().where(Radio.id == id)
    #q.execute()
    update = Radio.update(exist=2).where(Radio.id == id)
    update.execute()

def radio_exist(url) :
    timeout = 2
    cmd = '/usr/bin/mpg123 -q -t --timeout %d %s ' % (timeout, url)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    count = 0
    while p.poll() is None:
        if count > timeout:
            p.kill()
            print colored('running %d sec' % count, 'green')
            return True
        count += 1
        time.sleep(1)

    print colored('waited %d sec' % count, 'red')
    return False

def singlecheck(url):
    if radio_exist(url):
        print colored("Radio streams %s " % (url), 'green')
    else:
        print colored("Radio DOESNT stream %s " % (url), 'red')
    sys.exit(1)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--player', action="store", default="mpg123")
    parser.add_argument('--database', action="store", default="database.db")
    parser.add_argument('-s', '--single', action="store", default='')
    parser.add_argument('-g', '--genre', action="store", default='')

    # get args
    args = parser.parse_args()

    if args.single != '':
        print 'Searching for ' , args.single
        singlecheck(args.single)

    if args.genre != '':
        genre = args.genre
        print 'Searching for ' , genre
        #radios = Radio.select().where((Radio.genre.contains( genre )) & (Radio.exist == 1) & (Radio.id > 1103))
        radios = Radio.select().where((Radio.genre.contains( genre )) & (Radio.exist == 1) )
    else:
        radios = Radio.select().where((Radio.exist == 1))

    db.connect()

    for r in radios:
        os.system('pkill mpg123')
        text = r.url
        url, sep, tail = text.partition('?')
        if url == '' or radio_exist(url) == False:
            delradio(r.id)
            print colored('Deleted %s %s "%s"' % (r.id, r.radio, r.url), 'red')
        else:
            updradio(r.id)
            print colored("Radio streams %s %s" % (r.radio, r.url), 'green')

