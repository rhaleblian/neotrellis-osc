# Sends and receives OSC messages in conjunction with an attached
# Adafruit NeoTrellis.
# Keypresses send OSC messages.

__copyright__ = '2021-2022 org.yoyodyne Yoyodyne Research'

# Portions of code adapted from:
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import asyncio
import logging
import os
import re

from adafruit_blinka.board.beagleboard import beaglebone_black
from adafruit_neotrellis.neotrellis import NeoTrellis
import board
import busio
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


### NeoTrellis setup

color_press = (200,200,200)
color_clear = (0,0,0)

# define these now so we can use them in the button callback
client = udp_client.SimpleUDPClient('127.0.0.1', 7562)
send_address = '/1/neotrellis'


def trellis_i2c_bus():
    SCL = board.SCL
    SDA = board.SDA
    if os.environ.get('PEPPER'):
        # switch the I2C interface
        SCL = beaglebone_black.pin.I2C1_SCL
        SDA = beaglebone_black.pin.I2C1_SDA
    return busio.I2C(SCL, SDA)

trellis = NeoTrellis(trellis_i2c_bus())


def trellis_callback(event):
    """ this will be called when button events are received """
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        trellis.pixels[event.number] = color_press
        client.send_message(send_address, [event.number, 1])
    # turn the LED off when a falling edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = color_clear
        client.send_message(send_address, [event.number, 0])


# for each key...
for i in range(16):
    # activate rising edge event
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge event
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # clear the LED
    trellis.pixels[i] = color_clear
    # set the callback we defined above
    trellis.callbacks[i] = trellis_callback


### OSC setup

handshake = False
dispatcher = dispatcher.Dispatcher()


def handler(address, **args):
    print(f'received {address} {args}')
    if re.match('/osc-setup', address):
        client.send_message('/osc-setup-reply', 1)
        logging.info('OSC handshake complete')
        handshake = True
    elif re.match(r'/osc-acknowledge', address):
        print(args)
    elif re.match(r'/1/neotrellis/pixel', address):
        print('got a pixel message')


dispatcher.set_default_handler(handler)
# send all events to the default handler
dispatcher.map('/', handler)


### asyncio server setup


async def loop():
    while True:
        # call any triggered callbacks
        trellis.sync()
        # the trellis can only be read every 17 milliseconds or so
        await asyncio.sleep(0.02)


async def main():
    server = osc_server.AsyncIOOSCUDPServer(('127.0.0.1', 7563), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    await loop()
    transport.close()


logging.info('starting server, press Ctrl-C to quit')
asyncio.run(main())
