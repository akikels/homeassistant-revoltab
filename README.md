# Revoltab HIDE Integration for Home Assistant

This custom integration allows you to control and monitor **Revoltab HIDE** devices directly from Home Assistant. It utilizes the Revoltab Cloud API to provide seamless control and real-time status updates.

## ✨ Features
* **Power Control**: Turn your HIDE device on or off (Start/Stop).
* **Intensity Selection**: Choose from 7 predefined levels (Subtle to Intense) for easy control.
* **Intensity Slider**: A dedicated level slider (1-7) for precise intensity management.
* **Fill Level Monitoring**: Track the remaining scent/liquid capacity in percent.
* **Connectivity Status**: Real-time monitoring of your device's online/offline status.
* **Configurable Polling**: Adjust the update interval (Pollrate) directly in the UI without touching any code.
* **Modern UI**: Includes official branding with logos and icons for a native Home Assistant feel.

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

### Initial Setup
1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration** and search for **Revoltab HIDE**.
3. Enter your **Bearer Token** in the setup window.
4. Your device will automatically appear with all its sensors and controls.

### Adjusting the Update Interval (Pollrate)
You can change how often Home Assistant fetches data from the API:
1. Go to **Settings** > **Devices & Services**.
2. Find the **Revoltab HIDE** integration.
3. Click on **Configure**.
4. Enter your desired interval in seconds (Default: `5`).
5. Click **Submit**. The integration will reload automatically with the new settings.

---

## ℹ️ Technical Notes

### Cloud-Based API
This integration communicates with Revoltab's servers via the Internet. There is currently no local API available.

### Intensity Levels
The integration maps the API's 0-100% range to 7 user-friendly levels:
* **1 (Subtle)** | **2 (Relaxed)** | **3 (Balanced)** | **4 (Moderate)** | **5 (Pleasant)** | **6 (Strong)** | **7 (Intense)**

---

## 🛠 Troubleshooting

### "Invalid Auth" Error
* Ensure you copied the full token correctly.
* Verify you used the [Loxone Portal](https://backend.revoltab.com/loxone/) to generate the key.

### Missing Icons or German Labels
* If the icons or translations do not appear correctly, clear your browser cache (**Ctrl + F5**) and ensure the `translations` folder is present in your installation.

---

*Disclaimer: This is an unofficial integration and is not affiliated with or endorsed by Revoltab AG.*