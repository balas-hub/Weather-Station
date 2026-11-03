/*
  =============================================================================
  AI Weather Prediction System - Arduino Uno Sensor Node
  =============================================================================
  Target: Arduino Uno (ATmega328P)
  Sensors:
    - Bosch BMP280 (I2C): Barometric Pressure (hPa), Temperature (°C), Altitude (m)
    - 3-Pin DHT11 Module (Single-Wire Digital): Temperature (°C), Humidity (%)
      * Note: 3-pin modules have the 10k pull-up resistor pre-soldered on-board.
  Wiring:
    - BMP280 SDA -> A4, SCL -> A5, VCC -> 3.3V/5V, GND -> GND
    - DHT11 Data (OUT/S) -> Pin 2, VCC (+) -> 5V/3.3V, GND (-) -> GND
    - Direct UART (NO VOLTAGE DIVIDER):
      * Arduino Pin 1 (TX) -> Directly to ESP32 GPIO 16 (RX2)
      * Arduino Pin 0 (RX) -> Directly to ESP32 GPIO 17 (TX2)
      * Arduino GND        -> ESP32 GND (Common Ground)
  Output:
    - High-integrity JSON stream over Hardware Serial to ESP32 @ 115200 baud
    - Cadence: 1 reading every 60 seconds
  =============================================================================
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

// --- 3-Pin DHT11 Pin Definition ---
// Connect the Data / Signal pin (marked 'S' or 'OUT') to Arduino Pin 2
const int DHT_PIN = 2;

// BMP280 Instance (I2C address 0x76 or 0x77)
Adafruit_BMP280 bmp;

// Timing configuration
unsigned long lastReadTime = 0;
const unsigned long READ_INTERVAL_MS = 60000UL; // 60 seconds

/*
  Self-contained, robust DHT11 driver.
  Reads 40 bits (5 bytes) with timeout protection and checksum verification.
  Requires NO extra external libraries for DHT11!
*/
bool readDHT11(float &temperature, float &humidity) {
  uint8_t data[5] = {0, 0, 0, 0, 0};

  // 1. Send Start Signal to DHT11
  pinMode(DHT_PIN, OUTPUT);
  digitalWrite(DHT_PIN, LOW);
  delay(20); // Hold LOW for at least 18ms
  digitalWrite(DHT_PIN, HIGH);
  delayMicroseconds(30);
  pinMode(DHT_PIN, INPUT_PULLUP);

  // 2. Wait for DHT11 response (80µs LOW, then 80µs HIGH)
  unsigned long t = micros();
  while (digitalRead(DHT_PIN) == HIGH) {
    if (micros() - t > 100) return false;
  }
  t = micros();
  while (digitalRead(DHT_PIN) == LOW) {
    if (micros() - t > 100) return false;
  }
  t = micros();
  while (digitalRead(DHT_PIN) == HIGH) {
    if (micros() - t > 100) return false;
  }

  // 3. Read 40 data bits
  for (int i = 0; i < 40; i++) {
    // Wait for the 50µs LOW pulse starting each bit
    t = micros();
    while (digitalRead(DHT_PIN) == LOW) {
      if (micros() - t > 100) return false;
    }

    // Measure duration of HIGH pulse
    unsigned long pulseStart = micros();
    while (digitalRead(DHT_PIN) == HIGH) {
      if (micros() - pulseStart > 120) return false;
    }
    unsigned long pulseLen = micros() - pulseStart;

    // Pulse > 40µs represents bit '1', shorter is bit '0'
    int byteIdx = i / 8;
    data[byteIdx] <<= 1;
    if (pulseLen > 40) {
      data[byteIdx] |= 1;
    }
  }

  // 4. Verify Checksum: Byte4 must equal sum of bytes 0..3
  uint8_t checksum = data[0] + data[1] + data[2] + data[3];
  if (data[4] != checksum) {
    return false; // Checksum mismatch
  }

  // DHT11 specifications: data[0] = humidity int, data[2] = temp int, data[3] = temp decimal
  humidity = (float)data[0] + ((float)data[1] * 0.1);
  temperature = (float)data[2] + ((float)data[3] * 0.1);

  // Basic sanity validation
  if (humidity < 15.0 || humidity > 95.0 || temperature < 0.0 || temperature > 55.0) {
    return false;
  }

  return true;
}

void setup() {
  // Initialize Serial UART to ESP32
  // DIRECT CONNECTION: Uno TX (Pin 1) directly to ESP32 GPIO 16 (RX2) without voltage divider
  Serial.begin(115200);
  while (!Serial && millis() < 3000);

  pinMode(DHT_PIN, INPUT_PULLUP);

  // Initialize BMP280 with auto-detect address (0x76 or 0x77)
  bool bmpFound = bmp.begin(0x76);
  if (!bmpFound) {
    bmpFound = bmp.begin(0x77);
  }

  if (bmpFound) {
    // Normal mode, 500ms standby, 16x filtering for meteorological precision
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                    Adafruit_BMP280::SAMPLING_X2,
                    Adafruit_BMP280::SAMPLING_X16,
                    Adafruit_BMP280::FILTER_X16,
                    Adafruit_BMP280::STANDBY_MS_500);
  }

  // Onboard LED ready blink
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  delay(300);
  digitalWrite(13, LOW);

  // Trigger initial telemetry read immediately
  lastReadTime = millis() - READ_INTERVAL_MS;
}

void loop() {
  unsigned long now = millis();
  if (now - lastReadTime >= READ_INTERVAL_MS) {
    lastReadTime = now;

    // 1. Read BMP280
    float bmp_temp = bmp.readTemperature();
    float bmp_pressure = bmp.readPressure() / 100.0F; // Convert Pa to hPa
    float bmp_altitude = bmp.readAltitude(1013.25);

    bool bmp_valid = (!isnan(bmp_temp) && !isnan(bmp_pressure) && bmp_pressure > 300.0 && bmp_pressure < 1100.0);
    if (!bmp_valid) {
      bmp_temp = -999.0;
      bmp_pressure = -999.0;
      bmp_altitude = -999.0;
    }

    // 2. Read 3-Pin DHT11 Sensor
    float dht_temp = -999.0;
    float dht_humi = -999.0;
    bool dht_valid = readDHT11(dht_temp, dht_humi);

    // 3. Construct and emit standard JSON frame
    // Emits both dht_* and sht_* fields to maintain full backend compatibility
    Serial.print("{\"source\":\"uno_node\",\"bmp_temp\":");
    Serial.print(bmp_temp, 2);
    Serial.print(",\"bmp_pressure\":");
    Serial.print(bmp_pressure, 2);
    Serial.print(",\"bmp_altitude\":");
    Serial.print(bmp_altitude, 2);
    Serial.print(",\"dht_temp\":");
    Serial.print(dht_temp, 2);
    Serial.print(",\"dht_humidity\":");
    Serial.print(dht_humi, 2);
    Serial.print(",\"sht_temp\":");
    Serial.print(dht_temp, 2); // Alias for backend compatibility
    Serial.print(",\"sht_humidity\":");
    Serial.print(dht_humi, 2); // Alias for backend compatibility
    Serial.print(",\"bmp_ok\":");
    Serial.print(bmp_valid ? 1 : 0);
    Serial.print(",\"dht_ok\":");
    Serial.print(dht_valid ? 1 : 0);
    Serial.print(",\"sht_ok\":");
    Serial.print(dht_valid ? 1 : 0);
    Serial.println("}");

    // Activity blink
    digitalWrite(13, HIGH);
    delay(40);
    digitalWrite(13, LOW);
  }
}
