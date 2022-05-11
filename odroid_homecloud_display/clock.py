#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
An analog clockface with date & time.
"""

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
import requests
from PIL import ImageFont, ImageDraw, Image
import time
import datetime
import asyncio
from bitcoinrpc import BitcoinRPC

serial = i2c(port=0, address=0x3C)
# device = sh1106(serial, rotate=0)
device = ssd1306(serial, rotate=2)
event_loop = asyncio.get_event_loop()

def main():
    event_loop.run_until_complete(loop())

async def loop():
    blocks_last_time = "Unknown"
    rpc = BitcoinRPC("127.0.0.1", 8332, "rpchost", "rpcpassword")

    while True:
        try:
            bci = await rpc.getblockchaininfo()
        except Exception:
            continue

        blocks = 'block:' + str(bci['blocks'])

        if (bci['initialblockdownload']):
            sync = 'ibd ' + str(round(bci['verificationprogress'] * 100, 2)) + '%'
        else:
            sync = '100%'

        size = "{:.2f}".format(bci['size_on_disk'] / 1024 / 1024 / 1024) + ' GB'

        # mediantime = datetime.datetime.utcfromtimestamp(bci['mediantime']).strftime('%Y-%m-%d')

        # defining key/request url
        key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        # requesting data from url
        data = requests.get(key)
        data = data.json()
        price = '1SAT:' + format(1/data['price'], '.6f') + '$'

        if blocks != blocks_last_time:
            blocks_last_time = blocks
            with canvas(device) as draw:
                  font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 15)
                  draw.text((0, 2), blocks, font=font, fill=1)
                  draw.text((0, 18), sync, font=font, fill=1)
                  draw.text((0, 34), price, font=font, fill=1)
                  draw.text((0, 50), size, font=font, fill=1)

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
