function create_bot_message(message) {
    var conversation = document.getElementById("conversation");

    conversation.append(
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


function update_events(events) {

}


function submit() {
    var conversation = document.getElementById("conversation");
    var event_list = document.getElementById("event_list");
    var user_input = document.getElementById("#user_input");
    var user_message = user_input.val();

    // Add user message box
    conversation.append(
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
            // On success:
            // Create a message box with the bot's answer
            create_bot_message(result.message);
            // Clear the event list, and add the events we received
            update_events(result.events);
        } 
      });

    // Empty the input field
    user_input.val("");
}