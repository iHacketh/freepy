freepy
======

A Python Actor based application server powered by FreeSWITCH. Freepy enables Python developers to rapidly build complex communications solutions by providing a simple programming model along with primitives to communicate with FreeSWITCH asynchronously over the event socket.

Getting Started
---------------

Before we start working with freepy it is a good idea to have a working installation of FreeSWITCH. If you need help please follow the instructions provided on the [FreeSWITCH wiki page](http://wiki.freeswitch.org/wiki/Download_%26_Installation_Guide).

For the impatient, I have written a FreeSWITCH installation script in Python for Ubuntu following the latest stable release on the 14.x branch that may be helpful and can be located @ [FreeSWITCH Installer](https://github.com/thomasquintana/freeswitch-installer).

Installing Using RPMs
---------------------
Thankfully, Iskren Hadzhinedev has been kind enough to contribute [RPMS for CentOS 6.5 64-bit](https://drive.google.com/folderview?id=0B6jtlloOxsC9dXVUbnQ5QWxTRlE&usp=sharing).


Installing Using PyPi
---------------------
Iskren Hadzhinedev was also kind enough to provide a PyPi patch, script, and instructions.

```
$] pip install freepy
```

Next, edit the file located @ lib/python2.7/site-packages/freepy/conf/settings.py so freeswitch_host has the correct information to connect to your FreeSWITCH instance.

Finally, run the server.

```
$] freepy-server
```

*To configure how messages get routed to switchlets please edit the file located @ lib/python2.7/site-packages/freepy/conf/rules.py.*

Installing From Github
----------------------
To get started with freepy we must first install the dependencies. This can be done either system wide or in a virtual environment. In this getting started guide we will create a virtual environment in which to run freepy.

```
$] git clone https://github.com/thomasquintana/freepy.git
$] cd freepy
$] virtualenv env
$] . env/bin/activate
$] pip install -r ./requirements.txt
```

Next, edit the file located @ ./conf/settings.py so freeswitch_host has the correct information to connect to your FreeSWITCH instance.

Once everything is configured we are ready to take freepy for a run.

```
$] python run.py
```

*To configure how messages get routed to switchlets please edit the file located @ ./conf/rules.py.*

More documentation is on the way soon but for now an example heartbeat monitor [switchlet](https://github.com/thomasquintana/freepy/blob/master/switchlets/heartbeat/example.py) is provided.

Notes
-----

*The FreeSWITCH event socket module only listens on IP address 127.0.0.1 by default. Please make sure if FreeSWITCH is on a different machine that you bind the event socket module to the LAN IP.*

*Information on the state machines used by FreePy can be found @ [Declarative FSMs](https://github.com/thomasquintana/declarative-fsm)*

Contributions
-------------

In this section we extends our appreciation for community members who have helped improve the project and in turn have made it better for everyone.

**A special thanks too:**

*Cristian Groza* - Wrote documentation & unit tests for the commands.py file.

*Iskren Hadzhinedev* - Contributed PyPi script/instructions, RPM spec files, and RPMs.
