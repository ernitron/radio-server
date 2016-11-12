# Radio-server

Radio Server for Debian based system, RaspberryPI, CHIP 9$ Computer and more... 

It is a minimalistic wrap on mpg123//mplayer//omxplayer and a bunch of internet radio url addresses kept in a sqlite3 DB. Design is responsive by means of Twitter:Bootstrap.

Is is just a simple web interfcae to search, play, modify Internet Radios. Adding your genre, and information to search easily.


## Installation on Raspberry // CHIP whatever

Just copy the branch in a directory like /usr/local/bin/radioserver 

Starting from git repository I would suggest this (suppose your target device is 192.168.2.123):

	ssh root@192.168.168.2.123
	cd /tmp
	git clone https://github.com/ernitron/radio-server.git
	cd radio-server
	sudo cp -a radio-server /usr/local/bin

Install cherrypy3 and sqlite3 

	$ sudo apt-get install python-cherrypy3
	$ sudo apt-get install sqlite3

Install player
	$ sudo apt-get install mplayer 
    OR
	$ sudo apt-get install mpg123 
	
Configure parameters in radioserver.sh # it is already preconfigured if installation is in /usr/local/bin/radioserver
Anyway it is possible to change default parameters of server like

	--port 80 (default is 8804)
	--player mpg123 OR mplayer OR omxplayer (for RaspberryPi)
	--etc. see code. 

Optional update-rc.d to let it start on boot (debian/ubuntu/raspiban/chip linux)

	$ cd /usr/loca/bin/radioserver
	$ sudo cp radioserver.sh /etc/init.d
	$ sudo update-rc.d radioserver.sh defaults
  
Start / Stop script

	$ sudo /etc/init.d/radioserver.sh start   # ( or stop, status, etc )


## USAGE

Just open browser and point to web address of the appliance.
	eg: http://192.168.2.123:8804

Webapp is protected:

	user: admin
	pass: webradio

User interface is pretty self-explaining.

Search for radio (null search provide full list)
Preset are 
	RAI=Italian Radio RAI, RMC=RadioMonteCarlo, NL=Nederland Radio

Just click play> and it will play on appliance

To edit just tick edit and reload search

Volume should work (but is an hack with alsamixer... well everything is an hack! and was never intended to be public)

Just enjoy!


# WARNING 

## Database
database.db is filled with Internet Radio taken from Internet

They can be changed /insert/modify/delete with User interface

It took me sometime to discover them... I guess internet radio apps make that part of their value ;)


