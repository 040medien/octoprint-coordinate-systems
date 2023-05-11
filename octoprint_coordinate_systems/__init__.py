import octoprint.plugin
from octoprint.events import Events

class CoordinateSystemsPlugin(octoprint.plugin.StartupPlugin,
                              octoprint.plugin.TemplatePlugin,
                              octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.SimpleApiPlugin):

    def __init__(self):
        pass

    ## StartupPlugin mixin

    def on_after_startup(self):
        self._logger.info("Coordinate Systems Plugin started")

    ## TemplatePlugin mixin

    def get_template_configs(self):
        return [
            {
                "type": "tab",
                "custom_bindings": True,
                "template": "coordinate_systems_tab.jinja2",
                "name": "Coordinate Systems"
            }
        ]

    ## SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(offsets={})

    ## AssetPlugin mixin

    def get_assets(self):
        return dict(
            js=["js/coordinate_systems.js"],
            css=["css/coordinate_systems.css"]
        )

    ## SimpleApiPlugin mixin

    def get_api_commands(self):
        return {
            "set_offsets": ["offsets"]
        }

    def on_api_command(self, command, data):
        if command == "set_offsets":
            offsets = data.get("offsets", None)
            if offsets is not None:
                self.set_offsets(offsets)

    def set_offsets(self, system, xOffset, yOffset, zOffset):
            # Send G53 to switch to machine coordinates
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
    
                # Set new positions for the workspace coordinate system
                self._printer.commands("G92 X{} Y{} Z{}".format(newX, newY, newZ))
    
                # Unsubscribe from the 'PositionUpdate' event
                self._event_bus.unsubscribe(Events.POSITION_UPDATE, on_position_update)
    
            # Subscribe to the 'PositionUpdate' event
            self._event_bus.subscribe(Events.POSITION_UPDATE, on_position_update)

__plugin_name__ = "Coordinate Systems Plugin"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = CoordinateSystemsPlugin()
