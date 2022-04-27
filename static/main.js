$(document).ready( function(){
    $("#flip-1").bind("change", function(){
        //console.log("Light 1: " + $(this).val());
        $.ajax({
            type: "POST",
            url: "/gpio/",
            data: {
                pin: 18,
                state: $(this).val()
            },
            //success: function(data) {
                //console.log("Light 1: " + $(this).val());
                //$( "#weather-temp" ).html( "<strong>" + data + "</strong> degrees" );
            //}
        });
     });

    $("#flip-2").bind("change", function(){
        console.log("Light 2: " + $(this).val());
     });

     
});
