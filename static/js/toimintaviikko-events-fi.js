fetch("/api/events/")
  .then((response) => response.json())
  .then((data) => {
    const eventsList = document.getElementById("events-list");

    // Sort events by date
    data.sort((a, b) => {
      const dateA = new Date(a.date);
      const dateB = new Date(b.date);
      return dateA - dateB;
    });

    data.forEach((event) => {
      const eventDiv = document.createElement("div");
      eventDiv.className = "event";

      const eventTitle = document.createElement("div"); // Changed from h3
      eventTitle.textContent = event.title_fi;
      eventTitle.className = "event-title"; // Add a class for styling

      const eventDate = document.createElement("p");
      eventDate.textContent = event.date;
      eventDate.className = "date";

      const eventDescription = document.createElement("p");
      eventDescription.textContent = event.description_fi;

      const signupButton = document.createElement("a");
      signupButton.href = `/signup/${event._id}`;
      signupButton.textContent = "Ilmoittaudu";
      signupButton.className = "cta-button";

      eventDiv.appendChild(eventTitle);
      eventDiv.appendChild(eventDate);
      eventDiv.appendChild(signupButton);
      eventsList.appendChild(eventDiv);
    });
  })
  .catch((error) => {
    console.error("Error fetching events:", error);
  });
