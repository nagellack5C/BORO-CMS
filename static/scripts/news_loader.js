var offset = 0;
function load_news(){
    console.log("/news/" + offset);
    $.ajax({
        type: "GET",
        contentType: 'application/json',
        url: "/news/" + offset,
        success:function(response){
            console.log(response);
            $("#news").html(response)
        }
    }).done(function ( data, textStatus, jqXHR) {
        // console.log("response is", jqXHR);
        if (jqXHR.status == 204) {
            offset -= 10;
            // console.log("changing offset to", offset);
        }
    });
}
$("#newer").click(function () {
    offset -= 10;
    if (offset < 0) {
        offset = 0;
    } else {
        load_news();
    }
    console.log(offset)
});
$("#older").click(function () {
    offset += 10;
    load_news();
    console.log(offset)
});
