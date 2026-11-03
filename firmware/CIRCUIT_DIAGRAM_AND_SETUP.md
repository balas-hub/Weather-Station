# ⚡ Hardware Wiring & Circuit Guide (Direct Connection, 3-Pin DHT11)

Complete assembly instructions for the **AI Weather Station** using **Arduino Uno**, **Bosch BMP280**, **3-Pin DHT11 Module**, and **ESP32** (Direct Connection without voltage divider).

---

## 1. Pin Interconnection Map

### A. Arduino Uno to Bosch BMP280 (I²C Protocol)
| BMP280 Pin | Arduino Uno Pin | Note |
|------------|-----------------|------|
| **VCC**    | **3.3V** (or 5V) | Connect to 3.3V power rail (or 5V if module has onboard 662K regulator) |
| **GND**    | **GND**         | Common Ground |
| **SCL**    | **A5**          | I²C Clock |
| **SDA**    | **A4**          | I²C Data |
| **CSB**    | **3.3V** (VCC)  | High enables I²C mode |
| **SDO**    | **GND** / **VCC** | GND = Address `0x76`, VCC = Address `0x77` |

---

### B. Arduino Uno to 3-Pin DHT11 Module (Single-Wire Digital)
> [!NOTE]
> 3-pin DHT11 breakout modules (labeled `+`, `OUT`/`S`, `-`) come with a **built-in onboard SMD pull-up resistor** and bypass capacitor on the PCB. No external resistors are needed!

| 3-Pin DHT11 Module Pin | Arduino Uno Pin | Note |
|------------------------|-----------------|------|
| **VCC (+ / VDD)**      | **5V** or **3.3V** | Power rail |
| **DATA (OUT / S)**     | **Digital Pin 2** | Direct connection (onboard pull-up already present) |
| **GND (-)**            | **GND**         | Common Ground |

---

### C. Arduino Uno to ESP32 Gateway (Direct UART — WITHOUT Voltage Divider)
> [!NOTE]
> **Direct Wiring (No Voltage Divider)**: Connect Arduino Uno Pin 1 directly to ESP32 GPIO 16 with a jumper wire. Both boards share a common ground reference.

| Arduino Uno Pin | Direct Jumper Wire | ESP32 Pin | Purpose |
|-----------------|--------------------|-----------|---------|
| **Pin 1 (TX)**  | **Direct Wire (No Divider)** | **GPIO 16 (RX2)** | Telemetry data stream into ESP32 |
| **Pin 0 (RX)**  | **Direct Wire**              | **GPIO 17 (TX2)** | Communication / ACK |
| **GND**         | **Direct Wire**              | **GND**           | **Essential:** Common ground reference |

---

## 2. Direct Wiring Schematic Overview

```
                          +-------------------+
                          |   Arduino Uno     |
                          |   (ATmega328P)    |
                          +---+---+---+---+---+
                              |   |   |   |
      I2C (A4/A5) ------------+   |   |   +-------- Direct UART (Pin 1 TX / Pin 0 RX)
          |                       |   |                 | (DIRECT CONNECTION - NO DIVIDER)
          v                       |   |                 v
+-------------------+             |   |         +-------------------+
|   Bosch BMP280    |             |   |         |      ESP32        |
| Barometer & Temp  |             |   |         | Wi-Fi & NTP Gate  |
+-------------------+             |   |         +---------+---------+
                                  |   |                   |
    Digital Pin 2 ----------------+   |                   | Wi-Fi 2.4GHz
          |                           |                   v
          v                           |         +-------------------+
+-------------------+                 |         |   Django Server   |
|   3-Pin DHT11     |                 |         | (Local PC / LAN)  |
| Humidity & Temp   |                 |         +-------------------+
+-------------------+                 |
                                      |
                   Common Rails (5V / 3.3V / GND)
```

---

## 3. Flashing & Testing Steps

1. In Arduino IDE:
   - For Arduino Uno: Open `arduino_sensor.ino`. Ensure **Adafruit BMP280 Library** is installed. DHT11 driver is self-contained with no extra libraries needed. Flash to Uno (unplug Pin 0/Pin 1 while flashing, then plug back in).
   - For ESP32: Open `esp32_bridge.ino`. Set your Wi-Fi credentials and PC LAN IP. Flash to ESP32.
2. Power both boards. The ESP32's onboard LED will indicate Wi-Fi connection and blink with each telemetry packet transmitted to the Django backend!
