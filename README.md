# InnoLab lux sensor receiver

Read live light intensity from the OhStem InnoLab BLE sensor `inno-013-7985`. The receiver was tested on Debian 13 with the physical sensor.

Disconnect the InnoLab app from the sensor before running.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python receiver.py
```

Each line contains a local ISO 8601 timestamp followed by the reading and unit. Press Ctrl+C to exit.

- [BLE protocol specification](spec/protocol.md)
- [Receiver behavior specification](spec/receiver.md)
- [Capture and validation notes](analysis.md)
- [Verified BLE operations](commands.md)
