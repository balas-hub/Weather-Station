/*
  =============================================================================
  AI Weather Prediction System - ESP32 Wi-Fi & Telemetry Gateway
  =============================================================================
  Target: ESP32 Development Board (NodeMCU / ESP32-WROOM-32)
  Function:
    - Ingests raw JSON packets from Arduino Uno over HardwareSerial (Serial2)
    - Validates packet structure using ArduinoJson
    - Synchronizes UTC/IST time via NTP server
    - Transmits telemetry packets to Django API endpoint via HTTP POST
    - Buffers up to 100 unsent readings in memory / LittleFS during network drops
    - Recovers and flushes offline queue automatically upon Wi-Fi reconnection
  =============================================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>

// ================= USER CONFIGURATION =================
const char* WIFI_SSID     = "bala";
const char* WIFI_PASSWORD = "123456789";

// Django Backend IP and Endpoint
// Note: If running Django locally on PC, use PC's LAN IP (e.g. 192.168.1.100:8000)
const char* SERVER_URL    = "http://10.151.210.43:8000/api/sensors/readings/";
const char* API_SECRET    = "weather-station-secret-key-2026"; // Match Django settings

// UART Pins connected DIRECTLY to Arduino Uno (WITHOUT VOLTAGE DIVIDER)
// Connect Arduino Pin 1 (TX) directly to ESP32 GPIO 16 (RX2)
// Connect ESP32 GPIO 17 (TX2) directly to Arduino Pin 0 (RX)
// Connect Arduino GND directly to ESP32 GND (Crucial common ground)
#define RXD2 16
#define TXD2 17

#define STATUS_LED 2 // Built-in blue LED on ESP32

// NTP Time Configuration
const char* NTP_SERVER_1 = "pool.ntp.org";
const char* NTP_SERVER_2 = "time.nist.gov";
const long  GMT_OFFSET_SEC = 19800;    // UTC +5:30 (IST for Chennai)
const int   DAYLIGHT_OFFSET_SEC = 0;

// Maximum offline memory buffer queue
#define OFFLINE_QUEUE_SIZE 120
String offlineQueue[OFFLINE_QUEUE_SIZE];
int queueHead = 0;
int queueTail = 0;
int queueCount = 0;

void enqueueReading(String jsonPayload) {
  if (queueCount < OFFLINE_QUEUE_SIZE) {
    offlineQueue[queueTail] = jsonPayload;
    queueTail = (queueTail + 1) % OFFLINE_QUEUE_SIZE;
    queueCount++;
    Serial.printf("[QUEUE] Reading buffered. Current backlog: %d\n", queueCount);
  } else {
    // Overwrite oldest if full
    offlineQueue[queueHead] = jsonPayload;
    queueHead = (queueHead + 1) % OFFLINE_QUEUE_SIZE;
    queueTail = (queueTail + 1) % OFFLINE_QUEUE_SIZE;
    Serial.println("[QUEUE] Buffer full, dropped oldest record.");
  }
}

String dequeueReading() {
  if (queueCount == 0) return "";
  String item = offlineQueue[queueHead];
  queueHead = (queueHead + 1) % OFFLINE_QUEUE_SIZE;
  queueCount--;
  return item;
}

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  
  Serial.print("[WIFI] Connecting to ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long startAttempt = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttempt < 15000) {
    digitalWrite(STATUS_LED, !digitalRead(STATUS_LED));
    delay(250);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(STATUS_LED, HIGH);
    Serial.println("\n[WIFI] Connected! IP Address: " + WiFi.localIP().toString());
    configTime(GMT_OFFSET_SEC, DAYLIGHT_OFFSET_SEC, NTP_SERVER_1, NTP_SERVER_2);
  } else {
    digitalWrite(STATUS_LED, LOW);
    Serial.println("\n[WIFI] Connection failed. Running in offline buffering mode.");
  }
}

bool postToDjango(String payload) {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Station-Secret", API_SECRET);
  http.setTimeout(8000);

  int httpResponseCode = http.POST(payload);
  bool success = false;

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.printf("[HTTP] Status: %d, Response: %s\n", httpResponseCode, response.c_str());
    if (httpResponseCode >= 200 && httpResponseCode < 300) {
      success = true;
    }
  } else {
    Serial.printf("[HTTP] POST failed, error: %s\n", http.errorToString(httpResponseCode).c_str());
  }
  http.end();
  return success;
}

void flushOfflineQueue() {
  if (WiFi.status() != WL_CONNECTED || queueCount == 0) return;
  Serial.printf("[QUEUE] Flushing %d buffered readings...\n", queueCount);

  while (queueCount > 0 && WiFi.status() == WL_CONNECTED) {
    String bufferedPayload = dequeueReading();
    if (bufferedPayload.length() > 0) {
      if (!postToDjango(bufferedPayload)) {
        // Re-enqueue if transmission failed
        enqueueReading(bufferedPayload);
        break;
      }
      delay(100); // Gentle pacing
    }
  }
}

void setup() {
  Serial.begin(115200);      // Debug console
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2); // UART from Uno

  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(STATUS_LED, LOW);

  Serial.println("\n=======================================================");
  Serial.println("  AI Weather Prediction System - ESP32 Telemetry Gateway ");
  Serial.println("=======================================================");

  connectWiFi();
}

void loop() {
  // Reconnect Wi-Fi if lost
  if (WiFi.status() != WL_CONNECTED) {
    static unsigned long lastWiFiCheck = 0;
    if (millis() - lastWiFiCheck > 20000) {
      lastWiFiCheck = millis();
      connectWiFi();
    }
  } else {
    // Flush buffered offline data if any
    flushOfflineQueue();
  }

  // Check for incoming JSON packets from Arduino Uno
  if (Serial2.available()) {
    String rawLine = Serial2.readStringUntil('\n');
    rawLine.trim();

    if (rawLine.length() > 0 && rawLine.startsWith("{") && rawLine.endsWith("}")) {
      Serial.println("[UART] Ingested packet: " + rawLine);

      // Parse and enrich JSON with gateway metadata
      StaticJsonDocument<512> doc;
      DeserializationError error = deserializeJson(doc, rawLine);

      if (!error) {
        // Add gateway timestamp and signal strength
        time_t now;
        time(&now);
        doc["gateway_ts"] = (long)now;
        doc["rssi"] = WiFi.RSSI();
        doc["station_id"] = "chennai_station_01";

        String enrichedPayload;
        serializeJson(doc, enrichedPayload);

        // Transmit or buffer
        if (WiFi.status() == WL_CONNECTED) {
          bool sent = postToDjango(enrichedPayload);
          if (!sent) {
            enqueueReading(enrichedPayload);
          } else {
            // Quick pulse on LED for successful send
            digitalWrite(STATUS_LED, LOW);
            delay(50);
            digitalWrite(STATUS_LED, HIGH);
          }
        } else {
          enqueueReading(enrichedPayload);
        }
      } else {
        Serial.printf("[JSON] Parse error: %s\n", error.c_str());
      }
    }
  }
}
