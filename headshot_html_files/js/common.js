$(document).ready(function(){

    $("#login_btn").click(function(){
        $.ajax(
            {
                type: "POST",
                url: "http://localhost:8080/user/login",
                data: {"user_email": $('#u_email').val(), "password": $('#u_pass').val()},
                xhrFields: {
                    withCredentials: true
                },
                success: function(response)
                {
                    console.log('Login successfull');
                    $('#error_msg').text(response.message);
                }
            });
    });

    $("#signup_btn").click(function(){
        $.ajax({
            type: "POST",
            url: "http://localhost/user/signup",
            data: { "user_name": $('#u_name').val(),
                "user_email": $('#u_email').val(),
                "password": $('#u_pass').val(),
                "first_name": $('#u_first').val(),
                "last_name": $('#u_last').val(),
                "d_o_b": $('#u_dob').val(),
                "gender":$('input[name=gender]:checked').val(),
                "country": $('#u_country').val() },
            xhrFields: {
                withCredentials: true
            },
            succcess: function(response){
                console.log("user_created");
                $('#error_msg').text(response.message);

            }
        });
    });

    $("#drop-down").click(function(){
        if($("#profile-button").hasClass("glyphicon-chevron-down"))
            $("#profile-button").switchClass("glyphicon-chevron-down","glyphicon-chevron-up");
        else
            $("#profile-button").switchClass("glyphicon-chevron-up","glyphicon-chevron-down");
        $("#profile").toggle();
    });

    $( "#u_dob" ).datepicker({
        dateFormat: "yy/dd/mm"
    });

});