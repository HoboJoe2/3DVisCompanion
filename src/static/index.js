var modelData = {};

var socket = io.connect(window.location.origin);

// Update the table's data
function populateTable() {
    const $tableBody = $("#modelsTable tbody");
    $tableBody.empty(); // Clear the table body

    $.each(modelData, function(path, metadata) {
        var nameFilterValue = $('#namefilter').val();
        var categoryFilterValue = $('#categoryfilter').val();
        if ((!nameFilterValue && !categoryFilterValue) || (metadata.modelDisplayName.includes(nameFilterValue) && metadata.modelCategory.includes(categoryFilterValue))) {
            const row = `
            <tr>
                <td><input type="text" value="${metadata.modelDisplayName}" class="display-input"></td>
                <td><input type="text" value="${metadata.modelCategory}" class="category-input"></td>
                <td>
                    <button class="update-btn" data-path="${path}">Update</button>
                    <button class="delete-btn" data-path="${path}">Delete</button>
                </td>
            </tr>
        `;
        $tableBody.append(row);
        }
    });
    socket.emit('json_transfer_to_python', modelData);
}

// Update a row's data
$(document).on('click', '.update-btn', function() {
    $("#status").text("Updating...");
    const path = $(this).data("path");
    const row = $(this).closest('tr');;
    const newDisplayName = row.find('.display-input').val();
    const newCategory = row.find('.category-input').val();

    // Update the model data
    modelData[path].modelDisplayName = newDisplayName;
    modelData[path].modelCategory = newCategory;

    populateTable();  // Re-populate the table after update

    $("#status").text("Model updated.");
    setTimeout(function() {
        $("#status").text("");
    }, 2000);
});

// Delete a row's data
$(document).on('click', '.delete-btn', function() {
    $("#status").text("Deleting...");
    const path = $(this).data("path");
    if (confirm("Are you sure you want to delete this model?")) {
        delete modelData[path];  // Delete the entry
        populateTable();  // Re-populate the table after deletion
    }

    $("#status").text("Model deleted.");
    setTimeout(function() {
        $("#status").text("");
    }, 2000);
});

$(document).on('click', '#importButton', function() {
    $("#status").text("Importing model...");
});

$(document).on('click', '#importAllButton', function() {
    $("#status").text("Importing all models...");
});

socket.on('json_transfer_to_js', function(data) {
    modelData = data;
});

socket.on('connect', function() {
    populateTable();
});

$('.filter').on('input', function() {
    populateTable();
})

$(document).ready(function() {
    $("#rotate").on({
        mouseenter() {
            $(this).addClass("logo");
        },
        animationend() {
            $(this).removeClass("logo");
        },
    });
})
