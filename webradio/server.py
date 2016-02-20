#!/usr/bin/env python
"""
  My code server application
  I should know what it does
  For my eyes only
"""

#CREATE TABLE Radio(id integer primary key autoincrement, radio text, genre text, url text);
uuid='56ty66ba-6kld-9opb-ak29-0t7f5d294686'

# Import CherryPy global namespace
import os
import sys
import time
import socket
import random
import cherrypy
import sqlite3 as lite
import re
import subprocess

# Globals
version = "4.0"
database = "database.db"
player = ''

header = '''<!DOCTYPE html>
<html lang="en">
<head>
  <title>My Radio Web Server</title>
  <meta name="generator" content="Vim">
  <meta charset=utf-8">
  <link rel="icon" type="image/png" href="/static/css/icon.png" />
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="/static/js/jquery-2.0.3.min.js"></script>
  <script src="/static/js/bootstrap.min.js"></script>
  <link rel="stylesheet" href="/static/css/bootstrap.min.css">

<!-- Custom styles for this template -->
<link href="/static/css/sticky-footer.css" rel="stylesheet">
<style media="screen" type="text/css">
#radio-playing { display: none; }
#radio-table  { display: none; }
#radio-volume { display: none; }
.jumbotron { padding: 10px 10px; }
</style>

<script type="text/javascript">
     function fmodradio(rid) {
        $.post('/m/', {id: rid},
            function(data){
                $("#radio-table").html(data);
                $("#radio-table").show();
            },
            "html"
        );
     }
     function fdelradio(rid) {
       var r = confirm("DELETING " + rid);
       if (r != true) { return; }
       $.post('/d/', {id: rid},
            function(data){
                $("#radio-table").html(data);
                $("#radio-table").show();
            },
            "html"
        );
     }
     function fplayradio(rid) {
        $.post('/p/', {id: rid},
            function(data){
                $("#radio-playing").html(data);
                $("#radio-playing").show();
                $("#radio-volume").hide();
            },
            "html"
        );
     }
     function fvolradio(updown) {
        $.post('/v/', {vol: updown},
            function(data){
                $("#radio-volume").html(data);
                $("#radio-volume").show();
            },
            "html"
        );
     }
     function fkilradio() {
        $.post('/k/',
            function(data){
                $("#radio-volume").html(data);
                $("#radio-volume").show();
            },
            "html"
        );
     }
     function sgenradio(gen) {
        $.post('/g/', {genre: gen},
            function(data) {
                $("#radio-table").html(data);
                $("#radio-table").show();
            },
            "html"
        );
     }

// ----------------------------------------------------------
     $(document).ready(function() {
         $('body').on('click', '#button-modify', function(e) {
             i = $("#idm").val()
             n = $("#namem").val()
             g = $("#genrem").val()
             u = $("#urlm").val()
             $.post("/f/", {id: i, name: n, genre: g, url: u})
              .done(function(data) {
                $("#radio-table").html(data);
                $("#radio-table").show();
            });
            e.preventDefault();
         });
         $('#namem').keyup(function(e){
            if(e.keyCode == 13) {
                $('#button-modify').click();
            }
         });
         $('#genrem').keyup(function(e){
            if(e.keyCode == 13) {
                $('#button-modify').click();
            }
         });
         $('#urlm').keyup(function(e){
            if(e.keyCode == 13) {
                $('#button-modify').click();
            }
         });
         $('#button-search').click(function(e) {
             n = $("#name").val()
             g = $("#genre").val()
             if ($("#editmode").is(":checked")) { t = "True" } else { t = "False" }
             $.post("/g/", {name: n, genre: g, editmode: t})
              .done(function(data) {
                  $("#radio-table").html(data);
                  $("#radio-table").show();
            });
            e.preventDefault();
         });
         $('#name').keyup(function(e){
            if(e.keyCode == 13) {
                $('#button-search').click();
            }
         });
         $('#genre').keyup(function(e){
            if(e.keyCode == 13) {
                $('#button-search').click();
            }
         });
         $("#button-insert").click(function(e) {
             n = $("#namei").val()
             g = $("#genrei").val()
             u = $("#urli").val()
             $.post("/i/", {name: n, genre: g, url: u})
              .done(function(data) {
                  $("#radio-table").html(data);
                  $("#radio-table").show();
            });
            e.preventDefault();
         });
         $("#play-radio").click(function(e) {
             i = $("#idp").val()
             $.post("/p/", {id: i})
              .done(function(data) {
                  $("#radio-playing").html(data);
                  $("#radio-playing").show();
            });
            e.preventDefault();
         });
       });
     </script>
</head>
<body>

<div class="container-fluid">
   <div class='jumbotron'>
      <h2><a href="/">Radio Server</a>
      <a href="#" onClick="fvolradio('down')"><span class="glyphicon glyphicon-volume-down"></span></a>
      <a href="#" onClick="fvolradio('up')"><span class="glyphicon glyphicon-volume-up"></span></a>
      <a href="#" onClick="fkilradio('up')"> <span class="glyphicon glyphicon-record"></span></a>
      </h2>
      <p>
      <div class="form-group">
        <input type="text" id="name" name="name" placeholder="radio to search">
        <label >Genre:</label>
        <input type="text" id="genre" name="genre" placeholder="genre" >
        <input type="checkbox" id="editmode" name="editmode" >
        <label >edit</label>
        <button id="button-search">Search</button>
      [ <a href="#" onClick="sgenradio('rai')"> rai </a>|
      <a href="#" onClick="sgenradio('rmc')"> rmc </a> |
      <a href="#" onClick="sgenradio('nl')"> nl </a> ]
      </div>
      </p>
      <p>
      <div class="form-group">
      <input type="text" id="namei" name="name" placeholder="Radio Name">
        <label >Genre: </label>
       <input type="text" id="genrei" name="genre" placeholder="genre">
        <label >url: </label>
        <input type="text" id="urli" name="url" placeholder="http://example.com">
       <button id="button-insert">Insert</button>
      </div>
      </p>

    <small><div id="radio-playing"> </div></small>
    </br>
   </div> <!-- Jumbotron END -->

 <div id="radio-volume"> </div>
 <div id="radio-table"> </div>
'''

footer = '''<p></div></body></html>'''


# ------------------------ AUTHENTICATION --------------------------------
from cherrypy.lib import auth_basic

# Admin Pass Database: admin:webradio ;)
users = {'admin': '29778a9bdb2253dd8650a13b8e685159'}

def validate_password(self, login, password):
    if login in users :
        if encrypt(password) == users[login] :
            cherrypy.session['username'] = login
            cherrypy.session['database'] = userdatabase(login)
            return True

    return False

def encrypt(pw):
    from md5 import md5
    return md5(pw).hexdigest()

# ------------------------ CLASS --------------------------------
class RadioServer:
    @cherrypy.expose
    def index(self):
        html = header
        (radio, genre, url) = getradio('0')
        if url != 0:
             playradio(url)
             html += 'Starting Play %s' % url
        html += getfooter()
        return html

    @cherrypy.expose
    def g(self, name="", genre="", editmode=None):

        list = searchradio(name.decode('utf8'), genre)

        listhtml = '''<table class="table table-condensed">'''
        count = 0
        for code in list:
            listhtml += '''<tr>'''
            if (editmode != None and editmode == "True") :
                listhtml += '''<td width="100px"><a href="#" onClick="fmodradio('%d')">Mod <span class="glyphicon glyphicon-pencil"></span></a></td>''' % (int(code[0]))
                listhtml += '''<td width="100px"><a href="#" onClick="fdelradio('%d')"><span class="glyphicon glyphicon-trash"></span></a></td>''' % (int(code[0]))
            listhtml += '''<td width="200px">%s</td>''' % code[1]
            listhtml += '''<td width="100px">%s</td>''' % code[2]
            listhtml += '''<td width="100px"><a href="%s" target="_blank">%s</a></td>''' % (code[3], getshort(code[3]))
            listhtml += '''<td><a href="#" onClick="fplayradio('%d')">Play <span class="glyphicon glyphicon-play"></span></a></td>''' % (int(code[0]))
            listhtml += '''</tr>'''
            count += 1
        listhtml += '''</table>'''
        listhtml += '''</div> </div>'''

        html = ""
        html += '''<div class="row"> <div class="col-md-8"> '''
        html += '''<h2> %d Results for '%s' + '%s'</h2>''' % (count, name, genre)
        html += listhtml

        return html

    @cherrypy.expose
    def i(self, name="", genre="", url=""):

        html = "<h2>Insert</h2>"
        if name == "" or name == None :
          html += "Error no name"
          return html

        if insert(name, genre, url) == False:
            html += "Error db "
            return html

        html += '''<h3>This radio has been inserted</h3>'''
        html += '''<p><table class="table table-condensed">'''
        html += ''' <tr> '''
        html += '''  <td>radio: <strong>%s</strong></td> ''' % name
        html += '''  <td>genre: <strong>%s</strong></td> ''' % genre
        html += '''  <td>url: <strong><a href="%s" target="_blank">%s</a></strong></td> ''' % (url, url)
        #html += '''  <td width="300px"><a href="#" onClick="fplayradio('%d')"> Play ''' % (int(id))
        html += '''<span class="glyphicon glyphicon-play"></span></a></td>'''
        html += ''' </tr> '''
        html += '''</table>'''

        return html

    @cherrypy.expose
    def d(self, id=""):

        html = "<h2>Delete</h2>"
        if id == "" or id == None :
            html += "Error"
            return html

        if id == "0" :
          html += "0 is reserved, sorry"
          return html

        if delete(id) == False:
            html += "Delete error in id" % id
            html += getfooter()
            return html

        html += "Item %s deleted" % id
        return html

    @cherrypy.expose
    def p(self, id=""):

        html = ""
        if id == "" or id == None :
            html += "Error no radio id"
            return html

        if id == "0" :
          html += "0 is reserved, sorry"
          return html

        (radio, genre, url) = getradio(id)
        if playradio(url) == False:
            html += "Error in parameter %s" % url
            return html

        cherrypy.session['playing'] = id
        html += '''<h3>Now Playing: '''
        html += '''<a href="%s">%s</a>''' % (url, radio)
        html += '''<a href="#" onClick="fplayradio('%s')">''' % id
        html += '''<span class="glyphicon glyphicon-play"></span></a>'''
        html += '''&nbsp;<a href="#" onClick="fmodradio('%s')"><span class="glyphicon glyphicon-pencil"></span></a></small>&nbsp;''' % id
        html += '''<a href="#" onClick="fdelradio('%s')"><span class="glyphicon glyphicon-trash"></span></a>''' % id
        html += '''</h3>'''
        return html

    @cherrypy.expose
    def v(self, vol=""):
        html = ""
        if vol == "" or vol == None :
           html += "Error"
        v = volume(vol)

        html += "<h6>%s (%s) </h6>" % (v, vol)
        return html

    @cherrypy.expose
    def m(self, id):

        html = '''<h2>Modify</h2>'''

        if id == "" or id == None :
          html += "Error"
          return html

        if id == "0" :
          html += "0 is reserved, sorry"
          return html

        (name, genre, url) = getradio(id)
        html += '''<input type="hidden" id="idm" name="id" value="%s">''' % id
        html += '''<input type="text" id="namem" name="name" value="%s">''' % name
        html += '''genre: <input type="text" id="genrem" name="genre" value="%s"> ''' % genre
        html += '''url: <input type="text" id="urlm" name="url" value="%s"> ''' % url
        html += '''<button id="button-modify">Change</button>'''

        return html

    @cherrypy.expose
    def f(self, id="", name="", genre="", url=""):

        html = '''<h2>Modified</h2>'''
        if id == "" or id == None :
          html += "Error missing id"
          return html

        if id == "0" :
          html += "0 is reserved, sorry"
          return html

        if modify(id, name, url, genre) == False:
            html += "Error in DB"
            return html

        (name, genre, url) = getradio(id)
        html += '''<p><table class="table table-condensed">'''
        html += '''<tr>'''
        html += '''<td width="100px"><a href="#" onClick="fmodradio('%s')">''' % id
        html += '''Mod <span class="glyphicon glyphicon-pencil"></span></a></td>'''
        html += '''<td width="200px">%s</td>''' % name
        html += '''<td width="200px">%s</td>''' % genre
        html += '''<td><a href="%s" target="_blank">%s</a></td>''' % (url, url)
        html += '''<td width="300px"><a href="#" onClick="fplayradio('%s')">'''% id
        html += '''Play <span class="glyphicon glyphicon-play"></span></a></td>'''
        html += '''</tr>'''
        html += '''</table>'''

        return html

    @cherrypy.expose
    def k(self):
        html = "<h2>Stopping</h2>"
        killall()
        return html

# ------------------------ DATABASE --------------------------------
def getfooter() :
    global footer, version

    db = cherrypy.session['database']
    try:
        con = lite.connect( db )
        cur = con.cursor()
        sql = "select radio, genre, url from Radio where id=0"
        cur.execute(sql)
        (radio, genre, url) = cur.fetchone()
    except:
        (radio, genre, url) = ('ERROR', sql, '')

    con.close()

    hostname = socket.gethostname()
    f = '''<footer class="footer"> <div class="container">'''
    f += '''<p class="text-muted">'''
    f += '''Session id: %s - Session Database %s<br>''' % (cherrypy.session.id, cherrypy.session['database'])
    f += '''Host: %s - Version: %s - Updated: %s // Last: %s''' % (hostname, version, genre, url)
    f += '''</p>'''
    f += '''</div></footer>'''
    return f + footer

def updateversiondb(cur) :
    db = cherrypy.session['database']
    username = cherrypy.session['username']

    dt = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        sql = "UPDATE Radio SET radio='%s', genre='%s' WHERE id = 0" % (hostname, dt)
        cur.execute(sql)
    except:
        return

def delete(id) :
    db = cherrypy.session['database']
    try:
        con = lite.connect( db )
        cur = con.cursor()
    	sql =  "DELETE from Radio WHERE id = '%s'" % (id)
    	cur.execute(sql)
        ret = True
    except:
        print "Error deleting sql %s" % sql
        ret = False

    updateversiondb(cur)
    con.commit()
    con.close()
    return ret

def insert(radio, genre, url) :
    db = cherrypy.session['database']

    try:
        con = lite.connect( db )
        cur = con.cursor()
    	sql =  "INSERT INTO Radio (radio, genre, url) VALUES('%s', '%s', '%s')" % (radio, genre, url)
    	cur.execute(sql)
        ret = True
    except:
        print "Error inserting sql %s" % sql
        ret = False

    updateversiondb(cur)
    con.commit()
    con.close()
    return ret

def modify(id, radio, url, genre) :
    db = cherrypy.session['database']

    try:
        con = lite.connect( db )
        cur = con.cursor()
    	sql = "UPDATE Radio SET radio='%s', url='%s', genre='%s' WHERE id = %s" % (radio, url, genre, id)
    	cur.execute(sql)
        ret = True
    except:
        print "Error modify sql %s" % sql
        ret = False

    updateversiondb(cur)
    con.commit()
    con.close()
    return ret

def getradio(id) :
    db = cherrypy.session['database']
    try:
        con = lite.connect( db )
        cur = con.cursor()
        cur.execute("select radio, genre, url from Radio where id=%s" % id)
    except:
        rows = ('Radio Not Found', 'none', './Hey-yay-hey.mp3')

    rows = cur.fetchone()
    con.close()

    return rows

def searchradio(radio, genre) :
    db = cherrypy.session['database']

    o = 'order by radio'
    o = ''
    try:
        sql = "select id, radio, genre, url from Radio where radio like '%%%s%%' and genre like '%%%s%%' and id != 0 %s" % (radio, genre, o)
        con = lite.connect( db )
        cur = con.cursor()
        cur.execute(sql)
    except:
        return [(0, sql, o, genre)]

    rows = cur.fetchall()
    con.close()
    return rows


def updatelastradio(url) :
    db = cherrypy.session['database']
    try:
        con = lite.connect( db )
        cur = con.cursor()
        sql = "UPDATE Radio SET url='%s' WHERE id=0" % (url)
        cur.execute(sql)
        con.commit()
        con.close()
    except:
        return


def userdatabase(user) :
    db = database
    if not os.path.isfile(db):
        return None
    return db


def getshort(code) :
    newcode = code
    if len(newcode) > 30 :
          newcode = newcode[0:30]

    return str(newcode)

def setplayer(p):
    global player
    player = p

def playradio(url):
    global player

    status = 0
    killall()

    if player == 'mplayer':
        command = "/usr/bin/mplayer -really-quiet %s" % url
        pidplayer = subprocess.Popen(command, shell=True).pid
        status = True
    if player == 'omxplayer':
        # Process is in background
        p = 'omxplayer'
        status = subprocess.Popen([p, url])

    updatelastradio(url)
    return status

def killall():
    global player
    status = 0
    if player == 'mplayer':
        status = subprocess.call(["killall", "mplayer"])

    if player == 'omxplayer':
        control = "/usr/local/bin/omxcontrol"
        status = subprocess.call([control,  "stop"])
        status = subprocess.call(["killall", "omxplayer.bin"])

    return status

def volume(vol) :
    global player

    if player == 'mplayer':
        return volume_mplayer(vol)

    if player == 'omxplayer':
        return volume_omxplayer(vol)

def volume_mplayer(vol):

    # With ALSA on CHIP
    if vol == 'up':
        db = subprocess.check_output(["amixer set 'Power Amplifier' 5%+"], shell=True)
        #db = os.system("amixer set 'Power Amplifier' 5%+")
    if vol == 'down':
        db = subprocess.check_output(["amixer set 'Power Amplifier' 5%-"], shell=True)
        #db = os.system("amixer set 'Power Amplifier' 5%-")

    i = db.rfind(':')
    return db[i+1:]

def volume_omxplayer(vol) :
    import math
    control = "/usr/local/bin/omxcontrol"
    if vol == 'up' :
        db = subprocess.check_output([control, "volumeup"])
    else :
        db = subprocess.check_output([control, "volumedown"])

    v = subprocess.check_output([control, "volume"])
    i = v.rfind(':')
    db = 10.0 * math.log(float(v[i+1:]), 10)
    volstring = "%-2.2f dB" % db
    return volstring

# ------------------------ SYSTEM --------------------------------

def writemypid(pidfile):
    pid = str(os.getpid())
    try:
        f = file(pidfile, 'w')
        f.write(pid)
        f.close
    except:
        pass

# Cherrypy Management
def error_page_404(status, message, traceback, version):
    html = header
    html += "%s<br>" % (status)
    html += "%s" % (traceback)
    html += getfooter()
    return html

# Secure headers!
def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"

if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser()
    parser.add_option('--port', action="store", dest="port", type="int", default=8804)
    parser.add_option('--stage', action="store", dest="stage", type="string", default="production")
    parser.add_option('--database', action="store", dest="database", type="string", default="database.db")
    parser.add_option('--root', action="store", dest="root", type="string", default=".")
    parser.add_option('--pid', action="store", dest="pid", type="string", default="webradio.pid")
    parser.add_option('--player', action="store", dest="player", type="string", default="mplayer")

    # get args
    options, args = parser.parse_args()

    # Where to start, what to get
    root = os.path.abspath(options.root)
    database = os.path.join(root, options.database)
    os.chdir(root)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    setplayer(options.player)

    writemypid(options.pid)

    settings = {'global': {'server.socket_host': "0.0.0.0",
                           'server.socket_port' : options.port,
                           'server.ssl_module':'builtin',
                           'server.ssl_certificate':'keys/aitekssl.crt',
                           'server.ssl_private_key':'keys/aitekssl.key',
                           'log.screen': True,
                          },
               }
    if options.port != 443 :
        settings = {'global': {'server.socket_host': "0.0.0.0",
                               'server.socket_port' : options.port,
                               'log.screen': True,
                              },
               }

    conf = {'/static': {'tools.staticdir.on': True,
                     'tools.staticdir.root': current_dir,
                     'tools.staticfile.filename': 'icon.png',
                     'tools.staticdir.dir': 'static'
                    },
            '/':    {
                     'tools.auth_basic.on': True,
                     'tools.auth_basic.realm': 'localhost',
                     'tools.auth_basic.checkpassword': validate_password,
                     'tools.secureheaders.on' : True,
                     'tools.sessions.on': True,
                    },
           }

    #cherrypy.config.update(file = 'configuration.conf')
    cherrypy.config.update(settings)
    cherrypy.config.update({'error_page.404': error_page_404})
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)

    # To make it ZERO CPU usage 
    cherrypy.engine.timeout_monitor.unsubscribe()
    cherrypy.engine.autoreload.unsubscribe()

    # Cherry insert pages
    serverroot = RadioServer()

    # Start the CherryPy server.
    cherrypy.quickstart(serverroot, config=conf)

