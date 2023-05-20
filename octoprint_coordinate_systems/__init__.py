import octoprint.plugin
from octoprint.events import Events
from octoprint.settings import NoSuchSettingsPath
from flask import jsonify, request

class CoordinateSystemsPlugin(octoprint.plugin.StartupPlugin,
                              octoprint.plugin.TemplatePlugin,
                              octoprint.plugin.AssetPlugin,
                              octoprint.plugin.EventHandlerPlugin,
                              octoprint.plugin.SettingsPlugin,
                              octoprint.plugin.BlueprintPlugin):
    def __init__(self):
        super().__init__()
        self.processing_offsets = False

    def get_template_configs(self):
        return [
            {"type": "tab", "custom_bindings": False, "template": "coordinate_systems_tab.jinja2"}
        ]

    def get_assets(self):
        return {
            "js": ["js/coordinate_systems.js"],
            "css": ["css/coordinate_systems.css"]
        }

    @octoprint.plugin.BlueprintPlugin.route("/set_offsets", methods=["POST"])
    def set_offsets_route(self):
        data = request.json
        system = data.get('system')
        x_offset = data.get('x_offset')
        y_offset = data.get('y_offset')
        z_offset = data.get('z_offset')
        self.set_offsets(system, x_offset, y_offset, z_offset)
        return jsonify(success=True)

    @octoprint.plugin.BlueprintPlugin.route("/save_offsets", methods=["POST"])
    def save_offsets_route(self):
        data = request.json
        system = data.get('system')
        x_offset = data.get('x_offset')
        y_offset = data.get('y_offset')
        z_offset = data.get('z_offset')
        label = data.get('label')
        self.save_offsets(system, x_offset, y_offset, z_offset, label)
        return jsonify(success=True)

    @octoprint.plugin.BlueprintPlugin.route("/load_offsets", methods=["GET"])
    def load_offsets_route(self):
        system = request.args.get('system')
        offsets = self.load_offsets(system)
        return jsonify(offsets=offsets)

    @octoprint.plugin.BlueprintPlugin.route("/set_position", methods=["POST"])
    def set_position_route(self):
        data = request.json
        system = data.get('system')
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')
        self.set_position(system, x, y, z)
        return jsonify(success=True)

    @octoprint.plugin.BlueprintPlugin.route("/set_system", methods=["POST"])
    def set_system_route(self):
        data = request.json
        system = data.get('system')
        self.set_system(system)
        return jsonify(success=True)

    def save_offsets(self, system, xOffset, yOffset, zOffset, label):
        self._settings.set(["offsets", system], {"x": xOffset, "y": yOffset, "z": zOffset, "label": label})
        self._settings.save()  # save the settings to file

    def load_offsets(self, system):
        try:
            return self._settings.get(["offsets", system])
        except NoSuchSettingsPath:
            return {"x": 0, "y": 0, "z": 0, "label": ""}  # return default offsets and label if none exist

    def set_offsets(self, system, xOffset, yOffset, zOffset):
        self._logger.info("Setting offsets: system=%s, xOffset=%s, yOffset=%s, zOffset=%s" % (system, xOffset, yOffset, zOffset))

        self.processing_offsets = True
        
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.zOffset = zOffset
        
        # Switch to the desired workspace coordinate system
        self._printer.commands(system)

        # Reset the workspace coordinate system to machine zero
        self._printer.commands("G92.1")

        # Get position update
        self._printer.commands("M114")

    def set_position(self, system, x, y, z):
        self._logger.info("Setting position: system=%s, x=%s, y=%s, z=%s" % (system, x, y, z))

        # Switch to the desired workspace coordinate system
        self._printer.commands(system)

        # Set new position for the workspace coordinate system
        self._printer.commands("G92 X{} Y{} Z{}".format(x, y, z))

    def set_system(self, system):
        # Switch to the desired workspace coordinate system
        self._printer.commands(system)

    # ~~ EventPlugin mixin
    def on_event(self, event, payload):
        if event == Events.POSITION_UPDATE:
            if self.processing_offsets:
                self._logger.info("Received POSITION_UPDATE event: payload=%s" % payload)

                newX = payload["x"] - self.xOffset
                newY = payload["y"] - self.yOffset
                newZ = payload["z"] - self.zOffset
            
                self._printer.commands("G92 X{} Y{} Z{}".format(newX, newY, newZ))
            
                self.processing_offsets = False  # reset the flag

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
