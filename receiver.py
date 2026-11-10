"""Receive live lux notifications from the InnoLab light sensor."""

import asyncio
import logging
import math
import struct
from datetime import datetime
from functools import reduce
from operator import xor

from bleak import BleakClient, BleakScanner
from bleak.exc import BleakError

DEVICE_NAME = "inno-013-7985"
UART_TX = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"


def decode_lux(data):
    if len(data) != 11 or data[:3] != b"\xaa\x0d\x00" or data[-1] != 0xbb:
        return None
    if reduce(xor, data[:10]) != 0xff:
        return None
    lux, = struct.unpack_from("<f", data, 5)
    return lux if math.isfinite(lux) and lux >= 0 else None


def on_notification(_characteristic, data):
    lux = decode_lux(data)
    if lux is None:
        logging.debug("Ignored frame %s", data.hex(" "))
        return
    print(f"{datetime.now().astimezone().isoformat(timespec='milliseconds')} {lux:g} lux", flush=True)


async def receive():
    while True:
        try:
            logging.info("Scanning for %s", DEVICE_NAME)
            device = await BleakScanner.find_device_by_name(DEVICE_NAME, timeout=10)
            if device is None:
                logging.warning("Sensor not found")
            else:
                disconnected = asyncio.Event()
                async with BleakClient(
                    device, disconnected_callback=lambda _: disconnected.set(), timeout=15
                ) as client:
                    await client.start_notify(UART_TX, on_notification)
                    logging.info("Subscribed to lux notifications")
                    await disconnected.wait()
                logging.warning("Sensor disconnected")
        except (BleakError, TimeoutError) as error:
            logging.warning("Bluetooth operation failed: %s", error)
        await asyncio.sleep(2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        asyncio.run(receive())
    except KeyboardInterrupt:
        logging.info("Stopped")
