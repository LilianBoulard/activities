function envoyer(){
    var newMsg = document.getElementById("newMsg");
    //var userMsg= document.getElementById("textAreaExample2");
    $( "#newMsg" ).append("<li class='d-flex justify-content-between mb-4'>"+
                            "<div class='card w-100'>"+
                            "<div class='card-header d-flex justify-content-between p-3'>"+
                                "<p class='fw-bold mb-0'>utilisateur</p>"+
                                "<p class='text-muted small mb-0'><i class='far fa-clock'></i> 13 mins ago</p>"+
                            "</div>"+
                            "<div class='card-body'>"+
                                "<p class='mb-0'>"+
                                $("#textAreaExample2").val()+
                               "</p>"+
                            "</div>"+
                            "</div>"+
                            "<img src='/static/user.png' alt='avatar' class='rounded-circle d-flex align-self-start ms-3 shadow-1-strong' width='60'>"+
                        "</li>");
   
    $( "#textAreaExample2" ).val( "" );


    $.ajax({
        type: "POST",
        url: "/nltkresponse",
        data: JSON.stringify($("#textAreaExample2").val()),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            $( "#newMsg" ).append("<li class='d-flex justify-content-between mb-4'>"+
                                        "<img src='/static/imgRobot.jpg' alt='avatar'"+
                                        "class='rounded-circle d-flex align-self-start me-3 shadow-1-strong' width='60'>"+
                                        "<div class='card'>"+
                                        "<div class='card-header d-flex justify-content-between p-3'>"+
                                            "<p class='fw-bold mb-0'>Bot</p>"+
                                            "<p class='text-muted small mb-0'><i class='far fa-clock'></i> 10 mins ago</p>"+
                                        "</div>"+
                                        "<div class='card-body'>"+
                                            "<p class='mb-0'>"+
                                            result.msg+
                                            "</p>"+
                                        "</div>"+
                                        "</div>"+
                                   "</li>"
                                );
        } 
      });
}