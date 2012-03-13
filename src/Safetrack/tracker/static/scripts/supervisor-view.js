function addToMonitored(added) {
    monitored[added] = true;
}

function rmFromMonitored(removed) {
    monitored[removed] = false;
}

function getTeams() {
    $.ajax({
        url:getTeamsURL,
        dataType: 'json',
        success: function(data) {

            var optionTags = '<option value="">Please Select a Group</option>';

            for (var i = 0; i < data.length; i++) {
                optionTags += '<option value="';
                optionTags += data[i];
                optionTags += '">'+data[i]+'</option>';
            } 
    
            $('#teamSelect').html(optionTags);

        },
        failure: function (data) {
            console.log('Failed at getTeams');
        } 
    });
}

$(function() {
    $("#tableHeader").click(function () {
        $("#memberTable").toggle();    
    });

    $("#all").click(function() {
        $.each(monitored, function (key,val) {
            if (!$("#"+key).hasClass('highlighted')) {
                monitored[key] = true;
                $("#"+key).addClass('highlighted');
            }
        })
    });
    $("#none").click(function () {
        $.each(monitored, function (key,val) {
            if ($("#"+key).hasClass('highlighted')) {
                monitored[key] = false;
                $("#"+key).removeClass('highlighted');
            }
        })
    });

    if ($("#userType").text().substr(13,1)=="S") {
        getMembers(setViewInteractivity);
    }
    if ($("#userType").text().substr(13,1)=="M") {

        $("#teamSelect").change(function () {
            if ($(this).val() != "") {
                getMembers(setViewInteractivity,false,$(this).val()); 
            } 
            else {
                $("#member").empty();
            }
        });

        getTeams();
        initSearchbar(setViewInteractivity);
    }
    
});

//background ajax calls every 30seconds
periodicCheck = setInterval(latestInfo,5000)
