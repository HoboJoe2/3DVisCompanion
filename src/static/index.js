var modelData = {}

const socket = io();

// Update the table's data
function populateTable() {
    console.log("populating table")
    const $tableBody = $("#jsonTable tbody");
    $tableBody.empty(); // Clear the table body

    $.each(modelData, function(path, metadata) {
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
    });
    socket.emit('json_transfer_to_client', "modelData");
    console.log("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaamodeldata is")
    console.log(modelData)
}

// Update a row's data
$(document).on('click', '.update-btn', function() {
    const path = $(this).data("path");
    const row = $(this).closest('tr');
    const newName = row.find('.name-input').val();
    const newDisplayName = row.find('.display-input').val();
    const newCategory = row.find('.category-input').val();

    // Update the model data
    modelData[path].originalModelName = newName;
    modelData[path].modelDisplayName = newDisplayName;
    modelData[path].modelCategory = newCategory;

    populateTable();  // Re-populate the table after update
});

// Delete a row's data
$(document).on('click', '.delete-btn', function() {
    const path = $(this).data("path");
    delete modelData[path];  // Delete the entry
    populateTable();  // Re-populate the table after deletion
});

socket.on('json_transfer_to_server', function(data) {
    console.log("aaaa");
    //modelData = data;
    console.log("hi");
    //console.log(data);
    //console.log(modelData);
    //populateTable();
});

$(document).on('click', '#btn', function() {
    console.log("clicked");
    console.log(modelData);
})

$(document).ready(function() {
    console.log("dom is ready");
    $("#rotate").on({
        mouseenter() {
            $(this).addClass("logo");
        },
        animationend() {
            $(this).removeClass("logo");
        },
    });
})