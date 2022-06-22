//lien site icon https://fontawesome.com/v4/icons/
tag_array = {
    "Atelier":"<i class='fa fa-gavel' aria-hidden='true'></i>",
    "Conférence":"<i class='fa fa-volume-up' aria-hidden='true'></i>",
    "Street-art":"<i class='fa fa-building' aria-hidden='true'></i>",
    "Art contemporain":"",
    "Expo":"",
    "Sciences":"",
    "Cinéma":"<i class='fa fa-film' aria-hidden='true'></i>",
    "Histoire":"<i class='fa fa-university' aria-hidden='true'></i>",
    "Humour":"<i class='fa fa-smile-o' aria-hidden='true'></i>",
    "Concert":"<i class='fa fa-microphone' aria-hidden='true'></i>",
    "Musique":"<i class='fa fa-music' aria-hidden='true'></i>",
    "Enfants":"<i class='fa fa-child' aria-hidden='true'></i>",
    "Loisirs":"",
    "Photo":"<i class='fa fa-camera-retro' aria-hidden='true'></i>",
    "Gourmand":"",
    "Théâtre":"",
    "LGBT":"<i class='fa fa-venus-double' aria-hidden='true'></i><i class='fa fa-mars-double' aria-hidden='true'></i>",
    "Danse":"",
    "Spectacle musical":"",
    "Littérature":"<i class='fa fa-book' aria-hidden='true'></i>",
    "Nature":"<i class='fa fa-tree' aria-hidden='true'></i>",
    "Balade":"",
    "Sport":"<i class='fa fa-futbol-o' aria-hidden='true'></i>",
    "Peinture":"<i class='fa fa-paint-brush' aria-hidden='true'></i>",
    "Innovation":"<i class='fa fa-microchip' aria-hidden='true'></i>",
    "Clubbing":"",
    "Solidarité":"<i class='fa fa-users' aria-hidden='true'></i>",
    "Cirque":"",
    "Brocante":"<i class='fa fa-dropbox' aria-hidden='true'></i>",
    "BD":"<i class='fa fa-book' aria-hidden='true'></i>",
    "Salon":""
    }


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


function remove_criteria(pill_id) {
    // TODO: Remove criteria from model
    // Remove the pill from the screen
    pill = document.getElementById(pill_id);
    pill.parentNode.removeChild(pill);
}


function update_pills() {
    const pill_list = document.getElementById("pills");
    // Empty the pill list
    pill_list.innerHTML = "";
    // Populate it with info coming from server
    $.ajax({
        type: "POST",
        url: "/get_request_info",
        contentType: "application/json",
        success: function(result) {
            for (const [index, pill_info] of result.entries()) {
                pill_list.innerHTML += (
                    "<div class='pill' id='pill_" + index + "'>" +
                        "<button class='remove' onClick='remove_criteria(\"pill_" + index + "\")'>" +
                            "X" +
                        "</button>" +
                        "<div class='text'>" +
                            pill_info +
                        "</div>" +
                    "</div>"
                )
            }
        }
    });
}


function display_all_events(events) {
    const event_list = document.getElementById("event_list");
    // TODO: limit number of events shown
    // TODO (even later): Make infinite scroll
    event_list.innerHTML = "";
    for (const event of events) {
        picto="";
        for(const tag of event.tags.split(";")){
            if (tag == tag_array[0]){
                console.log("1");
            }
            }
        event_list.innerHTML += (
            "<li class='list-group-item' id='" + event.pk + "'>" +
                "<div class='card row-hover pos-relative py-3 px-3 mb-3 border-warning border-top-0 border-right-0 border-bottom-0 rounded-0'>" +
                    "<div class='row align-items-center'>" +
                        "<div class='row align-items-left'>"+
                            "<h5 class='text-primary'> " + event.title + " </h5>"+
                        "</div>"+
                        "<div class='row align-items-left'>"+
                            "<p class='font-italic'> <i class='fa fa-map-marker' aria-hidden='true'></i> " + event.place + " </p>"+
                        "</div>"+
                        "<div class='row'>"+
                            "<div class='col-sm'>"+
                            event.tags.replaceAll(";",", ")+
                            "</div>"+
                            "<div class='col-sm'>"+
                            "</div>"+
                            "<div class='col-sm'>"+
                                picto+
                            "</div>"+
                        "</div>"+
                    "</div>" +
                "</div>" +
            "</li>"
        );
    }
}



/*
function remove_events(events) {
    for (const event of events) {
        let element = document.getElementById(event);
        element.parentNode.removeChild(element);
    }
}
*/


function update_events(events) {
    // TODO: improve so that :
    //  - it removes events that are already present and  should not anymore
    //  - it adds missing events
    // Currently, removes all elements and adds them back again
    display_all_events(events);
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
            create_bot_message(result.message);
            update_events(result.events);
            update_pills();
        },
        error: function(xhr) {
            create_bot_message("Oups, j'ai pété les plombs 🤖");
        }
    });

    // Empty the input field
    user_input.value = "";
}
