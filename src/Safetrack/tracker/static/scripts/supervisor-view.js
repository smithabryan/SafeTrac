function addToMonitored(added) {
    monitored[added] = true;
}

function rmFromMonitored(removed) {
    monitored[removed] = false;
}

function setInteractivity() {
    var groupBlk = $('#groupBlk ul');
    var members = groupBlk.find('li');
    $.each(members,function (ind) {
        $(members[ind]).qtip({
            content: $(members[ind]).attr('id')+"<br />"+$(members[ind]).attr('data-location'),
            show: 'mouseover',
            hide: 'mouseout',
            position: {
                corner: {
                    target: 'topRight',
                    tooltip: 'bottomLeft'
                }
            }
            style: {
                padding: 5,
                border: {
                    radius: 5
                }
            }
        });                          

        $(members[ind]).click(function () {

            if ($(this).hasClass('highlighted')) {
                $(this).removeClass('highlighted');
                rmFromMonitored($(this).attr('id'));
            }
            else {
                $(this).addClass('highlighted');
                addToMonitored($(this).attr('id')); 
            }
       }); 
    });
}

$(function() {
    $("#tableHeader").click(function () {
        $("#memberTable").toggle();    
    });  
    $("#selectAll").click(function() {
        //implement
    });
    $("#none").click(function () {
        //implement
    });

    if ($("#userType").text().substr(13,1)=="S") {
        getMembers(setInteractivity);
    }
});

//background ajax calls every 30seconds
periodicCheck = setInterval(latestInfo,5000)
