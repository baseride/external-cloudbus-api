
Vehicle fleet and mobile personnel management smart systems
`BaseRide.com <http://www.baseride.com>`_

External usage examples.

Dependencies
================

Python examples were tested with Python 2.7.

First example depends on requests library::

    $ pip install pip install requests

Second example depends on Autobahn
with Twisted support::

    $ pip install autobahn[twisted]

C# examples were tested with Visual Studio 2010 & .NET Framework 4.

Cloudbus external API usage examples (Baseride)
====================================================

First example -- python/api2_test.py -- is Cloudbus API call from Python via HTTP.

It queries information about user which credentials are used for the call.
Also, data for the "Demo Cloudbus" enterprise vehicle query is requested

Second example -- python/socket_test.py -- is Python realtime websocket event subscriprion.

Script subscribes for "Demo Cloudbus" events which are triggered when enterprise vehicles enter its geozones.
Script uses Twisted framework for demo purposes.

All server data comes in JSON format.

csharp/api2_test example is C# external API Cloudbus через HTTP call.

It queries information about user which credentials are used for the call.
Also, data for the Demo Cloudbus enterprise vehicle query is requested
