# Revoltab HIDE Integration for Home Assistant

This custom integration allows you to control and monitor **Revoltab HIDE** devices (retractable scent/power sockets) directly from Home Assistant. It utilizes the Revoltab Cloud API to provide seamless control and real-time status updates.

## ✨ Features
* **Power Control**: Turn your HIDE device on or off (Start/Stop).
* **Intensity Adjustment**: Set the operation intensity (0-100%) via a slider.
* **Fill Level Monitoring**: Track the remaining capacity (scent/liquid) in percent.
* **Connectivity Status**: Monitor if your device is currently online or offline.
* **Automatic Synchronization**: Status updates every 10 seconds (configurable) to match the Revoltab App.
* **Device Grouping**: All entities (switch, slider, sensors) are grouped under a single "HIDE" device for a clean UI.

---

## 🚀 Installation

### 1. Via HACS (Recommended)
1. Open **HACS** in your Home Assistant instance.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Add the URL of this repository: `https://github.com/akikels/homeassistant-revoltab`
4. Select **Integration** as the category and click **Add**.
5. Search for "Revoltab HIDE" and click **Download**.
6. **Restart Home Assistant.**

### 2. Manual Installation
1. Download the `custom_components/revoltab` folder from this repo.
2. Copy the folder into your Home Assistant directory under `/config/custom_components/`.
3. **Restart Home Assistant.**

---

## 🔑 How to get your Bearer Token

To use this integration, you need an API Bearer Token from the Revoltab backend:

1. Visit the integration portal: [backend.revoltab.com/loxone/](https://backend.revoltab.com/loxone/)
2. Log in using your official **Revoltab App credentials**.
3. In the device overview, locate the **"Generate Key"** button.
4. Copy the generated string. This is your **Bearer Token** used for the setup.

---

## ⚙️ Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Revoltab HIDE**.
4. Enter your **Bearer Token** in the setup window.
5. Your device will automatically appear with all its sensors and controls.

---

## ℹ️ Important Technical Notes

### Cloud-Based API
This integration is **cloud-based**. It communicates with Revoltab's servers via the Internet. There is currently no local API available for these devices.

### Polling Rate & Rate Limiting
By default, the integration fetches data every **10 seconds**. This allows for quick updates if you change settings in the official Revoltab app. 
* Changing the intensity or power state in Home Assistant triggers an **immediate** status refresh.
* If you experience "Unavailable" states, you may be hitting a rate limit. In this case, increase the `SCAN_INTERVAL` in `__init__.py`.

---

## 🛠 Troubleshooting

### "Invalid Auth" Error
* Ensure you copied the full token correctly.
* Make sure you used the [Loxone Portal](https://backend.revoltab.com/loxone/) to generate the key, as standard app keys might not work with the API.

### Missing Entities
* If the Intensity slider or Sensors do not appear, clear your browser cache (`Ctrl + F5`) and ensure you have updated to the latest version of this integration.

---

*Disclaimer: This is an unofficial integration and is not affiliated with or endorsed by Revoltab AG.*
