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
SERVER=chip1
SCRIPT=webradio.sh
INSTALLDIR=/usr/local/bin/webradio

run:
	python server.py --port 80 &

pre-install:
	sudo apt-get install python-cherrypy3
	sudo apt-get install sqlite3

deploy:
	rsync -av . root@$(SERVER):/tmp
	echo  "everything is in /tmp now; dont forget to launch make install on server"
	ssh root@$(SERVER)

install:
	mkdir -p $(INSTALLDIR)
	mkdir -p $(INSTALLDIR)/static
	install server.py $(INSTALLDIR)
	rsync -av static/ $(INSTALLDIR)/static
	rsync $(SCRIPT) /etc/init.d/
	update-rc.d $(SCRIPT) defaults

check:
	python -m py_compile *.py
	rm -f *.pyc

inst:
	python -m py_compile *.py
	rm -f *.pyc
	sudo /etc/init.d/$(SCRIPT) stop
	sudo install *.py $(INSTALLDIR)
	sudo /etc/init.d/$(SCRIPT) start


copyontarget:
	python -m py_compile *.py
	rm -f *.pyc
	rsync -av -n --exclude '.git' --exclude 'STUFF' --exclude 'BACKUP' --exclude '*.pid' ./ root@$(SERVER):/$(INSTALLDIR)/

copyfromtarget:
	rsync -av -n --exclude '*.pid'  root@$(SERVER):/$(INSTALLDIR)/ .
	scp  root@$(SERVER):/$(INSTALLDIR)/server.py .

start:
	sudo /etc/init.d/$(SCRIPT) start

stop:
	sudo /etc/init.d/$(SCRIPT) stop

#Pass is diver 
backup:
	@echo "$$BAD***$$NORMAL " Use pass as diver " $$BAD***$$NORMAL" 
	rm -f database.db database.zip BACKUP/database.zip
	mkdir -p /tmp/dbbackup BACKUP
	scp root@$(SERVER):/$(INSTALLDIR)/database.* /tmp/dbbackup
	zip -j -e -r database.zip /tmp/dbbackup/database.*
	#zip -j -e -r database.zip $(INSTALLDIR)/database.*
	mv database.zip BACKUP
	rm -rf /tmp/dbbackup

sampledb:
	sqlite3 database.sample.db < STUFF/schema.db

