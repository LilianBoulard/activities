function create_bot_message(message) {
    const conversation = document.getElementById("conversation");
    const event_list=document.getElementById("event_list");

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


function update_events(events) {
    console.log("events=", events);
    event_list.innerHTML=""
    if(events.length !== 0){
        for(var i= 0; i < 50; i++)
        {
             event_list.innerHTML +=(
            "<li class='list-group-item'>"+
                "<div class='card row-hover pos-relative py-3 px-3 mb-3 border-warning border-top-0 border-right-0 border-bottom-0 rounded-0'>"+
                "<div class='row align-items-center'>"+
                  "<div class='col-md-8 mb-3 mb-sm-0'>"+
                    "<h5>"+
                      "<a href='#' class='text-primary'>"+events[i].title_event+"</a>"+
                    "</h5>"+
                    "<p class='text-sm'><span class='op-6'>Posted</span> <a class='text-black' href='#'>20 minutes</a> <span class='op-6'>ago by</span> <a class='text-black' href='#'>KenyeW</a></p>"+
                    "<div class='text-sm op-5'> <a class='text-black mr-2' href='#'>#C++</a> <a class='text-black mr-2' href='#'>#AppStrap Theme</a> <a class='text-black mr-2' href='#'>#Wordpress</a> </div>"+
                  "</div>"+
                  "<div class='col-md-4 op-7'>"+
                    "<div class='row text-center op-7'>"+
                      "<div class='col px-1'> <i class='ion-connection-bars icon-1x'></i> <span class='d-block text-sm'>141 Votes</span> </div>"+
                      "<div class='col px-1'> <i class='ion-ios-chatboxes-outline icon-1x'></i> <span class='d-block text-sm'>122 Replys</span> </div>"+
                      "<div class='col px-1'> <i class='ion-ios-eye-outline icon-1x'></i> <span class='d-block text-sm'>290 Views</span> </div>"+
                    "</div>"+
                  "</div>"+
                "</div>"+
              "</div>"+
            "</li>"
            )
       }
    }


}


function submit() {
    const conversation = document.getElementById("conversation");
    const event_list = document.getElementById("event_list");
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
            // On success:
            // Create a message box with the bot's answer
            create_bot_message(result.message);
            // Clear the event list, and add the events we received
            update_events(result.events);
        } 
      });

    // Empty the input field
    user_input.value = "";
}