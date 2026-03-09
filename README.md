# Revoltab HIDE Integration for Home Assistant

This custom integration allows you to control **Revoltab HIDE** devices (retractable sockets and connectors) directly from Home Assistant. Instead of manually adding REST commands to your `configuration.yaml` for every single device, this integration automatically discovers all devices linked to your account.

## ✨ Features
* **Automatic Discovery**: Automatically finds all HIDE devices associated with your Revoltab account.
* **Easy Setup**: Configuration via the Home Assistant user interface (Config Flow) – no YAML required.
* **Switch Entities**: Control (extend/retract) your devices just like a standard switch.

---

## 🚀 Installation

### 1. Via HACS (Recommended)
1. Open **HACS** in your Home Assistant instance.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Add the URL of this repository: `[https://github.com/akikels/homeassistant-revoltab](https://github.com/akikels/homeassistant-revoltab)`
4. Select **Integration** as the category and click **Add**.
5. Search for "Revoltab HIDE" and click **Download**.
6. **Restart Home Assistant.**

### 2. Manual Installation
1. Download the `custom_components/revoltab` folder from this repo.
2. Copy the folder into your Home Assistant directory under `/config/custom_components/`.
3. **Restart Home Assistant.**

---

## 🔑 How to get your API Key

To use this integration, you need an API key from the Revoltab backend:

1. Visit the dedicated integration page: [backend.revoltab.com/loxone/](https://backend.revoltab.com/loxone/).
2. Log in using your official **Revoltab App credentials**.
3. In the device overview, locate the **"Generate Key"** button.
4. Copy the generated key. You will need to paste it into the Home Assistant setup window.

---

## ⚙️ Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Revoltab HIDE**.
4. Enter the **API Key** you generated in the previous step.
5. Your devices will automatically appear as new switch entities.

---

## 🛠 Troubleshooting

### "Invalid Auth" Error
* Ensure the key was copied correctly without trailing spaces.
* Verify that you logged into the [Loxone sub-page](https://backend.revoltab.com/loxone/), as this is the specific portal for third-party system keys.

### Integration not found in the list
* If the integration does not appear after a restart, try clearing your browser cache (`Ctrl + F5` or `Cmd + Shift + R`).

---

*Disclaimer: This is an unofficial integration and is not affiliated with or endorsed by Revoltab AG.*
