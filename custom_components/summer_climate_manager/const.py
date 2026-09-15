DOMAIN = "summer_climate_manager"
PLATFORMS = ["sensor", "binary_sensor", "switch", "select"]

CONF_GRID_IMPORT = "grid_import"
CONF_GRID_EXPORT = "grid_export"
CONF_EV_CHARGING = "ev_charging"
CONF_EV_POWER = "ev_power"

CONF_KIDS_CLIMATE = "kids_climate"
CONF_KIDS_TEMP = "kids_temp"
CONF_KIDS_HUMIDITY = "kids_humidity"

CONF_NURSERY_CLIMATE = "nursery_climate"
CONF_NURSERY_TEMP = "nursery_temp"
CONF_NURSERY_HUMIDITY = "nursery_humidity"

CONF_MASTER_CLIMATE = "master_climate"
CONF_MASTER_TEMP = "master_temp"
CONF_MASTER_HUMIDITY = "master_humidity"

CONF_OPEN_CLIMATE = "open_climate"
CONF_OPEN_TEMP = "open_temp"
CONF_OPEN_HUMIDITY = "open_humidity"

CONF_HISENSE_ECO = "hisense_eco"
CONF_HISENSE_QUIET = "hisense_quiet"

DEFAULTS = {
    "normal_target": 24.0,
    "solar_target": 22.0,
    "bedroom_ceiling": 25.0,
    "open_ceiling": 27.0,
    "solar_light_w": 1500,
    "solar_medium_w": 2500,
    "solar_high_w": 4000,
}
