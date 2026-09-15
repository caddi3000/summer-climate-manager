# Summer Climate Manager

Solar-aware summer climate monitoring for Home Assistant.

## v0.1.2

This release is **monitor-only** and does not send commands to air conditioners.

## Required repository layout

The GitHub repository root must contain these items directly:

```text
summer-climate-manager/
├── custom_components/
│   └── summer_climate_manager/
│       ├── __init__.py
│       ├── binary_sensor.py
│       ├── config_flow.py
│       ├── const.py
│       ├── entity.py
│       ├── logic.py
│       ├── manifest.json
│       ├── select.py
│       ├── sensor.py
│       ├── strings.json
│       ├── switch.py
│       └── translations/
│           └── en.json
├── hacs.json
├── README.md
└── .gitignore
```

Do **not** upload the outer extracted folder as another directory inside the GitHub repository.

## HACS installation

Add `https://github.com/caddi3000/summer-climate-manager` as a HACS custom repository with category **Integration**.

After installation, restart Home Assistant and add **Summer Climate Manager** from Settings → Devices & services.

## Privacy

The repository contains no household entity IDs or credentials. Entity selection is performed locally in the Home Assistant config flow.

Never commit access tokens, passwords, API keys, Home Assistant backups, `secrets.yaml`, `.storage`, databases, or configuration files containing private information.
