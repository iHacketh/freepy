freepy
======

A Python Actor based application server powered by FreeSWITCH. Freepy enables Python developers to rapidly build complex communications solutions by providing a simple programming model along with primitives to communicate with FreeSWITCH asynchronously over the event socket.

Getting Started
---------------

Before we start working with freepy it is a good idea to have a working installtion of FreeSWITCH. If you need help please follow the instructions provided on the [FreeSWITCH wiki page](http://wiki.freeswitch.org/wiki/Download_%26_Installation_Guide).

To get started with freepy we must first install the dependencies. This can be done either system wide or in a virtual environment. In this getting started guide we will create a virtual environment in which to run freepy.

```
$] git clone https://github.com/thomasquintana/freepy.git
$] cd freepy
$] virtualenv env
$] . env/bin/activate
$] pip install -r ./requirements.txt
```

Next, edit the file located @ ./conf/settings.py so freeswitch_host has the correct information to connect to your FreeSWITCH instance.

*The FreeSWITCH event socket module only listens on IP address 127.0.0.1 by default. Please make sure if FreeSWITCH is on a different machine that you bind the event socket module to the LAN IP.*

Once everything is configured we are ready to take freepy for a run.

```
$] python run.py
```

*To configure how messages get routed to switchlets please edit the file located @ ./conf/rules.py.*

More documentation is on the way soon but for now an example heartbeat monitor [switchlet](https://github.com/thomasquintana/freepy/blob/master/switchlets/heartbeat/example.py) is provided.

That's all there is to it!