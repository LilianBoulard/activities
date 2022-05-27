function envoyer(){
    var conversation = document.getElementById("conversation");
    $("#conversation").append(
    "<li class='d-flex justify-content-between mb-4'>" +
        "<div class='card w-100'>" +
            "<div class='card-body'>" +
                "<p class='mb-0'>" +
                $("#user_input").val() +
               "</p>" +
            "</div>" +
        "</div>" +
        "<img src='/static/user.png' alt='avatar' class='rounded-circle d-flex align-self-start ms-3 shadow-1-strong' width='60'>" +
    "</li>");

    // Empty the input field
    $("#user_input").val("");


    $.ajax({
        type: "POST",
        url: "/nltkresponse",
        data: JSON.stringify($("#user_input").val()),
        success: function(result) {
            $("#conversation").append(
            "<li class='d-flex justify-content-between mb-4'>" +
                "<img src='/static/imgRobot.jpg' alt='avatar'" +
                "class='rounded-circle d-flex align-self-start me-3 shadow-1-strong' width='60'>" +
                "<div class='card'>" +
                "<div class='card-body'>" +
                    "<p class='mb-0'>" +
                    result.message +
                    "</p>" +
                "</div>" +
                "</div>" +
            "</li>");
        } 
      });
}