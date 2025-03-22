# Beem Solar Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

This is a Home Assistant custom component for integrating with Beem Solar, allowing you to monitor your solar power generation data within Home Assistant.

## Features

- Real-time power generation monitoring
- Daily energy production tracking
- Monthly energy production tracking
- Automatic data updates via cloud polling

## Installation

### Option 1: HACS Installation (Recommended)

HACS est la méthode recommandée pour installer Beem Solar, car elle simplifie l'installation et les mises à jour.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=benlec&repository=ha-beem&category=integration)

Pour installer Beem Solar via HACS :

1.  Cliquez sur le badge ci-dessus pour ajouter ce dépôt personnalisé à HACS.
2.  Installez l'intégration "Beem Solar" depuis HACS.

### Option 2: Manual Installation

1. Download the latest release from the GitHub repository
2. Copy the `custom_components/ha-beem` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click the "+ Add Integration" button
3. Search for "Beem Solar"
4. Follow the configuration steps:
   - Enter your Beem Solar username
   - Enter your Beem Solar password

## Available Sensors

The integration provides the following sensors:

- **Power Generation**: Current power output in watts
- **Daily Energy**: Total energy generated today in kilowatt-hours
- **Monthly Energy**: Total energy generated this month in kilowatt-hours

## Requirements

- Home Assistant installation
- Beem Solar account credentials
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