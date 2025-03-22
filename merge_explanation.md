## Folder Structure Issue Resolution

The integration currently has duplicate folders:
- `custom_components/beem/`
- `custom_components/ha-beem/`

### Analysis
1. The correct domain name is "ha-beem" as shown in the manifest.json
2. The following files need to be moved from beem/ to ha-beem/:
   - api.py
   - config_flow.py
   - coordinator.py
   - helpers.py
   - sensor.py
   - translations/ directory

### Required Actions
1. Move all files from custom_components/beem/ to custom_components/ha-beem/
2. Delete the empty beem/ directory
3. Update any domain references in the code from "beem" to "ha-beem" if needed

### Implementation Steps
Let me proceed with creating/moving these files in the correct location while maintaining their content.