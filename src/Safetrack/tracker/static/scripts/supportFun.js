var monitored = new Object() 
var getTeamUserURL = "/getMembers.py/"
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

function getMembers(onComplete,delBtn) {
    items = []
    $.ajax({
        type: "GET",
        url: getTeamUserURL, 
        data: {},
        dataType: "json",
        success: function(data) {
            $.each(data, function(ind) {
                console.log(data[ind])
                var liTag = '<li class="highlighted" id="'+data[ind].name+'"';
                    liTag += ' data-location="'+data[ind].location+'">';
                if (delBtn) {
                    liTag += '<img class="xBtn" src="/static/assets/x.png" />'
                }
                    liTag += '<img src="'+data[ind].profile+'" /></li>';
                items.push(liTag);

                monitored[data[ind].name] = true;
            });

            $('#groupBlk #member').html(items.join(''))
            onComplete();
        },
        error: function(data) {
            alert("fail");
        }
    });
};    

function latestInfo() {
    //if management, should read two var
    var searchName = "";
    var teamView = false;

    if ($("#userType").val().substr(13,1)=="M") {
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
            summaryDiv.html("<h3>Normal</h3>");

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
                if (!details['state']) { 
                    summaryDiv.find('h3').addClass('warning');
                    summaryDiv.find('h3').html("Attention"); 
                    $('<li >',{"class":'warning',html:name+" is in danger."}).appendTo(summaryDiv); 

                    for (var i = 0; i < details['aboveLimits'].length; i++) {
                        var txt = "#"+name+details['aboveLimits'][i]['sensorName'];
                        
                        if (details['aboveLimits'][i]['isHigh'])
                            $(txt).addClass('dangerHigh')
                        else
                            $(txt).addClass('dangerLow')
                    }        
                } 
            })
            $('<br />').appendTo(summaryDiv);
        },
        failure: function (data) {
            alert('fail')
        } 
    });
}

