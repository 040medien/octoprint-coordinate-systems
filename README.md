# OctoPrint Coordinate Systems Plugin

This plugin for OctoPrint makes it easier to work with the Workspace Coordinate Systems (G54-G59.3) in the Marlin firmware.

## Features

- Switch between different Workspace Coordinate Systems.
- Display the current position and offsets for the selected coordinate system.
- Set the position in the selected coordinate system.
- Set the offsets for the selected coordinate system.
- Save and restore offsets for each coordinate system.
- Assign labels to coordinate systems for easy identification.

## Installation

You can install this plugin via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/040medien/octoprint-coordinate-systems/archive/master.zip

## Usage

1. Open the "Coordinate Systems" tab in OctoPrint.
2. Select the coordinate system you want to work with from the dropdown menu.
3. The current position and offsets for the selected system will be displayed.
4. Enter the new position or offsets in the respective fields and click the "Set Position" or "Set Offsets" button to apply them.
5. If you want to assign a label to the selected system for easy identification, enter it in the "Label" field and click the "Save" button.
6. You can restore the saved offsets and label for each system by selecting it from the dropdown menu and clicking the "Restore" button.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the terms of the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
