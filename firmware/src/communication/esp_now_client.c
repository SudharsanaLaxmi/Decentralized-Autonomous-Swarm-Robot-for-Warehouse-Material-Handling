"""
ESP-NOW Communication Client (Firmware)

Low-level communication interface for ESP32 robots using ESP-NOW protocol.
"""

/*
 * ESP-NOW Client Implementation
 * 
 * Handles peer-to-peer communication between ESP32 robots.
 * Low latency (<50ms), range 200-300m line-of-sight.
 * 
 * Configuration in firmware/include/config.h
 */

#ifdef ESP_PLATFORM

#include <esp_wifi.h>
#include <esp_now.h>
#include <WiFi.h>
#include <string.h>
#include <queue>

// Message structure (must be <250 bytes for ESP-NOW)
typedef struct {
    uint8_t msg_type;
    uint8_t robot_id;
    uint16_t sequence;
    uint32_t timestamp;
    uint8_t payload[32];  // Variable payload
} esp_now_msg_t;

// Queue for received messages
static std::queue<esp_now_msg_t> rx_queue;
static SemaphoreHandle_t rx_sem = nullptr;

// Callback when data is sent
static void on_data_sent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    char macStr[18];
    snprintf(macStr, sizeof(macStr), "%02X:%02X:%02X:%02X:%02X:%02X",
             mac_addr[0], mac_addr[1], mac_addr[2],
             mac_addr[3], mac_addr[4], mac_addr[5]);
    
    if (status == ESP_NOW_SEND_SUCCESS) {
        ESP_LOGD(TAG, "Last Packet Sent to : %s, Status = SUCCESS", macStr);
    } else {
        ESP_LOGD(TAG, "Last Packet Sent to : %s, Status = FAIL", macStr);
    }
}

// Callback when data is received
static void on_data_recv(const uint8_t *mac_addr, const uint8_t *incomingData, int len) {
    if (len > sizeof(esp_now_msg_t)) {
        ESP_LOGW(TAG, "Received message too large: %d bytes", len);
        return;
    }
    
    // Copy to queue
    esp_now_msg_t msg;
    memcpy(&msg, incomingData, len);
    
    if (xQueueSend(rx_queue, &msg, 0) != pdTRUE) {
        ESP_LOGW(TAG, "RX queue full, dropping message");
    }
}

/**
 * Initialize ESP-NOW communication
 * 
 * Returns: 0 on success, -1 on error
 */
int esp_now_init() {
    
    // Create receive queue
    rx_queue = xQueueCreate(20, sizeof(esp_now_msg_t));
    if (!rx_queue) {
        ESP_LOGE(TAG, "Failed to create RX queue");
        return -1;
    }
    
    // Initialize WiFi
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    
    // Initialize ESP-NOW
    if (esp_now_init() != ESP_OK) {
        ESP_LOGE(TAG, "Error initializing ESP-NOW");
        return -1;
    }
    
    // Register send/receive callbacks
    esp_now_register_send_cb(on_data_sent);
    esp_now_register_recv_cb(on_data_recv);
    
    // Set PMF (Protected Management Frames)
    WiFi.beginSmartConfig();
    delay(100);
    
    ESP_LOGI(TAG, "ESP-NOW initialized");
    return 0;
}

/**
 * Add peer for communication
 * 
 * Args:
 *   mac_addr: Peer MAC address (6 bytes)
 *   channel: WiFi channel (1-13)
 * 
 * Returns: 0 on success
 */
int esp_now_add_peer(const uint8_t *mac_addr, uint8_t channel) {
    
    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, mac_addr, 6);
    peerInfo.channel = channel;
    peerInfo.encrypt = false;  // No encryption for low latency
    
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        ESP_LOGE(TAG, "Failed to add peer");
        return -1;
    }
    
    char macStr[18];
    snprintf(macStr, sizeof(macStr), "%02X:%02X:%02X:%02X:%02X:%02X",
             mac_addr[0], mac_addr[1], mac_addr[2],
             mac_addr[3], mac_addr[4], mac_addr[5]);
    ESP_LOGI(TAG, "Peer added: %s", macStr);
    
    return 0;
}

/**
 * Send message to peer
 * 
 * Args:
 *   mac_addr: Destination MAC address
 *   data: Message data
 *   len: Message length (must be < 250 bytes)
 * 
 * Returns: 0 on success
 */
int esp_now_send_msg(const uint8_t *mac_addr, const uint8_t *data, int len) {
    
    if (len > 250) {
        ESP_LOGE(TAG, "Message too large: %d bytes", len);
        return -1;
    }
    
    esp_err_t result = esp_now_send(mac_addr, (uint8_t *)data, len);
    
    if (result != ESP_OK) {
        ESP_LOGE(TAG, "Error sending message: %d", result);
        return -1;
    }
    
    return 0;
}

/**
 * Receive message (non-blocking)
 * 
 * Args:
 *   msg: Pointer to message structure
 *   timeout_ms: Timeout in milliseconds (0 = non-blocking)
 * 
 * Returns: 0 if message received, -1 if timeout
 */
int esp_now_recv_msg(esp_now_msg_t *msg, uint32_t timeout_ms) {
    
    if (!msg) {
        return -1;
    }
    
    if (xQueueReceive(rx_queue, msg, pdMS_TO_TICKS(timeout_ms)) == pdTRUE) {
        return 0;
    }
    
    return -1;  // Timeout
}

/**
 * Get receive queue depth
 */
uint32_t esp_now_get_queue_depth() {
    return uxQueueMessagesWaiting(rx_queue);
}

/**
 * Deinitialize ESP-NOW
 */
void esp_now_deinit() {
    esp_now_deinit();
    vQueueDelete(rx_queue);
    rx_queue = nullptr;
}

#endif  // ESP_PLATFORM
