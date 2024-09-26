var modelData = {"models": "nothing"};

var socket = io.connect(window.location.origin);

// Update the table's data
function populateTable() {
    console.log("populating table");
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
    console.log("table populated");
    socket.emit('json_transfer_to_python', modelData);
}

// Update a row's data
$(document).on('click', '.update-btn', function() {
    console.log("updating");
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
    console.log("deleting");
    const path = $(this).data("path");
    delete modelData[path];  // Delete the entry
    populateTable();  // Re-populate the table after deletion
});

socket.on('json_transfer_to_js', function(data) {
    console.log("json_transfer_to_js recieved");
    console.log(JSON.stringify(data));
    modelData = data;
});

socket.on('connect', function() {
    console.log("connected");
    populateTable();
});

$(document).on('click', '#btn', function() {
    console.log("clicked, modeldatainjsis");
    console.log(JSON.stringify(modelData));
    socket.emit('json_transfer_to_python', {"hi_py": "hi"});
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