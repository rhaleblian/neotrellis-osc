# neotrellis-osc

An OSC sender/receiver connected to an Adafruit NeoTrellis.

Specifically motivated for use with Bela (bela.io), but should be useful
under any platform supporting the NeoTrellis Python libraries.  You will
need to skip Bela-specific steps.


## Bela and PEPPER

The only nearly turnkey affordance I can see for connecting NeoTrellis with
Bela is the one provided by Adafruit for CircuitPython.  
The approach is to use it to provide an OSC sender/receiver running on the
Bela itself. Then, an audio process can talk to it regardless of the
chosen programming idiom (C, Pure Data, etc) via its OSC API.

This code requires `asyncio` from Python 3.7 or later, which is not
available from the current Bela image.  We get around this by building
Python 3.9 for "on-the-side" installation -- it does not replace or overlay
the Python that is included with the Bela image.


## Installation on Bela

Install a prebuilt Python 3.9 into the /opt directory.
The unpacked installation is 209MB.  Make sure you have enough room for it
and the initial tarball too.

     cd /
     tar xf python-3.9-bela.tar.gz

Create an isolated virtualenv with that new Python.

     cd
     /opt/python3.9/bin/python3 -m venv venv

Enter the virtualenv and install Python packages.

     source /root/venv/bin/activate
     pip3 install -r /root/neotrellis-py/requirements.txt


### Operation

Now that your shell is in the set up virtualenv,

     cd /root/neotrellis-osc
     python3 ./neotrellis.py

Pressing a button will send a message

     /1/neotrellis <button_index> <button_state>

where button_index is 0-15 and state is 1 when pressed.

A message will be printed if an OSC message is received with address

     /1/neotrellis/pixel

Right now nothing is done on the device when these arrive.


### Does this have to run on the Bela itself?

It does not.  @rhaleblian has run it on Raspberry Pis and had them
receive from Bela.


### Does it really need asyncio?

If you only wanted to process OSC messages coming in to the NeoTrellis,
you could use one of the other kinds of service models that `python-osc`
provides.

