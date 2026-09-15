# Summer Climate Manager v0.1.3

Solar-aware summer climate monitoring for Home Assistant, now with a companion interactive Lovelace floorplan card.

## New in v0.1.3

- Bundled `custom:summer-climate-floorplan` frontend card.
- Bundled floorplan/dashboard artwork.
- Live Kids, Nursery, Master and Open Plan overlays.
- Click/tap a room to open its detail pane.
- Manual AC controls remain available while the manager itself stays in Monitor mode.
- The card reads the entity selections already made in the integration via the new **Frontend Config** entity.
- The frontend module is registered automatically by the integration after Home Assistant restarts.

## Update

Replace the repository contents with this release, commit/push, refresh HACS, update Summer Climate Manager, then **restart Home Assistant**.

After restart, add a Manual card to any dashboard:

```yaml
type: custom:summer-climate-floorplan
```

No entity IDs are required in the card YAML.

## How to verify it loaded

1. Settings → Devices & services → Summer Climate Manager should show a `Frontend Config` sensor with state `ready`.
2. Opening `/summer_climate_manager/floorplan.png` on your Home Assistant host should show the bundled artwork.
3. The Manual card above should render the floorplan instead of reporting an unknown custom element.
4. Room temperatures/humidity should match the underlying Home Assistant sensors and update as their states change.
5. Tapping a room should change the right-hand detail panel. **AC controls** opens Home Assistant's normal climate more-info dialog.

If the card says it is waiting for Frontend Config, reload the integration/restart Home Assistant. If Home Assistant says the custom card does not exist, hard-refresh the browser/app after the restart.

## Safety

v0.1.3 does not enable automatic AC actuation. The decision engine remains monitor/recommendation-first. Buttons in the frontend are explicit manual climate commands.


## v0.1.4

Fixes loading of the companion Lovelace card.

The integration now serves its frontend assets through Home Assistant's supported
`async_register_static_paths` API and registers the card JavaScript with the
frontend during integration setup.

After updating and restarting Home Assistant, use:

```yaml
type: custom:summer-climate-floorplan
```

If a browser had v0.1.3 open, perform one hard refresh after the Home Assistant
restart. The resource URL includes a v0.1.4 cache-busting query string.


## v0.1.5

- New approved floorplan artwork.
- The mock dashboard chrome/data is cropped out of the background; temperatures and states are live Lovelace overlays.
- Added a clickable Delta AC Max / EVCC hotspot over the under-house garage area.
- Added an EV Charger tile that opens the configured EVCC/charger entity.
- Full-width responsive layout.
- Fixed floorplan asset URL, GUI version reporting, Unicode symbols and cache busting.
