import logging
from datetime import timedelta
import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (CoordinatorEntity, DataUpdateCoordinator)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=15)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = LoggameraCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()

    entities = [
        LoggameraAccumulatedSensor(coordinator, entry.entry_id),
        LoggameraDeltaSensor(coordinator, entry.entry_id, hass),
    ]
    async_add_entities(entities)

class LoggameraCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config_data: dict):
        super().__init__(
            hass,
            _LOGGER,
            name="Loggamera Data Coordinator",
            update_interval=SCAN_INTERVAL,
        )
        self.api_key = config_data["api_key"]
        self.device_id = config_data["device_id"]

    async def _async_update_data(self):
        _LOGGER.info("Loggamera update: fetching latest kWh")
        url = "https://platform.loggamera.se/api/v2/PowerMeter"
        headers = {"Content-Type": "application/json"}
        json_data = {
            "ApiKey": self.api_key,
            "DeviceId": self.device_id
        }

        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=json_data) as resp:
                        if resp.status != 200:
                            raise Exception(f"API error: {resp.status}")
                        data = await resp.json()
                        total_kwh = next(
                            (float(x["Value"]) for x in data["Data"]["Values"]
                             if x["Name"] == "ConsumedTotalInkWh"),
                            None
                        )
                        return {"total_kwh": total_kwh}
        except Exception as err:
            raise UpdateFailed(f"Failed to fetch data: {err}") from err

class LoggameraAccumulatedSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"loggamera_consumption_accumulated_{entry_id}"
        self._attr_name = "Loggamera Consumption Accumulated"
        self._attr_native_unit_of_measurement = "kWh"
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self):
        return self.coordinator.data.get("total_kwh")

class LoggameraDeltaSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, hass: HomeAssistant):
        super().__init__(coordinator)
        self.hass = hass
        self._attr_unique_id = f"loggamera_consumption_{entry_id}"
        self._attr_name = "Loggamera Consumption"
        self._attr_native_unit_of_measurement = "kWh"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        current = self.coordinator.data.get("total_kwh")
        last_state = self.hass.states.get(self.entity_id)
        if last_state and last_state.state not in (None, "", "unknown", "unavailable"):
            try:
                previous_total = float(last_state.attributes.get("last_total", 0))
                delta = current - previous_total
                return round(delta, 3)
            except Exception:
                return 0.0
        return 0.0

    @property
    def extra_state_attributes(self):
        return {
            "last_total": self.coordinator.data.get("total_kwh")
        }
