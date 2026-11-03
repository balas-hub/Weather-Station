# 🌦️ AI Weather Prediction & Forecasting Observatory System

An end-to-end, ultra-accurate IoT & Artificial Intelligence weather forecasting platform built with **Arduino Uno**, **Bosch BMP280**, **Sensirion SHT11**, **ESP32 Wi-Fi Gateway**, **Django 5**, and a **custom continuous-learning AI Ensemble (TFT + Quantile Regressors)**.

Specifically calibrated for the microclimate of **Poonamallee, Chennai, Tamil Nadu, India** (13.089017°N, 80.102193°E).

---

## 🚀 Key Highlights & Capabilities

- **Hybrid Hardware Fusion**:
  - **Bosch BMP280** (I²C): High-precision barometric pressure (hPa), ambient temperature (°C), altitude estimation.
  - **3-Pin DHT11 Module** (Single-Wire Digital): Relative humidity (%) and ambient temperature (°C). Built-in onboard pull-up resistor.
  - **Arduino Uno**: Ingests sensor data, computes dew point sanity checks, formats unified JSON packet over UART (115200 baud).
  - **ESP32 Gateway**: Direct UART connection (without voltage divider). Ingests UART packets, syncs UTC/IST clock via NTP, dispatches HTTP POST telemetry to Django server every 60 seconds, with an offline memory queue that buffers up to 120 readings during network dropouts.
- **Ultra-Accurate Custom AI Model**:
  - **Multi-target Gradient Boosting Ensemble** with 10th and 90th percentile quantile prediction bounds.
  - **Meteorological Feature Engineering**: Cyclic diurnal ($sin/cos$), annual solar harmonics ($sin/cos$), Chennai Northeast Monsoon regime flags, barometric tendency ($\Delta P / 3h$), Magnus dew point, and NOAA Heat Index.
  - **Bootstrapped with 33,000+ hourly ERA5 reanalysis records** directly from the Open-Meteo European Meteorological Archive.
  - **Continuous Nightly Learning**: APScheduler automatically triggers nightly retraining at 02:00 AM IST, blending newly collected local sensor readings into the training corpus.
- **Dual Forecast Horizons**:
  - **24-Hour Hourly Forecast**: Hourly temperature, humidity, pressure, expected condition, and uncertainty envelopes.
  - **Multi-Year Future Date Predictor**: Query weather for tomorrow, next month, or a specific date in **2027, 2028, or 2030** using Fourier seasonal climate harmonics and regional monsoon analogs.
- **Extreme Weather Hazard Engine with Historical Analog Pattern Matching**:
  - Monitors for rapid pressure drops ($\Delta P \le -3.5$ to $-6.0$ hPa / 3h), moisture saturation, and dangerous heat index levels.
  - Matches live atmospheric trajectories against **historic Chennai regional disasters** using multi-attribute distance metrics:
    - *December 2015 Chennai Mega Floods* (494 mm rainfall in 24 hours)
    - *2016 Cyclone Vardah* (130 km/h eyewall winds, pressure plunged to 975 hPa)
    - *2020 Cyclone Nivar*
    - *December 2023 Cyclone Michaung Urban Deluge* (450 mm rainfall)
    - *May 2024 Extreme Coastal Heatwave & Moisture Shock* (Heat index > 48°C)
  - Dispatches emergency notifications across **Browser Dashboard, Telegram Bot, Email SMTP, and Twilio SMS**.
- **Modern Dark-Theme SPA Dashboard**:
  - Responsive glassmorphism interface powered by **Tailwind CSS** and **Chart.js**.
  - Live metric gauges, interactive 24h hourly forecast spline chart, 24h/7d/30d historical telemetry viewer, future date AI predictor, and historical disaster catalog.

---

## 📐 Hardware Wiring & Interconnection

See [`firmware/CIRCUIT_DIAGRAM_AND_SETUP.md`](file:///e:/weather%20predection/firmware/CIRCUIT_DIAGRAM_AND_SETUP.md) for full schematic details.

### Pinout Table (Direct Wiring, 3-Pin DHT11)

| Sensor / Module | Board | Pin Connection | Notes |
|-----------------|-------|----------------|-------|
| **BMP280 VCC**  | Uno   | **3.3V**       | Or 5V if module has onboard 662K regulator |
| **BMP280 GND**  | Uno   | **GND**        | Common Ground |
| **BMP280 SCL**  | Uno   | **A5**         | I²C Clock |
| **BMP280 SDA**  | Uno   | **A4**         | I²C Data |
| **DHT11 VCC (+)** | Uno | **5V / 3.3V**  | Power rail |
| **DHT11 DATA (OUT/S)** | Uno | **D2**   | **Direct wire** (3-pin modules have onboard pull-up) |
| **DHT11 GND (-)** | Uno | **GND**       | Common Ground |
| **Uno TX (Pin 1)** | ESP32 | **GPIO 16 (RX2)** | **Direct Wire (WITHOUT voltage divider)** |
| **Uno RX (Pin 0)** | ESP32 | **GPIO 17 (TX2)** | Direct Wire |
| **ESP32 GND**   | Uno   | **GND**        | Common ground rail |

---

## 🛠️ Installation & Setup Guide

### 1. Python Environment Setup
The project comes pre-configured with a virtual environment in `.venv/`.

```powershell
# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install requirements (if modifying or updating)
pip install -r requirements.txt
```

### 2. Database Migrations & Initial AI Bootstrap
Run the automated bootstrap script. It will seed the disaster catalog, prepare historical ERA5 Chennai records, seed 48 hours of baseline telemetry, train the AI ensemble, and generate the initial 24h forecast:

```powershell
python scripts\bootstrap_weather_ai.py
```

### 3. Launch the Web Server & Observatory Dashboard

```powershell
# Run the local server accessible to PC and ESP32 on your LAN
python manage.py runserver 0.0.0.0:8000
```

Open your browser and navigate to:
👉 **`http://localhost:8000/`**

---

## ⚡ Flashing the Microcontrollers

### A. Arduino Uno Firmware
File: [`firmware/arduino_sensor/arduino_sensor.ino`](file:///e:/weather%20predection/firmware/arduino_sensor/arduino_sensor.ino)
1. Open the `.ino` file in the Arduino IDE.
2. Under **Tools -> Manage Libraries...**, install:
   - `Adafruit BMP280 Library`
   - `Adafruit Unified Sensor`
   - `ArduinoJson` (v6 or v7)
3. Disconnect Pin 0 / Pin 1 while uploading code to the Uno, then reattach the UART wires to the ESP32.

### B. ESP32 Gateway Firmware
File: [`firmware/esp32_bridge/esp32_bridge.ino`](file:///e:/weather%20predection/firmware/esp32_bridge/esp32_bridge.ino)
1. Open the sketch in the Arduino IDE (select **ESP32 Dev Module**).
2. Configure your Wi-Fi credentials and PC LAN IP:
   ```cpp
   const char* WIFI_SSID     = "YOUR_WIFI_NAME";
   const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
   const char* SERVER_URL    = "http://192.168.1.100:8000/api/sensors/readings/";
   ```
3. Upload to your ESP32. The onboard LED will pulse upon Wi-Fi connection and confirm packet transmissions to Django.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/sensors/readings/` | Ingests sensor packet from ESP32 (`X-Station-Secret` protected) |
| `GET`  | `/api/sensors/latest/` | Returns the most recent live sensor observation |
| `GET`  | `/api/sensors/history/?range=24h` | Returns time-series sensor history (`24h`, `7d`, `30d`) |
| `GET`  | `/api/ai/forecast-24h/` | Returns 24-hour hourly AI predictions with uncertainty bounds |
| `GET`  | `/api/ai/predict-date/?date=YYYY-MM-DD` | Projects weather for tomorrow, next year, or 2030 |
| `POST` | `/api/ai/retrain/` | Triggers immediate on-demand model retraining |
| `GET`  | `/api/ai/status/` | Returns model performance metrics (MAE, RMSE, R²) |
| `GET`  | `/api/alerts/active/` | Returns active hazard alerts with matched historical analogs |
| `POST` | `/api/alerts/<id>/dismiss/` | Acknowledges and dismisses an alert |
| `GET`  | `/api/alerts/historical-catalog/` | Catalog of historical Chennai extreme disaster signatures |
| `POST` | `/api/alerts/test/` | Triggers test alert dispatch (Email, Telegram, SMS, Dashboard) |
| `GET`  | `/api/simulate/` | Injects realistic simulated telemetry for hardware-in-the-loop testing |

---

## 🧪 Automated Test Suite

Run the test suite to verify all sensor ingestion, AI forecasting, historical matching, and dashboard views:

```powershell
python manage.py test tests
```
*Result: 6/6 tests passing (OK)*

---

## 🔔 Configuring Alert Channels (Optional)

Configure notifications in your `.env` or system environment variables:
- **Telegram Bot**: Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.
- **Email Notifications**: Set `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `ALERT_RECIPIENT_EMAIL`.
- **Twilio SMS**: Set `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, and `TWILIO_TO_NUMBER`.

---

## 👥 Station Location Metadata
- **Observatory**: Poonamallee Weather Observatory, Chennai
- **Coordinates**: Latitude 13.089017°N, Longitude 80.102193°E
- **Monsoon Zone**: Northeast Monsoon (NEM) coastal catchment basin
- **Target Horizons**: 24-Hour Hourly & Multi-Year Projection (2026–2030+)
