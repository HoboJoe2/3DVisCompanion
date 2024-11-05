var jsonData = {
    "last_error": false,
    "models": [],
    "scenes": [],
    "options": {}
};

var socket = io();

// Update the tables data
function refreshData() {
    if (jsonData["last_error"]) { // This will be set to false by python after it recieves the websocket call at the end of this function
        alert("Failed import of one or more models! See command prompt window for more details. Error message:        " + jsonData["last_error"]);
    }

    $("#modelsTable tbody").empty(); // Clear tables
    $("#scenesTable tbody").empty();

    $.each(jsonData["models"], function(index, object) { // For each model
        $.each(object, function(path, metadata) { // For the data inside each model
            var modelNameFilterValue = $('#modelnamefilter').val().toLowerCase();
            var modelCategoryFilterValue = $('#modelcategoryfilter').val().toLowerCase();
            var modelDisplayName = metadata.modelDisplayName.toLowerCase()
            var modelCategory = metadata.modelCategory.toLowerCase()
            if ((!modelNameFilterValue && !modelCategoryFilterValue) || (modelDisplayName.includes(modelNameFilterValue) && modelCategory.includes(modelCategoryFilterValue))) { // If the model name/category matches the filters
                    const row = `
                    <tr>
                        <td><input type="text" value="${metadata.modelDisplayName}" class="display-input"></td>
                        <td><input type="text" value="${metadata.modelCategory}" class="category-input"></td>
                        <td>
                            <button class="update-btn" data-path="${path}" data-objecttype="model">Update</button>
                            <button class="delete-btn" data-path="${path}" data-objecttype="model">Delete</button>
                        </td>
                    </tr>
                `; // Doesn't use modelDisplayName variable because it should be case sensitive, whereas comparing against filters shouldn't be case sensitive
                ($("#modelsTable tbody")).append(row); // Add generated row to table
            }
        });
    });

    $.each(jsonData["scenes"], function(index, object) { // Very similar to the models table, this could have maybe been done in the same loop as the models for better code quality but oh well
        $.each(object, function(path, metadata) {
            var sceneNameFilterValue = $('#scenenamefilter').val().toLowerCase();
            var sceneCategoryFilterValue = $('#scenecategoryfilter').val().toLowerCase();
            var sceneDisplayName = metadata.sceneDisplayName.toLowerCase()
            var sceneCategory = metadata.sceneCategory.toLowerCase()
            if ((!sceneNameFilterValue && !sceneCategoryFilterValue) || (sceneDisplayName.includes(sceneNameFilterValue) && sceneCategory.includes(sceneCategoryFilterValue))) {
                const row = `
                    <tr>
                        <td><input type="text" value="${metadata.sceneDisplayName}" class="display-input"></td>
                        <td><input type="text" value="${metadata.sceneCategory}" class="category-input"></td>
                        <td>
                            <button class="update-btn" data-path="${path}" data-objecttype="scene">Update</button>
                            <button class="delete-btn" data-path="${path}" data-objecttype="scene">Delete</button>
                        </td>
                    </tr>
                `;
                ($("#scenesTable tbody")).append(row);
            }
        });
    });

    $.each(jsonData["options"], function(key, value) { // Iterate over each option
        const $element = $("#" + key); // Get the element id of the option
        if ($element.attr("type") === "range") { // If the element is a slider
            $element.val(value); // Set the slider value to the value that was in the json
            $("#" + key + "Value").text(value); // Update the text
        } else if ($element.attr("type") === "checkbox") { // If the element is a checkbox
            $element.prop("checked", value);
        } else if ($element.prop("tagName") === "SELECT") { // If the element is a dropdown
            $element.val(value);
        };
    });

    socket.emit('json_transfer_to_python', jsonData); // Send the updated data to the backend
}

$(document).on('click', '.update-btn', function() {
    $("#status").text("Updating...");

    // Data is tied to the button in the row when the rows are generated
    const objectType = $(this).data("objecttype");
    const path = $(this).data("path");

    const row = $(this).closest('tr'); // Get the row that contains the button
    const newName = row.find('.display-input').val(); // Get the value from the input in the name field
    const newCategory = row.find('.category-input').val(); // Get the value from the input in the category field

    if (newCategory === "All") {
        $("#status").text("Category name cannot be 'All'");
        setTimeout(function() {
            $("#status").text("");
        }, 2000);
        return;
    }

    if (newName === "") {
        $("#status").text("Model name cannot be empty");
        setTimeout(function() {
            $("#status").text("");
        }, 2000);
        return;
    }

    if (objectType === "model") {
        $.each(jsonData.models, function(index, model) {
            if (model[path]) {
                model[path].modelDisplayName = newName; // Doesn't actually change the json file, this is handled in main.py by the updateAndDeleteJSONFiles function
                model[path].modelCategory = newCategory;
            }
        });
    }

    if (objectType === "scene") {
        $.each(jsonData.scenes, function(index, scene) {
            if (scene[path]) {
                scene[path].sceneDisplayName = newName; // Doesn't actually change the json file, this is handled in main.py by the updateAndDeleteJSONFiles function
                scene[path].sceneCategory = newCategory;
            }
        });
    }

    refreshData(); // Re-populate the table, also necessary to send the current data (with the updated names and categories) to python

    $("#status").text("Updated.");
    setTimeout(function() {
        $("#status").text("");
    }, 2000);
});

$(document).on('click', '.delete-btn', function() {
    // Data is tied to the button in the row when the rows are generated
    const objectType = $(this).data("objecttype");
    const path = $(this).data("path");

    if (confirm("Are you sure you want to delete this?")) {
        $("#status").text("Deleting...");
        if (objectType === "model") {
            $.each(jsonData.models, function(index, model) { 
                if (model[path]) {
                    delete model[path] // Doesn't actually delete the file, this is handled in main.py by the updateAndDeleteJSONFiles function
                }
            });
        }
    
        if (objectType === "scene") {
            $.each(jsonData.scenes, function(index, scene) {
                if (scene[path]) {
                    delete scene[path] // Doesn't actually delete the file, this is handled in main.py by the updateAndDeleteJSONFiles function
                }
            });
        }
        $("#status").text("Deleted.");
        refreshData(); // Re-populate the table, also necessary to send the current data (with the models/scenes missing from the array) to python
    }
    setTimeout(function() {
        $("#status").text("");
    }, 2000);
});

$(document).ready(function() {
    $(document).on('keydown', function(event) { // Disallow double quotes as they cant be escaped in the json
        if (event.key === '"') {
            event.preventDefault();
            alert('Double quotes are not allowed');
        }
    });

    $(document).on("paste", function(event) { // Stop double quotes being pasted in
        // Get the pasted data
        let paste = event.originalEvent.clipboardData.getData('text');
        if (paste.includes('"')) {
            event.preventDefault();
            alert('Double quotes are not allowed');
        }
    });

    $('#saveButton').on('click', function() {
        jsonData.options.cameraSensitivity = parseFloat($('#cameraSensitivity').val());
        jsonData.options.movementSpeed = parseFloat($('#movementSpeed').val());
        jsonData.options.positionSpeed = parseFloat($('#positionSpeed').val());
        jsonData.options.rotationSpeed = parseFloat($('#rotationSpeed').val());
        jsonData.options.scaleSpeed = parseFloat($('#scaleSpeed').val());
        jsonData.options.wandSmoothing = parseFloat($('#wandSmoothing').val());
        jsonData.options.invertCameraControls = $('#invertCameraControls').is(':checked');
        jsonData.options.hideControls = $('#hideControls').is(':checked');
        jsonData.options.graphicsQuality = $('#graphicsQuality').val();

        socket.emit('json_transfer_to_python', jsonData);
    });

    $(document).on('click', '#importButton', function() {
        $("#status").text("Importing model...");
    });
    
    $(document).on('click', '#importAllButton', function() {
        $("#status").text("Importing all models...");
    });

    socket.on('json_transfer_to_js', function(data) { // Update the current data when python sends it through a websocket
        jsonData = data;
    });
    
    socket.on('connect', function() { // Will be called after each model import because of how flask redirects work
        refreshData();
    });
    
    $(document).on('input', '.filter', function() { // Will be called whenever anything is typed in the filter fields
        refreshData();
    });
});
