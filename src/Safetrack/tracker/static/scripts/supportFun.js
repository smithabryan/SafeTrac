var monitored = new Object() 
var getTeamsURL = "/getTeams.py/"
var usernameToNameMap = new Object();
var getTeamUserURL = "/getMembers.py/"
var updateUsersStatus = "/getUsersStatus.py/"
var connectionLost = false;
//
//this file definitely needs to be cleaned soon~
////$.ajaxSetup ({
//    cache: false
//});

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function log( message ) {
		$( "<div/>" ).text( message ).prependTo( "#log" );
		$( "#log" ).scrollTop( 0 );
};

function initSearchbar (onSearchFunc,manageFlag) {
	$( "#search" ).autocomplete({
		source: function( request, response ) {
			$.ajax({
				url: "/getUsers.py/",
				dataType: "json",
				data: {
					featureClass: "P",
					style: "full",
					maxRows: 12,
					name_startsWith: request.term
				},
				success: function( data ) {
					response( $.map( data, function( item ) {
						return {
		                    label: item.name + ", " + item.location,
							value: item.name
						}
					}));
				}
			});
		},
		minLength: 2,
		select: function( event, ui ) {
            //console.log(ui.item.value)
            $.ajax({
				url: "/addUser.py/",
				data: {"name":ui.item.value},
				success: function(data) {
                    getMembers(onSearchFunc,manageFlag,ui.item.value);
				}
			});
		},
		open: function() {
			$( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
		},
		close: function() {
			$( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
		}
	});
}

function setViewInteractivity() {
    var groupBlk = $('#groupBlk ul');
    var members = groupBlk.find('li');

    $.each(members,function (ind) {
        $(members[ind]).qtip({
            content: $(members[ind]).attr('data-name')+"<br />"+$(members[ind]).attr('data-location'),
            show: 'mouseover',
            hide: 'mouseout',
            position: {
                corner: {
                    target: 'topRight',
                    tooltip: 'bottomLeft'
                }
            },
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
    getAllData();
}

function setManageInteractivity() {
    var groupBlk = $('#groupBlk ul');
    var members = groupBlk.find('li');

    $(".xBtn").click(function () {
        var clicked = this;

        $.ajax({
        		url: "/removeUser.py/",
				data: {name: $(".xBtn").parent().attr('data-name')},

				success: function( data ) {
                    $(clicked).parent().fadeOut('slow', function() {
                        $(clicked).parent().remove();
                    });
                }
		});
    });


    $.each(members,function (ind) {
        $(members[ind]).qtip({
            content: $(members[ind]).attr('data-name')+"<br />"+$(members[ind]).attr('data-location'),
            show: 'mouseover',
            hide: 'mouseout',
            position: {
                corner: {
                    target: 'topRight',
                    tooltip: 'bottomLeft'
                    
                }
            },
            style: {
                padding: 5,
                border: {
                    radius: 5
                }
            }
            
        });
        $(members[ind]).click(function () {
            //need to delete the char

       }); 
                        
    });
}

function getMembers(onComplete,delBtn,data) {
    items = []
    $.ajax({
        type: "GET",
        url: getTeamUserURL, 
        data: {'supervisorname':data },
        dataType: "json",
        success: function(data) {
            //console.log(data);
            $.each(data, function(ind) {
                //console.log(data[ind])
                var liTag = '<li id="'+data[ind].username+'"';
                    liTag += ' data-location="'+data[ind].location+'"';
                    liTag += ' data-name="'+data[ind].name+'"';
                if (delBtn) {
                    liTag += '><img class="xBtn" src="/static/assets/x.png" />'
                }
                else {
                    liTag += 'class="highlighted">'; 
                }
                    liTag += '<img src="'+data[ind].profile+'" /></li>';

                items.push(liTag);

                monitored[data[ind].username] = true;
                usernameToNameMap[data[ind].username] = [data[ind].name];
            });

            //console.log(items)
            $('#groupBlk #member').html(items.join(''))
            onComplete();
        },
        error: function(data) {
            alert("fail");
        }
    });
};    

function latestInfo() {
    var teamFlag = 0;
    var searchName = '';

    if ($("#userType").text().substr(13,1)=="M") {
        teamFlag = $("#member li").size();

        if (teamFlag > 1) {
            searchName = $("#teamSelect").val(); 
            teamFlag = true;
        }
        else {
            searchName = $("#member li").attr("data-name");
            teamFlag = false;
            console.log(searchName)
        }
    }

    $.ajax ({
        type: "GET",
        url: updateUsersStatus,
        data: {"searchName":searchName,"teamFlag":teamFlag},
        dataType: "json",
        success: function(data) {
            var summaryDiv = $("#summary");
            var detailTable = $("#memberTable");

            detailTable.empty();
            summaryDiv.find('h3').html("Normal");
            summaryDiv.find('ul').empty();

            var heading = '<td id="name">Name</td>';
            heading += '<td id="temp">Temperature</td>';
            heading += '<td id="humid">Humidity</td>';
            heading += '<td id="noise">Noise</td>';
            heading += '<td id="impact">Impact</td>';

            $('<tr />',{html:heading}).appendTo(detailTable)
           

            $.each(data, function (name,details) {
                var tableTags = '<td>'+details['name']+'</td>';
                tableTags += '<td id="'+name+'temp">'+details['temp']+'</td>';
                tableTags += '<td id="'+name+'humid">'+details['humid']+'</td>';
                tableTags += '<td id="'+name+'noise">'+details['noise']+'</td>';
                tableTags += '<td id="'+name+'impact">'+details['impact']+'</td>';

                $('<tr />',{html:tableTags}).appendTo(detailTable);
                $('#outputData').append(tableTags);

                if (!details['state']) {
                    summaryDiv.find('h3').addClass('warning');
                    summaryDiv.find('h3').html("Attention");

                    $('<li >',{"class":'warning',html:details['name']+" is in danger."}).appendTo(summaryDiv.find('ul'));

                    for (var i = 0; i < details['aboveLimits'].length; i++) {
                        var txt = "#"+name+details['aboveLimits'][i]['sensorName'];

                        if (details['aboveLimits'][i]['isHigh'])
                            $(txt).addClass('dangerHigh')
                        else
                            $(txt).addClass('dangerLow')
                    }       
                }
                else {
                    summaryDiv.find('h3').removeClass('warning');
                    summaryDiv.find('h3').html("Normal");
                    summaryDiv.find('ul').empty();

                    for (var i = 0; i < details['aboveLimits'].length; i++) {
                        var txt = "#"+name+details['aboveLimits'][i]['sensorName'];
                        $(txt).removeClass('dangerHigh');
                        $(txt).removeClass('dangerLow');
                    }
                }
                if (connectionLost) {
                    detailTable.empty();
                    summaryDiv.html("<h3>Connection Lost!</h3>");
                    var heading = '<td id="name"></td>';
                    heading += '<td id="temp"></td>';
                    heading += '<td id="humid"></td>';
                    heading += '<td id="noise"></td>';
                    heading += '<td id="impact"></td>';       
                }
         })

         $('<br />').appendTo(summaryDiv);

        },
        failure: function (data) {
            alert('fail')
        }
    });
}

function checkConnection(){
	$.getJSON("/checkIfConnected/", function(data){
		if(data == true) {
           connectionLost = true; 
	    } 
        else {
            connectionLost = false;
        }
	});
};

function serialSafetyFeedback() {
	$.getJSON("/serialSafetyFeedback/",function(data){});	
}

