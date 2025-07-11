# GlowSwitch HA

A Home Assistant integration for controlling GlowSwitch Bluetooth LE devices locally.

## Features

*   **Local Control:** Communicates directly with your devices over Bluetooth Low Energy for a fast and private experience.
*   **Auto-Discovery:** Automatically discovers and configures `glowswitch` and `glowdim` devices.
*   **On/Off Control:** Provides on/off control for `glowswitch` devices.
*   **Brightness Control:** Supports brightness adjustment for `glowdim` devices.
*   **Robust Connection:** Automatically handles device disconnections and reconnections (e.g., after a power cycle).

## Supported Devices

This integration was built to support the devices defined in `DEVICEINFO.MD`:

*   **glowswitch**: A simple on/off light.
*   **glowdim**: A light with brightness control.

## Installation

1.  Ensure the [Bluetooth integration](https://www.home-assistant.io/integrations/bluetooth/) is enabled and configured in Home Assistant.
2.  Copy the `custom_components/glowswitch_ha` directory into the `<config>/custom_components` directory of your Home Assistant installation.
3.  Restart Home Assistant.

## Configuration

This integration uses auto-discovery to find and set up devices.

1.  After installation and restarting, navigate to **Settings** > **Devices & Services**.
2.  If your GlowSwitch device is powered on and within range, it will appear as a discovered device.
3.  Click **Configure** on the discovered device card to add it to Home Assistant.

A light entity will be created for your device, which you can then add to your Lovelace dashboards.
