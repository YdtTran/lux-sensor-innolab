# BLE protocol specification

This specification describes the observed behavior of the OhStem InnoLab light sensor `inno-013-7985`.

## GATT

| Role | UUID |
| --- | --- |
| Nordic UART service | `6e400001-b5a3-f393-e0a9-e50e24dcca9e` |
| Sensor to host, notify | `6e400003-b5a3-f393-e0a9-e50e24dcca9e` |
| Host to sensor, write | `6e400002-b5a3-f393-e0a9-e50e24dcca9e` |

Enable notifications on the sensor-to-host characteristic. On the tested unit, the subscription alone starts a stream. The receiver resolves characteristics by UUID and sends no application writes.

## Light notification

Each observed notification contains one 11-byte frame. Offsets are zero-based.

| Offset | Size | Field |
| --- | ---: | --- |
| 0 | 3 | Observed prefix `aa 0d 00` |
| 3 | 2 | Variable bytes with unknown meaning |
| 5 | 4 | Lux as an IEEE-754 little-endian float32 |
| 9 | 1 | Bitwise complement of the XOR of bytes 0–8 |
| 10 | 1 | Observed terminator `bb` |

Test vector `aa 0d 00 58 04 00 00 8a 43 cd bb` decodes to **276 lux**.

See [capture notes](../analysis.md) for evidence and limits.
