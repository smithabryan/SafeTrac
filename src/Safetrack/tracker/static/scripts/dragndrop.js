var monitored = new Object()

var getTeamUserURL = "/getUsers.py/"
var addToMonitoredURL = "/addToMonitored.py/"
var rmFromMonitoredURL = "/removeMonitored.py/"

var updateUsersStatus = "/getUsersStatus.py/"

$.ajaxSetup ({
    cache: false
});

function latestInfo() {
    //make sure getting the proper data here but excluding not monitored users
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
     /*$.ajax ({
        type: "POST",
        url: rmFromMonitored,
        data: removed,
        success: function(data) {
           //do nothing for now 
        },
        failure: function (data) {
            alert('fail')
        } 
    });*/
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
periodicCheck = setInterval(latestInfo,30000)
