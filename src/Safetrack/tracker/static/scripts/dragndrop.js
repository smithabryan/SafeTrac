var monitored = new Object() 
var getTeamUserURL = "/getUsers.py/"
var updateUsersStatus = "/getUsersStatus.py/"

//this file definitely needs to be cleaned soon~

$.ajaxSetup ({
    cache: false
});

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function latestInfo() {
    //if management, should read two var
    var searchName = "";
    var teamView = false;

    if ($("#userType").val().substr(14,1)=="M") {
        searchName = $("#searchName").val();
        teamView = $("#teamView").checked ? true : false; 
    }

    $.ajax ({
        type: "GET",
        url: updateUsersStatus,
        data: {"searchName":searchName,"teamView":teamView},
        dataType: "json",
        success: function(data) {
            var summaryDiv = $("#summary");
            var detailTable = $("#memberTable");

            detailTable.empty();
            summaryDiv.html("Normal");

            var heading = '<td id="name">Name</td>';
            heading += '<td id="temp">Temperature</td>';
            heading += '<td id="humid">Humidity</td>';
            heading += '<td id="noise">Noise</td>';
            heading += '<td id="impact">Impact</td>';

            $('<tr />',{html:heading}).appendTo(detailTable)
            
            $.each(data, function (name,details) {
                
                var tableTags = '<td>'+name+'</td>';
                tableTags += '<td id="'+name+'temp">'+details['temp']+'</td>';
                tableTags += '<td id="'+name+'humid">'+details['humid']+'</td>';
                tableTags += '<td id="'+name+'noise">'+details['noise']+'</td>';
                tableTags += '<td id="'+name+'impact">'+details['impact']+'</td>';

                $('<tr />',{html:tableTags}).appendTo(detailTable)

                if (details['safe']) { 
                   //this is BAD!
                    summaryDiv.find('h3').addClass('warning');
                    summaryDiv.find('h3').html("Attention"); 
                    $('<li >',{html:name+"is in danger."}).appendTo(summaryDiv.find('ul')); 
                }
                else {
                    for (var i = 0; i < details['aboveLimits'].size; i++) {
                        if (details['isHigh'])
                            $("#"+name+details['sensorName']).addClass('dangerHigh')
                        else
                            $("#"+name+details['sensorName']).addClass('dangerLow')
                    }        
                } 
            })
        },
        failure: function (data) {
            alert('fail')
        } 
    });
}

function setInteractivity() {
    var groupBlk = $('#groupBlk ul');
    var members = groupBlk.find('li');
    $.each(members,function (ind) {
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

function addToMonitored(added) {
    console.log(added);
    monitored[added] = true;
    /*$.ajax ({
        type: "POST",
        url: addToMonitoredURL,
        data: added, 
        success: function(data) {
           //do nothing for now 
        },
        failure: function (data) {
            alert('fail')
        } 
    });*/
}

function rmFromMonitored(removed) {
    monitored[removed] = false;
}

function getUsers() {
    items = []
    $.ajax({
        type: "GET",
        url: getTeamUserURL, 
        data: {},
        dataType: "json",
        success: function(data) {
            $.each(data, function(ind) {
                items.push('<li id="'+data[ind].name+'">' + '<img src="'+data[ind].profile+'"></li>');
            });

            $('#groupBlk #member').html(items.join(''))
            setInteractivity();
        },
        error: function(data) {
            alert("fail");
        }
    });
};    

$(function() {
    getUsers()
});

//background ajax calls every 30seconds
periodicCheck = setInterval(latestInfo,5000)
