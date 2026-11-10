# Receiver behavior specification

- Discover the sensor by advertised name `inno-013-7985` and connect using the discovered BLE identity.
- Subscribe to Nordic UART TX. Use the [protocol specification](protocol.md) to validate and decode notifications.
- Ignore frames with invalid length, prefix, terminator, or checksum, and readings that are negative or non-finite.
- Print valid readings to standard output as a local ISO 8601 timestamp with milliseconds, a space, the lux value, and ` lux`. Send diagnostics to standard error.
- Retry discovery after a link loss or a handled Bluetooth error. Exit cleanly on Ctrl+C.

The live smoke test verifies that the receiver prints lux values while the InnoLab app is disconnected. Forced link-loss recovery and synchronized comparison with the app under controlled lighting remain unverified.
