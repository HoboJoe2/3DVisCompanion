var jsonData = {
    "models": [],
    "scenes": [],
    "options": {
        "cameraSensitivity": 50,
        "movementSpeed": 50,
        "positionSpeed": 50,
        "rotationSpeed": 50,
        "scaleSpeed": 50,
        "renderDistance": 5000,
        "invertCameraControls": false,
        "hideControls": false
    }
};

var socket = io.connect(window.location.origin);

// Update the tables data
function populateTables() {
    const $modelsTableBody = $("#modelsTable tbody");
    const $scenesTableBody = $("#scenesTable tbody");

    $modelsTableBody.empty(); // Clear the table body
    $scenesTableBody.empty();

    modelData = jsonData["models"];
    sceneData = jsonData["scenes"];

    $.each(modelData, function(index, object) {
        $.each(object, function(path, metadata) {
            var modelNameFilterValue = $('#modelnamefilter').val().toLowerCase();
            var modelCategoryFilterValue = $('#modelcategoryfilter').val().toLowerCase();
            if ((!modelNameFilterValue && !modelCategoryFilterValue) || (metadata.modelDisplayName.toLowerCase().includes(modelNameFilterValue) && metadata.modelCategory.toLowerCase().includes(modelCategoryFilterValue))) {
                const row = `
                <tr>
                    <td><input type="text" value="${metadata.modelDisplayName}" class="display-input"></td>
                    <td><input type="text" value="${metadata.modelCategory}" class="category-input"></td>
                    <td>
                        <button class="update-btn" data-path="${path}" data-objecttype="model">Update</button>
                        <button class="delete-btn" data-path="${path}" data-objecttype="model">Delete</button>
                    </td>
                </tr>
            `;
            $modelsTableBody.append(row);
            }
        });
    });

    $.each(sceneData, function(index, object) {
        $.each(object, function(path, metadata) {
            var sceneNameFilterValue = $('#scenenamefilter').val().toLowerCase();
            var sceneCategoryFilterValue = $('#scenecategoryfilter').val().toLowerCase();
            if ((!sceneNameFilterValue && !sceneCategoryFilterValue) || (metadata.sceneDisplayName.toLowerCase().includes(sceneNameFilterValue) && metadata.sceneCategory.toLowerCase().includes(sceneCategoryFilterValue))) {
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
            $scenesTableBody.append(row);
            }
        });
    });

    socket.emit('json_transfer_to_python', jsonData);
}

// Update a row's data
$(document).on('click', '.update-btn', function() {
    $("#status").text("Updating...");

    const objectType = $(this).data("objecttype");
    const path = $(this).data("path");
    const row = $(this).closest('tr');
    const newName = row.find('.display-input').val();
    const newCategory = row.find('.category-input').val();

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
        // Update the model data
        $.each(jsonData.models, function(index, model) {
            if (model[path]) {
                model[path].modelDisplayName = newName;
                model[path].modelCategory = newCategory;
            }
        });
    }

    if (objectType === "scene") {
        // Update the scene data
        $.each(jsonData.scenes, function(index, scene) {
            if (scene[path]) {
                scene[path].sceneDisplayName = newName;
                scene[path].sceneCategory = newCategory;
            }
        });
    }

    populateTables();  // Re-populate the table after update

    $("#status").text("Updated.");
    setTimeout(function() {
        $("#status").text("");
    }, 2000);
});

// Delete a row's data
$(document).on('click', '.delete-btn', function() {
    const objectType = $(this).data("objecttype");
    const path = $(this).data("path");

    if (confirm("Are you sure you want to delete this?")) {
        $("#status").text("Deleting...");
        if (objectType === "model") {
            // Update the model data
            $.each(jsonData.models, function(index, model) {
                if (model[path]) {
                    delete model[path]
                }
            });
        }
    
        if (objectType === "scene") {
            // Update the scene data
            $.each(jsonData.scenes, function(index, scene) {
                if (scene[path]) {
                    delete scene[path]
                }
            });
        }
        $("#status").text("Model deleted.");
        populateTables();  // Re-populate the table after deletion
    }
    setTimeout(function() {
        $("#status").text("");
    }, 2000);
});

$(document).ready(function() {
    $(document).on('keydown', function(event) {
        if (event.key === '"') {
            event.preventDefault();
            alert('Double quotes are not allowed');
        }
    });

    $(document).on("paste", function(event) {
        // Get the pasted data
        let paste = event.originalEvent.clipboardData.getData('text');
        if (paste.includes('"')) {
            event.preventDefault();
            alert('Double quotes are not allowed');
        }
    });

    $('#saveButton').on('click', function() {
        jsonData.options.cameraSensitivity = $('#cameraSensitivity').val();
        jsonData.options.movementSpeed = $('#movementSpeed').val();
        jsonData.options.positionSpeed = $('#positionSpeed').val();
        jsonData.options.rotationSpeed = $('#rotationSpeed').val();
        jsonData.options.scaleSpeed = $('#scaleSpeed').val();
        jsonData.options.renderDistance = $('#renderDistance').val();
        jsonData.options.invertCameraControls = $('#invertCameraControls').is(':checked');
        jsonData.options.hideControls = $('#hideControls').is(':checked');

        socket.emit('json_transfer_to_python', jsonData);
    });

    $(document).on('click', '#importButton', function() {
        $("#status").text("Importing model...");
    });
    
    $(document).on('click', '#importAllButton', function() {
        $("#status").text("Importing all models...");
    });

    socket.on('error', function() {
        alert("error")
    });
    
    socket.on('json_transfer_to_js', function(data) {
        jsonData = data;
    });
    
    socket.on('connect', function() {
        populateTables();
    });
    
    $(document).on('input', '.filter', function() {
        populateTables();
    })
})
