tag_array = {
    "art_contemporain": "",
    "atelier": "<i class='fa fa-gavel fa-lg' aria-hidden='true'></i>",
    "balade":" ",
    "bd": "<i class='fa fa-book fa-lg' aria-hidden='true'></i>",
    "brocante": "<i class='fa fa-dropbox fa-lg' aria-hidden='true'></i>",
    "cinéma": "<i class='fa fa-film fa-lg' aria-hidden='true'></i>",
    "cirque": "",
    "clubbing": "",
    "concert": "<i class='fa fa-microphone fa-lg' aria-hidden='true'></i>",
    "conférence": "<i class='fa fa-volume-up fa-lg' aria-hidden='true'></i>",
    "danse": "",
    "enfants": "<i class='fa fa-child fa-lg' aria-hidden='true'></i>",
    "expo": "",
    "gourmand": "",
    "histoire": "<i class='fa fa-university fa-lg' aria-hidden='true'></i>",
    "humour": "<i class='fa fa-smile-o fa-lg' aria-hidden='true'></i>",
    "innovation": "<i class='fa fa-microchip fa-lg' aria-hidden='true'></i>",
    "lgbt": "<i class='fa fa-venus-double fa-lg' aria-hidden='true'></i><i class='fa fa-mars-double fa-4px' aria-hidden='true'></i>",
    "littérature": "<i class='fa fa-book fa-lg' aria-hidden='true'></i>",
    "loisirs": "",
    "musique": "<i class='fa fa-music fa-lg' aria-hidden='true'></i>",
    "nature": "<i class='fa fa-tree fa-lg' aria-hidden='true'></i>",
    "peinture": "<i class='fa fa-paint-brush fa-lg' aria-hidden='true'></i>",
    "photo": "<i class='fa fa-camera-retro fa-lg' aria-hidden='true'></i>",
    "salon": "",
    "sciences": "",
    "solidarité": "<i class='fa fa-users fa-lg' aria-hidden='true'></i>",
    "spectacle_musical": "",
    "sport": "<i class='fa fa-futbol-o fa-lg' aria-hidden='true'></i>",
    "street_art": "<i class='fa fa-building fa-lg' aria-hidden='true'></i>",
    "théâtre": ""
}


function create_bot_message(message) {
    const conversation = document.getElementById("conversation");

    conversation.innerHTML += (
        "<li class='d-flex justify-content-between mb-4'>" +
            "<img src='https://cdn.pixabay.com/photo/2017/10/24/00/39/bot-icon-2883144_1280.png' alt='avatar'" +
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
            console.log(result);
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
        picto = "";

        for(const tag of event.tags){
            if (tag_array[tag] != undefined){
                picto += tag_array[tag] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
            }
        }
        event_list.innerHTML += (
            "<li class='list-group-item' id='" + event.pk + "'>" +
                "<a target='_blank' href='" + event.url + "'>" +
                    "<div class='card row-hover pos-relative py-3 px-3 mb-3 border-warning border-top-0 border-right-0 border-bottom-0 rounded-0'>" +
                        "<div class='row align-items-center'>" +
                            "<div class='row align-items-left'>" +
                                "<h5 class='text-primary'> " + event.title + " </h5>" +
                            "</div>" +
                            "<div class='row align-items-left'>" +
                                "<p class='font-italic'> <i class='fa fa-map-marker' aria-hidden='true'></i> " + event.place + " </p>" +
                            "</div>" +
                            "<div class='row'>" +
                                "<div class='col-lg'>" +
                                    event.tags +
                                "</div>" +
                                "<div class='col-sm-2'>" +
                                "</div>" +
                                "<div class='col-lg'>" +
                                    picto +
                                "</div>" +
                            "</div>" +
                        "</div>" +
                    "</div>" +
                "</a>" +
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
    //  - it removes events that are already present
    //  - it adds missing events
    // Currently, removes all elements and adds them back again
    display_all_events(events);
}


function on_load() {
    create_bot_message(
        "Bonjour 😄 <br />" +
        "Je peux t'aider à trouver des évènements sur Paris ! ✨ <br />" +
        "Parles moi du type d'évènement qui te plairait, " +
        "de ton budget et/ou de la date qui te conviens !"
    )
    $.ajax({
        type: "POST",
        url: "/get_all_events",
        contentType: "application/json",
        success: function(result) {
            display_all_events(result.events);
            update_pills();
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
            "<img src='https://www.pngall.com/wp-content/uploads/5/Profile-Avatar-PNG.png' alt='avatar' class='rounded-circle d-flex align-self-start ms-3 shadow-1-strong' width='60'>" +
        "</li>"
    );

    // Sends the user message to the server
    $.ajax({
        type: "POST",
        url: "/nlp",
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


function submit_on_enter(event) {
    if (event.keyCode == 13 || event.keyCode == 10) {
        submit();
    }
}