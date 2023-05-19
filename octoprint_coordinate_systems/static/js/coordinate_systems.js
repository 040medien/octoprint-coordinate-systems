$(function() {
    function CoordinateSystemsViewModel(parameters) {
        var self = this;
    
        self.control = parameters[0];
    
        self.gcode = ko.observable('');
        
        self.activeSystem = ko.observable('G54');
        self.xOffset = ko.observable(0);
        self.yOffset = ko.observable(0);
        self.zOffset = ko.observable(0);
        self.xPosition = ko.observable(0);
        self.yPosition = ko.observable(0);
        self.zPosition = ko.observable(0);
        self.label = ko.observable();

        self.systemLabels = ko.observableArray([]);
        
        self.availableSystems = ko.observableArray([
            'G54',
            'G55',
            'G56',
            'G57',
            'G58',
            'G59',
            'G59.1',
            'G59.2',
            'G59.3',
        ]);

        self.save_offsets = function(system, xOffset, yOffset, zOffset, label) {
            OctoPrint.postJson('plugin/coordinatesystems/save_offsets', {
                system: system,
                x_offset: xOffset,
                y_offset: yOffset,
                z_offset: zOffset,
                label: label
            });
        };

        self.restore_offsets = function(system) {
            OctoPrint.getJson('plugin/coordinatesystems/load_offsets', {
                system: system
            }).done(function(response) {
                var offsets = response.offsets;
                self.xOffset(offsets.x);
                self.yOffset(offsets.y);
                self.zOffset(offsets.z);
                self.label(offsets.label);

                var systemIndex = self.systemLabels().findIndex(function(element) {
                    return element.system === system;
                });

                if (systemIndex !== -1) {
                    self.systemLabels()[systemIndex].label = offsets.label;
                } else {
                    self.systemLabels.push({system: system, label: offsets.label});
                }

                self.set_offsets(system, offsets.x, offsets.y, offsets.z);
            });
        };

        self.sendCustomCommand = function(command) {
            var gcode = self.gcode();
            if (!gcode) {
                return;
            }
        
            self.control.sendCustomCommand({ command: gcode });
            self.gcode('');
        };

        self.systemOptions = ko.computed(function() {
            return self.availableSystems().map(function(system) {
                var label = self.systemLabels().find(function(element) {
                    return element.system === system;
                });

                return {
                    system: system,
                    text: system + (label ? " (" + label.label + ")" : "")
                };
            });
        });
        
        self.activeSystem.subscribe(function(newSystem) {
            // Switch to the new coordinate system
            OctoPrint.postJson('plugin/coordinatesystems/set_system', {
                system: newSystem
            });

            // Request current position
            OctoPrint.control.sendGcode('M114');
        });

        self.set_offsets = function(system, xOffset, yOffset, zOffset) {
            // Use OctoPrint's API client library to make a POST request to your plugin's API endpoint
            OctoPrint.postJson('plugin/coordinatesystems/set_offsets', {
                system: system,
                x_offset: xOffset,
                y_offset: yOffset,
                z_offset: zOffset
            });
        };

        self.set_position = function(system, x, y, z) {
            OctoPrint.postJson('plugin/coordinatesystems/set_position', {
                system: system,
                x: x,
                y: y,
                z: z
            });
        };

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != 'coordinatesystems') {
                return;
            }

            if (data.type == 'positionUpdate') {
                self.xPosition(data.x);
                self.yPosition(data.y);
                self.zPosition(data.z);
            }
        };
    }
    
    OCTOPRINT_VIEWMODELS.push({
        construct: CoordinateSystemsViewModel,
        dependencies: ["settingsViewModel"],  // List of other ViewModels that your ViewModel depends on
        elements: ["#tab_plugin_coordinatesystems"]  // IDs of the HTML elements to bind your ViewModel to
    });
});
