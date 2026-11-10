# Verified BLE operations

| Operation | UUID or handle | Request and result |
| --- | --- | --- |
| Subscribe to Nordic UART TX | Characteristic `6e400003-b5a3-f393-e0a9-e50e24dcca9e`; observed CCCD 0x002B | ATT Write Request `12 2b 00 01 00` enables notifications. The sensor replies with `13` and streams binary lux frames in `1b 2a 00 …` notifications. Bleak performs the CCCD write through `start_notify`. |

Nordic UART RX is `6e400002-b5a3-f393-e0a9-e50e24dcca9e`. No UART RX command is required for live lux on the tested sensor. The retained Android summary is truncated, so it cannot establish the absence of every app write. The receiver sends no application commands. The Battery Level characteristic (`2a19` in service `180f`) was independently discovered and is separate from the lux stream.
