# Gemini Project Context: glowswitch_ha

This document provides context for the Gemini agent regarding the `glowswitch_ha` project.

## Project Overview

`glowswitch_ha` is a custom integration for Home Assistant designed to control a line of Bluetooth Low Energy (BLE) lighting products from the brand "glowswitch". The integration allows users to control these lights directly and locally from their Home Assistant instance.

## Core Functionality

- **Device Types:** The integration supports two types of devices:
    - `glowswitch`: A simple on/off light.
    - `glowdim`: A light with brightness control.
- **Communication:** Control is performed locally over Bluetooth LE.
- **Home Assistant Integration:** It integrates with Home Assistant's `light` platform.
- **Discovery:** It uses Home Assistant's Bluetooth auto-discovery mechanism to find and configure new devices.
- **Configuration:** The integration is configured via the Home Assistant UI (Config Flow), with support for both auto-discovery and manual setup.

## Technical Details

- **Language:** Python 3
- **Framework:** [Home Assistant Integration Framework](https://developers.home-assistant.io/)
- **Key Dependencies:**
    - `bleak-retry-connector`: Used for robustly handling BLE device connections, especially after power cycles.
- **Directory Structure:**
    - `custom_components/glowswitch_ha/`: The root directory for the integration.
        - `manifest.json`: Declares the integration's metadata, version, dependencies, and Bluetooth service UUIDs for discovery.
        - `light.py`: Defines the light entities and handles communication with the devices.
        - `config_flow.py`: Manages the user configuration process (both discovery and manual setup).
        - `const.py`: Stores constant values like the domain and service UUIDs.
        - `translations/en.json`: Contains the English UI strings for the configuration flow.
        - `hacs.json`: Provides metadata for the Home Assistant Community Store (HACS).
- **Versioning:** The project uses semantic versioning (e.g., `v0.2.3`). Versions are tracked with Git tags, which is a requirement for HACS.

## Device BLE Specifications

- **glowswitch device:**
    - Service UUID: `12345678-1234-5678-1234-56789abcdef0`
    - Characteristic UUID: `12345678-1234-5678-1234-56789abcdef1`
    - Commands: `0x01` (On), `0x00` (Off)

- **glowdim device:**
    - Service UUID: `12345678-1234-5678-1234-56789abcdefa`
    - Characteristic UUID: `12345678-1234-5678-1234-56789abcdef1`
    - Commands: `0x00` (Off) to `0x64` (100% brightness)
