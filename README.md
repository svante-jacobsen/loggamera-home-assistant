# Loggamera Home Assistant Integration

A custom integration for Home Assistant that connects to the [Loggamera](https://loggamera.se/) API to fetch energy consumption data from a Loggamera-connected power meter.

## Features

- Fetches accumulated energy consumption (in kWh) every 15 minutes.
- Calculates deltas (consumption between updates).
- Fully compatible with Home Assistant’s Energy Dashboard via the `total_increasing` state class.

## Requirements

To use this integration, the following is required:

- A **Power Meter** connected to the Loggamera platform.
- An active **Loggamera account**.
- **API access** enabled by Loggamera (you must email them to request access).

## Installation

1. Copy the `loggamera/` folder into your `config/custom_components/` directory:

```
config/
└── custom_components/
    └── loggamera/
        ├── __init__.py
        ├── sensor.py
        ├── manifest.json
        └── const.py
```

2. Restart Home Assistant.

3. Add the integration via the UI:
   - Go to **Settings > Devices & Services > Add Integration**.
   - Search for **Loggamera** and follow the setup flow.

## Configuration

You’ll need:
- Your **API Key** from Loggamera.
- Your **Device ID**.

These are provided by Loggamera and can be entered via the integration setup in the Home Assistant UI.

## Update Interval

The integration fetches new data every **15 minutes** using Home Assistant’s `DataUpdateCoordinator`.

## API Usage

This integration uses the **PowerMeter** part of the Loggamera API, documented here:
[https://documenter.getpostman.com/view/6665372/SzYexbZa](https://documenter.getpostman.com/view/6665372/SzYexbZa)

It specifically queries:

```
POST https://platform.loggamera.se/api/v2/PowerMeter
```

…and expects a JSON payload with the API key and device ID.

## Sensors

| Sensor Name                        | Description                                 |
|-----------------------------------|---------------------------------------------|
| `sensor.loggamera_consumption_accumulated` | Total energy consumed in kWh (accumulated). |
| `sensor.loggamera_consumption`    | Delta energy consumed since last update.    |

## Development

This integration is written using Home Assistant’s async architecture. It uses a `DataUpdateCoordinator` for clean separation of concerns and periodic background updates.

To test locally:
```bash
hass -c /path/to/config
```

## License

MIT License

---

Maintained with 💡 by [Your Name]