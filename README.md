# neotrellis-osc

An example of an OSC sender/receiver connected to an Adafruit NeoTrellis.

Specifically motivated for use with [Bela](http://bela.io), but should be useful
under any platform supporting the NeoTrellis Python libraries.  You will
need to skip Bela-specific steps.

This example stands atop of [python-osc](https://python-osc.readthedocs.io/en/latest/#) and Adafruit's [CircuitPython](https://circuitpython.org) libraries.


## Bela and PEPPER

The only nearly turnkey affordance I can see for connecting NeoTrellis with
Bela is the one provided by Adafruit for CircuitPython.  The approach is to use it
to provide an OSC sender/receiver running on the Bela itself.  Then, an audio process
can talk to it regardless of the chosen programming idiom (C, Pure Data, etc)
via that idiom's means of using OSC.

This code requires `asyncio` from Python 3.7 or later, which is not
available from the current Bela image.  We get around this by using
a Python 3.9 built for "on-the-side" installation -- meaning that it does not
replace or overlay the Python that is included with the Bela image.


## Installation on Bela

Clone this repo into your Bela projects directory.

    cd Bela/projects
    git clone https://github.com/rhaleblian/neotrellis-osc

Install a prebuilt Python 3.9 into the /opt directory.  An archive file is
available here:  https://drive.google.com/file/d/1Vw7DrXY2N4nZDzh19C8dljliSerUS_4c/view?usp=sharing

The unpacked installation is 209MB.  Make sure you have enough room for it
and the initial tarball too.

     cd /
     tar xf /root/python-3.9-bela.tar.gz

You now have a directory `/opt/python3.9`.

Create an isolated virtualenv with that new Python.

     /opt/python3.9/bin/python3 -m venv /root/venv

Enter the virtualenv and install Python packages.

     source /root/venv/bin/activate
     pip3 install -r /root/Bela/projects/neotrellis-osc/requirements.txt


## Operation

Now that your shell is in the virtualenv,

     cd /root/Bela/projects/neotrellis-osc
     python3 ./neotrellis.py

In the Bela IDE, run the project.

Pressing a button will send a message

     /1/neotrellis <button_index> <button_state>

where button_index is 0-15 and state is 1 when pressed.

Addresses for OSC messages received by the audio process will be printed.
When our NeoTrellis message arrives, the key and state gets printed.
Right now nothing special is done on the device in terms of audio
 when Neotrellis messages arrive.


## Notes

### Does this have to run on the Bela itself?

The Python bit does not.
@rhaleblian has run it on a Raspberry Pi and had it receive from Bela.
Adjust IP addresses and ports as needed.


### Does it really need asyncio?

If you only wanted to process OSC messages coming in to the NeoTrellis,
you could use one of the other kinds of server models that `python-osc`
provides.  Then the Python that Bela has would be sufficient.

