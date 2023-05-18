import octoprint.plugin
from octoprint.events import Events
from octoprint.settings import NoSuchSettingsPath

class CoordinateSystemsPlugin(octoprint.plugin.StartupPlugin,
                              octoprint.plugin.TemplatePlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.EventHandlerPlugin,
                              octoprint.plugin.SettingsPlugin):

    def get_template_configs(self):
        return [
            {"type": "tab", "custom_bindings": True, "template": "coordinate_systems_tab.jinja2"}
        ]

    def save_offsets(self, system, xOffset, yOffset, zOffset, label):
        self._settings.set(["offsets", system], {"x": xOffset, "y": yOffset, "z": zOffset, "label": label})
        self._settings.save()  # save the settings to file

    def load_offsets(self, system):
        try:
            return self._settings.get(["offsets", system])
        except NoSuchSettingsPath:
            return {"x": 0, "y": 0, "z": 0, "label": ""}  # return default offsets and label if none exist

    def set_offsets(self, system, xOffset, yOffset, zOffset):
        # Switch to machine coordinates
        self._printer.commands("G53")

        # Request current machine coordinates with M114
        self._printer.commands("M114")

        # Define a callback to handle the 'PositionUpdate' event
        def on_position_update(event, payload):
            # Calculate new positions based on the desired offsets
            newX = payload["x"] - xOffset
            newY = payload["y"] - yOffset
            newZ = payload["z"] - zOffset

            # Switch to the desired workspace coordinate system
            self._printer.commands(system)

            # Reset the workspace coordinate system to machine zero
            self._printer.commands("G92.1")

            # Set new positions for the workspace coordinate system
            self._printer.commands("G92 X{} Y{} Z{}".format(newX, newY, newZ))

            # Unsubscribe from the 'PositionUpdate' event
            self._event_bus.unsubscribe(Events.POSITION_UPDATE, on_position_update)

        # Subscribe to the 'PositionUpdate' event
        self._event_bus.subscribe(Events.POSITION_UPDATE, on_position_update)

    def set_position(self, system, x, y, z):
        # Switch to the desired workspace coordinate system
        self._printer.commands(system)

        # Set new position for the workspace coordinate system
        self._printer.commands("G92 X{} Y{} Z{}".format(x, y, z))

    def set_system(self, system):
        # Switch to the desired workspace coordinate system
        self._printer.commands(system)

    def on_event(self, event, payload):
        if event == Events.POSITION_UPDATE:
            # Get the current position
            x = payload['x']
            y = payload['y']
            z = payload['z']

            # Update the position in the frontend
            self._plugin_manager.send_plugin_message(self._identifier, {
                'type': 'positionUpdate',
                'x': x,
                'y': y,
                'z': z
            })

__plugin_name__ = "Workspace Coordinate Systems"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = CoordinateSystemsPlugin()
