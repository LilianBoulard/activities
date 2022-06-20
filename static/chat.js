function create_bot_message(message) {
    const conversation = document.getElementById("conversation");

    conversation.innerHTML += (
        "<li class='d-flex justify-content-between mb-4'>" +
            "<img src='/static/imgRobot.jpg' alt='avatar'" +
            "class='rounded-circle d-flex align-self-start me-3 shadow-1-strong' width='60'>" +
            "<div class='card'>" +
            "<div class='card-body'>" +
                "<p class='mb-0'>" +
                    message +
                "</p>" +
            "</div>" +
            "</div>" +
        "</li>"
    );
}


function display_all_events(events) {
    const event_list = document.getElementById("event_list");
    // TODO: limit number of events shown
    // TODO (even later): Make infinite scroll
    event_list.innerHTML = "";
    for (const event of events) {
        event_list.innerHTML += (
            "<li class='list-group-item' id='" + event.pk + "'>" +
                "<div class='card row-hover pos-relative py-3 px-3 mb-3 border-warning border-top-0 border-right-0 border-bottom-0 rounded-0'>" +
                    "<div class='row align-items-center'>" +
                        "<div class='row align-items-left' id ='title'>"+
                            "<h5 class='text-primary'> " + event.title + " </h5>"+
                        "</div>"+
                        "<div class='row align-items-left' id ='place'>"+
                            "<p class='font-italic'> <i class='fa fa-map-marker' aria-hidden='true'></i> " + event.place + " </p>"+
                        "</div>"+
                        "<div class='row' id ='tag_n_picto'>"+
                            "<div class='col' id ='tag'>"+
                                "<p class='font-italic'> " + event.tags + " </p>"+
                            "<div class='col' id ='picto'>"+
                                "<img src='/imgRobot.jpg' class='img-fluid' alt='Responsive image'>"+
                            "</div>"+
                        "</div>"+
                    "</div>" +
                "</div>" +
            "</li>"
        );
    }
}

function remove_events(events) {
    for (const event of events) {
        let element = document.getElementById(event);
        element.parentNode.removeChild(element);
    }
}


function on_load() {
    create_bot_message(
        "Bonjour 😄 <br />" +
        "Je peux t'aider à trouver des évènements sur Paris ! ✨ <br />" +
        "Parles moi du type d'évènement qui te plairait, " +
        "de ton budget, de la date qui te conviens " +
        "et/ou de la localisation qui t'arrange !"
    )
    $.ajax({
        type: "POST",
        url: "/get_all_events",
        contentType: "application/json",
        success: function(result) {
            // Clear the event list, and add the events we received
            display_all_events(result.events);
        }
    });
}


function submit() {
    const conversation = document.getElementById("conversation");
    const user_input = document.getElementById("user_input");
    var user_message = user_input.value;

    // Add user message box
    conversation.innerHTML += (
        "<li class='d-flex justify-content-between mb-4'>" +
            "<div class='card w-100'>" +
                "<div class='card-body'>" +
                    "<p class='mb-0'>" +
                        user_message +
                    "</p>" +
                "</div>" +
            "</div>" +
            "<img src='/static/user.png' alt='avatar' class='rounded-circle d-flex align-self-start ms-3 shadow-1-strong' width='60'>" +
        "</li>"
    );

    // Sends the user message to the server
    $.ajax({
        type: "POST",
        url: "/nltkresponse",
        data: JSON.stringify(user_message),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            // Create a message box with the bot's answer
            create_bot_message(result.message);
            // Remove from the screen the events that do not match (events)
            remove_events(result.events);
        },
        error: function(xhr) {
            create_bot_message("Oups, j'ai pété les plombs 🤖");
        }
    });

    // Empty the input field
    user_input.value = "";
}