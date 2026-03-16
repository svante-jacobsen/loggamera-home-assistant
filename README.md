# Loggamera Home Assistant Integration

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg?logo=HomeAssistantCommunityStore&logoColor=white)](https://github.com/hacs/integration) [![GitHub release](https://img.shields.io/github/v/release/svante-jacobsen/loggamera-home-assistant?style=flat-square)](https://github.com/svante-jacobsen/loggamera-home-assistant/releases) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)


A custom integration for Home Assistant that connects to the [Loggamera](https://loggamera.se/) API to fetch energy consumption data from a Loggamera-connected power meter.


## About this integration
This **Home Assistant integration for Loggamera** allows users to automatically fetch power data from their Loggamera-connected meters and display it in Home Assistant’s Energy Dashboard, providing seamless monitoring of energy consumption.

## Features

- Fetches accumulated energy consumption (in kWh) every 15 minutes.
- Fully compatible with Home Assistant’s Energy Dashboard via the `total_increasing` state class.

## Requirements

To use this integration, the following is required:

- A **Power Meter** connected to the Loggamera platform.
- An active **Loggamera account**.
- **API access** enabled by Loggamera (you must email them to request access).

## Installation

### HACS Installation

1. Open **HACS** in Home Assistant.
2. Go to **Integrations** and click the `+` button.
3. Search for **Loggamera** and install it.
4. Restart Home Assistant.

### Manual Installation

1. Copy the `loggamera/` folder into your `config/custom_components/` directory.
2. Restart Home Assistant.
3. In Home Assistant, go to **Settings > Devices & Services > Add Integration**.
4. Search for **Loggamera** and follow the setup flow.

## Configuration

You’ll need:
- Your **API Key** from Loggamera.
- Your **Device ID**.

These are provided by Loggamera and can be entered via the integration setup UI.

## Screenshot

<img width="1184" height="436" alt="Screenshot 2026-03-16 163510" src="https://github.com/user-attachments/assets/c7f7b888-07c3-4cb1-99b8-82eda682e494" />

## API Usage

This integration uses the **PowerMeter** part of the Loggamera API, documented here:
[https://documenter.getpostman.com/view/6665372/SzYexbZa](https://documenter.getpostman.com/view/6665372/SzYexbZa)

## Sensors

| Sensor Name                        | Description                                 |
|-----------------------------------|---------------------------------------------|
| `sensor.loggamera_consumption`    | Total energy consumed in kWh (accumulated). |

## Development

This integration is written using Home Assistant’s async architecture. It uses a `DataUpdateCoordinator` for clean separation of concerns and periodic background updates.

To test locally:
```bash
hass -c /path/to/config
```

## License

MIT License

---

Maintained with 💡 by Svante Jacobsen

https://my.home-assistant.io/redirect/hacs_repository/?owner=svante-jacobsen&repository=loggamera-home-assistant&category=integration
