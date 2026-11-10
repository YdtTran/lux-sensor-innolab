# InnoLab light sensor BLE analysis

## Environment and capture

The USB-connected OPPO CPH2095 ran Android 12 and ColorOS 12.1. ADB was authorized. The host ran Debian 13 with BlueZ, an active Bluetooth adapter, and `btmon`.

For this run, ADB opened Developer options, selected the unfiltered **Enabled** option for Bluetooth HCI snoop, restarted Bluetooth, and verified `mSnoopLogSettingAtEnable = full` in `adb shell dumpsys bluetooth_manager`. ADB opened InnoLab, created a numeric view, connected to `inno-013-7985`, selected **Độ sáng (lux)**, then ran Play from approximately 08:51:33 to 08:51:41 UTC+07 on November 10, 2026. The sensor tile showed 272–273 lux before Play. The test used ambient light. ADB disconnected the sensor and disabled HCI snoop after collection.

To repeat the capture, disconnect other sensor clients, enable full snoop under **Settings → System settings → Developer options**, restart Bluetooth, then connect with InnoLab. Log the times of connection, Play, each lighting change, Stop, and disconnect. Hold normal, covered, and brighter conditions for about 10 seconds each and record displayed lux for each. Keep the raw report private.

```sh
umask 077
mkdir -p .capture
adb bugreport .capture/innolab_capture.zip
unzip -Z1 .capture/innolab_capture.zip | grep -i snoop
```

The protected Bluetooth log directory denied shell access, and the exported report contained no dedicated snoop file. The fallback was the summary from `adb shell dumpsys bluetooth_manager`. Extract the lines between the BTSNOOP_LOG_SUMMARY markers, pipe the base64 body to Android's [btsnooz.py](https://android.googlesource.com/platform/packages/modules/Bluetooth/+/refs/heads/main/system/tools/scripts/btsnooz.py), then read the result using `btmon -r FILE`. The summary retained the CCCD write but truncated notification data after the first three value bytes. Linux received full notifications independently using Bleak. Wireshark was unnecessary.

## Packet evidence

The Android summary shows an ATT Write Request (0x12) to CCCD handle 0x002B with value `01 00`, a successful Write Response (0x13), and repeated Handle Value Notifications (0x1B) on value handle 0x002A. The capture's descriptor discovery identified 0x002B as UUID 0x2902. Linux service discovery mapped the descriptor to the Nordic UART TX characteristic (UUID beginning with 6e400003). On this Linux backend, Bleak reported TX handle 0x0029 while the Android trace carried its notification value on 0x002A. The receiver subscribes by UUID.

The direct Linux subscription streamed without any application write to UART RX. Example notifications:

| Raw bytes | Decoded lux |
| --- | ---: |
| `aa 0d 00 58 04 00 00 8a 43 cd bb` | 276 |
| `aa 0d 00 54 04 00 80 8a 43 41 bb` | 277 |

Each observed light notification is an 11-byte binary frame. The first three bytes are `aa 0d 00`. Bytes 3–4 vary and their purpose is unknown. Bytes 5–8 contain an IEEE-754 float32 in little-endian order. Byte 9 matches the bitwise complement of the XOR of bytes 0–8 in the observed samples. Byte 10 is `bb`. Byte offsets are zero-based.

The standalone receiver printed 95 valid readings (241–277 lux, mostly 276–277) from the physical sensor in a nine-second test and stopped cleanly on SIGINT. The app had shown 272–273 lux earlier. A synchronized comparison under controlled light changes, reconnect testing after a forced link loss, and testing other sensor firmware remain outstanding.

## Run on Debian

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python receiver.py
```

Disconnect InnoLab before running. The receiver scans by advertised name, subscribes to UART TX, validates and decodes each frame, and prints local timestamps with lux. It scans again after disconnect and exits on Ctrl+C.
