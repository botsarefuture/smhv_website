const eventContainer = document.getElementById("event-container");
    const totalRolesElement = document.querySelector(".total-info");
    const totalProgressBar = document.querySelector(".total-progress-fill");
    const totalNumbersElement = document.querySelector(
      ".total-progress-numbers"
    );
    const errorBox = document.querySelector(".error-box"); // Add error box element
    const EventDetailsmodal = document.getElementById("event-details-modal");

    // Function to create event cards
    function createEventCard(event) {
      const card = document.createElement("div");
      card.classList.add("event-card");
      const roles = event.roles;
      const roles_min = roles.reduce(
        (total, role) => total + role.min_count,
        0
      );
      const roles_now = roles.reduce((total, role) => total + role.count, 0);
      // Check if roles_min and roles_now are valid numbers, and provide default values if they are not.
      const rolesMinText = Number.isNaN(roles_min) ? 0 : roles_min;
      const rolesNowText = Number.isNaN(roles_now) ? 0 : roles_now;

      card.innerHTML = `
    <h2>${event.title_fi}</h2>
    <p>Date: ${event.date}</p>
    <div class="progress-container">
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${
              roles_min > 0 ? (roles_now / roles_min) * 100 : 0
            }%;"></div>
        </div>
    </div>
    <p class="progress-numbers">(${roles_now}/${roles_min})</p>
    <button class="event-details-button" data-event-id="${
      event._id
    }">View Details</button>
`;

      // Add a custom class to the "View Details" button
      const button = card.querySelector(".event-details-button");
      button.classList.add("show-details-button");

      return card;
    }

    function displayEventDetails(eventDetails) {
      const modal = document.getElementById("event-details-modal");
      const titleElement = document.getElementById("event-details-title");
      const contentElement = document.getElementById("event-details-content");

      // Clear the previous content
      titleElement.textContent = "";
      contentElement.innerHTML = "";

      // Set the title of the modal
      titleElement.textContent = eventDetails.title_fi;

      // Create and append content to the modal
      const descriptionElement = document.createElement("p");
      descriptionElement.textContent = eventDetails.description_fi;

      const dateElement = document.createElement("p");
      dateElement.textContent = `Date: ${eventDetails.date}`;

      const locationElement = document.createElement("p");
      locationElement.textContent = `Location: ${eventDetails.location_fi}`;

      // Create role cards and status bars for each role
      eventDetails.roles.forEach((role) => {
        const roleCard = document.createElement("div");
        roleCard.classList.add("role-card");

        const roleName = document.createElement("h3");
        roleName.textContent = role.fi_name;

        const roleDescription = document.createElement("p");
        roleDescription.textContent = role.fi_description;

        const statusBar = document.createElement("div");
        statusBar.classList.add("status-bar");
        const statusFill = document.createElement("div");
        statusFill.classList.add("status-fill");
        statusFill.style.width = `${(role.count / role.min_count) * 100}%`; // Fill width based on data
        statusBar.appendChild(statusFill);

        const roleCount = document.createElement("p");
        roleCount.classList.add("count");
        roleCount.textContent = `(${role.count}/${role.min_count})`;

        roleCard.appendChild(roleName);
        roleCard.appendChild(roleDescription);
        roleCard.appendChild(statusBar);
        roleCard.appendChild(roleCount);

        contentElement.appendChild(roleCard);
      });

      // Append all content elements to the modal
      contentElement.appendChild(descriptionElement);
      contentElement.appendChild(dateElement);
      contentElement.appendChild(locationElement);

      // Show the modal
      modal.style.display = "block";
    }
    // Event listener to handle the button click
    eventContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("show-details-button")) {
        const eventId = event.target.getAttribute("data-event-id");
        // Fetch event data from /api/events/event_id (replace with your actual URL)
        fetch(`/api/events/${eventId}`)
          .then((response) => response.json())
          .then((data) => {
            // Display event details in the modal
            displayEventDetails(data);
          })
          .catch((error) => {
            console.error("Error fetching event data:", error);
          });
      }
    });

    // Function to close the modal
    function closeModal() {
      const modal = document.getElementById("event-details-modal");
      modal.style.display = "none";
    }

    // Close the modal when the close button is clicked
    const closeButton = document.getElementById("close-button");
    closeButton.addEventListener("click", closeModal);

    // Close the modal when the user clicks outside of it
    window.addEventListener("click", (event) => {
      if (event.target === eventDetailsModal) {
        closeModal();
      }
    });

    // Function to fetch and update event data
    function updateEventData() {
      errorBox.style.display = "none";

      fetch("/api/events/")
        .then((response) => response.json())
        .then((data) => {
          const eventData = data;
          eventContainer.innerHTML = "";
          updateTotalRoles(eventData);

          eventData.forEach((event) => {
            const card = createEventCard(event);
            eventContainer.appendChild(card);
          });
        })
        .catch((error) => {
          console.error("Error fetching event data:", error);
          errorBox.textContent = "Failed to fetch data from the server.";
          errorBox.style.display = "block";
        });
    }

    // Event listener to handle the button click
    eventContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("event-details-button")) {
        const eventId = event.target.getAttribute("data-event-id");
        // Fetch details for the specific event using `/api/events/<event_id>`
        fetch(`/api/events/${eventId}`)
          .then((response) => response.json())
          .then((eventDetails) => {
            // Process and display the event details (e.g., role statistics or participants)
            // You can create a modal or a new section on the page to display the details.
            // Update the DOM with the event details.
            displayEventDetails(eventDetails);
          })
          .catch((error) => {
            console.error("Error fetching event details:", error);
          });
      }
    });

    // Function to update total roles and progress bar
    function updateTotalRoles(eventData) {
      let totalRolesMin = 0;
      let totalRolesNow = 0;

      eventData.forEach((event) => {
        totalRolesMin += event.roles.reduce(
          (total, role) => total + role.min_count,
          0
        );
        totalRolesNow += event.roles.reduce(
          (total, role) => total + role.count,
          0
        );
      });

      totalNumbersElement.textContent = `(${totalRolesNow}/${totalRolesMin})`;

      const totalPercentage =
        totalRolesMin > 0 ? (totalRolesNow / totalRolesMin) * 100 : 0;
      totalProgressBar.style.width = totalPercentage + "%";
    }

    // Function to hide the error box
    function hideErrorBox() {
      errorBox.style.opacity = 0;
      errorBox.style.transform = "translateX(-100%)";
      setTimeout(() => {
        errorBox.style.display = "none";
      }, 500); // Adjust the duration as needed
    }

    // Function to fetch and update event data
    function updateEventData() {
      // Fetch event data from the API
      fetch("/api/events/")
        .then((response) => response.json())
        .then((data) => {
          const eventData = data; // Assuming the API response is an array of events
          // Clear the existing event cards
          eventContainer.innerHTML = "";

          eventData.forEach((event) => {
            const card = createEventCard(event);
            eventContainer.appendChild(card);
          });

          // Update the total roles information
          updateTotalRoles(eventData);

          hideErrorBox();
        })

        .catch((error) => {
          console.error("Error fetching event data:", error);
          // Display the error box with a smooth appearance
          errorBox.textContent = "Failed to fetch data from the server.";
          errorBox.style.display = "block";
          errorBox.style.opacity = 1;
          errorBox.style.transform = "translateX(0)";
        });
    }
    // Initial data load
    updateEventData();

    // Set up automatic updates every 5 minutes (adjust the interval as needed)
    setInterval(updateEventData, 1000); // 300,000 milliseconds = 5 minutes

    // CSS transition for number updates
    const animateNumbers = document.querySelectorAll(".animate-number");
    animateNumbers.forEach((number) => {
      number.style.transition = "color 0.5s, font-size 0.5s";
    });