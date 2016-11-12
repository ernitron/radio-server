#
# My Web Radio Server
# ernitron (c) 2013
#
#
## Color definition. Stolen from gentoo ;)
# normally no changes needed to this settings
GOOD=$'\e[32;01m'
WARN=$'\e[33;01m'
BAD=$'\e[31;01m'
NORMAL=$'\e[0m'
HILITE=$'\e[36;01m'
BRACKET=$'\e[34;01m'
#

# Variables
SERVER=yourserver
SERVERS=yourservers
SCRIPT=radioserver.sh
INSTALLDIR=/usr/local/bin/radioserver

STATIC = static
PACKAGES= server.py database.db

run:
	python server.py --port 80 &

check:
	python -m py_compile *.py
	rm -f *.pyc

pre-install:
	sudo apt-get install sqlite3
	sudo pip install cherrypy

rsync: check
	rsync -av $(PACKAGES) $(VIEW) $(STATIC) $(SCRIPT) root@$(SERVER):/$(INSTALLDIR)/

revsync:
	rsync -av root@$(SERVER):/$(INSTALLDIR)/server.py  .

git:
	git commit -m 'update ${DATE}' -a
	git push

