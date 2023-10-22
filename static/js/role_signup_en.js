// Add an event listener for role checkboxes
document.querySelectorAll(".custom-checkbox").forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
        const roleContainer = checkbox.closest(".role");
        const progressBar = roleContainer.querySelector(".progress-bar");
        const roleCount = roleContainer.querySelector(".role-count");
        const roleData = fix_role();

        // Check if the checkbox was checked or unchecked
        if (checkbox.checked) {
            if (!roleData.checked) {
                // If it wasn't checked before, increment the count
                roleData.count += 1;
                roleData.checked = true;
            }
        } else {
            if (roleData.checked) {
                // If it was checked before, decrement the count
                roleData.count -= 1;
                roleData.checked = false;
            }
            // Ensure the count doesn't go below 0
            if (roleData.count < 0) {
                roleData.count = 0;
            }
        }

        // Update the role count and progress bar
        roleCount.textContent = `Currently: ${roleData.count} / Required: ${roleData.min_count}`;
        progressBar.style.width = `${(roleData.count / roleData.min_count) * 100}%`;
        function fix_role() {
            const roleDataString = roleContainer.getAttribute("data-role");
  
            // Remove single quotes inside double-quoted strings
            const cleanedRoleDataString = roleDataString.replace(
                /&quot;([^'&]+)&quot;/g,
                (match, content) => `&quot;${content.replace(/'/g, "")}&quot;`
            );
            console.log(cleanedRoleDataString);
  
            // Replace single quotes with double quotes for values or keys that don't start with "
            const cleanedRoleDataString1 = cleanedRoleDataString.replace(
                /("[^"]*")|'([^']+)'/g,
                (match, doubleQuoted, singleQuoted) => {
                    if (doubleQuoted) {
                        return doubleQuoted; // Leave double-quoted parts unchanged
                    } else if (singleQuoted) {
                        return `"${singleQuoted.replace(/'/g, "")}"`; // Replace single quotes with double quotes
                    }
                }
            );
  
            console.log(cleanedRoleDataString1);
  
            // Replace single quotes with double quotes for values or keys that don't start with " and ensure values don't start with "
            const cleanedRoleDataString2 = cleanedRoleDataString1.replace(
                /("[^"]*")|'([^']+)'/g,
                (match, doubleQuoted, singleQuoted) => {
                    if (doubleQuoted) {
                        return doubleQuoted; // Leave double-quoted parts unchanged
                    } else if (singleQuoted) {
                        // Check if the single-quoted part starts with a double quote, and if it does, replace single quotes with double quotes
                        if (singleQuoted.startsWith('"')) {
                            return singleQuoted.replace(/'/g, "");
                        } else {
                            return `"${singleQuoted.replace(/'/g, "")}"`;
                        }
                    }
                }
            );
  
            const final = cleanedRoleDataString2.replace("''", '""');
  
            // Parse the JSON data
            const roleData = JSON.parse(final);
            console.log(roleData);
            return roleData;
        }
    });
});

// Lisää klikkitapahtuman kuuntelija jokaiseen roolilaatikkoon
document.querySelectorAll(".role").forEach(function (box) {
    // When a roolilaatikkoa is clicked, toggle the checkbox and apply styles
    box.addEventListener("click", function () {
        const checkbox = box.querySelector(".custom-checkbox");
        checkbox.checked = !checkbox.checked;
        box.classList.toggle("selected", checkbox.checked);
    });

    var open = false;

    box.querySelector(".view-more-button").addEventListener("click", toggleText);
    box.querySelector(".role-description").addEventListener("click", toggleText);

    function toggleText() {
        var description = box.querySelector(".role-description");
        var button = box.querySelector(".view-more-button");
        
        const checkbox = box.querySelector(".custom-checkbox");
        checkbox.checked = !checkbox.checked;
        box.classList.toggle("selected", checkbox.checked);

        if (open === true) {
            description.style.maxHeight = "40px"; // Säädä korkeutta tarpeen mukaan
            description.classList.add("fade");
            open = !open;
            button.innerHTML = "Show more ⏷";
        } else {
            description.style.maxHeight = "none";
            description.classList.remove("fade");
            open = !open;
            button.innerHTML = "Hide ⏶";
        }
    }
});
