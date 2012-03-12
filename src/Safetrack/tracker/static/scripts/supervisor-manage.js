function log( message ) {
		$( "<div/>" ).text( message ).prependTo( "#log" );
		$( "#log" ).scrollTop( 0 );
};

function setInteractivity() {
    var groupBlk = $('#groupBlk ul');
    var members = groupBlk.find('li');

    $(".xBtn").click(function () {
        var clicked = this;

        $.ajax({
        		url: "/removeUser.py/",
				data: {name: $(".xBtn").parent().attr('id')},

				success: function( data ) {
                    $(clicked).parent().fadeOut('slow', function() {
                        $(clicked).parent().remove();
                    });
                }
		});
    });


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

$(function () {
    getMembers(setInteractivity,true);

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
			log( ui.item ?
                "Selected: " + ui.item.label :
				"Nothing selected, input was " + this.value);
            $.ajax({
				url: "/addUser.py/",
				data: {"name":ui.item.value},
				success: function(data) {
                    if (data!="200")
                        alert('error')
                    else
                        getMembers(setInteractivity,true);
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
});

