var monitored = new Object()
var usersStatusURL = "ajax/usersStatus.py" //returns data in JSON
var usersGraphURL = "????"

$.ajaxSetup ({
    cache: false
});

$(function() {
    var viewBlk = $('#viewBlk');
    var groupBlk = $('#groupBlk');
    
    $('li',$('#groupBlk')).draggable();
   
    groupBlk.droppable({
        accept: "#group li",
        activeClass: "highlightSelection",
        drop: function(event,ui) {
            //remove from ajax calls
        }
    viewBlk.droppable({
        accept: "#group li",
        activeClass: "highlightSelection",
        drop: function(event,ui) {
            //add to ajax calls
        }
    });
});

function latestInfo(users) {
    $.getJSON(
        usersStatusURL,
        {users:monitored},

        function(data) {
            $.each(data,function(key,val) {
                $("#"+key).find('stat').html(val)
                if (val == "Danger") {
                    //add styles !!!
                }
            })
        });
    //graph AJAX call - Zach?
    $.getJSON()

}

//background ajax calls every 30seconds
periodicCheck = setInterval(latestInfo(user),30000)
