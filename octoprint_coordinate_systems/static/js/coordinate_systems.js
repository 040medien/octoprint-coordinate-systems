$(function() {
    function CoordinateSystemsViewModel(parameters) {
        var self = this;
        
        self.control = parameters[0];
        
        self.gcode = ko.observable('');
        
        self.sendCustomCommand = function(command) {
            var gcode = self.gcode();
            if (!gcode) {
                return;
            }
            
            self.control.sendCustomCommand({ command: gcode });
            self.gcode('');
        };

        self.set_offsets = function(system, xOffset, yOffset, zOffset) {
            // Use OctoPrint's API client library to make a POST request to your plugin's API endpoint
            OctoPrint.postJson('plugin/coordinate_systems/set_offsets', {
                system: system,
                x_offset: xOffset,
                y_offset: yOffset,
                z_offset: zOffset
            });
        };
    }
    
    OCTOPRINT_VIEWMODELS.push([
        CoordinateSystemsViewModel,
        ['controlViewModel'],
        ['#tab_plugin_coordinate_systems']
    ]);
});
