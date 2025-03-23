# Beem Energy Integration for Home Assistant

![](/custom_components/ha-beem/brands/logo/logo.png)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)


[!["Buy Me A Banana"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/benlec)


This is a Home Assistant custom component for integrating with Beem Energy, allowing you to monitor your solar power generation data within Home Assistant.

## Features

- Real-time power generation monitoring
- Daily energy production tracking
- Monthly energy production tracking
- Automatic data updates via cloud polling

## Installation

### Option 1: HACS Installation (Recommended)

HACS is the recommended method to install Beem Energy as it simplifies installation and updates.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=benlec&repository=ha-beem&category=integration)

To install Beem Energy via HACS:

1.  Click the badge above to add this custom repository to HACS.
2.  Install the "Beem Energy" integration from HACS.

### Option 2: Manual Installation

1. Download the latest release from the GitHub repository
2. Copy the `custom_components/ha-beem` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click the "+ Add Integration" button
3. Search for "Beem Energy"
4. Follow the configuration steps:
   - Enter your Beem Energy email address and password
   - Optionally set the number of months of historical data to fetch (0-12 months)
   - Setting a value greater than 0 will retrieve historical energy production data for that many months
   - Enter your Beem Energy username
   - Enter your Beem Energy password

## Available Sensors

| Sensor Name | Description | Device Class | State Class | Unit |
|------------|-------------|--------------|-------------|------|
| Monthly Energy | Total energy consumption for the current month | energy | total_increasing | kWh |
| Daily Energy | Total energy consumption for the current day | energy | total_increasing | kWh |
| Current Power | Current power consumption | power | measurement | W |

## Historical Data

You can fetch historical data for specific months using the `fetch_historical_data` service. This allows you to retrieve past energy production data that wasn't automatically collected by Home Assistant.

To use this service:
1. Go to Developer Tools > Services
2. Select the "Beem Energy: Fetch Historical Data" service
3. Enter the month (1-12) and year for which you want to fetch data
4. Click "Call Service"

The historical data will be stored in your Home Assistant's database and will be available for visualization in graphs and statistics.

## Requirements

- Home Assistant installation
- Beem Energy account credentials
- Internet connection for cloud polling

## Technical Details

- **Version**: 0.1.0
- **IoT Class**: Cloud Polling
- **Dependencies**: aiohttp>=3.0.0

## Support

For bugs and feature requests, please [open an issue](https://github.com/benlec/ha-beem/issues) on GitHub.

## Credits

Created and maintained by [@benlec](https://github.com/benlec)

## License

This project is licensed under the MIT License - see the LICENSE file for details.