$(function () {
  function CoordinateSystemsViewModel(parameters) {
    var self = this;

    self.settingsViewModel = parameters[0];

    self.setOffsets = function (system) {
      var offsets = {
        X: parseFloat($(`input[data-system="${system}"][data-axis="X"]`).val()) || 0,
        Y: parseFloat($(`input[data-system="${system}"][data-axis="Y"]`).val()) || 0,
        Z: parseFloat($(`input[data-system="${system}"][data-axis="Z"]`).val()) || 0,
      };

      OctoPrint.simpleApiCommand("coordinate_systems", "set_offsets", { offsets: offsets, system: system })
        .done(function () {
          new PNotify({
            title: "Offsets Applied",
            text: `Offsets for ${system} have been set.`,
            type: "success",
            hide: true,
          });
        })
        .fail(function () {
          new PNotify({
            title: "Error Applying Offsets",
            text: `There was an error setting offsets for ${system}.`,
            type: "error",
            hide: true,
          });
        });
    };
  }

  OCTOPRINT_VIEWMODELS.push({
    construct: CoordinateSystemsViewModel,
    dependencies: ["settingsViewModel"],
    elements: ["#coordinate_systems"],
  });

  // Add event listener for the "Set Offsets" button
  $(document).on("click", ".btn-set-offsets", function () {
    var system = $(this).data("system");
    var coordinateSystemsViewModelInstance = OCTOPRINT_VIEWMODELS_BY_CONSTRUCTOR.CoordinateSystemsViewModel[0];
    coordinateSystemsViewModelInstance.setOffsets(system);
  });
});
